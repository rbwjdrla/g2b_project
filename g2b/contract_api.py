from .utils import fetch_data

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
