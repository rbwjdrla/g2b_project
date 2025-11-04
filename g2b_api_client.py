import requests
import logging
from sqlalchemy import create_engine, text


class G2BApiClient:
    def __init__(self, db_url, service_key):
        self.db_url = db_url
        self.service_key = service_key
        self.engine = create_engine(db_url, echo=False)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def fetch_data(self, url, params):
        try:
            response = requests.get(url, params=params, timeout=20)
            print("\n=== ✅ RAW RESPONSE ===")
            print(response.text[:1000])  # 실제 응답 확인
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"❌ API 요청 실패: {url} ({e})")
            return None

    def fetch_contract_list(self, start_date, end_date):
        base_url = "https://apis.data.go.kr/1230000/ao/CntrctInfoService/getCntrctInfoListThng"
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 1,
            "inqryBgnDt": start_date,
            "inqryEndDt": end_date,
            "serviceKey": self.service_key,
            "type": "json"
        }
        data = self.fetch_data(base_url, params)
        if not data or "response" not in data:
            logging.warning("⚠️ 계약정보 응답이 비어있습니다.")
            return []
        return data["response"].get("body", {}).get("items", [])

    def fetch_plan_list(self, start_date, end_date):
        base_url = "https://apis.data.go.kr/1230000/ao/OrderPlanSttusService/getOrderPlanSttusListThng"
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 1,
            "orderBgnYm": start_date[:6],
            "orderEndYm": end_date[:6],
            "serviceKey": self.service_key,
            "type": "json"
        }
        data = self.fetch_data(base_url, params)
        if not data or "response" not in data:
            logging.warning("⚠️ 발주계획 응답이 비어있습니다.")
            return []
        return data["response"].get("body", {}).get("items", [])

    def run(self, start_date, end_date):
        print("📅 최근 10일간 G2B 데이터 업데이트 중...")
        print("📦 계약정보 수집 중...")
        data_contract = self.fetch_contract_list(start_date, end_date)
        print(f"🧾 계약정보 수집 결과: {len(data_contract)}건")

        print("📦 발주계획 수집 중...")
        data_plan = self.fetch_plan_list(start_date, end_date)
        print(f"🧾 발주계획 수집 결과: {len(data_plan)}건")

        print("✅ G2B 데이터 업데이트 완료")
