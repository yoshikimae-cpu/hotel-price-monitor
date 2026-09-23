import requests
from bs4 import BeautifulSoup
import json

# LINE Messaging API
LINE_CHANNEL_ACCESS_TOKEN = "Xxi39ehPxJ1Wwb66fHWRKB9O5uPWqkkrdxgk1kdVf8JDcbj0nDQiQTtDmOo9rya/TdbKsL+8vDnzhAqCAKxRiGsjcxE4rB2NTfG11wpYSAaPDCNH08hXVy7Fd01Q65w6+KyKRYHdAGSCrxlfTZs7tAdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "goldyossy0127"  # ← あなたがここに貼る

# 楽天トラベルURL
RAKUTEN_URL = "https://travel.rakuten.co.jp/HOTEL/74733/74733.html?s_kwcid=paidsearch&ifd=152995&iasid=weg_trmd_travel-booking_&ultra_advid=7262886452&ultra_cid=23255152279&ultra_agid=189173333472&gclsrc=aw.ds&&saf_src=google_g&saf_pt=&saf_kw=%E3%83%9B%E3%83%86%E3%83%AB%20%E3%83%9F%E3%83%A9%E3%82%B3%E3%82%B9%E3%82%BF%20%E4%BA%88%E7%B4%84&saf_dv=&saf_cam=23255152279&saf_grp=189173333472&saf_ad=784430104546&saf_acc=7262886452&gad_source=1&gad_campaignid=23255152279&gbraid=0AAAAAD-xRgOpWcFcoUkVROTXziYFUfldy&gclid=Cj0KCQjwzsjVBhC3ARIsALnMv4lxDpO4DkYsJ0L516ZcUOChG-22BckpDBzgppylY_qM3y89xWMEn7UaAmr5EALw_wcB"

# じゃらんURL
JALAN_URL = "https://www.jalan.net/yad370886/"


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

    if message:
        send_line(message)

    save_price(last)


if __name__ == "__main__":
    main()
