import os
import requests
from bs4 import BeautifulSoup

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")
RAKUTEN_URL = os.getenv("RAKUTEN_URL")
JALAN_URL = os.getenv("JALAN_URL")
TEST_MODE = os.getenv("TEST_MODE")  # "true" or "false"

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
    requests.post(url, headers=headers, json=body)

def get_price(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    price = soup.find("span", class_="price")  # 必要なら調整
    return price.text if price else "価格が取得できませんでした"

# --- テスト配信モード ---
if TEST_MODE == "true":
    push_message("テスト配信：GitHub Actions から正常に送信できました！")
    exit()

# --- 通常処理 ---
rakuten_price = get_price(RAKUTEN_URL)
jalan_price = get_price(JALAN_URL)

message = f"楽天: {rakuten_price}\nじゃらん: {jalan_price}"
push_message(message)
