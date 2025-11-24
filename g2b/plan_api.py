from .utils import fetch_data
from database import SessionLocal
import logging
from models import OrderPlan
def fetch_plans(service_key, start_date, end_date):
    url = "https://apis.data.go.kr/1230000/ao/OrderPlanSttusService/getOrderPlanSttusListThng"
    params = {
        "pageNo": 1,
        "numOfRows": 100,
        "inqryDiv": 1,
        "orderBgnYm": start_date[:6],
        "orderEndYm": end_date[:6],
        "serviceKey": service_key,
        "type": "json"
    }
    data = fetch_data(url, params)
    if not data or "response" not in data:
        return []
    return data["response"].get("body", {}).get("items", [])


def upsert_plans(items):
    db = SessionLocal()
    try:
        for item in items:
            no = item.get("orderPlanSno")
            if not no:
                continue

            obj = db.query(OrderPlan).filter(OrderPlan.order_plan_unty_no == no).first()
            if obj is None:
                obj = OrderPlan(order_plan_unty_no=no)
                db.add(obj)

            obj.biz_name = item.get("bizNm")
            obj.order_year = item.get("orderYear")
            obj.order_month = item.get("orderMnth")
            obj.order_amount = (
                int(item.get("sumOrderAmt")) if item.get("sumOrderAmt") else None
            )
            obj.ordering_agency = item.get("orderInsttNm")

        db.commit()
        logging.info(f"💾 발주계획 저장 완료: {len(items)}건")
    except Exception as e:
        logging.error(f"❌ 발주계획 upsert 실패: {e}")
        db.rollback()
    finally:
        db.close()
