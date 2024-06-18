from flask import Flask, request, render_template, jsonify
from logging import getLogger, DEBUG, INFO, ERROR, WARNING, Formatter, StreamHandler, FileHandler
import sqlite3
import os
import configparser
import json
import datetime
from contextlib import closing

app = Flask(__name__)

logger = None

@app.route('/news', methods=['POST', 'GET'])
def index():
    try:
        # POSTされたデータを格納
        if request.method == "POST":
            data = request.get_json()
            print(f"post data: {data}")
            # 環境変数'username'を取得
            #username = os.environ.get('username')
            username = "0bf"
            
            print(f"username: {username}")
            with open(f"temp/data_{username}.json", 'w') as f:
                json.dump(data, f)
            # ユーザのIDをクライアントに返す
            return jsonify({'username': username}), 200

        
        elif request.method == "GET":
            err_flg = False

            username = request.args.get('username')
            with open(f"temp/data_{username}.json", 'r') as f:
                data = json.load(f)
            os.remove(f"temp/data_{username}.json")
            print(f"json data on GET: {data}")  # JSONデータを取得して表示

            # 過去掲載ニュースの取得
            filter_app_list = []
            # eVDI起動時はフィルターをかけた状態でニュースを抽出
            if data['from_batch'] == 1:
                filter_app_list = data['apps']
            # for val in data['apps']:
            # filter_app_list.append(val[0])
            previous_data = get_news(0, filter_app_list)
            previous_data_filtered = filter_items(previous_data)

            # フィルタ用アプリ名の取得
            apps_query = "SELECT DISTINCT AppCategory, Path FROM App_Mgmt;"
            apps_data = query_db(apps_query)
            apps_data_filtered = filter_items(apps_data)

            if data['from_batch'] == 1:
                return render_template('index.html', news_data=data['news'], apps_data=apps_data, filter_apps=filter_app_list, previous_news_data=previous_data_filtered)
            else:
                return render_template('index.html', news_data=data['news'], apps_data=apps_data, filter_apps=[], previous_news_data=previous_data_filtered)
    except Exception as e:
        logger.error(f"(index): {e}")

# フィルタ検索の処理
@app.route('/search', methods=['POST'])
def search():
    try:
        # 選択されたアプリ名の取得
        selected_apps = request.get_json()
        logger.info("(search) AppName Search Start...")
        logger.debug(f"(search) selected_apps: {selected_apps}")

        # 選択されたアプリ名に紐づくニュースを取得
        previous_data = get_news(0, selected_apps)
        new_news_data = get_news(1, selected_apps)

        # ファイルパスにファイルが存在するレコードのみを抽出
        previous_data_filtered = filter_items(previous_data)
        new_news_data_filtered = filter_items(new_news_data)

        # フィルタ用アプリ名の取得処理
        apps_query = "SELECT DISTINCT AppCategory, Path FROM App_Mgmt;"
        apps_data = query_db(apps_query)
        apps_data_filtered = filter_items(apps_data)

        return jsonify({
            'filtered_previous_data': previous_data_filtered,
            'filtered_new_data': new_news_data_filtered,
            'filtered_apps': apps_data_filtered
        }), 200
    except Exception as e:
        logger.error(f"(search): {e}")

# 掲載用ニュースの取得処理
def get_news(news_type, filter_app_list=[]):
    try:
        if news_type == 1:
            sql = create_new_news(filter_app_list)
        else:
            sql = create_previous_news(filter_app_list)
        logger.debug(f"(get_news) sql: {sql}")
        rows = query_db(sql)
        return rows
    except Exception as e:
        logger.error(f"(get_news): {e}")


# 過去掲載ニュースのSQL文を作成
def create_previous_news(filter_app_list):
    try:
        sql = """
        SELECT App_Mgmt.AppCategory, App_Mgmt.Path, News_Mgmt.News_FileName, News_Mgmt.Category,
        News_Mgmt.Title, News_Mgmt.PublicationDate, News_Mgmt.Year
        FROM News_Mgmt
        JOIN ID_Mgmt
        ON News_Mgmt.ID = ID_Mgmt.NewsID
        JOIN App_Mgmt
        ON ID_Mgmt.AppID = App_Mgmt.ID
        WHERE TRUE
        """
        if filter_app_list:
            sql += " AND AppCategory IN (" + ",".join(filter_app_list) + ")"
        return sql + ";"
    except Exception as e:
        logger.error(f"(create_previous_news): {e}")


# 新着ニュースのSQL文を作成
def create_new_news(filter_app_list):
    sql = """
    SELECT App_Mgmt.AppCategory, App_Mgmt.Path, News_Mgmt.News_FileName, News_Mgmt.Category,
    News_Mgmt.Title, News_Mgmt.PublicationDate, News_Mgmt.Year
    FROM News_Mgmt
    JOIN ID_Mgmt
    ON News_Mgmt.ID = ID_Mgmt.NewsID
    JOIN App_Mgmt
    ON ID_Mgmt.AppID = App_Mgmt.ID
    WHERE 
    App_Mgmt.endflag = 0 AND News_Mgmt.endflag = 0
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
    try:
        filtered_data = []
        for item in data:
            app_name = item[0]  # AppName
            app_path = item[1]  # Path
            if os.path.exists(app_path):
                filtered_data.append(item)
        return filtered_data
    except Exception as e:
        logger.error(f"(filter_items): {e}")

if __name__ == "__main__":
    # アプリケーションの起動時に一度だけ ini ファイルを読み込む
    read_ini()
    app.run(debug=True)

