import logging
from g2b.contract_api import fetch_contracts
from g2b.plan_api import fetch_plans
from g2b.bidding_api import fetch_biddings
from g2b.award_api import fetch_awards

def run_all(service_key, start_date, end_date):
    logging.info(f"📅 G2B 데이터 업데이트 중... ({start_date} ~ {end_date})")

    contracts = fetch_contracts(service_key, start_date, end_date)
    logging.info(f"🧾 계약정보 수집 결과: {len(contracts)}건")

    plans = fetch_plans(service_key, start_date, end_date)
    logging.info(f"🧾 발주계획 수집 결과: {len(plans)}건")

    biddings = fetch_biddings(service_key, start_date, end_date)
    logging.info(f"🧾 입찰공고 수집 결과: {len(biddings)}건")

    awards = fetch_awards(service_key, start_date, end_date)
    logging.info(f"🧾 낙찰정보 수집 결과: {len(awards)}건")

    logging.info("✅ G2B 데이터 업데이트 완료")
