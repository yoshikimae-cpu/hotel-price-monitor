import requests
from bs4 import BeautifulSoup
import json
import os

# LINE Notify token（GitHub Secrets から読み取る）
LINE_NOTIFY_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]

# 楽天トラベルURL（GitHub Secrets）
RAKUTEN_URL = os.environ["RAKUTEN_URL"]

# じゃらんURL（GitHub Secrets）
JALAN_URL = os.environ["JALAN_URL"]


def send_line(message):
    """LINE Notifyでメッセージ送信"""
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }
    data = {"message": message}
    requests.post(url, headers=headers, data=data)


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

    # 楽天トラベル値下がりチェック
    if rakuten_price:
        if last["rakuten"] is None or rakuten_price < last["rakuten"]:
            message += f"楽天トラベル値下がり！\n現在価格: ￥{rakuten_price:,}\n{RAKUTEN_URL}\n"
        last["rakuten"] = rakuten_price

    # じゃらん値下がりチェック
    if jalan_price:
        if last["jalan"] is None or jalan_price < last["jalan"]:
            message += f"じゃらん値下がり！\n現在価格: ￥{jalan_price:,}\n{JALAN_URL}\n"
        last["jalan"] = jalan_price

    # 値下がりがあれば通知
    if message:
        send_line(message)

    save_price(last)


if __name__ == "__main__":
    main()
