from datetime import datetime
from utils import fetch_data
from database import SessionLocal
import logging
from models import Bidding


def fetch_biddings(service_key, start_date, end_date):
    """입찰공고 수집 (전체 페이징 처리)"""
    
    apis = [
        ("http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwk", "공사"),
        ("http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServc", "용역"),
        ("http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoThng", "물품"),
    ]
    
    all_items = []
    inqry_bgn = start_date + "0000"
    inqry_end = end_date + "2359"
    
    for url, notice_type in apis:
        page = 1
        type_items = []  # 유형별 임시 리스트
        
        while True:
            params = {
                "pageNo": page,
                "numOfRows": 100,
                "inqryDiv": 1,
                "inqryBgnDt": inqry_bgn,
                "inqryEndDt": inqry_end,
                "serviceKey": service_key,
                "type": "json"
            }
            
            data = fetch_data(url, params)
            
            if not data or "response" not in data:
                logging.warning(f"❌ {notice_type} 페이지 {page} 응답 없음")
                break
            
            body = data["response"].get("body", {})
            items = body.get("items", [])
            total_count = body.get("totalCount", 0)
            
            if not items:
                logging.info(f"✅ {notice_type} 수집 완료 (총 {len(type_items)}건)")
                break
            
            # notice_type 태깅
            for item in items:
                item["_notice_type"] = notice_type
            
            type_items.extend(items)
            
            logging.info(f"📄 {notice_type} 페이지 {page}: {len(items)}건 (총 {total_count}건 중 {len(type_items)}건)")
            
            # 유형별 완료 체크
            if len(type_items) >= total_count:
                logging.info(f"✅ {notice_type} 전체 수집 완료 ({len(type_items)}건)")
                break
            
            page += 1
        
        all_items.extend(type_items)
    
    logging.info(f"🎉 입찰공고 전체 수집 완료: {len(all_items)}건")
    return all_items


def parse_datetime(date_str):
    """날짜 문자열을 datetime으로 변환"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        try:
            return datetime.strptime(date_str[:12], "%Y%m%d%H%M")
        except:
            return None


def upsert_biddings(items):
    """입찰공고 DB 저장"""
    db = SessionLocal()
    success_count = 0
    
    try:
        for item in items:
            try:
                notice_no = item.get("bidNtceNo")
                if not notice_no:
                    continue
                
                obj = db.query(Bidding).filter(Bidding.notice_number == notice_no).first()
                
                if obj is None:
                    obj = Bidding(notice_number=notice_no)
                    db.add(obj)
                
                notice_type = item.get("_notice_type")
                
                obj.notice_type = notice_type
                obj.title = item.get("bidNtceNm")
                obj.ordering_agency = item.get("ntceInsttNm")
                obj.demanding_agency = item.get("dminsttNm")
                obj.contract_method = item.get("cntrctCnclsMthdNm")
                obj.bidding_method = item.get("bidMethdNm")
                
                # ✅ 공사/용역/물품 구분해서 예산액 파싱
                if notice_type == "물품":
                    budget_value = item.get("asignBdgtAmt")
                else:
                    budget_value = item.get("bdgtAmt")
                
                obj.budget_amount = int(float(budget_value)) if budget_value else None
                obj.estimated_price = int(float(item.get("presmptPrce"))) if item.get("presmptPrce") else None
                
                obj.notice_date = parse_datetime(item.get("bidNtceDt"))
                obj.bid_close_date = parse_datetime(item.get("bidClseDt"))
                obj.order_instt_cd = item.get("ntceInsttCd")
                obj.order_instt_nm = item.get("ntceInsttNm")
                obj.description = item.get("bidNtceDtlUrl")
                obj.bidding_url = item.get("bidNtceUrl")
                
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
