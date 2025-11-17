import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_data(url, params):
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        logging.info(f"🌐 {url}")
        return r.json()
    except Exception as e:
        logging.error(f"❌ API 요청 실패: {url} ({e})")
        logging.error(f"resp.text: {getattr(r, 'text', 'no response')}")
        return None
