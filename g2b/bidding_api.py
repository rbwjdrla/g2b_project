from datetime import datetime
from utils import fetch_data
from database import SessionLocal
import logging
from models import Bidding

def fetch_biddings(service_key, start_date, end_date):
    apis = [
        ("http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwk", "공사"),  # 공사
        ("http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServc", "용역"),   # 용역
        ("http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThng", "물품"),  # 물품
    ]
    all_items = []
    inqry_bgn = start_date + "0000"
    inqry_end = end_date + "2359"
    
    for url, notice_type in apis:  # notice_type 추가
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
            # 각 item에 notice_type 추가
            for item in items:
                item["_notice_type"] = notice_type
            all_items.extend(items)
    
    return all_items

def parse_datetime(date_str):
    """날짜 문자열을 datetime으로 변환"""
    if not date_str:
        return None
    try:
        # "2025-11-24 08:20:31" 형식
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        try:
            # "202511240820" 형식 (만약을 위해)
            return datetime.strptime(date_str[:12], "%Y%m%d%H%M")
        except:
            return None


def upsert_biddings(items):
    db = SessionLocal()
    success_count = 0
    
    try:
        for item in items:
            try:
                notice_no = item.get("bidNtceNo")
                if not notice_no:
                    continue
                
                # 기존 레코드 조회
                obj = db.query(Bidding).filter(Bidding.notice_number == notice_no).first()
                
                if obj is None:
                    # 새 레코드 생성
                    obj = Bidding(notice_number=notice_no)
                    db.add(obj)
                
                # 필드 업데이트
                obj.notice_type = item.get("_notice_type")
                obj.title = item.get("bidNtceNm")
                obj.ordering_agency = item.get("ntceInsttNm")
                obj.demanding_agency = item.get("dminsttNm")
                obj.contract_method = item.get("cntrctCnclsMthdNm")
                obj.bidding_method = item.get("bidMethdNm")
                obj.budget_amount = int(item.get("bdgtAmt")) if item.get("bdgtAmt") else None
                obj.estimated_price = int(item.get("presmptPrce")) if item.get("presmptPrce") else None
                obj.notice_date = parse_datetime(item.get("bidNtceDt"))
                obj.bid_close_date = parse_datetime(item.get("bidClseDt"))
                obj.order_instt_cd = item.get("ntceInsttCd")
                obj.order_instt_nm = item.get("ntceInsttNm")
                obj.description = item.get("bidNtceDtlUrl")
                obj.bidding_url = item.get("bidNtceUrl")
                
                # ✅ 각 아이템마다 즉시 커밋!
                db.commit()
                success_count += 1
                
            except Exception as e:
                logging.error(f"❌ 입찰공고 {notice_no} 저장 실패: {e}")
                db.rollback()
                continue
        
        logging.info(f"💾 입찰공고 저장 완료: {success_count}건")
        
    except Exception as e:
        logging.error(f"❌ 입찰공고 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()