import requests
import psycopg2
#import password as pw
import socket
import os

myip = socket.gethostbyname(socket.gethostname())
if '172.17.0.0'<= myip <= '172.17.255.255':
    from . import password as pw
    print("本機")
    DATABASE = pw.DATABASE
    USER = pw.USER
    PASSWORD = pw.PASSWORD
    HOST = pw.HOST
else:
    DATABASE = os.environ['DATABASE']
    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
    HOST = os.environ['HOST']
     

print(f'我的ip是{myip}')

def lastest_datetime_data()->list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    SELECT 站點名稱,更新時間,行政區,地址,總車輛數,可借,可還
    FROM 台北市youbike
    WHERE (更新時間,站點名稱) IN (
	        SELECT MAX(更新時間),站點名稱
	        FROM 台北市youbike
	        GROUP BY 站點名稱
            );
    '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return rows

def search_sitename(word:str) -> list[tuple]:
    conn = psycopg2.connect(database=DATABASE,
                            user=USER, 
                            password=PASSWORD,
                            host=HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
        SELECT 站點名稱,更新時間,行政區,地址,總車輛數,可借,可還
        FROM 台北市youbike
        WHERE (更新時間,站點名稱) IN (
	          SELECT MAX(更新時間),站點名稱
	          FROM 台北市youbike
	            GROUP BY 站點名稱
        )  AND 站點名稱 like %s
        '''
    cursor.execute(sql,[f'%{word}%'])
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows