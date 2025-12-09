"""
DB 마이그레이션: ML 분석 필드 추가
biddings 테이블에 ai_category, ai_tags, competition_level 컬럼 추가
"""

import logging
from sqlalchemy import text
from database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    """ML 분석 필드 추가 마이그레이션"""

    logger.info("🔄 DB 마이그레이션 시작: ML 분석 필드 추가")

    with engine.connect() as conn:
        try:
            # 1. ai_category 컬럼 추가
            logger.info("  - ai_category 컬럼 추가 중...")
            conn.execute(text("""
                ALTER TABLE biddings
                ADD COLUMN IF NOT EXISTS ai_category VARCHAR(100);
            """))
            conn.commit()
            logger.info("  ✅ ai_category 추가 완료")

            # 2. ai_tags 컬럼 추가
            logger.info("  - ai_tags 컬럼 추가 중...")
            conn.execute(text("""
                ALTER TABLE biddings
                ADD COLUMN IF NOT EXISTS ai_tags TEXT;
            """))
            conn.commit()
            logger.info("  ✅ ai_tags 추가 완료")

            # 3. competition_level 컬럼 추가
            logger.info("  - competition_level 컬럼 추가 중...")
            conn.execute(text("""
                ALTER TABLE biddings
                ADD COLUMN IF NOT EXISTS competition_level VARCHAR(20);
            """))
            conn.commit()
            logger.info("  ✅ competition_level 추가 완료")

            logger.info("✅ 마이그레이션 완료!")

        except Exception as e:
            logger.error(f"❌ 마이그레이션 실패: {e}")
            conn.rollback()
            raise


if __name__ == "__main__":
    migrate()
