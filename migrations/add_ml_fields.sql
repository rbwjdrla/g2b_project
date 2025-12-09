-- ML 분석 필드 추가 마이그레이션
-- 실행 방법: psql -U username -d dbname -f add_ml_fields.sql

-- biddings 테이블에 ML 분석 필드 추가
ALTER TABLE biddings
ADD COLUMN IF NOT EXISTS ai_category VARCHAR(100);

ALTER TABLE biddings
ADD COLUMN IF NOT EXISTS ai_tags TEXT;

ALTER TABLE biddings
ADD COLUMN IF NOT EXISTS competition_level VARCHAR(20);

-- 컬럼에 코멘트 추가
COMMENT ON COLUMN biddings.ai_category IS 'AI 자동 분류 카테고리';
COMMENT ON COLUMN biddings.ai_tags IS 'AI 생성 태그 (JSON)';
COMMENT ON COLUMN biddings.competition_level IS '경쟁 강도 (저/중/고)';

-- 인덱스 추가 (검색 성능 향상)
CREATE INDEX IF NOT EXISTS idx_biddings_ai_category ON biddings(ai_category);
CREATE INDEX IF NOT EXISTS idx_biddings_competition_level ON biddings(competition_level);

-- 확인
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'biddings'
  AND column_name IN ('ai_category', 'ai_tags', 'competition_level');
