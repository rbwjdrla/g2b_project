import requests
import logging
from sqlalchemy import create_engine, text
from datetime import datetime


class G2BApiClient:
    def __init__(self, db_url, service_key):
        self.db_url = db_url
        self.service_key = service_key
        self.engine = create_engine(db_url, echo=False)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # --------------------------
    # 공통 fetch 함수
    # --------------------------
    def fetch_data(self, url, params):
        try:
            response = requests.get(url, params=params, timeout=20)
            logging.info(f"🌐 {url}")
            print("\n=== ✅ RAW RESPONSE ===")
            print(response.text[:500])
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"❌ API 요청 실패: {url} ({e})")
            logging.error(f"resp.text: {getattr(response, 'text', 'no response')}")
            return None

    # --------------------------
    # ① 계약정보 (YYYYMMDD)
    # --------------------------
    def fetch_contract_list(self, start_date, end_date):
        base_url = "https://apis.data.go.kr/1230000/ao/CntrctInfoService/getCntrctInfoListThng"
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 3,  # ✅ 1 → 3 수정
            "inqryBgnDt": start_date[:8],
            "inqryEndDt": end_date[:8],
            "serviceKey": self.service_key,
            "type": "json"
        }
        data = self.fetch_data(base_url, params)
        if not data or "response" not in data:
            logging.warning("⚠️ 계약정보 응답이 비어있음")
            return []
        return data["response"].get("body", {}).get("items", [])

    # --------------------------
    # ② 발주계획 (YYYYMM)
    # --------------------------
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
            logging.warning("⚠️ 발주계획 응답이 비어있음")
            return []
        return data["response"].get("body", {}).get("items", [])

    # --------------------------
    # ③ 입찰공고 (공사 / 용역 / 물품)
    # --------------------------
    def fetch_bid_public(self, start_date, end_date, kind="공사"):
        base_url_map = {
            "공사": "http://apis.data.go.kr/1230000/BidPublicInfoService04/getBidPblancListInfoServc01",
            "용역": "http://apis.data.go.kr/1230000/BidPublicInfoService05/getBidPblancListInfoServc02",
            "물품": "http://apis.data.go.kr/1230000/BidPublicInfoService06/getBidPblancListInfoServc03"
        }

        base_url = base_url_map[kind]
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 1,
            "inqryBgnDt": f"{start_date[:8]}0000",
            "inqryEndDt": f"{end_date[:8]}2359",
            "serviceKey": self.service_key,
            "type": "json"
        }

        data = self.fetch_data(base_url, params)
        if not data or "response" not in data:
            logging.warning(f"⚠️ {kind} 입찰공고 응답이 비어있음")
            return []
        return data["response"].get("body", {}).get("items", [])

    # --------------------------
    # ④ 낙찰정보 (공사)
    # --------------------------
    def fetch_scsbid_info(self, start_date, end_date):
        base_url = "http://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoCnstwk"
        params = {
            "pageNo": 1,
            "numOfRows": 100,
            "inqryDiv": 3,
            "inqryBgnDt": f"{start_date[:8]}0000",
            "inqryEndDt": f"{end_date[:8]}2359",
            "serviceKey": self.service_key,
            "type": "json"
        }
        data = self.fetch_data(base_url, params)
        if not data or "response" not in data:
            logging.warning("⚠️ 낙찰정보 응답이 비어있음")
            return []
        return data["response"].get("body", {}).get("items", [])

    # --------------------------
    # DB 저장 함수들
    # --------------------------
    def save_contracts_to_db(self, items):
        if not items:
            logging.warning("⚠️ 저장할 계약정보가 없습니다.")
            return
        try:
            with self.engine.begin() as conn:
                for item in items:
                    conn.execute(
                        text("""
                            INSERT INTO contracts (
                                cntrct_no, cntrct_nm, cntrct_instt_nm,
                                cntrct_mthd_nm, cntrct_amt, supler_nm,
                                created_at, updated_at
                            )
                            VALUES (:no, :name, :inst, :mthd, :amt, :supler, NOW(), NOW())
                            ON CONFLICT (cntrct_no) DO NOTHING
                        """),
                        {
                            "no": item.get("dcsnCntrctNo"),
                            "name": item.get("cntrctNm"),
                            "inst": item.get("cntrctInsttNm"),
                            "mthd": item.get("baseLawNm"),
                            "amt": item.get("thtmCntrctAmt"),
                            "supler": item.get("cntrctInsttOfclNm"),
                        }
                    )
            logging.info(f"✅ {len(items)}건의 계약정보 저장 완료")
        except Exception as e:
            logging.error(f"❌ 계약정보 저장 실패: {e}")

    def save_plans_to_db(self, items):
        if not items:
            logging.warning("⚠️ 저장할 발주계획이 없습니다.")
            return
        try:
            with self.engine.begin() as conn:
                for item in items:
                    conn.execute(
                        text("""
                            INSERT INTO order_plans (
                                order_plan_unty_no, biz_nm, order_instt_nm,
                                sum_order_amt, order_year, order_mnth,
                                created_at, updated_at
                            )
                            VALUES (:no, :biz, :inst, :amt, :yr, :mn, NOW(), NOW())
                            ON CONFLICT (order_plan_unty_no) DO NOTHING
                        """),
                        {
                            "no": item.get("orderPlanSno"),
                            "biz": item.get("bizNm"),
                            "inst": item.get("orderInsttNm"),
                            "amt": item.get("sumOrderAmt"),
                            "yr": item.get("orderYear"),
                            "mn": item.get("orderMnth"),
                        }
                    )
            logging.info(f"✅ {len(items)}건의 발주계획 저장 완료")
        except Exception as e:
            logging.error(f"❌ 발주계획 저장 실패: {e}")

    def save_awards_to_db(self, items):
        if not items:
            logging.warning("⚠️ 저장할 낙찰정보가 없습니다.")
            return
        try:
            with self.engine.begin() as conn:
                for item in items:
                    conn.execute(
                        text("""
                            INSERT INTO awards (
                                bidno, bidname, bidwinnm, succamt, order_instt_nm,
                                created_at, updated_at
                            )
                            VALUES (:bidno, :bidname, :winnm, :amt, :inst, NOW(), NOW())
                            ON CONFLICT (bidno) DO NOTHING
                        """),
                        {
                            "bidno": item.get("bidNtceNo"),
                            "bidname": item.get("bidNm"),
                            "winnm": item.get("sucessfulBidderNm"),
                            "amt": item.get("sucessfulBidAmt"),
                            "inst": item.get("orderInsttNm"),
                        }
                    )
            logging.info(f"✅ {len(items)}건의 낙찰정보 저장 완료")
        except Exception as e:
            logging.error(f"❌ 낙찰정보 저장 실패: {e}")

    # --------------------------
    # 실행 메인
    # --------------------------
    def run(self, start_date, end_date):
        logging.info(f"📅 G2B 데이터 업데이트 중... ({start_date} ~ {end_date})")

        # 계약정보
        contracts = self.fetch_contract_list(start_date, end_date)
        logging.info(f"🧾 계약정보 수집 결과: {len(contracts)}건")
        self.save_contracts_to_db(contracts)

        # 발주계획
        plans = self.fetch_plan_list(start_date, end_date)
        logging.info(f"🧾 발주계획 수집 결과: {len(plans)}건")
        self.save_plans_to_db(plans)

        # 입찰공고 - 공사, 용역, 물품
        for kind in ["공사", "용역", "물품"]:
            bids = self.fetch_bid_public(start_date, end_date, kind)
            logging.info(f"🧾 {kind} 입찰공고 수집 결과: {len(bids)}건")
            # (추후 biddings 테이블 매핑 예정)

        # 낙찰정보
        awards = self.fetch_scsbid_info(start_date, end_date)
        logging.info(f"🧾 낙찰정보 수집 결과: {len(awards)}건")
        self.save_awards_to_db(awards)

        logging.info("✅ G2B 데이터 업데이트 완료")
