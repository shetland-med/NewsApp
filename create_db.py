import sqlite3

def drop_table(con):
    con.execute("DROP TABLE NewsManagement;")
    con.execute("DROP TABLE AppManagement;")
    con.execute("DROP TABLE NewsPublication;")

def create_table(con):
    # ニュース管理テーブル作成
    con.execute("""CREATE TABLE NewsManagement (
        ID INTEGER PRIMARY KEY,
        Category TEXT,
        Title TEXT,
        Year INTEGER,
        PublicationDate TEXT,
        Deadline INTEGER,
        EndFlag INTEGER,
        Path TEXT
    );""")
    
    # アプリ管理テーブル作成
    con.execute("""CREATE TABLE AppManagement (
        ID TEXT PRIMARY KEY,
        AppName TEXT,
        Path TEXT,
        SortNumber INTEGER,
        EndFlag INTEGER
    );""")
    
    # ニュース掲載テーブル作成
    con.execute("""CREATE TABLE NewsPublication (
        NewsID INTEGER PRIMARY KEY,
        AppID TEXT
    );""")


def insert_data(con):
    con.execute("""INSERT INTO NewsManagement (ID, Category, Title, Year, PublicationDate, Deadline, EndFlag, Path) VALUES (2024042501, 'お知らせ', 'Autodeskバージョンアップ', 2024, '2024/5/8', 14, 0, '/news/autodest.html');""")
    con.execute("""INSERT INTO AppManagement (ID, AppName, Path, SortNumber, EndFlag) VALUES ('A001', 'test.py', 'C:\\Users\\ryoma\\Desktop\\Flask', 100, 0);""")
    con.execute("""INSERT INTO NewsPublication (NewsID, AppID) VALUES (2024042501, 'A001');""")

def select_data(con):
    try:
        data = con.execute("""
            SELECT *
            FROM NewsManagement
            WHERE
                DATE(
                    substr(PublicationDate, 1, instr(PublicationDate, '/') - 1) || '-' || -- 年
                    substr('0' || substr(PublicationDate, instr(PublicationDate, '/') + 1, instr(substr(PublicationDate, instr(PublicationDate, '/') + 1), '/') - 1), -2) || '-' || -- 月
                    substr('0' || substr(PublicationDate, instr(substr(PublicationDate, instr(PublicationDate, '/') + 1), '/') + instr(PublicationDate, '/') + 1), -2)  -- 日
                ) <= DATE('now') AND
                DATE('now') <= DATE(
                    substr(PublicationDate, 1, instr(PublicationDate, '/') - 1) || '-' || -- 年
                    substr('0' || substr(PublicationDate, instr(PublicationDate, '/') + 1, instr(substr(PublicationDate, instr(PublicationDate, '/') + 1), '/') - 1), -2) || '-' || -- 月
                    substr('0' || substr(PublicationDate, instr(substr(PublicationDate, instr(PublicationDate, '/') + 1), '/') + instr(PublicationDate, '/') + 1), -2), -- 日
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