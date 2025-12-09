# 🤖 ML 분석 기능 가이드

나라장터 입찰 공고 시스템에 추가된 머신러닝 분석 기능 사용 가이드입니다.

## 📋 목차

1. [기능 소개](#기능-소개)
2. [설치 및 설정](#설치-및-설정)
3. [API 사용법](#api-사용법)
4. [배치 분석](#배치-분석)
5. [프론트엔드 활용](#프론트엔드-활용)

---

## 🎯 기능 소개

### 1. 자동 카테고리 분류
공고명을 분석하여 자동으로 카테고리를 분류합니다.

**카테고리 목록:**
- IT (소프트웨어, 시스템, 홈페이지, 웹, 앱 등)
- 건설 (공사, 건축, 토목 등)
- 용역 (컨설팅, 자문, 연구 등)
- 물품 (구매, 납품 등)
- 교육, 의료, 청소, 보안, 인쇄, 운송 등
- 기타

### 2. 스마트 태그 생성
입찰 공고의 특성을 분석하여 자동으로 태그를 생성합니다.

**태그 종류:**
- **예산 기반**: "고액" (10억+), "중액" (1억+), "소액"
- **긴급성**: "긴급" (마감 3일 이내), "빠른마감" (7일 이내)
- **유형**: "유지보수", "신규사업", "재공고"

### 3. 경쟁 강도 예측
과거 데이터와 입찰 조건을 분석하여 경쟁 강도를 예측합니다.

**등급:**
- **고**: 경쟁이 매우 치열 (고액, 인기 분야)
- **중**: 보통 수준의 경쟁
- **저**: 경쟁이 낮음 (특수 분야, 소액)

### 4. 유사 공고 추천
TF-IDF 알고리즘을 사용하여 유사한 공고를 찾아줍니다.

---

## ⚙️ 설치 및 설정

### 1. 데이터베이스 마이그레이션

```bash
# PostgreSQL에 새 컬럼 추가
cd /home/user/g2b_project
psql -U [username] -d [database] -f migrations/add_ml_fields.sql
```

또는 Python 스크립트 사용:

```bash
cd g2b
python migrate_add_ml_fields.py
```

### 2. 의존성 확인

이미 `requirements.txt`에 포함되어 있습니다:
- `scikit-learn==1.4.0`
- `pandas==2.2.0`
- `numpy==1.26.3`

---

## 🔌 API 사용법

### 1. 단일 공고 분석

**POST** `/api/ml/analyze/{bidding_id}`

특정 공고에 대해 ML 분석을 실행하고 결과를 DB에 저장합니다.

```bash
curl -X POST "http://localhost:8000/api/ml/analyze/123"
```

**응답 예시:**
```json
{
  "bidding_id": 123,
  "title": "소프트웨어 유지보수 용역",
  "analysis": {
    "category": "IT",
    "tags": ["유지보수", "중액"],
    "competition_level": "중"
  }
}
```

### 2. 유사 공고 찾기

**GET** `/api/ml/similar/{bidding_id}?limit=5`

TF-IDF 기반으로 유사한 공고를 찾습니다.

```bash
curl "http://localhost:8000/api/ml/similar/123?limit=5"
```

**응답 예시:**
```json
{
  "bidding_id": 123,
  "title": "소프트웨어 유지보수 용역",
  "similar": [
    {
      "id": 456,
      "title": "시스템 유지보수 및 운영",
      "budget_amount": 50000000,
      "ai_category": "IT"
    }
  ]
}
```

### 3. 전체 공고 배치 분석

**POST** `/api/ml/analyze-all?limit=100`

미분석 공고들을 백그라운드에서 일괄 분석합니다.

```bash
curl -X POST "http://localhost:8000/api/ml/analyze-all?limit=100"
```

### 4. 카테고리 통계

**GET** `/api/ml/categories`

AI 카테고리별 공고 수를 조회합니다.

```bash
curl "http://localhost:8000/api/ml/categories"
```

**응답 예시:**
```json
{
  "categories": [
    {"category": "IT", "count": 1520},
    {"category": "건설", "count": 850},
    {"category": "용역", "count": 640}
  ]
}
```

### 5. 인기 태그

**GET** `/api/ml/tags?limit=20`

가장 많이 사용된 태그 목록을 조회합니다.

```bash
curl "http://localhost:8000/api/ml/tags?limit=20"
```

---

## 🔍 예산별 검색 (강화된 필터링)

### 기존 검색 API 확장

**GET** `/api/biddings`

이제 예산 범위로 필터링할 수 있습니다!

**새 파라미터:**
- `min_budget`: 최소 예산 (원)
- `max_budget`: 최대 예산 (원)
- `ai_category`: AI 카테고리 필터
- `competition_level`: 경쟁 강도 (저/중/고)

**사용 예시:**

```bash
# 1억 ~ 10억 사이의 IT 공고만 검색
curl "http://localhost:8000/api/biddings?min_budget=100000000&max_budget=1000000000&ai_category=IT"

# 경쟁 강도가 "저"인 공고만 검색
curl "http://localhost:8000/api/biddings?competition_level=저"

# 고액 공고 검색 (10억 이상)
curl "http://localhost:8000/api/biddings?min_budget=1000000000"
```

---

## 🚀 배치 분석

기존 데이터에 대해 ML 분석을 실행하는 스크립트입니다.

### 전체 데이터 분석

```bash
cd /home/user/g2b_project/g2b
python batch_ml_analysis.py
```

### 일부만 분석 (테스트용)

```bash
# 100개만 분석
python batch_ml_analysis.py 100
```

### 출력 예시

```
🚀 배치 분석 시작: 5420개 공고
⏳ 진행: 100/5420 (1.8%) - 성공: 98, 실패: 2
⏳ 진행: 200/5420 (3.7%) - 성공: 197, 실패: 3
...
✅ 배치 분석 완료!
   - 전체: 5420개
   - 성공: 5385개
   - 실패: 35개

==================================================
📊 ML 분석 통계
==================================================

🏷️  카테고리별 분포:
   - IT: 1520개
   - 건설: 850개
   - 용역: 640개
   - 물품: 520개
   - 기타: 480개

⚡ 경쟁 강도별 분포:
   - 고: 1200개
   - 중: 2800개
   - 저: 1385개

🔖 인기 태그 TOP 10:
   1. 중액: 2450개
   2. 유지보수: 1820개
   3. 고액: 1150개
   4. 소액: 1000개
   5. 신규사업: 850개
```

---

## 🎨 프론트엔드 활용 예시

### 1. 검색 필터 UI 추가

```javascript
// 예산 범위 슬라이더
<input
  type="range"
  min="0"
  max="10000000000"
  onChange={(e) => setMinBudget(e.target.value)}
/>

// 카테고리 선택
<select onChange={(e) => setCategory(e.target.value)}>
  <option value="">전체</option>
  <option value="IT">IT</option>
  <option value="건설">건설</option>
  <option value="용역">용역</option>
</select>

// API 호출
fetch(`/api/biddings?min_budget=${minBudget}&ai_category=${category}`)
```

### 2. 태그 배지 표시

```jsx
// 공고 목록에서 태그 표시
{bidding.ai_tags && JSON.parse(bidding.ai_tags).map(tag => (
  <span className="badge badge-primary" key={tag}>
    {tag}
  </span>
))}
```

### 3. 경쟁 강도 표시

```jsx
// 경쟁 강도에 따른 색상 변경
const getCompetitionColor = (level) => {
  switch(level) {
    case '고': return 'red';
    case '중': return 'orange';
    case '저': return 'green';
    default: return 'gray';
  }
};

<span style={{color: getCompetitionColor(bidding.competition_level)}}>
  경쟁강도: {bidding.competition_level}
</span>
```

### 4. 유사 공고 추천

```jsx
// 상세 페이지에서 유사 공고 표시
const [similar, setSimilar] = useState([]);

useEffect(() => {
  fetch(`/api/ml/similar/${biddingId}?limit=5`)
    .then(res => res.json())
    .then(data => setSimilar(data.similar));
}, [biddingId]);

return (
  <div className="similar-section">
    <h3>📌 유사한 공고</h3>
    {similar.map(item => (
      <div key={item.id}>
        <a href={`/biddings/${item.id}`}>{item.title}</a>
      </div>
    ))}
  </div>
);
```

---

## 🔧 커스터마이징

### 카테고리 추가

`g2b/ml_analyzer.py`의 `categories` 딕셔너리를 수정:

```python
self.categories = {
    'IT': ['소프트웨어', '시스템', ...],
    '새_카테고리': ['키워드1', '키워드2', ...],
}
```

### 태그 로직 수정

`generate_tags()` 메서드에서 새로운 태그 조건 추가:

```python
# 예: 공사 규모별 태그
if budget >= 50_000_000_000:  # 500억
    tags.append("대형공사")
```

---

## 📊 성능 최적화

### 인덱스 추가 (이미 SQL에 포함)

```sql
CREATE INDEX idx_biddings_ai_category ON biddings(ai_category);
CREATE INDEX idx_biddings_competition_level ON biddings(competition_level);
```

### 배치 분석 시 청크 크기 조절

```python
# batch_ml_analysis.py에서 커밋 주기 변경
if i % 100 == 0:  # 기본값
    db.commit()

if i % 500 == 0:  # 더 큰 청크로 변경
    db.commit()
```

---

## ❓ FAQ

**Q: 기존 데이터도 자동으로 분석되나요?**
A: 아니요. `batch_ml_analysis.py` 스크립트를 실행해야 합니다.

**Q: 새 공고는 자동으로 분석되나요?**
A: 현재는 수동으로 `/api/ml/analyze/{id}`를 호출해야 합니다.
   스케줄러에 추가하려면 `scheduler.py`를 수정하세요.

**Q: ML 모델을 학습시켜야 하나요?**
A: 아니요. 현재는 규칙 기반(키워드 매칭)과 TF-IDF를 사용합니다.
   추후 scikit-learn 분류 모델을 학습시킬 수 있습니다.

**Q: 예산 검색이 느려요**
A: `budget_amount` 컬럼에 인덱스를 추가하세요:
   ```sql
   CREATE INDEX idx_biddings_budget ON biddings(budget_amount);
   ```

---

## 🚀 다음 단계

1. **낙찰률 예측 모델** - 과거 데이터로 낙찰 확률 예측
2. **시계열 분석** - 입찰 트렌드 예측
3. **자연어 처리 강화** - BERT 모델로 공고 내용 분석
4. **실시간 알림** - 조건 맞는 공고 자동 알림

---

## 📞 문의

문제가 발생하면 이슈를 등록해주세요!
