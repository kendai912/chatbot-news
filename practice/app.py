import json
import random
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")

@app.route("/api/recommend_article")
def api_recommend_article():
    """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""
    #1. はてブのホットエントリーページのHTMLを取得する
    with urlopen("https://b.hatena.ne.jp/hotentry/all") as res:
        html = res.read().decode("utf-8")

    #2. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")

    #3. 記事一覧を取得する
    articles = soup.select(".entrylist-contents-title > a")
    articles = [{"content": article["title"], "link": article["href"]}  for article in articles]

    #4. ランダムに1件取得する
    pickup = articles[random.randint(0, len(articles)-1)]
        
    #5. 以下の形式で返却する.
    return json.dumps(pickup, ensure_ascii=False)

@app.route("/api/check_futsal_court", methods=["GET"])
def api_check_futsal_court():
    #1. 空き状況を確認したい日付を取得する
    yyyymmdd = request.args.get("start_date")

    #2. Labolaのセガサミーコートの予約状況に関するHTMLを取得する
    url = "https://labola.jp/r/shop/2127/calendar_week/" + yyyymmdd[0:4] + "/" + yyyymmdd[4:6] + "/" + yyyymmdd[6:8]
    with urlopen(url) as res:
        html = res.read().decode("utf-8")

    #3. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")

    #4. 余計な要素を削除する
    for br_elm in soup.find_all('br'):
        br_elm.decompose()
    
    for uline_elm in soup.select('.uline'):
        uline_elm.decompose()

    #4. 空いている日時を取得する
    free_courts = soup.select(".free > span > p")
    free_courts = [free_court.get_text(strip=True)  for free_court in free_courts]
        
    #5. 以下の形式で返却する.
    return json.dumps(free_courts, ensure_ascii=False)

if __name__ == "__main__":
    app.run(debug=True, port=5004)
