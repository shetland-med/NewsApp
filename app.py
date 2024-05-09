import sqlite3
from flask import render_template, request, Flask, jsonify

app = Flask(__name__)

@app.route('/news', methods=['POST'])
def index():
    # POSTで受け取ったJSONデータを処理
    data = request.get_json()
    # 受け取ったデータを元にHTMLページをレンダリング
    print(data)
    print(data["news"])
    return render_template('index.html', news_data=data['news'], apps_data=data['apps'])


def get_news(filter_app_list):
    try:
        with sqlite3.connect("NewsAppDB.db") as con:
            sql = create_previous_sql(filter_app_list)
            data = con.execute(sql)
            for row in data:
                print(row)
            data.close()
    except Exception as e:
        print(e)

def create_previous_sql(filter_app_list, newstype):
    sql = """
    SELECT AppManagement.AppName, AppManagement.Path,NewsManagement.Path, NewsManagement.Category,
    NewsManagement.Title, NewsManagement.PublicationDate, NewsManagement.Year 
    FROM NewsManagement 
    JOIN NewsPublication 
    ON NewsManagement.ID = NewsPublication.NewsID 
    JOIN AppManagement 
    ON NewsPublication.AppID = AppManagement.ID 
    WHERE TRUE
    """
    if newstype == "new":
        if filter_app_list:
            for app_name in filter_app_list:
                sql += " AND AppName = '" + app_name + "'"
    return sql + ";"

def create_new_sql():
    sql = """
    SELECT AppManagement.AppName, AppManagement.Path, NewsManagement.Category,
    NewsManagement.Title, NewsManagement.PublicationDate, NewsManagement.Year 
    FROM NewsManagement 
    JOIN NewsPublication 
    ON NewsManagement.ID = NewsPublication.NewsID 
    JOIN AppManagement 
    ON NewsPublication.AppID = AppManagement.ID 
    WHERE TRUE
    """
    return sql + ";"

def get_appname():
    sql = "SELECT AppName, Path FROM AppManagement;"
    return sql

if __name__ == "__main__":
    app.run(debug=True, port=5000)