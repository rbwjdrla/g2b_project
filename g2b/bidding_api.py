from .utils import fetch_data
from database import SessionLocal
def fetch_biddings(service_key, start_date, end_date):
    apis = [
        "http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoCnstwk",  # 공사
        "http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoServc",  # 용역
        "http://apis.data.go.kr/1230000/ad/BidPublicInfoService/getBidPblancListInfoFrgcpt",  # 물품
    ]

    all_items = []

    inqry_bgn = start_date + "0000"
    inqry_end = end_date + "2359"

    for url in apis:
        params = {
            "pageNo": 1,
            "numOfRows": 10,
            "inqryDiv": 1,
            "inqryBgnDt": inqry_bgn,
            "inqryEndDt": inqry_end,
            "serviceKey": service_key,
            "type": "json"
        }
        data = fetch_data(url, params)
        if data and "response" in data:
            items = data["response"].get("body", {}).get("items", [])
            all_items.extend(items)
    return all_items

# db 저장
def upsert_biddings(items):
    db = SessionLocal()
    try:
        for item in items:
            notice_no = item.get("bidNtceNo")  # 공고번호
            if not notice_no:
                continue

            # 기존 데이터 조회
            obj = db.query(Bidding).filter(Bidding.notice_number == notice_no).first()

            if obj is None:
                obj = Bidding(notice_number=notice_no)
                db.add(obj)

            # 필드 매핑 (키 이름은 실제 응답에서 반드시 확인!)
            obj.title = item.get("bidNtceNm")
            obj.ordering_agency = item.get("ntceInsttNm")
            obj.demanding_agency = item.get("dmandInsttNm")
            obj.contract_method = item.get("cntrctCnclsMthdNm")
            obj.bidding_method = item.get("bidMethdNm")

            obj.budget_amount = (
                int(item.get("asignBdgtAmt")) if item.get("asignBdgtAmt") else None
            )
            obj.estimated_price = (
                int(item.get("presmptPrce")) if item.get("presmptPrce") else None
            )

            obj.notice_date = item.get("bidNtceDt")
            obj.bid_close_date = item.get("bidClseDt")
            obj.description = item.get("bidNtceDtlUrl")
            obj.bidding_url = item.get("bidNtceUrl")

        db.commit()
        logging.info(f"💾 입찰공고 저장 완료: {len(items)}건")
    except Exception as e:
        logging.error(f"❌ 입찰공고 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()
