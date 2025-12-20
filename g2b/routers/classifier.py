"""
ML 분석 API 라우터
- 공고 자동 분석
- 유사 공고 찾기
- 배치 분석
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models import Bidding, Award
from ml_analyzer import analyzer
import logging
import json

router = APIRouter(prefix="/api/ml", tags=["classify"])
logger = logging.getLogger(__name__)


@router.post("/analyze/{bidding_id}")
def analyze_single_bidding(bidding_id: int, db: Session = Depends(get_db)):
    """단일 공고 ML 분석"""
    logger.info(f"🤖 공고 {bidding_id} ML 분석 시작")

    # 공고 조회
    bidding = db.query(Bidding).filter(Bidding.id == bidding_id).first()
    if not bidding:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")

    # 관련 낙찰 데이터 조회 (같은 발주기관)
    awards = db.query(Award).filter(
        Award.ntce_instt_nm == bidding.ordering_agency
    ).limit(100).all()

    awards_data = [
        {
            'prtcpt_cnum': a.prtcpt_cnum,
            'award_rate': a.award_rate
        }
        for a in awards if a.prtcpt_cnum
    ]

    # 태그 부여 
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

    db.commit()
    db.refresh(bidding)

    logger.info(f"✅ 공고 {bidding_id} 분석 완료: {result}")

    return {
        "bidding_id": bidding_id,
        "title": bidding.title,
        "analysis": {
            "category": result['ai_category'],
            "tags": json.loads(result['ai_tags']),
            "competition_level": result['competition_level']
        }
    }


@router.get("/similar/{bidding_id}")
def find_similar_biddings(
    bidding_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """유사 공고 찾기"""
    logger.info(f"🔍 공고 {bidding_id}와 유사한 공고 검색")

    # 대상 공고 조회
    target = db.query(Bidding).filter(Bidding.id == bidding_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")

    # 같은 카테고리의 공고들 조회
    similar_candidates = db.query(Bidding).filter(
        Bidding.ai_category == target.ai_category,
        Bidding.id != bidding_id
    ).limit(100).all()

    if not similar_candidates:
        return {"bidding_id": bidding_id, "similar": []}

    # TF-IDF 유사도 계산
    all_titles = [b.title for b in similar_candidates]
    similar_indices = analyzer.find_similar_biddings(
        target.title,
        all_titles,
        top_k=min(limit, len(all_titles))
    )

    # 결과 반환
    similar_biddings = [similar_candidates[i] for i in similar_indices]

    return {
        "bidding_id": bidding_id,
        "title": target.title,
        "similar": [
            {
                "id": b.id,
                "title": b.title,
                "budget_amount": b.budget_amount,
                "notice_type": b.notice_type,
                "ai_category": b.ai_category
            }
            for b in similar_biddings
        ]
    }


@router.post("/analyze-all")
def analyze_all_biddings_endpoint(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """전체 공고 배치 분석 (백그라운드)"""
    logger.info("🚀 전체 공고 배치 분석 시작 (백그라운드)")

    def batch_analyze():
        """배치 분석 백그라운드 작업"""
        query = db.query(Bidding).filter(Bidding.ai_category.is_(None))

        if limit:
            query = query.limit(limit)

        biddings = query.all()
        total = len(biddings)

        logger.info(f"📊 분석 대상: {total}개 공고")

        for i, bidding in enumerate(biddings, 1):
            try:
                bidding_dict = {
                    'title': bidding.title,
                    'budget_amount': bidding.budget_amount,
                    'notice_type': bidding.notice_type,
                    'notice_date': bidding.notice_date,
                    'bid_close_date': bidding.bid_close_date
                }

                result = analyzer.analyze_bidding(bidding_dict)

                bidding.ai_category = result['ai_category']
                bidding.ai_tags = result['ai_tags']
                bidding.competition_level = result['competition_level']

                if i % 100 == 0:
                    db.commit()
                    logger.info(f"⏳ 진행: {i}/{total} ({i/total*100:.1f}%)")

            except Exception as e:
                logger.error(f"❌ 공고 {bidding.id} 분석 실패: {e}")
                continue

        db.commit()
        logger.info(f"✅ 배치 분석 완료: {total}개 공고")

    background_tasks.add_task(batch_analyze)

    return {
        "status": "started",
        "message": "배치 분석이 백그라운드에서 실행 중입니다."
    }


@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """AI 카테고리 목록 및 통계"""
    stats = db.query(
        Bidding.ai_category,
        func.count(Bidding.id).label('count')
    ).filter(
        Bidding.ai_category.isnot(None)
    ).group_by(
        Bidding.ai_category
    ).all()

    return {
        "categories": [
            {"category": cat, "count": count}
            for cat, count in stats
        ]
    }


@router.get("/tags")
def get_popular_tags(limit: int = 20, db: Session = Depends(get_db)):
    """인기 태그 목록"""
    biddings = db.query(Bidding).filter(
        Bidding.ai_tags.isnot(None)
    ).all()

    # 태그 집계
    tag_counts = {}
    for b in biddings:
        if b.ai_tags:
            try:
                tags = json.loads(b.ai_tags)
                for tag in tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            except:
                continue

    # 정렬
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

    return {
        "tags": [
            {"tag": tag, "count": count}
            for tag, count in sorted_tags[:limit]
        ]
    }
