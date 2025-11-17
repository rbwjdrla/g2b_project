from .utils import fetch_data

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
