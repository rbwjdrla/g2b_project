from utils import fetch_data
from database import SessionLocal
from models import OrderPlan
from datetime import datetime
import logging


def fetch_plans(service_key, start_date, end_date):
    """발주계획 수집 - 전체 페이징 처리"""
    url = "https://apis.data.go.kr/1230000/ao/OrderPlanSttusService/getOrderPlanSttusListThng"
    
    all_items = []
    page = 1
    
    while True:
        params = {
            "pageNo": page,
            "numOfRows": 100,
            "inqryDiv": 1,
            "orderBgnYm": start_date[:6],
            "orderEndYm": end_date[:6],
            "serviceKey": service_key,
            "type": "json"
        }
        
        data = fetch_data(url, params)
        
        if not data or "response" not in data:
            break
        
        body = data["response"].get("body", {})
        items = body.get("items", [])
        total_count = body.get("totalCount", 0)
        
        if not items:
            break
        
        all_items.extend(items)
        
        logging.info(f"📄 발주계획 페이지 {page} 수집: {len(items)}건 (총 {total_count}건 중 {len(all_items)}건)")
        
        if len(all_items) >= total_count:
            break
        
        page += 1
    
    return all_items


def parse_datetime(date_str):
    """YYYYMMDDHHmmss 형식을 datetime으로 변환"""
    if not date_str or len(date_str) < 8:
        return None
    try:
        if len(date_str) >= 14:
            return datetime.strptime(date_str[:14], "%Y%m%d%H%M%S")
        else:
            return datetime.strptime(date_str[:8], "%Y%m%d")
    except:
        return None


def parse_int(value):
    """문자열을 정수로 변환"""
    if not value:
        return None
    try:
        return int(str(value).replace(",", ""))
    except:
        return None


def upsert_plans(items):
    """발주계획 DB 저장"""
    db = SessionLocal()
    saved_count = 0
    
    try:
        for item in items:
            unty_no = item.get("orderPlanUntyNo")
            
            if not unty_no:
                continue
            
            try:
                obj = db.query(OrderPlan).filter(OrderPlan.order_plan_unty_no == unty_no).first()
                
                if obj is None:
                    obj = OrderPlan(order_plan_unty_no=unty_no)
                    db.add(obj)
                
                obj.biz_nm = item.get("bizNm")
                obj.order_instt_nm = item.get("orderInsttNm")
                obj.dept_nm = item.get("deptNm")
                obj.ofcl_nm = item.get("ofclNm")
                obj.tel_no = item.get("telNo")
                obj.prcrmnt_methd = item.get("prcrmntMethd")
                obj.cntrct_mthd_nm = item.get("cntrctMthdNm")
                obj.sum_order_amt = parse_int(item.get("sumOrderAmt"))
                obj.sum_order_dol_amt = item.get("sumOrderDolAmt")
                obj.qty_cntnts = item.get("qtyCntnts")
                obj.unit = item.get("unit")
                obj.prdct_clsfc_no = item.get("prdctClsfcNo")
                obj.dtil_prdct_clsfc_no = item.get("dtilPrdctClsfcNo")
                obj.prdct_clsfc_no_nm = item.get("prdctClsfcNoNm")
                obj.dtil_prdct_clsfc_no_nm = item.get("dtilPrdctClsfcNoNm")
                obj.usg_cntnts = item.get("usgCntnts")
                obj.spec_cntnts = item.get("specCntnts")
                obj.rmrk_cntnts = item.get("rmrkCntnts")
                obj.order_year = item.get("orderYear")
                obj.order_mnth = item.get("orderMnth")
                obj.ntice_dt = parse_datetime(item.get("nticeDt"))
                obj.chg_dt = parse_datetime(item.get("chgDt"))
                
                db.commit()
                saved_count += 1
                
            except Exception as e:
                logging.error(f"❌ 발주계획 저장 실패 ({unty_no}): {e}")
                db.rollback()
                continue
        
        logging.info(f"💾 발주계획 저장 완료: {saved_count}건")
        
    except Exception as e:
        logging.error(f"❌ 발주계획 upsert 전체 실패: {e}")
        db.rollback()
    finally:
        db.close()
