from datetime import datetime
from utils import fetch_data
from database import SessionLocal
import logging
from models import Award

def fetch_awards(service_key, start_date, end_date):
    """낙찰정보 수집 (물품/공사/용역)"""
    
    # ✅ 올바른 Base URL
    base_url = "https://apis.data.go.kr/1230000/as/ScsbidInfoService"
    
    apis = [
        ("getOpengResultListInfoThng", "물품"),
        ("getOpengResultListInfoCnstwk", "공사"),
        ("getOpengResultListInfoServc", "용역")
    ]
    
    all_items = []
    inqry_bgn = start_date + "0000"
    inqry_end = end_date + "2359"
    
    for endpoint, notice_type in apis:
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
            
            # notice_type 추가
            for item in items:
                item["_notice_type"] = notice_type
            
            all_items.extend(items)
    
    return all_items


def parse_datetime(date_str):
    """날짜 문자열을 datetime으로 변환"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None


def parse_openg_corp_info(openg_corp_info):
    """개찰업체정보 파싱"""
    if not openg_corp_info:
        return None, None, None, None, None
    
    try:
        parts = openg_corp_info.split('^')
        if len(parts) >= 5:
            company_name = parts[0].strip()
            business_no = parts[1].strip()
            ceo_name = parts[2].strip()
            amount = int(parts[3]) if parts[3] else None
            rate = float(parts[4]) if parts[4] else None
            return company_name, business_no, ceo_name, amount, rate
    except:
        pass
    
    return None, None, None, None, None


def upsert_awards(items):
    """낙찰정보 DB 저장"""
    db = SessionLocal()
    success_count = 0
    
    try:
        for item in items:
            try:
                bid_ntce_no = item.get("bidNtceNo")
                bid_ntce_ord = item.get("bidNtceOrd", "000")
                notice_type = item.get("_notice_type")
                
                if not bid_ntce_no:
                    continue
                
                # 기존 레코드 조회
                obj = db.query(Award).filter(
                    Award.bid_ntce_no == bid_ntce_no,
                    Award.bid_ntce_ord == bid_ntce_ord,
                    Award.notice_type == notice_type
                ).first()
                
                if obj is None:
                    obj = Award(
                        bid_ntce_no=bid_ntce_no,
                        bid_ntce_ord=bid_ntce_ord,
                        notice_type=notice_type
                    )
                    db.add(obj)
                
                # 기본 정보
                obj.bid_clsfc_no = item.get("bidClsfcNo")
                obj.rbid_no = item.get("rbidNo")
                obj.bid_ntce_nm = item.get("bidNtceNm")
                obj.openg_dt = parse_datetime(item.get("opengDt"))
                
                # 낙찰 정보
                obj.prtcpt_cnum = int(item.get("prtcptCnum", 0))
                obj.openg_corp_info = item.get("opengCorpInfo")
                obj.progrs_div_cd_nm = item.get("progrsDivCdNm")
                
                # 개찰업체정보 파싱
                company, business_no, ceo, amount, rate = parse_openg_corp_info(
                    item.get("opengCorpInfo")
                )
                obj.award_company_name = company
                obj.award_business_no = business_no
                obj.award_ceo_name = ceo
                obj.award_amount = amount
                obj.award_rate = rate
                
                # 기관 정보
                obj.ntce_instt_cd = item.get("ntceInsttCd")
                obj.ntce_instt_nm = item.get("ntceInsttNm")
                obj.dminstt_cd = item.get("dminsttCd")
                obj.dminstt_nm = item.get("dminsttNm")
                
                # 메타 정보
                obj.inpt_dt = parse_datetime(item.get("inptDt"))
                obj.rsrvtn_prce_file_existnce_yn = item.get("rsrvtnPrceFileExistnceYn")
                obj.openg_rslt_ntc_cntnts = item.get("opengRsltNtcCntnts")
                
                db.commit()
                success_count += 1
                
            except Exception as e:
                logging.error(f"❌ 낙찰정보 {bid_ntce_no} 저장 실패: {e}")
                db.rollback()
                continue
        
        logging.info(f"💾 낙찰정보 저장 완료: {success_count}건")
        
    except Exception as e:
        logging.error(f"❌ 낙찰정보 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()