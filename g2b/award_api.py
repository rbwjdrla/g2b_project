from .utils import fetch_data
from g2b.database import SessionLocal
from g2b.models import award
import logging
def fetch_awards(service_key, start_date, end_date):
    url = "https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoCnstwk"
    params = {
        "pageNo": 1,
        "numOfRows": 100,
        "inqryDiv": 1,
        "inqryBgnDt": start_date[:8],
        "inqryEndDt": end_date[:8],
        "serviceKey": service_key,
        "type": "json"
    }
    data = fetch_data(url, params)
    if not data or "response" not in data:
        return []
    return data["response"].get("body", {}).get("items", [])



def upsert_awards(items):
    db = SessionLocal()
    try:
        for item in items:
            cont_no = item.get("cntrctNo")
            if not cont_no:
                continue

            obj = db.query(Award).filter(Award.contract_number == cont_no).first()
            if obj is None:
                obj = Award(contract_number=cont_no)
                db.add(obj)

            obj.bidname = item.get("bidNtceNm")
            obj.bidwinnm = item.get("sccNm")
            obj.succamt = (
                int(item.get("sccAmt")) if item.get("sccAmt") else None
            )
            obj.open_date = item.get("opengDt")

        db.commit()
        logging.info(f"💾 낙찰정보 저장 완료: {len(items)}건")
    except Exception as e:
        logging.error(f"❌ 낙찰정보 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()
