import requests
import psycopg2
#import password as pw
#from . import password as pw
import csv
import socket
import os
import base64

myip = socket.gethostbyname(socket.gethostname())

if '172.17.0.2' <= myip <= '172.17.255.255':
    print(f'本機{myip}')
    from . import password as rpw
    DATABASE=rpw.DATABASE
    USER=rpw.USER
    PASSWORD=rpw.PASSWORD
    HOST=rpw.HOST


else:
    print(f'server{myip}')
    DATABASE=os.environ['DATABASE']
    USER=os.environ['USER']
    PASSWORD=os.environ['PASSWORD'] 
    HOST=os.environ['HOST']




def __open_cpbl_data() ->list[dict]:

    pitchings_2022 = 'pitchings_2022_updated.csv'
    try:
        with open (pitchings_2022, mode='r', encoding='utf-8', newline='') as pitchings_file:
            pitchings_dictReader = csv.DictReader(pitchings_file)
            print('讀取成功')
            #print(list(pitchings_dictReader))
            return list(pitchings_dictReader)
    except Exception as e:
            print(f'讀取錯誤{e}')
            return  []
    

def __create_table(conn)->None:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")    
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE  IF NOT EXISTS cpbl_pitchings(
            "年份"	TEXT NOT NULL,
            "所屬球隊" TEXT NOT NULL,
            "球員編號" INTEGER NOT NULL,
            "球員姓名" TEXT NOT NULL,
            "出場數" TEXT NOT NULL,
            "先發次數" INTEGER,
            "中繼次數" INTEGER,
            "勝場數" INTEGER,
            "敗場數" INTEGER,
            "救援成功" INTEGER,
            "中繼成功" INTEGER,
            "有效局數" FLOAT,
            "面對打者數" INTEGER,
            "被安打數" INTEGER,
            "被全壘打數" INTEGER,
            "保送數" INTEGER,
            "三振數" INTEGER,
            "自責分" INTEGER,
            "投打習慣" TEXT NOT NULL,
            "背號" INTEGER,
            "身高體重" TEXT NOT NULL,
            "生日" TEXT NOT NULL,
            "照片網址" TEXT NOT NULL,
            "奪三振率" FLOAT NOT NULL,
            "防禦率" FLOAT NOT NULL,
            PRIMARY KEY("球員編號"),
            UNIQUE(年份, 球員編號)
        );
        '''
    )
    conn.commit()
    cursor.close()
    print("create_table成功")

def __insert_data(conn,values:list[any])->None:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    INSERT INTO cpbl_pitchings(年份, 所屬球隊, 球員編號, 球員姓名, 出場數, 先發次數, 中繼次數, 勝場數, 敗場數, 救援成功, 中繼成功, 有效局數, 面對打者數, 被安打數, 被全壘打數, 保送數, 三振數, 自責分, 投打習慣, 背號, 身高體重, 生日, 照片網址, 奪三振率, 防禦率)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (年份,球員編號) DO NOTHING
    '''
    cursor.execute(sql,values)    
    conn.commit()
    cursor.close()
    print('insert成功')

def updata_render_data()->None:
    '''
    下載,並更新資料庫
    '''
    data = __open_cpbl_data()
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
        
    __create_table(conn)
    for item in data:
            __insert_data(conn, values=[item['Year'], item['Team Name'], item['ID'], item['Name'], item['G'], item['GS'], item['GR'],item['W'], item['L'], item['SV'], item['HLD'], item['IP'], item['BF'], item['H'],item['HR'], item['BB'], item['SO'], item['ER'], item['B_t'], item['Number'], item['Ht_wt'],item['Born'],item['Img'],item['K9'],item['ERA']])

    conn.close()
    print('update成功')

#呼叫最新資料
def lastest_datetime_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
        from cpbl_pitchings
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print('latest成功')
    return rows

