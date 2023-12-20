import psycopg2
from . import password as pw
from werkzeug.security import check_password_hash

class InvalidEmailException(Exception):
    pass

def insert_data(values:list[any]=None)->None:
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    INSERT INTO 使用者("姓名", "性別", "聯絡電話", "電子郵件", "isGetEmail","出生年月日", "自我介紹", "密碼", "連線密碼") 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''
    try:    
        cursor.execute(sql,values)
    except psycopg2.errors.UniqueViolation:
        raise InvalidEmailException
    except Exception as e:
        print(e)
        raise RuntimeError  
    conn.commit()
    cursor.close()
    conn.close()

def validateUser(email:str,password:str)->tuple[bool,str]:
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER, 
                            password=pw.PASSWORD,
                            host=pw.HOST, 
                            port="5432")
    cursor = conn.cursor()
    sql = '''
    select 密碼,姓名
    from 使用者
    where 電子郵件 = %s
    '''

    cursor.execute(sql,[email])
    searchData:tuple[str,str] = cursor.fetchone() #傳出tuple(hash_apssword,name)
    hash_password = searchData[0]
    username = searchData[1]
    is_ok = check_password_hash(hash_password,password)        
    cursor.close()
    conn.close()
    return (is_ok,username) 


    

    