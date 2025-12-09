"""
배치 ML 분석 스크립트
기존 입찰 공고 데이터에 대해 ML 분석을 실행하고 결과를 DB에 저장
"""

import sys
import logging
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Bidding, Award
from ml_analyzer import analyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def batch_analyze_biddings(limit: int = None):
    """전체 입찰 공고 배치 분석"""

    db: Session = SessionLocal()

    try:
        # 미분석 공고 조회
        query = db.query(Bidding).filter(Bidding.ai_category.is_(None))

        if limit:
            query = query.limit(limit)

        biddings = query.all()
        total = len(biddings)

        logger.info(f"🚀 배치 분석 시작: {total}개 공고")

        if total == 0:
            logger.info("✅ 분석할 공고가 없습니다.")
            return

        success_count = 0
        error_count = 0

        for i, bidding in enumerate(biddings, 1):
            try:
                # 관련 낙찰 데이터 조회 (성능 최적화를 위해 제한)
                awards = db.query(Award).filter(
                    Award.ntce_instt_nm == bidding.ordering_agency
                ).limit(50).all()

                awards_data = [
                    {
                        'prtcpt_cnum': a.prtcpt_cnum,
                        'award_rate': a.award_rate
                    }
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
                bidding.competition_level = result['competition_level']

                success_count += 1

                # 100개마다 커밋
                if i % 100 == 0:
                    db.commit()
                    logger.info(f"⏳ 진행: {i}/{total} ({i/total*100:.1f}%) - 성공: {success_count}, 실패: {error_count}")

            except Exception as e:
                error_count += 1
                logger.error(f"❌ 공고 ID {bidding.id} 분석 실패: {e}")
                continue

        # 최종 커밋
        db.commit()

        logger.info(f"✅ 배치 분석 완료!")
        logger.info(f"   - 전체: {total}개")
        logger.info(f"   - 성공: {success_count}개")
        logger.info(f"   - 실패: {error_count}개")

    except Exception as e:
        logger.error(f"❌ 배치 분석 중 오류 발생: {e}")
        db.rollback()

    finally:
        db.close()


def print_statistics(db: Session):
    """분석 결과 통계 출력"""
    from sqlalchemy import func
    import json

    logger.info("\n" + "="*50)
    logger.info("📊 ML 분석 통계")
    logger.info("="*50)

    # 카테고리별 통계
    category_stats = db.query(
        Bidding.ai_category,
        func.count(Bidding.id).label('count')
    ).filter(
        Bidding.ai_category.isnot(None)
    ).group_by(
        Bidding.ai_category
    ).all()

    logger.info("\n🏷️  카테고리별 분포:")
    for cat, count in category_stats:
        logger.info(f"   - {cat}: {count}개")

    # 경쟁 강도별 통계
    competition_stats = db.query(
        Bidding.competition_level,
        func.count(Bidding.id).label('count')
    ).filter(
        Bidding.competition_level.isnot(None)
    ).group_by(
        Bidding.competition_level
    ).all()

    logger.info("\n⚡ 경쟁 강도별 분포:")
    for level, count in competition_stats:
        logger.info(f"   - {level}: {count}개")

    # 인기 태그
    biddings = db.query(Bidding).filter(
        Bidding.ai_tags.isnot(None)
    ).limit(1000).all()

    tag_counts = {}
    for b in biddings:
        if b.ai_tags:
            try:
                tags = json.loads(b.ai_tags)
                for tag in tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except:
                continue

    logger.info("\n🔖 인기 태그 TOP 10:")
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (tag, count) in enumerate(sorted_tags[:10], 1):
        logger.info(f"   {i}. {tag}: {count}개")

    logger.info("="*50 + "\n")


if __name__ == "__main__":
    # 커맨드 라인 인자로 limit 지정 가능
    limit = None
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
            logger.info(f"제한: {limit}개만 분석")
        except ValueError:
            logger.warning("잘못된 limit 값. 전체 분석을 진행합니다.")

    # 배치 분석 실행
    batch_analyze_biddings(limit)

    # 통계 출력
    db = SessionLocal()
    try:
        print_statistics(db)
    finally:
        db.close()
