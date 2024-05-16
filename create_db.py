import sqlite3

def drop_table(con):
    con.execute("DROP TABLE NewsManagement;")
    con.execute("DROP TABLE AppManagement;")
    con.execute("DROP TABLE NewsPublication;")

def create_table(con):
    # ニュース管理テーブル作成
    con.execute("""
        CREATE TABLE NewsManagement (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Title TEXT,
            Year INTEGER,
            PublicationDate TEXT,
            Deadline INTEGER,
            EndFlag INTEGER,
            Path TEXT
        );
    """)
    
    # アプリ管理テーブル作成
    con.execute("""
        CREATE TABLE AppManagement (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            AppName TEXT,
            Path TEXT,
            SortNumber INTEGER,
            EndFlag INTEGER
        );
    """)
    
    # ニュース掲載テーブル作成
    con.execute("""
        CREATE TABLE NewsPublication (
            NewsID INTEGER PRIMARY KEY,
            AppID INTEGER
        );
    """)


def insert_data(con):
    con.execute("""INSERT INTO NewsManagement (Category, Title, Year, PublicationDate, Deadline, EndFlag, Path) VALUES ('メンテナンス', 'Autodeskライセンス更新に伴う利用停止', 2023, '2023-1-10', 14, 0, '/news/autodesk.html');""")
    con.execute("""INSERT INTO AppManagement (AppName, Path, SortNumber, EndFlag) VALUES ('app.py', 'C:\\Users\\ryoma\\Desktop\\Flask\\newsapp', 100, 0);""")
    con.execute("""INSERT INTO NewsPublication (NewsID, AppID) VALUES (1,1);""")

    con.execute("""INSERT INTO NewsManagement (Category, Title, Year, PublicationDate, Deadline, EndFlag, Path) VALUES ('お知らせ', 'Autodesk新バージョンアップ', 2024, '2024-5-8', 14, 0, '/news/autodesk.html');""")
    con.execute("""INSERT INTO AppManagement (AppName, Path, SortNumber, EndFlag) VALUES ('script.py', 'C:\\Users\\ryoma\\Desktop\\Flask\\newsapp', 100, 0);""")
    con.execute("""INSERT INTO NewsPublication (NewsID, AppID) VALUES (2,2);""")

    con.execute("""INSERT INTO NewsManagement (Category, Title, Year, PublicationDate, Deadline, EndFlag, Path) VALUES ('(共通)', '岡崎地区の計画停電の案内', 2024, '2024-5-10', 14, 0, '/news/autodesk.html');""")
    con.execute("""INSERT INTO NewsPublication (NewsID, AppID) VALUES (3,1);""")
    
    con.execute("""INSERT INTO NewsManagement (Category, Title, Year, PublicationDate, Deadline, EndFlag, Path) VALUES ('お知らせ', '配属のお知らせ', 2024, '2024-3-21', 14, 0, '/news/autodesk.html');""")
    con.execute("""INSERT INTO NewsPublication (NewsID, AppID) VALUES (4,2);""")
def select_data(con):
    try:
        data = con.execute("""
            SELECT * 
            FROM NewsManagement
            WHERE 
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
        """)
        return data         
    except Exception as e:
        print(e)

try:
    with sqlite3.connect("NewsAppDB.db") as con:
        drop_table(con)
        create_table(con)
        insert_data(con)
        con.commit()
        data = select_data(con)
        for row in data:
            print(row)
            print(type(row))
        data.close()
except Exception as ex:
    print(ex)
