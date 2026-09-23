import os
import requests
from bs4 import BeautifulSoup

# --- Secrets / Environment variables ---
LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")
RAKUTEN_URL = os.getenv("RAKUTEN_URL")
JALAN_URL = os.getenv("JALAN_URL")
TEST_MODE = os.getenv("TEST_MODE")  # workflow_dispatch の入力値


# --- LINE Push API ---
def push_message(text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    body = {
        "to": USER_ID,
        "messages": [
            {"type": "text", "text": text}
        ]
    }

    response = requests.post(url, headers=headers, json=body)

    # GitHub Actions のログに必ず出す（原因特定用）
    print("=== LINE API Response ===")
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)


# --- Price Scraper ---
def get_price(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        price = soup.find("span", class_="price")
        return price.text if price else "価格が取得できませんでした"
    except Exception as e:
        return f"取得エラー: {e}"


# --- TEST MODE ---
# false 以外なら全部テスト扱いにする
if TEST_MODE and TEST_MODE.lower() != "false":
    push_message("テスト配信：GitHub Actions から正常に送信できました！")
    exit()


# --- Normal Mode ---
rakuten_price = get_price(RAKUTEN_URL)
jalan_price = get_price(JALAN_URL)

message = f"楽天: {rakuten_price}\nじゃらん: {jalan_price}"
push_message(message)
