from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_scheduler():
    """스케줄러 생성"""
    scheduler = BackgroundScheduler(timezone="UTC")
    return scheduler

def scheduled_job():
    """스케줄된 작업"""
    from apis.main import run_all
    
    today = datetime.now().strftime("%Y%m%d")
    logger.info(f"⏰ 자동 데이터 수집 시작 ({today})")
    
    try:
        run_all()
        logger.info(f"✅ 자동 데이터 수집 완료 ({today})")
    except Exception as e:
        logger.error(f"❌ 자동 데이터 수집 실패: {e}")
