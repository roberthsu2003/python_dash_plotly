import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import psycopg2
import password as pw


def __download_data(url: str) -> list[list]:
    # 建立隨機user_agent
    user_agent = UserAgent()

    # 建立隨機referer
    referer_choices = ['https://jplop.neocities.org/shar_free_movie_site',
                       'https://www.google.com',
                       'https://favsk.com/ani-gamer/',
                       'https://www.bing.com'] + [f'https://ani.gamer.com.tw/animeList.php?page={i+2}' for i in range(56)]
    referer = random.choice(referer_choices)

    # 開始爬蟲
    response = requests.get(
        url, headers={"User-Agent": user_agent.random, "Referer": referer, })
    response.encoding = 'utf8'
    if response.status_code == 200:
        print(f'請求成功：{response.status_code}')
    else:
        print(f'請求失敗：{response.status_code}')

    # 建立BeautifulSoup物件
    intro_data = BeautifulSoup(response.text, 'html.parser')
    anime_infos = intro_data.select('.theme-list-main')

    # 最後傳出的list
    anime_data = []

    # 使用迴圈從目標區塊取得資訊
    for anime_info in anime_infos:
        anime_name = anime_info.select_one('.theme-name').text.strip()
        # 區分全年齡版與年齡限制版
        if anime_info.select_one('.color-R18') is not None:
            anime_name = anime_name + ' 年齡限制版'
        show_view_number = anime_info.select_one(
            '.show-view-number > p').text.strip()
        anime_time = anime_info.select_one(
            '.theme-time').text.strip().replace('年份：', '')
        anime_episode = anime_info.select_one(
            '.theme-number').text.strip().replace('共', '').replace('集', '')
        anime_link = 'https://ani.gamer.com.tw/' + anime_info['href']

        # 建立隨機延遲
        delay_choices = [0.2, 0.5, 0.7, 1, 1.3, 1.8, 2]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)

        # 進入作品播放頁面取得詳細資訊
        r1 = requests.get(anime_link, headers={
            "User-Agent": user_agent.random, "Referer": referer, })
        r1.encoding = 'utf8'

        # 建立BeautifulSoup物件
        detail_data = BeautifulSoup(r1.text, 'html.parser')
        acg_score = detail_data.select_one('.acg-score')
        star = acg_score.select_one('.score-overall-number').text.strip()
        rating_people = acg_score.select_one(
            '.score-overall-people').text.strip().replace('人評價', '').replace(',', '')

        # 處理staff和tag
        type_list = detail_data.select_one('.type-list')
        staff = []
        tags = []
        pre_data = []
        for p in type_list.find_all('p'):
            staff.append(p.text)
        for li in type_list.select('.tag'):
            tags.append(li.text)

        # 建立一個list儲存除tag外所有資訊
        infos = [anime_name, show_view_number, anime_time, anime_episode,
                 anime_link, star, rating_people, staff[1], staff[2], staff[3]]

        # pre_data裡有一部作品所有資訊
        pre_data.append(infos)
        pre_data.append(tags)

        # anime_data裡有所有作品的pre_data
        anime_data.append(pre_data)

        # print(f'動畫名:{anime_name}\n觀看數:{show_view_number}\n季度:{anime_time}\n集數:{anime_episode}\n動畫連結:{anime_link}\n{star}\n{rating_people}\n導演:{staff[1]}\n代理商:{staff[2]}\n製作廠商:{staff[3]}\n分類:{tags}\n')

    return anime_data


def __create_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS 巴哈姆特動畫瘋(
	id SERIAL,
	動畫名 TEXT NOT NULL,
	觀看數 TEXT,
	季度 TEXT,
	集數 TEXT,
	動畫連結 TEXT,
	星級 TEXT,
	評分人數 TEXT,
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


def __insert_data(conn, infos: list[str], tags: list[str]) -> None:
    # 避免作品標籤超過6個
    if len(tags) >= 7:
        tags = [tags[i] for i in range(6)]

    # column_names必備元素
    column_names = [
        "動畫名", "觀看數", "季度", "集數", "動畫連結",
        "星級", "評分人數", "導演監督", "台灣代理", "製作廠商"
    ]

    # 依作品標籤數量增加column_names
    column_names += [f"作品分類{i + 1}" for i in range(len(tags))]

    # 基礎insert_sql
    insert_sql = f'''
        INSERT INTO 巴哈姆特動畫瘋
        ({','.join(column_names)})
        VALUES({','.join(['%s'] * len(column_names))})
        ON CONFLICT (動畫名) DO UPDATE SET
    '''
    # 基礎insert_sql + 更新內容
    update_content = [f"{column_names[i]}='{infos[i]}'" for i in range(1, 7)]
    on_conflict_sql = ', '.join(update_content)
    insert_sql += on_conflict_sql

    cursor = conn.cursor()
    cursor.execute(insert_sql, infos + tags)
    cursor.close()


def __last_page(url: str) -> int:
    user_agent = UserAgent()
    headers = {
        'user-agent': user_agent.random,
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf8'
    if response.status_code == 200:
        print(f'取得頁碼_訊息代號：{response.status_code}')
    else:
        print(f'取得頁碼_訊息代號：{response.status_code}')

    index = BeautifulSoup(response.text, 'html.parser')
    page_number = index.select_one('.page_number > a:last-child').text
    page_number = int(page_number)
    return page_number


def animad_scraper():
    # 與資料庫建立連接
    conn = psycopg2.connect(database=pw.DATABASE,
                            user=pw.USER,
                            password=pw.PASSWORD,
                            host=pw.HOST,
                            port=pw.PORT)
    # 創建資料表
    __create_table(conn)

    # 取得動畫列表最後一頁的頁碼
    page_number = __last_page('https://ani.gamer.com.tw/animeList.php?')

    # 開始逐頁下載資料
    n = 0
    for i in range(20):
        # 每頁的url
        url = f'https://ani.gamer.com.tw/animeList.php?page={i+1}'
        anime_data = __download_data(url)

        # infos_tags是由infos和tags二個list所組成的list
        for infos_tags in anime_data:
            __insert_data(conn, infos=infos_tags[0], tags=infos_tags[1])

        conn.commit()

        n += 1
        print(f'第{n}頁下載完畢')

        # 當爬取10頁內容後暫停10分鐘
        if n % 10 == 0:
            time.sleep(10*60)

    # 關閉資料庫
    conn.close()


if __name__ == '__main__':
    animad_scraper()
