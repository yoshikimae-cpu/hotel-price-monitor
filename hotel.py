import requests
from bs4 import BeautifulSoup
import json
import os

# Messaging API のチャネルアクセストークン
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

# 正しい userId（Uxxxxxxxxxxxx）
LINE_USER_ID = os.environ["LINE_USER_ID"]

RAKUTEN_URL = os.environ["RAKUTEN_URL"]
JALAN_URL = os.environ["JALAN_URL"]


def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [
            {"type": "text", "text": message}
        ]
    }
    requests.post(url, headers=headers, json=data)


def get_price_rakuten():
    r = requests.get(RAKUTEN_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    price_tag = soup.select_one(".price")
    if price_tag:
        price = price_tag.text.replace("円", "").replace(",", "")
        return int(price)
    return None


def get_price_jalan():
    r = requests.get(JALAN_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    price_tag = soup.select_one(".price")
    if price_tag:
        price = price_tag.text.replace("円", "").replace(",", "")
        return int(price)
    return None


def load_last_price():
    try:
        with open("hotel_price.json", "r") as f:
            return json.load(f)
    except:
        return {"rakuten": None, "jalan": None}


def save_price(data):
    with open("hotel_price.json", "w") as f:
        json.dump(data, f)


def main():
    last = load_last_price()

    rakuten_price = get_price_rakuten()
    jalan_price = get_price_jalan()

    message = ""

    if rakuten_price:
        if last["rakuten"] is None or rakuten_price < last["rakuten"]:
            message += f"楽天トラベル値下がり！\n現在価格: ￥{rakuten_price:,}\n{RAKUTEN_URL}\n"
        last["rakuten"] = rakuten_price

    if jalan_price:
        if last["jalan"] is None or jalan_price < last["jalan"]:
            message += f"じゃらん値下がり！\n現在価格: ￥{jalan_price:,}\n{JALAN_URL}\n"
        last["jalan"] = jalan_price

    if message:
        send_line(message)

    save_price(last)


if __name__ == "__main__":
    main()
