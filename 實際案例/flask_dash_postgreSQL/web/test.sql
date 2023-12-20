#檢查是否有這個表格
SELECT EXISTS (
SELECT 1
FROM information_schema.tables
WHERE table_name = '台北市youbike'
) AS table_existence;

#建立表格
CREATE TABLE IF NOT EXISTS 使用者(
	"id"	SERIAL,
	"姓名"	TEXT NOT NULL,
	"性別"	TEXT NOT NULL,
	"聯絡電話" TEXT,
	"電子郵件" TEXT NOT NULL,
	"isGetEmail" boolean NOT NULL,
	"出生年月日"	date,
	"自我介紹" TEXT,
	"密碼" TEXT,
	"連線密碼" TEXT,
	PRIMARY KEY("id"),
	UNIQUE("電子郵件")
);

#新增使用者
INSERT INTO 使用者("姓名", "性別", "聯絡電話", "電子郵件", "isGetEmail","出生年月日", "自我介紹", "密碼", "連線密碼") 
VALUES ('徐國堂','男','0935-123-456','roberthsu2003@gmail.com',true,'1970-03-01','老師','abc','efg')
    

