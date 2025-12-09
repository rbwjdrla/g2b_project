"""
ML 기반 입찰 공고 분석 모듈
- 자동 카테고리 분류
- 태그 생성 (긴급, 고액, 저경쟁 등)
- 경쟁 강도 예측
- 유사 공고 찾기
"""

import re
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


class BiddingAnalyzer:
    """입찰 공고 ML 분석기"""

    def __init__(self):
        self.categories = {
            'IT': ['소프트웨어', '시스템', '홈페이지', '웹', '앱', '프로그램', '개발', 'IT', '전산', '네트워크', '서버', 'DB', '데이터베이스', '클라우드'],
            '건설': ['공사', '건축', '토목', '시설', '건설', '보수', '개보수', '증축', '신축', '리모델링'],
            '용역': ['용역', '컨설팅', '자문', '연구', '조사', '분석', '평가', '진단', '관리'],
            '물품': ['구매', '납품', '물품', '제품', '기자재', '장비', '설비', '비품', '소모품'],
            '교육': ['교육', '연수', '훈련', '강의', '세미나', '워크샵', '특강'],
            '의료': ['의료', '병원', '의약', '간호', '치료', '진료', '건강'],
            '청소': ['청소', '환경', '미화', '위생', '방역', '소독'],
            '보안': ['보안', '경비', '방범', 'CCTV', '감시', '순찰'],
            '인쇄': ['인쇄', '출판', '제작', '디자인', '편집'],
            '운송': ['운송', '배송', '택배', '이사', '물류', '운반'],
        }

        self.vectorizer = None

    def classify_category(self, title: str) -> str:
        """공고명 기반 카테고리 자동 분류"""
        if not title:
            return "기타"

        title_lower = title.lower()

        # 키워드 매칭 스코어 계산
        scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword.lower() in title_lower)
            if score > 0:
                scores[category] = score

        # 가장 높은 스코어의 카테고리 반환
        if scores:
            return max(scores, key=scores.get)

        return "기타"

    def generate_tags(self, bidding_data: Dict) -> List[str]:
        """입찰 공고 데이터 기반 태그 생성"""
        tags = []

        title = bidding_data.get('title', '')
        budget = bidding_data.get('budget_amount')
        notice_date = bidding_data.get('notice_date')
        bid_close_date = bidding_data.get('bid_close_date')

        # 1. 예산 기반 태그
        if budget is not None and budget > 0:
            if budget >= 1_000_000_000:  # 10억 이상
                tags.append("고액")
            elif budget >= 100_000_000:  # 1억 이상
                tags.append("중액")
            else:
                tags.append("소액")

        # 2. 긴급성 태그 (공고일 ~ 마감일 간격)
        if notice_date and bid_close_date:
            if isinstance(notice_date, str):
                notice_date = datetime.fromisoformat(notice_date.replace('Z', '+00:00'))
            if isinstance(bid_close_date, str):
                bid_close_date = datetime.fromisoformat(bid_close_date.replace('Z', '+00:00'))

            days_diff = (bid_close_date - notice_date).days
            if days_diff <= 3:
                tags.append("긴급")
            elif days_diff <= 7:
                tags.append("빠른마감")

        # 3. 키워드 기반 태그
        title_lower = title.lower() if title else ''

        if any(word in title_lower for word in ['긴급', '신속', '즉시']):
            if "긴급" not in tags:
                tags.append("긴급")

        if any(word in title_lower for word in ['유지보수', '운영', '관리']):
            tags.append("유지보수")

        if any(word in title_lower for word in ['신규', '구축', '개발']):
            tags.append("신규사업")

        if '재공고' in title_lower or '재입찰' in title_lower:
            tags.append("재공고")

        return tags

    def calculate_competition_level(self, bidding_data: Dict, awards_data: Optional[List] = None) -> str:
        """경쟁 강도 예측 (저/중/고)"""

        # 기본 점수
        score = 0

        budget = bidding_data.get('budget_amount')
        notice_type = bidding_data.get('notice_type', '')

        # 1. 예산 기반 (예산이 클수록 경쟁 치열)
        if budget is not None and budget > 0:
            if budget >= 1_000_000_000:  # 10억 이상
                score += 3
            elif budget >= 500_000_000:  # 5억 이상
                score += 2
            elif budget >= 100_000_000:  # 1억 이상
                score += 1

        # 2. 공고 유형 기반
        if notice_type in ['용역', '물품']:
            score += 1  # 용역/물품이 공사보다 진입장벽 낮음

        # 3. 과거 낙찰 데이터가 있다면 활용
        if awards_data:
            avg_participants = np.mean([a.get('prtcpt_cnum', 0) for a in awards_data if a.get('prtcpt_cnum')])
            if avg_participants >= 10:
                score += 2
            elif avg_participants >= 5:
                score += 1

        # 점수 → 등급 변환
        if score >= 5:
            return "고"
        elif score >= 3:
            return "중"
        else:
            return "저"

    def find_similar_biddings(self, target_title: str, all_titles: List[str], top_k: int = 5) -> List[int]:
        """TF-IDF + 코사인 유사도로 유사 공고 찾기"""

        if not target_title or not all_titles:
            return []

        # TF-IDF 벡터화
        corpus = [target_title] + all_titles

        try:
            vectorizer = TfidfVectorizer(
                max_features=100,
                ngram_range=(1, 2),
                min_df=1
            )
            tfidf_matrix = vectorizer.fit_transform(corpus)

            # 코사인 유사도 계산
            target_vector = tfidf_matrix[0:1]
            similarities = cosine_similarity(target_vector, tfidf_matrix[1:]).flatten()

            # 상위 k개 인덱스 반환
            top_indices = similarities.argsort()[-top_k:][::-1]

            return top_indices.tolist()

        except Exception as e:
            print(f"유사 공고 찾기 실패: {e}")
            return []

    def analyze_bidding(self, bidding_data: Dict, awards_data: Optional[List] = None) -> Dict:
        """입찰 공고 종합 분석"""

        category = self.classify_category(bidding_data.get('title', ''))
        tags = self.generate_tags(bidding_data)
        competition = self.calculate_competition_level(bidding_data, awards_data)

        return {
            'ai_category': category,
            'ai_tags': json.dumps(tags, ensure_ascii=False),
            'competition_level': competition
        }


# 싱글톤 인스턴스
analyzer = BiddingAnalyzer()
