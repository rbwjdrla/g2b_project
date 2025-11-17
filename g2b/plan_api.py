from .utils import fetch_data

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
