create table 動畫瘋訓練資料集after as table 動畫瘋訓練資料集

select * from 動畫瘋訓練資料集after

select * from 動畫瘋訓練資料集after where 動畫名 like '%年齡限制版'

select * from 動畫瘋訓練資料集after where 動畫名 like '彼得・格里爾的賢者時間 Super Extra%'
update 動畫瘋訓練資料集after set 總觀看數=(402000 + 167000), 平均觀看數=(33500 + 13917) where 動畫名='彼得・格里爾的賢者時間 Super Extra 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類3='18禁' where 動畫名='彼得・格里爾的賢者時間 Super Extra 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='彼得・格里爾的賢者時間 Super Extra'

select * from 動畫瘋訓練資料集after where 動畫名 like '彼得・格里爾的賢者時間%'
update 動畫瘋訓練資料集after set 總觀看數=(550000 + 789000), 平均觀看數=(45833 + 65750) where 動畫名='彼得・格里爾的賢者時間 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類3='18禁' where 動畫名='彼得・格里爾的賢者時間 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='彼得・格里爾的賢者時間'

select * from 動畫瘋訓練資料集after where 動畫名 like '土下座跪求給看%'
update 動畫瘋訓練資料集after set 總觀看數=(820000 + 214000), 平均觀看數=(63077 + 16462) where 動畫名='土下座跪求給看 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類4='18禁' where 動畫名='土下座跪求給看 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='土下座跪求給看'

select * from 動畫瘋訓練資料集after where 動畫名 like '女神宿舍的管理員%'
update 動畫瘋訓練資料集after set 總觀看數=(679000 + 448000), 平均觀看數=(67900 + 44800) where 動畫名='女神宿舍的管理員。 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類4='18禁' where 動畫名='女神宿舍的管理員。 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='女神宿舍的管理員。'

select * from 動畫瘋訓練資料集after where 動畫名 like '無意間變成狗，被喜歡的女生撿回家。%'
update 動畫瘋訓練資料集after set 總觀看數=(476000 + 481000), 平均觀看數=(34000 + 34357) where 動畫名='無意間變成狗，被喜歡的女生撿回家。 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類2='18禁' where 動畫名='無意間變成狗，被喜歡的女生撿回家。 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='無意間變成狗，被喜歡的女生撿回家。'

select * from 動畫瘋訓練資料集after where 動畫名 like '異種族風俗娘評鑑指南%'
update 動畫瘋訓練資料集after set 總觀看數=(1244000 + 1834000), 平均觀看數=(103667 + 152833) where 動畫名='異種族風俗娘評鑑指南 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類4='18禁' where 動畫名='異種族風俗娘評鑑指南 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='異種族風俗娘評鑑指南'

select * from 動畫瘋訓練資料集after where 動畫名 like '終末的後宮%'
update 動畫瘋訓練資料集after set 總觀看數=(283000 + 731000), 平均觀看數=(25727 + 66455) where 動畫名='終末的後宮 年齡限制版'
update 動畫瘋訓練資料集after set 作品分類2='18禁' where 動畫名='終末的後宮 年齡限制版'
delete from 動畫瘋訓練資料集after where 動畫名='終末的後宮'

select * from 動畫瘋訓練資料集after where 原作載體='改編作品'
update 動畫瘋訓練資料集after set 原作載體='原創作品' where 動畫名 like '闇芝居%'
update 動畫瘋訓練資料集after set 原作載體='小說改編' where 動畫名='〈Infinite Dendrogram〉-無盡連鎖-'
update 動畫瘋訓練資料集after set 原作載體='漫畫改編' where 動畫名='壽司大相撲'
update 動畫瘋訓練資料集after set 原作載體='原創作品' where 動畫名='月歌。THE ANIMATION 2'

select * from 動畫瘋訓練資料集after where 動畫名 like '烙印勇士 黃金時代篇%'
update 動畫瘋訓練資料集after set 作品分類6='18禁' where 動畫名='烙印勇士 黃金時代篇 MEMORIAL EDITION 年齡限制版'
--刪掉不需要的資料
alter table 動畫瘋訓練資料集after drop column id
alter table 動畫瘋訓練資料集after drop column 台灣代理

alter table 動畫瘋訓練資料集after add constraint PK_動畫瘋訓練資料集after primary key(動畫名)

