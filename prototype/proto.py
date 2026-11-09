#!/usr/bin/env python3
"""Lightweight read-only prototype: Stellar Horizon -> CARF RelevantTransactions -> XML.
Public APIs only (horizon.stellar.org, datos.gov.co TRM). No credentials.
Identity data in output is SYNTHETIC TEST DATA (DocTypeIndic OECD11 = new test data)."""
import json, sys, urllib.request, urllib.parse, datetime as dt, collections, decimal
from decimal import Decimal as D
from lxml import etree

H = "https://horizon.stellar.org"
USDC = ("USDC", "GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN")
LOG = []

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "purserkit-proto"}), timeout=30) as r:
        return json.load(r)

def recs(path, **q):
    q.setdefault("limit", 200); q.setdefault("order", "desc")
    return get(f"{H}{path}?{urllib.parse.urlencode(q)}")["_embedded"]["records"]

def akey(code, issuer):  # asset key
    return "XLM" if code in (None, "", "native") else f"{code}:{issuer}"

def opasset(r, prefix=""):
    t = r.get(prefix + "asset_type")
    return "XLM" if t == "native" else akey(r.get(prefix + "asset_code"), r.get(prefix + "asset_issuer"))

# ---------- valuation ----------
_px = {}
def xlm_usd(ts):
    """XLM/USDC hourly close from Horizon trade_aggregations (DEX price as FMV proxy)."""
    hour = int(ts.replace(tzinfo=dt.timezone.utc).timestamp() // 3600 * 3600 * 1000)
    if hour in _px: return _px[hour]
    q = dict(base_asset_type="native", counter_asset_type="credit_alphanum4", counter_asset_code=USDC[0],
             counter_asset_issuer=USDC[1], resolution=3600000, start_time=hour - 6 * 3600000, end_time=hour + 3600000,
             order="desc", limit=1)
    r = get(f"{H}/trade_aggregations?{urllib.parse.urlencode(q)}")["_embedded"]["records"]
    _px[hour] = D(r[0]["close"]) if r else None
    return _px[hour]

def asset_xlm(asset, ts):
    """price of asset in XLM via Horizon trade_aggregations vs native (daily)."""
    code, iss = asset.split(":")
    day = int(ts.replace(tzinfo=dt.timezone.utc).timestamp() // 86400 * 86400 * 1000)
    k = (asset, day)
    if k in _px: return _px[k]
    q = dict(base_asset_type="credit_alphanum4" if len(code) <= 4 else "credit_alphanum12", base_asset_code=code,
             base_asset_issuer=iss, counter_asset_type="native", resolution=86400000,
             start_time=day - 7 * 86400000, end_time=day + 86400000, order="desc", limit=1)
    try:
        r = get(f"{H}/trade_aggregations?{urllib.parse.urlencode(q)}")["_embedded"]["records"]
        _px[k] = D(r[0]["close"]) if r else None
    except Exception as e:
        _px[k] = None
    return _px[k]

def usd_value(asset, units, ts):
    if asset == f"{USDC[0]}:{USDC[1]}": return units * 1, "USDC=1.00 (peg assumption)"
    p = xlm_usd(ts)
    if p is None: return None, "no XLM/USDC price"
    if asset == "XLM": return units * p, "DEX XLM/USDC 1h close"
    px = asset_xlm(asset, ts)
    if px is None: return None, "no DEX price vs XLM"
    return units * px * p, "DEX asset/XLM 1d close x XLM/USDC"

_trm = {}
def trm(day):
    """Banco de la Republica TRM via datos.gov.co Socrata dataset 32sa-8pi3."""
    if day in _trm: return _trm[day]
    q = {"$where": f"vigenciadesde <= '{day}T00:00:00.000' AND vigenciahasta >= '{day}T00:00:00.000'", "$limit": 1}
    r = get("https://www.datos.gov.co/resource/32sa-8pi3.json?" + urllib.parse.urlencode(q))
    _trm[day] = D(r[0]["valor"]) if r else None
    return _trm[day]

# ---------- classification ----------
# CARF buckets: C2C_IN, C2C_OUT, FIAT_IN, FIAT_OUT, XFER_IN(type), XFER_OUT(type), WALLET (unhosted), RRPT
def classify(acct, op, issuers_self=()):
    t, ev = op["type"], []
    ts = dt.datetime.strptime(op["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    def add(bucket, asset, amt, sub=None, note=""):
        ev.append(dict(ts=ts, bucket=bucket, sub=sub, asset=asset, units=D(amt), op=op["id"], optype=t, note=note))
    if t in ("payment",):
        a = opasset(op)
        issuer = op.get("asset_issuer")
        if op["to"] == acct and op["from"] != acct:
            note = "MINT from issuer" if op["from"] == issuer else ""
            add("XFER_IN", a, op["amount"], "CARF509", note)
        elif op["from"] == acct:
            note = "BURN (return to issuer)" if op["to"] == issuer else ""
            add("XFER_OUT", a, op["amount"], "CARF606", note)
            add("WALLET", a, op["amount"], None, "dest not known as VASP (no allow-list)")
    elif t.startswith("path_payment"):
        sa, da = opasset(op, "source_"), opasset(op)
        if op["from"] == acct:
            add("C2C_OUT", sa, op["source_amount"], note="path payment leg");
            if op["to"] == acct: add("C2C_IN", da, op["amount"], note="self path payment = swap")
            else:
                add("C2C_IN", da, op["amount"], note="implicit swap before transfer")
                add("XFER_OUT", da, op["amount"], "CARF606"); add("WALLET", da, op["amount"])
        elif op["to"] == acct:
            add("XFER_IN", da, op["amount"], "CARF509")
    elif t == "create_account":
        if op["funder"] == acct: add("XFER_OUT", "XLM", op["starting_balance"], "CARF606"); add("WALLET", "XLM", op["starting_balance"])
        elif op["account"] == acct: add("XFER_IN", "XLM", op["starting_balance"], "CARF509")
    elif t == "account_merge":
        pass  # amount only in effects (account_credited); needs /effects lookup
    elif t in ("claim_claimable_balance",):
        ev.append(dict(ts=ts, bucket="TODO", asset="?", units=D(0), op=op["id"], optype=t, note="amount via effects; often airdrop CARF501"))
    elif t == "invoke_host_function":
        for c in op.get("asset_balance_changes") or []:
            a = "XLM" if c["asset_type"] == "native" else akey(c.get("asset_code"), c.get("asset_issuer"))
            if c.get("to") == acct and c["type"] == "mint":
                add("XFER_IN", a, c["amount"], "CARF503", "SAC mint to user (mining-style reward)")
            elif c.get("to") == acct and c["type"] == "transfer":
                add("XFER_IN", a, c["amount"], "CARF509", "SAC transfer in; DeFi semantics unknown")
            elif c.get("from") == acct and c["type"] in ("transfer", "burn"):
                add("XFER_OUT", a, c["amount"], "CARF606", f"SAC {c['type']} out; DeFi semantics unknown")
    elif t in ("change_trust", "set_options", "manage_data", "bump_sequence", "set_trust_line_flags",
               "manage_sell_offer", "manage_buy_offer", "create_passive_sell_offer"):
        pass  # no value movement by op itself; offer fills come from /trades
    else:
        ev.append(dict(ts=ts, bucket="UNMAPPED", asset="?", units=D(0), op=op["id"], optype=t, note=""))
    return ev

def trades_events(acct, trades):
    ev = []
    for tr in trades:
        ts = dt.datetime.strptime(tr["ledger_close_time"], "%Y-%m-%dT%H:%M:%SZ")
        b = "XLM" if tr["base_asset_type"] == "native" else akey(tr["base_asset_code"], tr["base_asset_issuer"])
        c = "XLM" if tr["counter_asset_type"] == "native" else akey(tr["counter_asset_code"], tr["counter_asset_issuer"])
        if tr.get("base_account") == acct:  # base sold, counter bought
            ev += [dict(ts=ts, bucket="C2C_OUT", sub=None, asset=b, units=D(tr["base_amount"]), op=tr["id"], optype="trade", note=tr["trade_type"]),
                   dict(ts=ts, bucket="C2C_IN", sub=None, asset=c, units=D(tr["counter_amount"]), op=tr["id"], optype="trade", note=tr["trade_type"])]
        elif tr.get("counter_account") == acct:
            ev += [dict(ts=ts, bucket="C2C_OUT", sub=None, asset=c, units=D(tr["counter_amount"]), op=tr["id"], optype="trade", note=tr["trade_type"]),
                   dict(ts=ts, bucket="C2C_IN", sub=None, asset=b, units=D(tr["base_amount"]), op=tr["id"], optype="trade", note=tr["trade_type"])]
    return ev

# ---------- aggregation + XML ----------
NIT = "900000000"  # synthetic 9-digit NIT (Colombian tax ID), no check digit, per Anexo T6.17 of DIAN (Colombia's tax authority)
MSGREF = "CO2026CO" + NIT + "00001"  # 22 chars: CO+year+receiving country+NIT+5
NS = "urn:oecd:ties:carf:v1"; STF = "urn:oecd:ties:carfstf:v5"
def E(parent, tag, text=None, ns=NS, **attr):
    e = etree.SubElement(parent, f"{{{ns}}}{tag}", **attr)
    if text is not None: e.text = str(text)
    return e

TAG = dict(C2C_IN="CryptoToCryptoIn", C2C_OUT="CryptoToCryptoOut", FIAT_IN="CryptoFiatIn", FIAT_OUT="CryptoFiatOut",
           XFER_IN="CryptoTransferIn", XFER_OUT="CryptoTransferOut", WALLET="TransferWallet", RRPT="RRPT")
ORDER = list(TAG)

def build_xml(users, ccy):
    root = etree.Element(f"{{{NS}}}CARF_OECD", nsmap={None: NS, "stf": STF, "iso": "urn:oecd:ties:isocarftypes:v1"}, version="1.0")
    ms = E(root, "MessageSpec")
    for k, v in [("SendingEntityIN", NIT), ("TransmittingCountry", "CO"), ("ReceivingCountry", "CO"),
                 ("MessageType", "CARF"), ("MessageRefId", MSGREF), ("MessageTypeIndic", "CARF701"),
                 ("ReportingPeriod", "2026-12-31"), ("Timestamp", dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S"))]:
        E(ms, k, v)
    body = E(root, "CARFBody")
    rc = E(body, "RCASP"); rid = E(rc, "RCASP_ID"); ent = E(rid, "Entity")
    E(ent, "ResCountryCode", "CO"); E(ent, "TIN", NIT, issuedBy="CO"); E(ent, "Name", "TEST RCASP S.A.S. (synthetic)")
    ad = E(ent, "Address"); E(ad, "CountryCode", "CO"); af = E(ad, "AddressFix"); E(af, "City", "Bogota")
    E(rc, "Nexus", "CARF901")
    ds = E(rc, "DocSpec"); E(ds, "DocTypeIndic", "OECD11", ns=STF); E(ds, "DocRefId", MSGREF + "000001", ns=STF)
    for n, (acct, agg) in enumerate(users.items(), 1):
        cu = E(body, "CryptoUsers"); uid = E(cu, "UserID"); ind = E(uid, "Individual")
        E(ind, "ResCountryCode", "CO"); E(ind, "TIN", "NOTIN", unknown="true")
        nm = E(ind, "Name"); E(nm, "FirstName", "Test"); E(nm, "LastName", f"User{n}")
        ad = E(ind, "Address"); E(ad, "CountryCode", "CO"); af = E(ad, "AddressFix"); E(af, "City", "Medellin")
        E(ad, "AdditionalAddressInfo", f"stellar:{acct}")  # NOT a CARF field; demo-only linkage
        bi = E(ind, "BirthInfo"); E(bi, "BirthDate", "1990-01-01")
        for (asset, bucket, sub), v in sorted(agg.items(), key=lambda kv: (kv[0][0], ORDER.index(kv[0][1]), kv[0][2] or "")):
            rt = E(cu, "RelevantTransactions"); E(rt, "CryptoAsset", asset if asset == "XLM" else asset.split(":")[0] + " (" + asset.split(":")[1][:8] + "...)")
            b = E(rt, TAG[bucket])
            if bucket in ("XFER_IN", "XFER_OUT"): E(b, "TransferType", sub)
            if bucket != "WALLET": E(b, "NumberofTransactions", v["n"])
            E(b, "Amount", f"{v[ccy]:.2f}", currCode=ccy)
            E(b, "NumberofUnits", f"{v['units'].quantize(D('0.000001'))}")
        ds = E(cu, "DocSpec"); E(ds, "DocTypeIndic", "OECD11", ns=STF); E(ds, "DocRefId", MSGREF + f"{n+1:06d}", ns=STF)
    return root

def main():
    accounts = {
        "GAFK7XFZHMLSNV7OJTBO7BAIZA66X6QIBV5RMZZYXK4Q7ZSO52J5C3WQ": "USDC issuer distribution account (classic payments)",
        "GDSF6R22FZVRCUJWSUZANWU4SPXIP5Z33R67FGEUNVWT2OGTUMLUIOFJ": "high-frequency SDEX account (offers/trades)",
        "GBH7JO6POSQY2LRFKGZTIQN3AB42ARIUO3XCLOWTDQ6MD2JSNPTHOD3Z": "account receiving Soroban SAC mints (invoke_host_function)",
    }
    users, allev = {}, []
    stats = collections.Counter()
    for acct, label in accounts.items():
        ops = recs(f"/accounts/{acct}/operations", limit=50)
        trs = recs(f"/accounts/{acct}/trades", limit=50)
        ev = []
        for op in ops:
            stats[op["type"]] += 1
            ev += classify(acct, op)
        ev += trades_events(acct, trs)
        agg = collections.defaultdict(lambda: dict(n=0, units=D(0), USD=D(0), COP=D(0)))
        unpriced = 0
        for e in ev:
            if e["bucket"] in ("TODO", "UNMAPPED"): LOG.append(("skip", acct[:6], e)); continue
            usd, how = usd_value(e["asset"], e["units"], e["ts"])
            r = trm(e["ts"].date().isoformat())
            e.update(usd=usd, how=how, trm=r)
            if usd is None: unpriced += 1; LOG.append(("unpriced", acct[:6], e["asset"], how)); continue
            k = (e["asset"], e["bucket"], e.get("sub"))
            agg[k]["n"] += 1; agg[k]["units"] += e["units"]; agg[k]["USD"] += usd; agg[k]["COP"] += usd * r
        users[acct] = agg
        allev += [(acct, e) for e in ev]
        print(f"\n## {label} {acct[:8]}..: ops={len(ops)} trades={len(trs)} events={len(ev)} unpriced={unpriced}")
        for (a, b, s), v in agg.items():
            print(f"  {a[:14]:14} {b:9} {s or '':8} n={v['n']:3} units={v['units']:.7f} USD={v['USD']:.2f} COP={v['COP']:.2f}")
    print("\nop types seen:", dict(stats))
    print("price cache:", {str(k): str(v) for k, v in list(_px.items())[:6]}, "TRM:", {k: str(v) for k, v in _trm.items()})
    # sample events
    with open("events_sample.json", "w") as f:
        json.dump([dict(account=a, **{k: (str(v) if not isinstance(v, (str, int, type(None))) else v) for k, v in e.items()}) for a, e in allev[:40]], f, indent=1)
    for ccy in ("COP", "USD"):
        root = build_xml(users, ccy)
        etree.ElementTree(root).write(f"carf_proto_{ccy}.xml", pretty_print=True, xml_declaration=True, encoding="UTF-8")
    for l in LOG[:10]: print("LOG", l)

if __name__ == "__main__":
    main()


def dian_checks(path):
    """Business rules from DIAN Anexo T6.17 not enforced by the XSD."""
    t = etree.parse(path); ns = {"c": NS, "s": STF}; errs = []
    ms = t.find("c:MessageSpec", ns); g = lambda e: ms.findtext("c:" + e, namespaces=ns)
    ref = g("MessageRefId")
    if len(ref) != 22: errs.append("MessageRefId must be 22 chars")
    if ref[:2] != g("TransmittingCountry") or g("TransmittingCountry") != "CO": errs.append("TransmittingCountry must be CO and prefix MessageRefId")
    if ref[2:6] != g("ReportingPeriod")[:4]: errs.append("MessageRefId year != ReportingPeriod")
    if ref[6:8] != g("ReceivingCountry"): errs.append("MessageRefId country != ReceivingCountry")
    if ref[8:17] != g("SendingEntityIN") or not g("SendingEntityIN").isdigit() or len(g("SendingEntityIN")) != 9: errs.append("SendingEntityIN must be 9-digit NIT matching MessageRefId")
    if not g("ReportingPeriod").endswith("-12-31"): errs.append("ReportingPeriod must be YYYY-12-31")
    ids = [d.text for d in t.iter("{%s}DocRefId" % STF)]
    for d in ids:
        if len(d) != 28 or not d.startswith(ref) or not d[22:].isdigit(): errs.append("bad DocRefId " + d)
    if len(set(ids)) != len(ids): errs.append("duplicate DocRefId")
    for a in t.iter("{%s}Amount" % NS):
        if "." not in a.text or len(a.text.split(".")[1]) != 2: errs.append("Amount not 2 decimals: " + a.text)
    ccys = {a.get("currCode") for a in t.iter("{%s}Amount" % NS)}
    if len(ccys) > 1: errs.append("more than one currency in file (CARF: single fiat currency for FMV)")
    return errs or ["OK: DIAN T6.17 header/DocRefId/amount rules pass"]

if __name__ == "__main__":
    for c in ("COP", "USD"): print(c, dian_checks(f"carf_proto_{c}.xml"))