#查詢球員姓名
def search_sitename(word:str) -> list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    SELECT 
    年份, 
    所屬球隊, 
    球員編號, 
    球員姓名, 
    先發次數, 
    中繼次數, 
    勝場數, 
    敗場數, 
    三振數, 
    自責分
    FROM cpbl_pitchings
    WHERE 球員姓名 LIKE %s
        '''
    cursor.execute(sql,[f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#查詢球員編號，回傳製作K9及era圖表
def search_player_by_id(word:int) -> list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    SELECT 
    所屬球隊, 
    球員姓名, 
    背號, 
    投打習慣, 
    身高體重, 
    生日,
    奪三振率,
    防禦率
    FROM cpbl_pitchings
    WHERE 球員編號 = %s
        '''
    cursor.execute(sql,(word,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


#計算平均奪三振率與防禦率
def avg_k9_rea() -> list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    SELECT 
    所屬球隊, 
    球員姓名, 
    背號, 
    投打習慣, 
    身高體重, 
    生日,
    奪三振率,
    防禦率
    FROM cpbl_pitchings
        '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


#更新先發中繼圓餅圖
def search_player_game_pie(word:int) -> list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    SELECT 
    球員編號,
    所屬球隊, 
    球員姓名, 
    出場數,
    先發次數,
    中繼次數,
    勝場數,
    敗場數,
    救援成功,
    中繼成功,
    有效局數,
    面對打者數,
    被安打數,
    被全壘打數,
    保送數,
    三振數,
    自責分,
    奪三振率,
    防禦率
    FROM cpbl_pitchings
    WHERE 球員編號 = %s
        '''
    cursor.execute(sql,(word,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def team_selected(event, selectVar):
    select_value = selectVar.get()
    print(f"隊伍選擇: {select_value}")
    return select_value

def search_by_team(word:str):
    print(word) #使用者輸入的文字
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432") 
    cursor = conn.cursor() 
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
    from cpbl_pitchings
    WHERE 所屬球隊 LIKE ?
    '''
    cursor.execute(sql, [f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    #print(rows)
    return rows

#=============<PNG>按鈕用照片洗出編碼的地方======================
def team_logo(team:str):
    img_folder = os.path.join(os.getcwd(),'dash_file' ,'assets', 'img')
    team_png= f'{team}.png'
    team_logo = os.path.join(img_folder, team_png)

    with open(team_logo, "rb") as team_png:
        logo = base64.b64encode(team_png.read())
        logo = logo.decode()
        logo = "{}{}".format("data:image/png;base64, ", logo)
        
        return logo
    
#=============<IMG>按鈕用照片洗出編碼的地方======================
def img_pic(word:str):
    img_folder = os.path.join(os.getcwd(),'dash_file' ,'assets', 'img')
    img= f'{word}.jpg'
    img_path = os.path.join(img_folder, img)

    with open(img_path, "rb") as img:
        new_img = base64.b64encode(img.read())
        new_img = new_img.decode()
        new_img = "{}{}".format("data:image/jpg;base64, ", new_img)
        
        return new_img
    
#=====================樂天桃猿頁面用資料========================
    #呼叫最新資料
def rakuten_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
        from cpbl_pitchings
        where 所屬球隊 LIKE '樂天'
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#=====================中信兄弟頁面用資料========================
    #呼叫最新資料
def brothers_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
        from cpbl_pitchings
        where 所屬球隊 LIKE '中信'
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#=====================統一獅頁面用資料========================
    #呼叫最新資料
def lions_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
        from cpbl_pitchings
        where 所屬球隊 LIKE '統一'
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#=====================統一獅頁面用資料========================
    #呼叫最新資料
def fubon_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
        from cpbl_pitchings
        where 所屬球隊 LIKE '富邦'
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

#=====================統一獅頁面用資料========================
    #呼叫最新資料
def dragons_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 
        年份, 
        所屬球隊, 
        球員編號, 
        球員姓名, 
        先發次數, 
        中繼次數, 
        勝場數, 
        敗場數, 
        三振數, 
        自責分 
        from cpbl_pitchings
        where 所屬球隊 LIKE '味全'
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows