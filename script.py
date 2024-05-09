import sqlite3
import json
import os
import requests  # requests ライブラリをインポート
import webbrowser
import tempfile

def query_db(query):
    with sqlite3.connect('NewsAppDB.db') as conn:  # データベースファイル名を指定
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

def filter_items(data):
    filtered_data = []
    for item in data:
        app_name = item[0]  # AppName
        app_path = os.path.join(item[1], app_name)  # AppManagement.Path に AppName を追加してフルパスを生成
        if os.path.exists(app_path):
            filtered_data.append(item)
    return filtered_data

def main():
    # 新着ニュースの取得
    news_query = """
    SELECT AppManagement.AppName, AppManagement.Path, NewsManagement.Path, NewsManagement.Category,
           NewsManagement.Title, NewsManagement.PublicationDate, NewsManagement.Year
    FROM NewsManagement
    JOIN NewsPublication ON NewsManagement.ID = NewsPublication.NewsID
    JOIN AppManagement ON NewsPublication.AppID = AppManagement.ID
    WHERE AppManagement.endflag = 0 AND NewsManagement.endflag = 0;
    """
    news_data = query_db(news_query)
    print(f"news_data: {news_data}")

    # AppNameがPathに含まれるレコードの抽出
    filtered_news = filter_items(news_data)
    print(f"filtered_news: {filtered_news}")

    # フィルタ用アプリ名の取得
    apps_query = "SELECT AppName, Path FROM AppManagement;"
    apps_data = query_db(apps_query)
    print(f"apps_data: {apps_data}")

    # AppNameがPathに含まれるレコードの抽出
    filtered_apps = filter_items(apps_data)
    print(f"filtered_apps: {filtered_apps}")

    # 結果をJSON文字列に変換
    data = {'news': filtered_news, 'apps': filtered_apps}

    # POSTリクエストでデータをapp.pyに送信
    response = requests.post('http://localhost:5000/news', json=data)
    if response.status_code == 200:
        # 一時ファイルにHTMLレスポンスを保存
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding="utf-8") as f:
            f.write(response.text)
            # ブラウザで開く
            webbrowser.open(f.name)

if __name__ == '__main__':
    main()
