"""
G2B (나라장터) 공공데이터포털 API 연동 모듈
- 입찰공고 / 낙찰정보 / 계약정보 / 발주계획 4개 API 통합
- .env 파일의 G2B_API_KEY 사용
"""

import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from models import Bidding
from database import SessionLocal
from dotenv import load_dotenv

# ===== 환경 변수 로드 =====
load_dotenv()


class G2BApiClient:
    """공공데이터포털 G2B API 클라이언트"""

    def __init__(self):
        self.api_key = os.getenv("G2B_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 환경 변수에 G2B_API_KEY가 없습니다 (.env 확인 필요)")

        # API 엔드포인트 정의
        self.base_urls = {
            "bidding": "https://apis.data.go.kr/1230000/ad/BidPublicInfoService",
            "award": "https://apis.data.go.kr/1230000/as/ScsbidInfoService",
            "contract": "https://apis.data.go.kr/1230000/ao/CntrctInfoService",
            "plan": "https://apis.data.go.kr/1230000/ao/OrderPlanSttusService",
        }

    # ========================================================================
    # 공공데이터포털 API 공통 요청 함수
    # ========================================================================
    def _request(self, url: str, params: dict):
        """공통 API 요청 함수"""
        params["serviceKey"] = self.api_key
        params["type"] = "json"

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f"❌ API 요청 실패: {url} ({e})")
            return None

    # ========================================================================
    # 1️⃣ 입찰공고 정보 조회
    # ========================================================================
    def fetch_bidding_list(self, page: int = 1, rows: int = 50):
        url = f"{self.base_urls['bidding']}/getBidPblancListInfo"
        params = {"pageNo": page, "numOfRows": rows}
        return self._request(url, params)

    # ========================================================================
    # 2️⃣ 낙찰정보 조회
    # ========================================================================
    def fetch_award_list(self, page: int = 1, rows: int = 50):
        url = f"{self.base_urls['award']}/getScsbidListInfo"
        params = {"pageNo": page, "numOfRows": rows}
        return self._request(url, params)

    # ========================================================================
    # 3️⃣ 계약정보 조회
    # ========================================================================
    def fetch_contract_list(self, page: int = 1, rows: int = 50):
        url = f"{self.base_urls['contract']}/getCntrctInfoList"
        params = {"pageNo": page, "numOfRows": rows}
        return self._request(url, params)

    # ========================================================================
    # 4️⃣ 발주계획 현황 조회
    # ========================================================================
    def fetch_plan_list(self, page: int = 1, rows: int = 50):
        url = f"{self.base_urls['plan']}/getOrderPlanSttusList"
        params = {"pageNo": page, "numOfRows": rows}
        return self._request(url, params)

    # ========================================================================
    # 5️⃣ DB 저장 (입찰공고 기준)
    # ========================================================================
    def save_biddings_to_db(self, data):
        """입찰공고 데이터를 PostgreSQL에 저장"""
        if not data or "response" not in data:
            print("⚠️ 저장할 데이터가 없습니다.")
            return

        body = data["response"].get("body")
        if not body or "items" not in body:
            print("⚠️ API 응답에 데이터 없음.")
            return

        items = body["items"]
        db: Session = SessionLocal()
        count = 0

        try:
            for item in items:
                notice_number = item.get("bidNtceNo")
                if (
                    db.query(Bidding)
                    .filter(Bidding.notice_number == notice_number)
                    .first()
                ):
                    continue

                bidding = Bidding(
                    notice_number=notice_number,
                    title=item.get("bidNtceNm"),
                    ordering_agency=item.get("ntceInsttNm"),
                    demanding_agency=item.get("dminsttNm"),
                    contract_method=item.get("cntrctCnclsMthdNm"),
                    bidding_method=item.get("bidMethdNm"),
                    budget_amount=item.get("asignBdgtAmt"),
                    estimated_price=item.get("presmptPrce"),
                    notice_date=self._parse_date(item.get("ntceBgnde")),
                    bid_close_date=self._parse_date(item.get("ntceEndde")),
                    bidding_url=item.get("bidNtceDtlUrl"),
                    description=item.get("bidNtceCont", ""),
                )
                db.add(bidding)
                count += 1

            db.commit()
            print(f"✅ {count}건 저장 완료")
        except Exception as e:
            db.rollback()
            print(f"❌ DB 저장 실패: {e}")
        finally:
            db.close()

    # ========================================================================
    # 6️⃣ 날짜 파싱 유틸리티
    # ========================================================================
    @staticmethod
    def _parse_date(date_str: str):
        """YYYYMMDDHHmm 또는 YYYYMMDD 형식 → datetime 변환"""
        if not date_str:
            return None
        for fmt in ("%Y%m%d%H%M", "%Y%m%d"):
            try:
                return datetime.strptime(date_str, fmt)
            except Exception:
                continue
        return None

    # ========================================================================
    # 7️⃣ 최근 데이터 업데이트 (app.py에서 호출됨)
    # ========================================================================
    def update_all(self, days: int = 3):
        """
        최근 N일간의 입찰공고 데이터를 조회하여 DB에 저장
        (필요 시 낙찰/계약/발주계획 API로 확장 가능)
        """
        print(f"📅 최근 {days}일간 입찰공고 데이터 업데이트 중...")
        try:
            data = self.fetch_bidding_list(page=1, rows=100)
            self.save_biddings_to_db(data)
            print("✅ G2B 입찰공고 데이터 업데이트 완료")
        except Exception as e:
            print(f"❌ G2B 데이터 업데이트 실패: {e}")


# ========================================================================
# 단독 실행 테스트
# ========================================================================
if __name__ == "__main__":
    client = G2BApiClient()
    print("🚀 G2B 입찰공고 API 테스트 중...")
    data = client.fetch_bidding_list(page=1, rows=5)
    client.save_biddings_to_db(data)
