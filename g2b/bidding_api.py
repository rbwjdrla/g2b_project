from .utils import fetch_data

def fetch_biddings(service_key, start_date, end_date):
    apis = [
        "https://apis.data.go.kr/1230000/BidPublicInfoService04/getBidPblancListInfoServc01",  # 공사
        "https://apis.data.go.kr/1230000/BidPublicInfoService05/getBidPblancListInfoServc02",  # 용역
        "https://apis.data.go.kr/1230000/BidPublicInfoService06/getBidPblancListInfoServc03",  # 물품
    ]

    all_items = []
    for url in apis:
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
        if data and "response" in data:
            items = data["response"].get("body", {}).get("items", [])
            all_items.extend(items)
    return all_items
