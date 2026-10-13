import os
import requests
from bs4 import BeautifulSoup

NIE = "Z5056164X"
EXPEDIENTE = "E50202600870936"
URL = "https://sede.administracionespublicas.gob.es/infoext2/imprimir.html"

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not found.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def check_status():
    try:
        response = requests.get(URL, timeout=15)
        if response.status_code == 200:
            result_text = "تم تفقد الموقع بنجاح. يرجى مراجعة حالة الملف في الموقع الرسمي."
            send_telegram_message(f"🔔 <b>تقرير حالة الملف الإسباني</b>\n\nالرقم: {NIE}\nالملف: {EXPEDIENTE}\n\n{result_text}")
        else:
            send_telegram_message(f"⚠️ الموقع الإسباني لا يستجيب حالياً. كود الخطأ: {response.status_code}")
    except Exception as e:
        send_telegram_message(f"❌ حدث خطأ أثناء فحص الموقع: {str(e)}")

if __name__ == "__main__":
    check_status()
