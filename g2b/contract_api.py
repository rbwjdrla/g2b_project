from utils import fetch_data
from database import SessionLocal
from models import Contract
from datetime import datetime
import logging

def fetch_contracts(service_key, start_date, end_date):
    """계약정보 수집 (물품/용역/공사)"""
    
    base_url = "https://apis.data.go.kr/1230000/ao/CntrctInfoService"
    
    apis = [
        ("getCntrctInfoListThng", "물품"),
        ("getCntrctInfoListServc", "용역"),
        ("getCntrctInfoListCnstwk", "공사")
    ]
    
    all_items = []
    
    # ✅ YYYYMMDDHHmm 형식으로 변경!
    inqry_bgn = start_date + "0000"  # 20251125 → 202511250000
    inqry_end = end_date + "2359"    # 20251128 → 202511282359
    
    for endpoint, contract_type in apis:
        url = f"{base_url}/{endpoint}"
        
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 1,
            "inqryBgnDt": inqry_bgn,  # ✅ 12자리
            "inqryEndDt": inqry_end,  # ✅ 12자리
            "serviceKey": service_key,
            "type": "json"
        }
        
        data = fetch_data(url, params)
        if data and "response" in data:
            items = data["response"].get("body", {}).get("items", [])
            
            for item in items:
                item["_contract_type"] = contract_type
            
            all_items.extend(items)
    
    return all_items

def parse_date(date_str):
    """YYYYMMDD 형식을 datetime으로 변환"""
    if not date_str or len(date_str) < 8:
        return None
    try:
        return datetime.strptime(date_str[:8], "%Y%m%d")
    except:
        return None

def upsert_contracts(items):
    db = SessionLocal()
    try:
        for item in items:
            no = item.get("cntrctNo")
            if not no:
                continue
            
            #  필드명 수정
            obj = db.query(Contract).filter(Contract.cntrct_no == no).first()
            if obj is None:
                obj = Contract(cntrct_no=no)
                db.add(obj)
            
            #  필드명을 models.py와 일치시킴
            obj.cntrct_nm = item.get("cntrctNm")
            obj.cntrct_instt_nm = item.get("cntrctInsttNm")  # orderInsttNm → cntrctInsttNm
            obj.cntrct_mthd_nm = item.get("cntrctMthdNm")
            obj.cntrct_amt = int(item.get("cntrctAmt")) if item.get("cntrctAmt") else None
            obj.cntrct_dt = parse_date(item.get("cntrctDt"))  #  날짜 변환
            obj.cntrct_prd = item.get("cntrctPrd")
            obj.supler_nm = item.get("bidwinnm")  # 낙찰업체명
            
        db.commit()
        logging.info(f"💾 계약정보 저장 완료: {len(items)}건")
    except Exception as e:
        logging.error(f"❌ 계약정보 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()