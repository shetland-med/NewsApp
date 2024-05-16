import sqlite3
import os
import requests  
import webbrowser
import configparser

news_query = """
    SELECT 
    AppManagement.AppName, AppManagement.Path, NewsManagement.Path, NewsManagement.Category,
    NewsManagement.Title, NewsManagement.PublicationDate, NewsManagement.Year 
    FROM NewsManagement 
    JOIN NewsPublication 
    ON NewsManagement.ID = NewsPublication.NewsID 
    JOIN AppManagement 
    ON NewsPublication.AppID = AppManagement.ID 
    WHERE    
    AppManagement.endflag = 0 AND NewsManagement.endflag = 0
    AND
    DATE(
        substr(PublicationDate, 1, instr(PublicationDate, '-') - 1) || '-' ||
        substr('0' || substr(PublicationDate, instr(PublicationDate, '-') + 1, instr(substr(PublicationDate, instr(PublicationDate, '-') + 1), '-') - 1), -2) || '-' || 
        substr('0' || substr(PublicationDate, instr(substr(PublicationDate, instr(PublicationDate, '-') + 1), '-') + instr(PublicationDate, '-') + 1), -2)
    )<= DATE('now') AND
    DATE('now') <= DATE(
        substr(PublicationDate, 1, instr(PublicationDate, '-') - 1) || '-' || 
        substr('0' || substr(PublicationDate, instr(PublicationDate, '-') + 1, instr(substr(PublicationDate, instr(PublicationDate, '-') + 1), '-') - 1), -2) || '-' || 
        substr('0' || substr(PublicationDate, instr(substr(PublicationDate, instr(PublicationDate, '-') + 1), '-') + instr(PublicationDate, '-') + 1), -2),
        '+' || Deadline || ' days'
    );
"""

# SQL文を実行
def query_db(query, db_name):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

# ファイルパスにファイル名が存在するレコードを抽出
def filter_items(data):
    filtered_data = []
    for item in data:
        app_name = item[0]  # AppName
        if app_name == "(共通)":
            filtered_data.append(item)
        else:
            app_path = os.path.join(item[1], app_name)  
            if os.path.exists(app_path):
                filtered_data.append(item)
    return filtered_data

# iniファイルの読み込み
def read_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')
    server_url = config['SERVER']['ServerUrl']
    database_name = config['DATABASE']['Name']
    return server_url, database_name

def main():
    global news_query
    server_url, database_name = read_ini()  # iniファイルの読み込み
    
    # セッションを開始
    session = requests.Session()
    response = session.get(f"{server_url}/start_session")
    if response.status_code != 200:
        print("Failed to start session")
        return
    
    # 新着ニュースの取得
    news_data = query_db(news_query, database_name)
    # ファイルパスにファイルが存在するレコードのみを抽出
    filtered_news = filter_items(news_data)

    # フィルタ用アプリ名の取得
    apps_query = "SELECT AppName, Path FROM AppManagement;"
    apps_data = query_db(apps_query, database_name)
    filtered_apps = filter_items(apps_data)

    # JSON形式に格納
    headers = {'Content-Type': 'application/json'}
    data = {'news': filtered_news, 'apps': filtered_apps}
    
    # サーバ側にPOST
    response = session.post(f"{server_url}/news", json=data, headers=headers)
    if response.status_code == 200:
        response = session.get(f"{server_url}/news")  # セッションを利用してGETリクエストを送信
        if response.status_code == 200:
            webbrowser.open(f"{server_url}/news")  # ブラウザを起動し、HTMLを表示

if __name__ == '__main__':
    main()
