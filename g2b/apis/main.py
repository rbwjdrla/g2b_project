import logging
from datetime import datetime, timedelta
from config import settings
import gc

# 상대 경로 import
from .bidding_api import fetch_biddings, upsert_biddings
from .award_api import fetch_awards, upsert_awards
from .orderplan_api import fetch_plans, upsert_plans
# from .contract_api import fetch_contracts, upsert_contracts  # 계약정보 (현재 미사용)

logger = logging.getLogger(__name__)

def run_all(days=1):
    """
    전체 데이터 수집
    스케줄러에서 10분마다 자동 실행됨 (기본 2일치, 실시간)
    """
    service_key = settings.SERVICE_KEY

    # days일 전부터 오늘까지
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_day = start_date.strftime("%Y%m%d")
    end_day = end_date.strftime("%Y%m%d")

    logger.info(f"📅 G2B 데이터 수집 시작: {start_day} ~ {end_day} ({days}일)")
    
    try:
        # 1) 입찰공고
        logger.info("📋 입찰공고 수집 시작")
        biddings = fetch_biddings(service_key, start_day, end_day)
        if biddings:
            upsert_biddings(biddings)
            logger.info(f"✅ 입찰공고 수집 완료: {len(biddings)}건")
        
        # 2) 낙찰정보
        logger.info("🏆 낙찰정보 수집 시작")
        awards = fetch_awards(service_key, start_day, end_day)
        if awards:
            upsert_awards(awards)
            logger.info(f"✅ 낙찰정보 수집 완료: {len(awards)}건")
        
        # 3) 발주계획
        logger.info("📋 발주계획 수집 시작")
        plans = fetch_plans(service_key, start_day, end_day)
        if plans:
            upsert_plans(plans)
            logger.info(f"✅ 발주계획 수집 완료: {len(plans)}건")
        
        # logger.info("📄 계약정보 수집 시작")
        # contracts = fetch_contracts(service_key, start_day, end_day)
        # if contracts:
        #     upsert_contracts(contracts)
        #     logger.info(f"✅ 계약정보 수집 완료: {len(contracts)}건")
        
        logger.info("🎉 G2B 데이터 수집 완료")
        
    except Exception as e:
        logger.error(f"❌ G2B 데이터 수집 실패: {e}")
        raise
    finally:
        gc.collect()
