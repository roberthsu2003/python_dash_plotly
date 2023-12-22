--複製資料表
create table 動畫瘋訓練資料集after as table 動畫瘋訓練資料集

--搜尋指令
select * from 動畫瘋訓練資料集 order by id

select * from 動畫瘋訓練資料集 where 年份='2022'

select * from 動畫瘋訓練資料集 where 動畫名 like '%年齡限制版%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 order by id

select * from 動畫瘋訓練資料集 where 作品分類6 is not null

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 原作載體 is null or 新續作 is null order by 動畫名

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%賢者時間%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%鬼滅%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%小鳥之翼%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%GIVEN%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%ACCA%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%網球王子%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%忍者哈特利%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%叫我對大哥%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%無神世界的神明活動%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%星期一的豐滿%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%從零開始的異世界生活%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%水星的魔女%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%OVERLORD%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%打工吧，魔王大人！%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%MUV-LUV ALTERNATIVE%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%薄櫻鬼%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%MEGALOBOX%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%視覺監獄%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%WAVE!! ~來衝浪吧!!%'

select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 動畫名 like '%天地無用%'

select * from 動畫瘋訓練資料集 where 作品分類4='特攝'


--將月份轉為春、夏、秋、冬
select id, 動畫名, 年份, 月份, 原作載體, 新續作 from 動畫瘋訓練資料集 where 月份 not in ('冬番','春番','夏番','秋番')

update 動畫瘋訓練資料集 set 月份='冬番' where 月份 in ('01','02','03')

update 動畫瘋訓練資料集 set 月份='春番' where 月份 in ('04','05','06')

update 動畫瘋訓練資料集 set 月份='夏番' where 月份 in ('07','08','09')

update 動畫瘋訓練資料集 set 月份='秋番' where 月份 in ('10','11','12')


--刪除電影、舞台劇、特攝英雄、兒童向動畫
delete from 動畫瘋訓練資料集 where 動畫名='TEN·豪快者'
or 動畫名='機界戰隊全開者 VS 煌輝者 VS 前輩者'
or 動畫名='魔進戰隊煌輝者 VS 龍裝者'
or 動畫名='我的泰山爸爸'
or 動畫名='暴走哈姆醬'
or 動畫名='夏目友人帳特別上映版：喚石與可疑訪客'
or 動畫名='偶像學園 Planet!'
or 動畫名='鳴鳥不飛：烏雲密布'
or 動畫名='有貓注意！'
or 動畫名='小怪獸成長日記 第二季'
or 動畫名='垃圾總動員'
or 動畫名='寶可夢：皮卡丘與可可的冒險'
or 動畫名='築夢奇蹟'
or 動畫名='銀龍出任務'
or 動畫名='烘焙小精靈'
or 動畫名='整容液'
or 動畫名='喵的咧～貓咪戲說日本史！第五季'
or 動畫名='怪物彈珠 THE MOVIE 路西法 絕望的黎明'
or 動畫名='交錯的想念'
or 動畫名='海邊的異邦人'
or 動畫名='秘密結社 鷹之爪 -Golden Spell-'
or 動畫名='阿松～希皮波族與閃耀果實～'
or 動畫名='水豚君'
or 動畫名 like '%假面騎士%'
or 動畫名 like '%超人力霸王%'
or 動畫名 like '%戰士美少女%'
or 動畫名 like '%衝鋒戰士%'
or 動畫名 like '%舞台劇%'
or 動畫名 like '%劇場版%'
or 動畫名 like '%電影版%'
or 動畫名 like '%真人版%'
or 集數=1


--針對程式無法自動填入的標籤進行手動更正
update 動畫瘋訓練資料集 set 原作載體='漫畫改編', 新續作='續作'
where 動畫名='GIVEN 被贈與的未來 劇場版：反面的存在'
or 動畫名='GIVEN 被贈與的未來 劇場版'
or 動畫名='ACCA13 區監察課 Regards'
or 動畫名='彼得・格里爾的賢者時間 Super Extra 年齡限制版'
or 動畫名='彼得・格里爾的賢者時間 Super Extra'
or 動畫名='新網球王子 U-17 世界盃'
or 動畫名='新網球王子 冰帝 vs 立海 Game of Future'
or 動畫名='新 忍者哈特利 第六季'
or 動畫名='新 忍者哈特利 第五季'
or 動畫名='最遊記 RELOAD -ZEROIN-'
or 動畫名='烙印勇士 黃金時代篇 MEMORIAL EDITION 年齡限制版'
or 動畫名='鬼滅之刃 刀匠村篇'
or 動畫名='鬼滅之刃 遊郭篇'
or 動畫名='鬼滅之刃 無限列車篇'
or 動畫名='星期一的豐滿 第二季'
or 動畫名='排球少年！！第四季'
or 動畫名='排球少年！！第四季 Part 2'
or 動畫名='擅長捉弄人的高木同學 第三季'
or 動畫名='棒球大聯盟 2nd 第二季'
or 動畫名='路人超能 100 第三季'


