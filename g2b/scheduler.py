from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
from database import SessionLocal  
from models import Bidding, Award  
from ml_analyzer import analyzer  


logger = logging.getLogger(__name__)

def create_scheduler():
    """스케줄러 생성"""
    scheduler = BackgroundScheduler(timezone="Asia/Seoul")
    return scheduler

def scheduled_job():
    """스케줄된 작업 - 데이터 수집 + ML 분석 (2일치)"""
    from apis.main import run_all
    today = datetime.now().strftime("%Y%m%d")
    logger.info(f"⏰ 자동 데이터 수집 시작 ({today})")

    try:
        # 1. 데이터 수집 (2일치)
        run_all(days=2)
        logger.info(f"✅ 자동 데이터 수집 완료 ({today})")

        # 2. 새로 수집된 데이터 ML 분석
        logger.info(f"🤖 ML 분석 시작 (미분석 데이터)")
        analyze_new_biddings()
        logger.info(f"✅ ML 분석 완료")

    except Exception as e:
        logger.error(f"❌ 자동 작업 실패: {e}")


def analyze_new_biddings():
    """미분석 입찰 공고만 ML 분석"""
    db = SessionLocal()

    try:
        # 미분석 공고 조회 (ai_category가 None인 것들)
        unanalyzed = db.query(Bidding).filter(
            Bidding.ai_category.is_(None)
        ).all()

        count = len(unanalyzed)
        if count == 0:
            logger.info("  ℹ️ 분석할 새 공고 없음")
            return

        logger.info(f"  📊 분석 대상: {count}개 공고")

        for i, bidding in enumerate(unanalyzed, 1):
            try:
                # 관련 낙찰 데이터 조회 (경쟁 강도 예측용)
                awards = db.query(Award).filter(
                    Award.ntce_instt_nm == bidding.ordering_agency
                ).limit(50).all()

                awards_data = [
                    {'prtcpt_cnum': a.prtcpt_cnum, 'award_rate': a.award_rate}
                    for a in awards if a.prtcpt_cnum
                ]

                # ML 분석 실행
                bidding_dict = {
                    'title': bidding.title,
                    'budget_amount': bidding.budget_amount,
                    'notice_type': bidding.notice_type,
                    'notice_date': bidding.notice_date,
                    'bid_close_date': bidding.bid_close_date
                }

                result = analyzer.analyze_bidding(bidding_dict, awards_data)

                # DB 업데이트
                bidding.ai_category = result['ai_category']
                bidding.ai_tags = result['ai_tags']

                # 10개마다 커밋
                if i % 10 == 0:
                    db.commit()
                    logger.info(f"  ⏳ 진행: {i}/{count}")

            except Exception as e:
                logger.error(f"  ❌ 공고 ID {bidding.id} 분석 실패: {e}")
                continue

        # 최종 커밋
        db.commit()
        logger.info(f"  ✅ {count}개 공고 분석 완료")

    except Exception as e:
        logger.error(f"  ❌ ML 분석 중 오류: {e}")
        db.rollback()
    finally:
        db.close()
