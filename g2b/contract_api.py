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
    
    # YYYYMMDDHHmm 형식으로 변경
    inqry_bgn = start_date + "0000"
    inqry_end = end_date + "2359"
    
    for endpoint, contract_type in apis:
        url = f"{base_url}/{endpoint}"
        
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 1,
            "inqryBgnDt": inqry_bgn,
            "inqryEndDt": inqry_end,
            "serviceKey": service_key,
            "type": "json"
        }
        
        data = fetch_data(url, params)
        if data and "response" in data:
            items = data["response"].get("body", {}).get("items", [])
            
            # 계약 타입 태깅
            for item in items:
                item["_contract_type"] = contract_type
            
            all_items.extend(items)
    
    return all_items


def parse_date(date_str):
    """YYYY-MM-DD 형식을 date로 변환"""
    if not date_str:
        return None
    try:
        # "2024-12-03" 형식
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:
        return None


def parse_int(value):
    """문자열을 정수로 변환"""
    if not value:
        return None
    try:
        return int(value)
    except:
        return None


def upsert_contracts(items):
    """계약정보 DB 저장"""
    db = SessionLocal()
    saved_count = 0
    
    try:
        for item in items:
            # 통합계약번호 (Primary Key)
            unty_no = item.get("untyCntrctNo")
            contract_type = item.get("_contract_type", "")
            
            if not unty_no:
                continue
            
            try:
                # 기존 레코드 확인
                obj = db.query(Contract).filter(
                    Contract.unty_cntrct_no == unty_no,
                    Contract.contract_type == contract_type
                ).first()
                
                if obj is None:
                    obj = Contract(
                        unty_cntrct_no=unty_no,
                        contract_type=contract_type
                    )
                    db.add(obj)
                
                # 기본 정보
                obj.bsns_div_nm = item.get("bsnsDivNm")
                obj.dcsn_cntrct_no = item.get("dcsnCntrctNo")
                obj.cntrct_ref_no = item.get("cntrctRefNo")
                
                # 계약 상세
                obj.cntrct_nm = item.get("cntrctNm")
                obj.cmmn_cntrct_yn = item.get("cmmnCntrctYn")
                obj.lngtrm_ctnu_div_nm = item.get("lngtrmCtnuDivNm")
                obj.cntrct_cncls_date = parse_date(item.get("cntrctCnclsDate"))
                obj.cntrct_prd = item.get("cntrctPrd")
                obj.base_law_nm = item.get("baseLawNm")
                
                # 금액 정보
                obj.tot_cntrct_amt = parse_int(item.get("totCntrctAmt"))
                obj.thtm_cntrct_amt = parse_int(item.get("thtmCntrctAmt"))
                obj.grntymny_rate = item.get("grntymnyRate")
                obj.pay_div_nm = item.get("payDivNm")
                
                # 참조 정보
                obj.req_no = item.get("reqNo")
                obj.ntce_no = item.get("ntceNo")
                
                # 계약기관 정보
                obj.cntrct_instt_cd = item.get("cntrctInsttCd")
                obj.cntrct_instt_nm = item.get("cntrctInsttNm")
                obj.cntrct_instt_jrsdctn_div_nm = item.get("cntrctInsttJrsdctnDivNm")
                obj.cntrct_instt_chrg_dept_nm = item.get("cntrctInsttChrgDeptNm")
                obj.cntrct_instt_ofcl_nm = item.get("cntrctInsttOfclNm")
                obj.cntrct_instt_ofcl_tel_no = item.get("cntrctInsttOfclTelNo")
                obj.cntrct_instt_ofcl_fax_no = item.get("cntrctInsttOfclFaxNo")
                
                # 리스트 정보 (문자열로 저장)
                obj.dminstt_list = item.get("dminsttList")
                obj.corp_list = item.get("corpList")
                
                # URL
                obj.cntrct_info_url = item.get("cntrctInfoUrl")
                obj.cntrct_dtl_info_url = item.get("cntrctDtlInfoUrl")
                
                db.commit()
                saved_count += 1
                
            except Exception as e:
                logging.error(f"❌ 계약정보 저장 실패 ({unty_no}): {e}")
                db.rollback()
                continue
        
        logging.info(f"💾 계약정보 저장 완료: {saved_count}건")
        
    except Exception as e:
        logging.error(f"❌ 계약정보 upsert 전체 실패: {e}")
        db.rollback()
    finally:
        db.close()