update 動畫瘋訓練資料集 set 原作載體='漫畫改編', 新續作='新作'
where 動畫名='國高中一貫！！鬼滅學園物語'
or 動畫名='叫我對大哥 (WEB版)'
or 動畫名='叫我對大哥 (TV版)'
or 動畫名='彼得・格里爾的賢者時間'
or 動畫名='彼得・格里爾的賢者時間 年齡限制版'
or 動畫名='BURN THE WITCH 龍與魔女'
or 動畫名='遊戲王! SEVENS'
or 動畫名='汪汪與喵喵'
or 動畫名='房間露營'
or 動畫名='東方少年'
or 動畫名='東京 24 區'
or 動畫名='無神世界的神明活動'
or 動畫名='川尻小玉的懶散生活'
or 動畫名='藍色監獄'
or 動畫名='魔法水果籃 -前奏曲-'
or 動畫名='我們的黎明'
or 動畫名='急戰 5 秒殊死鬥'
or 動畫名='幼女社長'
or 動畫名='加油吧同期醬'
or 動畫名='夫婦以上，戀人未滿'
or 動畫名='工作細胞 Black'
or 動畫名='弩級戰隊 HXEROS'
or 動畫名='秘密內幕-女警的反擊'
or 動畫名='突然降臨的埃及神'
or 動畫名='變身成黑辣妹之後就和死黨上床了'



update 動畫瘋訓練資料集 set 原作載體='小說改編', 新續作='續作'
where 動畫名='Re：從零開始的異世界生活 第二季'
or 動畫名='Re：從零開始的異世界生活 新編集版'
or 動畫名='勇者、辭職不幹了'
or 動畫名='打工吧，魔王大人！第二季'
or 動畫名='在地下城尋求邂逅是否搞錯了什麼 第三季'
or 動畫名='在地下城尋求邂逅是否搞錯了什麼 第四季'
or 動畫名='異世界食堂 2'
or 動畫名='異世界魔王與召喚少女的奴隸魔術 Ω'
or 動畫名='轉生成女性向遊戲只有毀滅 END 的壞人大小姐 X'


update 動畫瘋訓練資料集 set 原作載體='小說改編', 新續作='新作'
where 動畫名='持續狩獵史萊姆三百年，不知不覺就練到 LV MAX'
or 動畫名='無職轉生，到了異世界就拿出真本事'
or 動畫名='被解僱的暗黑士兵（30多歲）開始了慢生活的第二人生'
or 動畫名='轉生成女性向遊戲只有毀滅 END 的壞人大小姐'


update 動畫瘋訓練資料集 set 原作載體='遊戲改編', 新續作='續作'
where 動畫名='MUV-LUV ALTERNATIVE% 第二季'
or 動畫名='暮蟬悲鳴時 業'
or 動畫名='艦隊 Collection 總有一天，在那片海'
or 動畫名='薄櫻鬼 新OVA'
or 動畫名='IDOLiSH7 - 偶像星願 - Second BEAT！'
or 動畫名='IDOLiSH7 - 偶像星願 - Third BEAT！'
or 動畫名='MUV-LUV ALTERNATIVE 第二季'


update 動畫瘋訓練資料集 set 原作載體='遊戲改編', 新續作='新作'
where 動畫名='ICHU 偶像進行曲'
or 動畫名='MUV-LUV ALTERNATIVE'
or 動畫名='白貓 Project Zero Chronicle 零之紀元'
or 動畫名='幻想三國誌 — 天元靈心記'
or 動畫名='機戰少女 Alice Expansion'
or 動畫名='機戰少女 Alice OVA'
or 動畫名='王之逆襲：意志的繼承者'


update 動畫瘋訓練資料集 set 原作載體='原創作品', 新續作='續作'
where 動畫名='荒野的壽飛行隊 完全版'
or 動畫名='天地無用！魎皇鬼 第 5 期'
or 動畫名='BUILD-DIVIDE -#FFFFFF- CODE WHITE'
or 動畫名='小鳥之翼 第二季'
or 動畫名='機動戰士鋼彈 水星的魔女 Season 2'
or 動畫名='異世界四重奏 第二季'


update 動畫瘋訓練資料集 set 原作載體='原創作品', 新續作='新作'
where 動畫名='奇米萌 CHIMIMO'
or 動畫名='DECA - DENCE'
or 動畫名='Futsal Boys！！！！！'
or 動畫名='白沙的 Aquatope'
or 動畫名='絆之 Allele'
or 動畫名='境界服務'
or 動畫名='噴嚏大魔王 2020'
or 動畫名='座敷童子塌塌米醬'
or 動畫名='淘氣貓 2020：家有圓圓？！我家的圓圓你知道嗎～'
or 動畫名='NOMAD MEGALOBOX 機甲拳擊 第二季'
or 動畫名='VISUAL PRISON 視覺監獄'
or 動畫名='WAVE!! ~來衝浪吧!!~'
or 動畫名='小鳥之翼'
or 動畫名='BUILD-DIVIDE -#000000- CODE BLACK'
or 動畫名='GIBIATE 獵魔武士'
or 動畫名='Praeter 之傷'
or 動畫名='群青的開幕曲'


update 動畫瘋訓練資料集 set 新續作='續作' where 動畫名 like '%第二季%'

update 動畫瘋訓練資料集 set 新續作='新作' where 動畫名 like '%第一季%'
