from .utils import fetch_data
from database import SessionLocal
def fetch_contracts(service_key, start_date, end_date):
    url = "https://apis.data.go.kr/1230000/ao/CntrctInfoService/getCntrctInfoListThng"
    params = {
        "pageNo": 1,
        "numOfRows": 100,
        "inqryDiv": 2,  # 월 단위 조회
        "inqryBgnDt": start_date[:6],
        "inqryEndDt": end_date[:6],
        "serviceKey": service_key,
        "type": "json"
    }
    data = fetch_data(url, params)
    if not data or "response" not in data:
        return []
    return data["response"].get("body", {}).get("items", [])


def upsert_contracts(items):
    db = SessionLocal()
    try:
        for item in items:
            no = item.get("cntrctNo")
            if not no:
                continue

            obj = db.query(Contract).filter(Contract.contract_number == no).first()
            if obj is None:
                obj = Contract(contract_number=no)
                db.add(obj)

            obj.contract_name = item.get("cntrctNm")
            obj.ordering_agency = item.get("orderInsttNm")
            obj.supplier = item.get("supplierNm")
            obj.amount = (
                int(item.get("cntrctAmt")) if item.get("cntrctAmt") else None
            )
            obj.contract_date = item.get("cntrctDt")

        db.commit()
        logging.info(f"💾 계약정보 저장 완료: {len(items)}건")
    except Exception as e:
        logging.error(f"❌ 계약정보 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()
