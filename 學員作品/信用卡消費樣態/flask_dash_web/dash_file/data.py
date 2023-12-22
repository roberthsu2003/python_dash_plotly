import requests
import psycopg2
#import password as pw
import pandas as pd
import csv
import os
import socket

myip = socket.gethostbyname(socket.gethostname())
if '172.17.0.0' <= myip <= '172.17.255.255':
    from . import password as pw
    DATABASE = pw.DATABASE
    USER = pw.USER
    PASSWORD = pw.PASSWORD
    HOST = pw.HOST
else:
    DATABASE = os.environ['DATABASE']
    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
    HOST = os.environ['HOST']

def __download_creditcard_data():
    edu_url = (
        "https://bas.nccc.com.tw/nccc-nop/OpenAPI/C05/educationconsumption/MCT/ALL"
    )
    response = requests.request("GET", edu_url)
    with open(f"./six_edu.csv", "wb") as file:
        file.write(response.content)
    print("教育程度資料讀取成功")

    age_url = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/C02/ageconsumption/MCT/ALL"
    response = requests.request("GET", age_url)
    with open(f"./six_age.csv", "wb") as file:
        file.write(response.content)
    print("年齡層消費資料讀取成功")

    job_url = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/C04/jobsconsumption/MCT/ALL"
    response = requests.request("GET", job_url)
    with open(f"./six_job.csv", "wb") as file:
        file.write(response.content)
    print("職業類別消費資料讀取成功")

    sex_url = "https://bas.nccc.com.tw/nccc-nop/OpenAPI/C01/sexconsumption/MCT/ALL"
    response = requests.request("GET", sex_url)
    with open(f"./six_sex.csv", "wb") as file:
        file.write(response.content)
    print("性別消費資料讀取成功")

    incom_url = (
        "https://bas.nccc.com.tw/nccc-nop/OpenAPI/C03/incomegroupsconsumption/MCT/ALL"
    )
    response = requests.request("GET", incom_url)
    with open(f"./six_incom.csv", "wb") as file:
        file.write(response.content)
    print("收入消費資料讀取成功")


def trans_data():
    area_code = {
        "63000000": "臺北市",
        "64000000": "高雄市",
        "65000000": "新北市",
        "66000000": "臺中市",
        "67000000": "臺南市",
        "68000000": "桃園市",
    }
    sex_code = {"1": "男性", "2": "女性"}
    type = ["age", "edu", "incom", "job", "sex"]
    for item in type:
        df = pd.read_csv(f"six_{item}.csv")
        if item == "edu":
            df = df[df["教育程度類別"] != "其他"]
        elif item == "job":
            df = df[df["職業類別"] != "其他"]

        df["年月"] = df["年月"].astype(str)
        df["年"] = df["年月"].str[:4]
        df["月"] = df["年月"].str[4:]
        df = df[(df["產業別"] != "其他")]
        df = df[df["年"] == "2023"]
        df = df.drop(columns=["年月"])
        df = df[["年", "月"] + [col for col in df.columns if col not in ["年", "月"]]]
        df = df.rename(columns={"信用卡交易金額[新台幣]": "信用卡交易金額"})
        df.to_csv(f"six_{item}.csv", index=False, encoding="utf-8")

        with open(f"six_{item}.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            fieldnames = csv_reader.fieldnames
            with open(
                f"six_{item}_2023.csv", "w", encoding="utf-8", newline=""
            ) as file:
                csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
                csv_writer.writeheader()

                for row in csv_reader:
                    row["地區"] = area_code.get(row["地區"], row["地區"])
                    if "性別" in fieldnames:
                        row["性別"] = sex_code.get(row["性別"], row["性別"])
                        new_row["性別"] = row["性別"]

                    new_row = {"地區": row["地區"]}
                    new_row.update(row)
                    csv_writer.writerow(new_row)


# ---------------create sql table----------------#
def __create_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS edu(
            "id" SERIAL,
            "年" INTEGER NOT NULL,
            "月" INTEGER NOT NULL,
            "地區" TEXT NOT NULL,
            "產業別" TEXT NOT NULL,
            "教育程度"	TEXT NOT NULL,
            "信用卡交易筆數" BIGINT NOT NULL,
            "信用卡交易金額" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
		"""
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS job(
            "id" SERIAL,
            "年" INTEGER NOT NULL,
            "月" INTEGER NOT NULL,
            "地區" TEXT NOT NULL,
            "產業別" TEXT NOT NULL,
            "職業類別"	TEXT NOT NULL,
            "信用卡交易筆數" BIGINT NOT NULL,
            "信用卡交易金額" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
		"""
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS age(
            "id" SERIAL,
            "年" INTEGER NOT NULL,
            "月" INTEGER NOT NULL,
            "地區" TEXT NOT NULL,
            "產業別" TEXT NOT NULL,
            "年齡層"	TEXT NOT NULL,
            "信用卡交易筆數" BIGINT NOT NULL,
            "信用卡交易金額" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
		"""
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS incom(
            "id" SERIAL,
            "年" INTEGER NOT NULL,
            "月" INTEGER NOT NULL,
            "地區" TEXT NOT NULL,
            "產業別" TEXT NOT NULL,
            "年收入"	TEXT NOT NULL,
            "信用卡交易筆數" BIGINT NOT NULL,
            "信用卡交易金額" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
		"""
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sex(
            "id" SERIAL,
            "年" INTEGER NOT NULL,
            "月" INTEGER NOT NULL,
            "地區" TEXT NOT NULL,
            "產業別" TEXT NOT NULL,
            "性別"	TEXT NOT NULL,
            "信用卡交易筆數" BIGINT NOT NULL,
            "信用卡交易金額" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
		"""
    )
    conn.commit()
    cursor.close()


# -----------------insert data-------------------#
def __insert_data(conn, tablename, values: list[any]) -> None:
    cursor = conn.cursor()

    # 根據 tablename 動態生成 SQL 語句
    table_columns = {
        "age": ["年齡層"],
        "edu": ["教育程度"],
        "incom": ["年收入"],
        "job": ["職業類別"],
        "sex": ["性別"],
    }

    for column in table_columns[tablename]:
        sql = f"INSERT INTO {tablename} (年, 月, 地區, 產業別, {column}, 信用卡交易筆數, 信用卡交易金額) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        print(sql)
        cursor.execute(sql, values)
        conn.commit()
    cursor.close()


def update_render_data() -> None:
    # ---------------連線到postgresql----------------#
    conn = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port="5432",
    )

    __create_table(conn)
    type = ["age", "edu", "incom", "job", "sex"]
    columns = ["年齡層", "教育程度類別", "年收入", "職業類別", "性別"]
    for item, column in zip(type, columns):
        with open(f"six_{item}_2023.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                __insert_data(
                    conn,
                    tablename=item,
                    values=[
                        row["年"],
                        row["月"],
                        row["地區"],
                        row["產業別"],
                        row[f"{column}"],
                        row["信用卡交易筆數"],
                        row["信用卡交易金額"],
                    ],
                )

    conn.close()


def search_data(dataName:str, tableName:str) -> list[tuple]:
    conn = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port="5432",
    )
    cursor = conn.cursor()
    sql = f"select 年, 月, 地區, 產業別, {dataName}, 信用卡交易筆數, 信用卡交易金額 from {tableName}"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows



#def main():
    __download_creditcard_data()
    trans_data()
    update_render_data()


#if __name__ == "__main__":
    main()
