import logging
from contract_api import fetch_contracts
from plan_api import fetch_plans
from bidding_api import fetch_biddings
from award_api import fetch_awards
from contract_api import fetch_contracts, upsert_contracts
from plan_api import fetch_plans, upsert_plans
from bidding_api import fetch_biddings, upsert_biddings
from award_api import fetch_awards, upsert_awards


def run_all(service_key, start_date, end_date):
    logging.info(f"📅 G2B 데이터 업데이트 중... ({start_date} ~ {end_date})")
    #1) 계약정보
    contracts = fetch_contracts(service_key, start_date, end_date)
    logging.info(f"🧾 계약정보 수집 결과: {len(contracts)}건")
    if contracts:
   	 upsert_contracts(contracts)

    #2) 발주계획
    plans = fetch_plans(service_key, start_date, end_date)
    logging.info(f"🧾 발주계획 수집 결과: {len(plans)}건")
    if plans:
   	 upsert_plans(plans)

    #3) 입찰공고
    biddings = fetch_biddings(service_key, start_date, end_date)
    logging.info(f"🧾 입찰공고 수집 결과: {len(biddings)}건")
    if biddings:
   	 upsert_biddings(biddings)

    #4) 낙찰정보
    awards = fetch_awards(service_key, start_date, end_date)
    logging.info(f"🧾 낙찰정보 수집 결과: {len(awards)}건")
    if awards:
   	 upsert_awards(awards)

    logging.info("✅ G2B 데이터 업데이트 완료")
