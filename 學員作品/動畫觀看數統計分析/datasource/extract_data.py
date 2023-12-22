import psycopg2
import password as pw


def __fetch_data(conn) -> list[tuple]:
    select_query = '''
        SELECT * FROM 巴哈姆特動畫瘋
        WHERE 季度 LIKE '2020%' OR
        季度 LIKE '2021%' OR
        季度 LIKE '2022%' OR
        季度 in ('2023/01','2023/04')
        order by id
        '''
    cursor = conn.cursor()
    cursor.execute(select_query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def __create_revised_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS 動畫瘋訓練資料集(
        id smallserial,
        動畫名 text,
        總觀看數 integer,
        平均觀看數 integer,
        年份 text,
        月份 text,
        集數 smallint,
        星級 real,
        評分人數 integer,
        導演監督 TEXT,
        台灣代理 TEXT,
        製作廠商 TEXT,
        作品分類1 TEXT,
        作品分類2 TEXT,
        作品分類3 TEXT,
        作品分類4 TEXT,
        作品分類5 TEXT,
        作品分類6 TEXT,
        原作載體 TEXT,
        新續作 TEXT,
        PRIMARY KEY(id),
        UNIQUE(動畫名)
    )
        '''
    )
    cursor.close()
    conn.commit()
    print('資料表創建成功')


def __convert_datatype(data: tuple) -> list:
    values = []

    # 加入動畫名
    values.append(data[1])

    # 處理觀看數
    if data[2] == '統計中':
        values.append(-1)
    elif data[2].find('萬') == -1:
        values.append(int(data[2]))
    else:
        vlist = data[2].split("萬")
        vfloat = float(vlist[0]) * 10000
        values.append(int(vfloat))

    # 加入年份、月份
    vlist = data[3].split("/")
    values.append(vlist[0])
    values.append(vlist[1])

    # 處理集數
    episode = int(data[4])
    values.append(episode)

    # 處理星級
    if data[6] == '--':
        values.append(-1)
    else:
        values.append(float(data[6]))

    # 加入評分人數
    if data[7] == '統計中':
        values.append(-1)
    else:
        values.append(int(data[7]))

    # 加入剩餘項目
    values.append(data[8])
    values.append(data[9])
    values.append(data[10])
    values.append(data[11])
    values.append(data[12])
    values.append(data[13])
    values.append(data[14])
    values.append(data[15])
    values.append(data[16])
    values.append(data[17])
    values.append(data[18])

    # 加入平均觀看數
    avg_view = round(values[1] / values[4])
    values.append(avg_view)
    return values


def __insert_data(conn, data: list) -> None:
    insert_query = f'''
        INSERT INTO 動畫瘋訓練資料集(
                動畫名,
                總觀看數,
                年份,
                月份,
                集數,
                星級,
                評分人數,
                導演監督,
                台灣代理,
                製作廠商,
                作品分類1,
                作品分類2,
                作品分類3,
                作品分類4,
                作品分類5,
                作品分類6,
                原作載體,
                新續作,
                平均觀看數
                )
                VALUES({','.join(['%s'] * 19)})
        '''
    cursor = conn.cursor()
    cursor.execute(insert_query, data)
    cursor.close()


def __extract_data():
    # 與資料庫建立連接
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER,
                            password=pw.PASSWORD,
                            host=pw.HOST,
                            port=pw.PORT)
    # 創建資料表
    __create_revised_table(conn)

    # 抓取訓練集所需資料
    rows = __fetch_data(conn)

    # 進行資料型別轉換後插入資料
    for row in rows:
        values = __convert_datatype(row)
        print(values)
        __insert_data(conn, data=values)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    __extract_data()
