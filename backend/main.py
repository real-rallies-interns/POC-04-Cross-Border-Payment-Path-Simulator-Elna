from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
import pandas as pd
import numpy as np

app = FastAPI(title="Real Rails – Payment Path Simulator API v2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def build_corridor_df():
    raw = [
        ("USA","IND","USD/INR",83.5,6.2,3.1,"LOW"),
        ("USA","MEX","USD/MXN",17.2,4.8,1.5,"LOW"),
        ("USA","CHN","USD/CNY",7.25,5.5,2.8,"MEDIUM"),
        ("GBR","IND","GBP/INR",106.0,5.9,2.7,"LOW"),
        ("GBR","NGA","GBP/NGN",1650.0,8.4,4.2,"HIGH"),
        ("UAE","IND","AED/INR",22.7,3.8,1.2,"LOW"),
        ("UAE","PAK","AED/PKR",76.0,4.1,1.5,"MEDIUM"),
        ("SGP","IDN","SGD/IDR",11200.0,3.2,1.0,"LOW"),
        ("DEU","TUR","EUR/TRY",32.5,4.6,1.8,"LOW"),
        ("USA","BRA","USD/BRL",5.05,6.8,3.5,"LOW"),
        ("AUS","IND","AUD/INR",54.2,5.1,2.4,"LOW"),
        ("CAN","PHL","CAD/PHP",56.0,5.7,2.9,"LOW"),
        ("JPN","VNM","JPY/VND",158.0,4.3,1.6,"LOW"),
    ]
    df = pd.DataFrame(raw, columns=["from_country","to_country","currency_pair","mid_rate","avg_fee_pct","avg_days","sanctions_risk"])
    rng = np.random.default_rng(42)
    df["fee_volatility"] = rng.uniform(0.3, 1.2, len(df)).round(2)
    df["delay_volatility"] = rng.uniform(0.5, 2.0, len(df)).round(2)
    df["network_fee_pct"] = rng.uniform(0.1, 0.4, len(df)).round(2)
    df["fx_spread_base"] = rng.uniform(1.2, 3.5, len(df)).round(2)
    return df

def build_banks_df():
    raw = [
        ("USA","JPMorgan Chase","New York","JPUS33XXX",95,True,32.5),
        ("USA","Citibank","New York","CITIUSXXXX",92,True,28.1),
        ("USA","Bank of America","New York","BOFAUS3NXXX",88,True,24.3),
        ("GBR","HSBC","London","MIDLGB22XXX",94,True,35.2),
        ("GBR","Barclays","London","BARCGB22XXX",90,True,22.8),
        ("GBR","NatWest","London","NWBKGB2LXXX",85,False,18.4),
        ("DEU","Deutsche Bank","Frankfurt","DEUTDEDBXXX",93,True,30.1),
        ("DEU","Commerzbank","Frankfurt","COBADEFFXXX",87,True,19.7),
        ("UAE","Emirates NBD","Dubai","EBILAEAD",89,True,26.4),
        ("UAE","First Abu Dhabi","Abu Dhabi","NBADAEAA",86,False,21.3),
        ("SGP","DBS Bank","Singapore","DBSSSGSG",96,True,38.9),
        ("SGP","OCBC","Singapore","OCBCSGSG",88,True,20.5),
        ("SGP","Standard Chartered","Singapore","SCBLSGSG",91,True,25.7),
        ("JPN","MUFG Bank","Tokyo","BOTKJPJT",92,True,29.8),
        ("JPN","Sumitomo Mitsui","Tokyo","SMBCJPJT",89,True,22.1),
        ("IND","State Bank of India","Mumbai","SBININBB",84,False,15.6),
        ("IND","ICICI Bank","Mumbai","ICICINBB",82,False,14.2),
        ("IND","HDFC Bank","Mumbai","HDFCINBB",83,False,13.8),
        ("MEX","BBVA Mexico","Mexico City","BCMRMXMM",80,False,18.9),
        ("MEX","Banamex","Mexico City","BNMXMXMM",78,False,16.3),
        ("CHN","Bank of China","Shanghai","BKCHCNBJ",87,True,27.4),
        ("CHN","ICBC","Shanghai","ICBKCNBJ",89,True,31.2),
        ("NGA","Zenith Bank","Lagos","ZEIBNGLA",72,False,12.1),
        ("NGA","GTBank","Lagos","GTBINGLA",70,False,10.8),
        ("PAK","HBL","Karachi","HABBPKKA",68,False,9.4),
        ("PAK","MCB Bank","Karachi","MUCBPKKA",65,False,8.7),
        ("IDN","Bank Mandiri","Jakarta","BMRIIDJA",76,False,14.5),
        ("IDN","BRI","Jakarta","BRINIDJA",74,False,12.9),
        ("TUR","Garanti BBVA","Istanbul","TGBATRIS",79,False,16.8),
        ("TUR","Akbank","Istanbul","AKBKTRIS",77,False,15.2),
        ("BRA","Itaú","Sao Paulo","ITAUBRSP",85,True,23.6),
        ("BRA","Bradesco","Sao Paulo","BBDEBRSP",83,False,19.1),
        ("AUS","Commonwealth Bank","Sydney","CTBAAU2S",90,True,28.7),
        ("AUS","ANZ","Melbourne","ANZBAU3M",88,True,24.5),
        ("CAN","RBC","Toronto","ROYCCAT2",91,True,27.3),
        ("CAN","TD Bank","Toronto","TDOMCATT",89,True,25.1),
        ("PHL","BDO Unibank","Manila","BNORPHMM",75,False,13.4),
        ("PHL","BPI","Manila","BOPIPHMM",73,False,11.9),
        ("VNM","Vietcombank","Hanoi","BFTVVNVX",71,False,10.2),
        ("VNM","BIDV","Hanoi","BIDVVNVX",69,False,9.1),
    ]
    df = pd.DataFrame(raw, columns=["country","name","city","swift_bic","dominance_score","is_tier1","market_share_pct"])
    rng = np.random.default_rng(99)
    df["base_fee_usd"] = rng.uniform(8, 45, len(df)).round(2)
    df["base_delay_hours"] = rng.uniform(0.5, 18, len(df)).round(1)
    return df

CORRIDOR_DF = build_corridor_df()
BANKS_DF = build_banks_df()

COUNTRY_NAMES = {
    "USA":"United States","IND":"India","MEX":"Mexico","CHN":"China",
    "GBR":"United Kingdom","NGA":"Nigeria","UAE":"UAE","PAK":"Pakistan",
    "SGP":"Singapore","IDN":"Indonesia","DEU":"Germany","TUR":"Turkey",
    "BRA":"Brazil","AUS":"Australia","CAN":"Canada","PHL":"Philippines",
    "JPN":"Japan","VNM":"Vietnam",
}

class Hop(BaseModel):
    hop_number: int
    institution: str
    role: str
    country: str
    fee_usd: float
    fee_breakdown: dict
    delay_hours: float
    swift_code: str
    sanctions_flag: str
    cumulative_fee_usd: float
    cumulative_hours: float
    amount_after_hop: float

class FXBreakdown(BaseModel):
    mid_market_rate: float
    bank_rate: float
    spread_pct: float
    hidden_cost_usd: float
    currency_pair: str

class RailComparison(BaseModel):
    rail: str
    avg_fee_pct: float
    avg_hours: float
    transparency: str
    settlement: str

class ControlNode(BaseModel):
    country: str
    bank: str
    dominance_score: int
    market_share_pct: float
    is_tier1: bool

class SimulationResult(BaseModel):
    from_country: str
    to_country: str
    from_name: str
    to_name: str
    send_amount: float
    hops: List[Hop]
    fx: FXBreakdown
    total_fee_usd: float
    total_fee_pct: float
    total_correspondent_fees: float
    total_network_fees: float
    total_fx_cost: float
    estimated_arrival_hours: float
    estimated_arrival_days: float
    amount_received: float
    sanctions_risk: str
    corridor_note: str
    rail_comparisons: List[RailComparison]

def get_corridor(from_c, to_c):
    match = CORRIDOR_DF[(CORRIDOR_DF["from_country"]==from_c)&(CORRIDOR_DF["to_country"]==to_c)]
    if not match.empty:
        return match.iloc[0]
    return pd.Series({"from_country":from_c,"to_country":to_c,"currency_pair":f"{from_c[:3]}/{to_c[:3]}","mid_rate":1.0,"avg_fee_pct":7.0,"avg_days":4.0,"sanctions_risk":"LOW","fee_volatility":0.8,"delay_volatility":1.2,"network_fee_pct":0.2,"fx_spread_base":2.5})

def get_banks(country):
    return BANKS_DF[BANKS_DF["country"]==country]

def fee_breakdown(base, net_pct, amount):
    c = round(base*0.6, 2)
    n = round(amount*net_pct/100, 2)
    p = round(base*0.4, 2)
    return {"correspondent_fee":c,"network_fee":n,"processing_fee":p,"total":round(c+n+p,2)}

def simulate_payment(from_c, to_c, amount):
    corridor = get_corridor(from_c, to_c)
    rng = np.random.default_rng(abs(hash(f"{from_c}{to_c}"))%(2**31))
    src = get_banks(from_c)
    dst = get_banks(to_c)
    sb = src.iloc[0] if not src.empty else None
    db = dst.iloc[0] if not dst.empty else None
    net_pct = float(corridor["network_fee_pct"])

    intermediaries = []
    if from_c in ["USA","GBR","SGP"] and to_c in ["IND","PAK","NGA","PHL","VNM"]:
        hub = "SGP" if from_c!="SGP" else "GBR"
        hb = get_banks(hub)
        if not hb.empty: intermediaries=[(hub,hb.iloc[0])]
    elif from_c=="UAE":
        intermediaries=[]
    elif from_c=="DEU":
        ub=get_banks("USA")
        if not ub.empty: intermediaries=[("USA",ub.iloc[1] if len(ub)>1 else ub.iloc[0])]
    else:
        hub="USA" if from_c!="USA" else "GBR"
        hb=get_banks(hub)
        if not hb.empty: intermediaries=[(hub,hb.iloc[0])]

    hops=[]
    cum_fee=0.0; cum_hrs=0.0; running=amount
    tot_corr=0.0; tot_net=0.0

    ob=float(sb["base_fee_usd"]) if sb is not None else float(rng.uniform(10,25))
    obd=fee_breakdown(ob,net_pct,running)
    od=round(max(0.5,float(sb["base_delay_hours"])*0.15+float(rng.uniform(-0.2,0.5))),1) if sb is not None else round(float(rng.uniform(0.5,2.0)),1)
    oname=f"{sb['name']} ({sb['city']})" if sb is not None else f"Central Bank ({from_c})"
    oswift=sb["swift_bic"][:8] if sb is not None else f"{from_c[:2]}AAXX"
    running-=obd["total"]; cum_fee+=obd["total"]; cum_hrs+=od
    tot_corr+=obd["correspondent_fee"]; tot_net+=obd["network_fee"]
    hops.append(Hop(hop_number=1,institution=oname,role="Originating Bank",country=from_c,fee_usd=round(obd["total"],2),fee_breakdown=obd,delay_hours=od,swift_code=oswift,sanctions_flag="CLEAR",cumulative_fee_usd=round(cum_fee,2),cumulative_hours=round(cum_hrs,1),amount_after_hop=round(running,2)))

    sr=str(corridor["sanctions_risk"])
    for i,(hc,hbank) in enumerate(intermediaries):
        hb_val=float(hbank["base_fee_usd"]) if hbank is not None else float(rng.uniform(15,45))
        hbd=fee_breakdown(hb_val,net_pct,running)
        hd=round(max(1.0,float(hbank["base_delay_hours"])*0.4+float(rng.uniform(0,2))),1) if hbank is not None else round(float(rng.uniform(4,18)),1)
        flag="MANUAL_REVIEW" if sr=="HIGH" and i==0 else "CLEAR"
        if flag=="MANUAL_REVIEW": hd+=float(rng.uniform(24,48))
        hswift=hbank["swift_bic"][:8] if hbank is not None else f"{hc[:2]}BBXX"
        hname=f"{hbank['name']} ({hbank['city']})" if hbank is not None else f"Hub Bank ({hc})"
        running-=hbd["total"]; cum_fee+=hbd["total"]; cum_hrs+=hd
        tot_corr+=hbd["correspondent_fee"]; tot_net+=hbd["network_fee"]
        hops.append(Hop(hop_number=len(hops)+1,institution=hname,role="Correspondent Bank",country=hc,fee_usd=round(hbd["total"],2),fee_breakdown=hbd,delay_hours=round(hd,1),swift_code=hswift,sanctions_flag=flag,cumulative_fee_usd=round(cum_fee,2),cumulative_hours=round(cum_hrs,1),amount_after_hop=round(running,2)))

    rb=float(db["base_fee_usd"])*0.5 if db is not None else float(rng.uniform(5,20))
    rbd=fee_breakdown(rb,net_pct*0.5,running)
    rd=round(max(0.5,float(db["base_delay_hours"])*0.1),1) if db is not None else round(float(rng.uniform(1,4)),1)
    rname=f"{db['name']} ({db['city']})" if db is not None else f"Central Bank ({to_c})"
    rswift=db["swift_bic"][:8] if db is not None else f"{to_c[:2]}CCXX"
    running-=rbd["total"]; cum_fee+=rbd["total"]; cum_hrs+=rd
    tot_corr+=rbd["correspondent_fee"]; tot_net+=rbd["network_fee"]
    hops.append(Hop(hop_number=len(hops)+1,institution=rname,role="Receiving Bank",country=to_c,fee_usd=round(rbd["total"],2),fee_breakdown=rbd,delay_hours=rd,swift_code=rswift,sanctions_flag="CLEAR",cumulative_fee_usd=round(cum_fee,2),cumulative_hours=round(cum_hrs,1),amount_after_hop=round(running,2)))

    mid=float(corridor["mid_rate"])
    sp=round(float(corridor["fx_spread_base"])+float(rng.uniform(-0.3,0.8)),2)
    br=round(mid*(1-sp/100),4)
    fxc=round(running*(sp/100),2)
    running-=fxc
    total_fee=round(amount-running,2)
    total_pct=round((total_fee/amount)*100,2)

    rails=[
        RailComparison(rail="SWIFT",avg_fee_pct=total_pct,avg_hours=round(cum_hrs,1),transparency="Low",settlement="T+1 to T+5"),
        RailComparison(rail="RTP / Instant",avg_fee_pct=round(total_pct*0.35,2),avg_hours=0.01,transparency="High",settlement="Real-time"),
        RailComparison(rail="Crypto / Stablecoin",avg_fee_pct=round(total_pct*0.08,2),avg_hours=0.25,transparency="Very High",settlement="Near-instant"),
    ]

    return SimulationResult(
        from_country=from_c,to_country=to_c,
        from_name=COUNTRY_NAMES.get(from_c,from_c),to_name=COUNTRY_NAMES.get(to_c,to_c),
        send_amount=amount,hops=hops,
        fx=FXBreakdown(mid_market_rate=mid,bank_rate=br,spread_pct=sp,hidden_cost_usd=fxc,currency_pair=str(corridor["currency_pair"])),
        total_fee_usd=total_fee,total_fee_pct=total_pct,
        total_correspondent_fees=round(tot_corr,2),total_network_fees=round(tot_net,2),total_fx_cost=fxc,
        estimated_arrival_hours=round(cum_hrs,1),estimated_arrival_days=round(cum_hrs/24,1),
        amount_received=round(running,2),sanctions_risk=sr,
        corridor_note=f"This {COUNTRY_NAMES.get(from_c,from_c)} → {COUNTRY_NAMES.get(to_c,to_c)} corridor averages {corridor['avg_fee_pct']}% in total friction costs per the World Bank Remittance Matrix.",
        rail_comparisons=rails,
    )

@app.get("/")
def root(): return {"status":"Real Rails API v2.0 — Synthetic Data Engine Active"}

@app.get("/corridors")
def list_corridors():
    return CORRIDOR_DF[["from_country","to_country","avg_fee_pct","avg_days","sanctions_risk"]].rename(columns={"from_country":"from","to_country":"to"}).assign(from_name=CORRIDOR_DF["from_country"].map(COUNTRY_NAMES),to_name=CORRIDOR_DF["to_country"].map(COUNTRY_NAMES)).to_dict(orient="records")

@app.get("/countries")
def list_countries():
    countries=set(CORRIDOR_DF["from_country"])|set(CORRIDOR_DF["to_country"])
    return [{"code":c,"name":COUNTRY_NAMES.get(c,c)} for c in sorted(countries)]

@app.get("/control-map")
def control_map():
    top=BANKS_DF.sort_values("dominance_score",ascending=False).groupby("country").head(1)
    return [ControlNode(country=r["country"],bank=f"{r['name']} ({r['city']})",dominance_score=int(r["dominance_score"]),market_share_pct=float(r["market_share_pct"]),is_tier1=bool(r["is_tier1"])).dict() for _,r in top.iterrows()]

@app.get("/simulate",response_model=SimulationResult)
def simulate(from_country:str=Query(...),to_country:str=Query(...),amount:float=Query(10000.0,ge=100,le=1_000_000)):
    return simulate_payment(from_country.upper(),to_country.upper(),amount)