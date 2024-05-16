from flask import Flask, request, render_template, jsonify, session
import sqlite3
import os
import configparser

app = Flask(__name__)
# セッション管理のための秘密鍵
app.secret_key = os.urandom(24)  

# セッションの開始
@app.route('/start_session', methods=['GET'])
def start_session():
    session['data'] = None
    return "Session started", 200


@app.route('/news', methods=['POST', 'GET'])
def index():
    # POSTされたデータをsessionに格納
    if request.method == "POST":
        data = request.get_json()
        session['data'] = data
        return "Data received", 200
    
    # 
    elif request.method == "GET":
        data = session.get('data')
        print(f"session data on GET: {data}")  # セッションデータを取得して表示
        previous_data = get_news(0)
        previous_data_filtered = filter_items(previous_data)
        if data:
            return render_template('index.html', news_data=data['news'], apps_data=data['apps'], previous_news_data=previous_data_filtered)
        else:
            # 新着ニュースの取得
            news_data = get_news(1)
            # ファイルパスにファイルが存在するレコードのみを抽出
            filtered_news = filter_items(news_data)

            # フィルタ用アプリ名の取得
            apps_query = "SELECT AppName, Path FROM AppManagement;"
            apps_data = query_db(apps_query)
            apps_data_filtered = filter_items(apps_data)
            return render_template('index.html', news_data=filtered_news, apps_data=apps_data_filtered, previous_news_data=previous_data_filtered)

# フィルタ検索の処理
@app.route('/search', methods=['POST'])
def search():
    # 選択されたアプリ名の取得
    selected_apps = request.get_json()
    print(f"selected_apps:{selected_apps}")
    
    # 選択されたアプリ名に紐づくニュースを取得
    previous_data = get_news(0, selected_apps)
    new_news_data = get_news(1, selected_apps)
    
    # ファイルパスにファイルが存在するレコードのみを抽出
    previous_data_filtered = filter_items(previous_data)
    new_news_data_filtered = filter_items(new_news_data)
    
    # フィルタ用アプリ名の取得処理
    apps_query = "SELECT AppName, Path FROM AppManagement;"
    apps_data = query_db(apps_query)
    apps_data_filtered = filter_items(apps_data)
    
    return jsonify({
        'filtered_previous_data': previous_data_filtered,
        'filtered_new_data': new_news_data_filtered,
        'filtered_apps': apps_data_filtered
    }), 200

# iniファイルの読み込み
def read_ini():
    config = configparser.ConfigParser()
    config.read('config.ini')
    app.config['DATABASE_NAME'] = config['DATABASE']['Name']

# SQL文を実行
def query_db(query):
    with sqlite3.connect(app.config['DATABASE_NAME']) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

# 掲載用ニュースの取得処理
def get_news(news_type, filter_app_list=[]):
    if news_type == 1:
        sql = create_new_news(filter_app_list)
    else:
        sql = create_previous_news(filter_app_list)
    rows = query_db(sql)
    return rows

# 過去掲載ニュースのSQL文を作成
def create_previous_news(filter_app_list):
    sql = """
    SELECT AppManagement.AppName, AppManagement.Path, NewsManagement.Path, NewsManagement.Category,
    NewsManagement.Title, NewsManagement.PublicationDate, NewsManagement.Year 
    FROM NewsManagement 
    JOIN NewsPublication 
    ON NewsManagement.ID = NewsPublication.NewsID 
    JOIN AppManagement 
    ON NewsPublication.AppID = AppManagement.ID 
    WHERE TRUE
    """
    if filter_app_list:
        sql += " AND AppName IN ('" + "','".join(filter_app_list) + "')"
    return sql + ";"

# 新着ニュースのSQL文を作成
def create_new_news(filter_app_list):
    sql = """
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
    )
    """
    if filter_app_list:
        sql += " AND AppName IN ('" + "','".join(filter_app_list) + "')"
    return sql

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

if __name__ == "__main__":
    read_ini()  # アプリケーションの起動時に一度だけ ini ファイルを読み込む
    app.run(debug=True, port=5000)
