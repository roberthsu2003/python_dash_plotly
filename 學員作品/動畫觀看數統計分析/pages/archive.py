import dash
from dash import html, dash_table, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

dash.register_page(__name__, title='動畫觀看數統計')

df = pd.read_csv('web_csv/BaHaMut_9.csv')
layout = html.Div(
    [
        html.Div([
            html.Div([
                dash_table.DataTable(
                    id='main_table',
                    data=df.to_dict('records'),
                    columns=[{'id': column, 'name': column}
                             for column in df.columns],
                    sort_action='native',  # 启用原生排序功能
                    sort_mode='multi',
                    style_table={'overflowY': 'auto',
                                 'height': '500px',},
                    style_cell={'whiteSpace': 'normal',
                                'textAlign': 'center'},
                    style_cell_conditional=[
                        {'if': {'column_id': '動畫名'}, 'width': '190px'}, {'if': {'column_id': '年份'}, 'width': '75px'}, {'if': {'column_id': '月份'}, 'width': '75px'}, {'if': {'column_id': '集數'}, 'width': '75px'}, {'if': {'column_id': '星級'}, 'width': '70px'}, {'if': {'column_id': '評分人數'}, 'width': '70px'}, {'if': {'column_id': '導演監督'}, 'width': '70px'}, {'if': {'column_id': '製作廠商'}, 'width': '85px'}, {'if': {'column_id': '作品分類1'}, 'width': '50px'}, {'if': {'column_id': '作品分類2'}, 'width': '50px'}, {'if': {'column_id': '作品分類3'}, 'width': '50px'}, {'if': {'column_id': '作品分類4'}, 'width': '50px'}, {'if': {'column_id': '作品分類5'}, 'width': '50px'}, {'if': {'column_id': '作品分類6'}, 'width': '50px'}, {'if': {'column_id': '原作載體'}, 'width': '50px'}, {'if': {'column_id': '新續作'}, 'width': '50px'}, {'if': {'column_id': '平均觀看數(萬)'}, 'width': '70px'}, {'if': {'column_id': '總觀看數(萬)'}, 'width': '70px'}],
                    page_size=8,
                    fixed_rows={'headers': True},
                    row_selectable="single",
                    selected_rows=[]
                ),
            ], className="main")
        ],
            className="main-row",
            style={"paddingTop": '5rem',
                   "marginBottom":"2rem"}),
        html.Div([html.H2('熱門作品 (≧∇≦)b')],className='subtitle'),
        html.Div([
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/jujutsu.png')], className='itemimage'), html.A([html.Span(['咒術迴戰'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=18626", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/ssss.png')], className='itemimage'), html.A([html.Span(['SPY×FAMILY 間諜家家酒'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=28798", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/attack.png')], className='itemimage'), html.A([html.Span(['進擊的巨人 The Final Season'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=19849", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/suraimu.png')], className='itemimage'), html.A([html.Span(['關於我轉生變成史萊姆這檔事 第二季'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=20530", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/musyoku.png')], className='itemimage'), html.A([html.Span(['無職轉生，到了異世界就拿出真本事'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=20620", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/re0.png')], className='itemimage'), html.A([html.Span(['Re：從零開始的異世界生活 第二季'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=16344", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/86.png')], className='itemimage'), html.A([html.Span(['86－不存在的戰區－'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=22245", target="_blank")
                          ], className='itemsize')
            ], className='card'), html.Div([
                html.Div([html.Div([html.Img(src='assets/images/kimetsu.png')], className='itemimage'), html.A([html.Span(['鬼滅之刃 遊郭篇'], className='imagetitle')], className='imageurl', href="https://ani.gamer.com.tw/animeVideo.php?sn=26850", target="_blank")
                          ], className='itemsize')
            ], className='card')
        ], className='action'),
        html.Div([html.H2('一月新番 ლ(´ڡ`ლ)')],className='subtitle2'),
        html.Div([
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/jitsuryokuS3.png')], className='itemimage'), html.A([html.Span(['歡迎來到實力至上主義的教室 第三季'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=133633", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/danjyonhan.png')], className='itemimage'), html.A([html.Span(['迷宮飯'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=126313", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/sureibu.png')], className='itemimage'), html.A([html.Span(['魔都精兵的奴隸'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=120671", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/sasaki.png')], className='itemimage'), html.A([html.Span(['佐佐木與文鳥小嗶'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=134321", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/yubisaki.png')], className='itemimage'), html.A([html.Span(['指尖相觸，戀戀不捨'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=133896", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/kingdom.png')], className='itemimage'), html.A([html.Span(['王者天下 第五季'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=134333", target="_blank")
                          ], className='itemsize')
            ], className='card'),
            html.Div([
                html.Div([html.Div([html.Img(src='assets/images/dangers.png')], className='itemimage'), html.A([html.Span(['我內心的糟糕念頭 第二季'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=133422", target="_blank")
                          ], className='itemsize')
            ], className='card'), html.Div([
                html.Div([html.Div([html.Img(src='assets/images/mofumofu.png')], className='itemimage'), html.A([html.Span(['為了在異世界也能摸摸毛茸茸努力'], className='imagetitle')], className='imageurl', href="https://acg.gamer.com.tw/acgDetail.php?s=129541", target="_blank")
                          ], className='itemsize')
            ], className='card')
        ], className='action2'),

        dbc.Modal(
            [],
            id="modal",
            className='modalsize',
            is_open=False,
            size='lg',
        )


    ],
    className="mycontainer"
)


@callback(
    Output("modal", "children"),
    Output("modal", "is_open"),
    Input('main_table', 'selected_rows')
)
def selectedRow(selected_rows):
    if len(selected_rows) != 0:
        oneSite: pd.DataFrame = df.iloc[[selected_rows[0]]],
        oneSite = oneSite[0]
        if df.iloc[selected_rows[0]][0] == '關於我轉生變成史萊姆這檔事 第二季':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/suraimu2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=20530", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['三上悟過著不起眼的人生，在隨機殺人魔肆虐下結束了三十七年生涯…… 看似如此。當他甦醒時，不僅眼睛看不見，就連耳朵也聽不到…… 面對一連串突發狀況，他意識到自己投胎轉世成「史萊姆」！儘管變成最弱魔物讓他頗有怨言，三上悟還是決定要快樂地過史萊姆生活，沒想到卻碰上天災級魔物「暴風龍維爾德拉」，命運就此出現巨大轉折──維爾德拉將他命名為「利姆路」，正要展開史萊姆式的異世界新生活時，卻被捲入哥布靈對牙狼族的紛爭之中，最後還莫名其妙當上魔物大王…… 能奪取對手能力的「捕食者」以及精通世界真理的「大賢者」，有這兩項特殊技能當武器，最強的史萊姆傳說正式展開！'], style={'marginTop': '25px'}, className='infotext')], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '咒術迴戰':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/jujutsu2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=18626", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                                                                                                                                                                                                        html.H3(['虎杖悠仁是一位體育萬能的高中生，某天他為了從「咒物」危機中解救學長姊，而吞下了詛咒的手指，讓「宿儺」這種詛咒跟自己合而為一。之後他加入了專門培養咒術師的學校「咒術高專」，並遇到了伏黑惠與釘崎野薔薇這兩位同學。某日，突然出現「特級咒物」，他們三人就奉命到現場支援。為了實現爺爺要他「助人」的遺言，虎杖將會繼續與「詛咒」奮鬥下去。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == 'SPY×FAMILY 間諜家家酒':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/ssss2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=28798", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['每一個人都擁有不想讓任何人看見得自己的一面―― 位在世界各國於檯面下進行激烈情報戰的時代。東國與西國已經維持了數十年的冷戰狀態。所屬西國情報局對東課 <WISE> 厲害的間諜〈黃昏〉，為了前往找尋被譽為是會威脅到東西國和平的危險人物，東國的國家統一黨總裁 唐納文・戴斯蒙德 所正在籌備的戰爭計畫，被賦予了一項極秘任務。其名稱為 Operation〈梟〉。內容講述「在一週內組建家庭，並潛入戴斯蒙德兒子所就讀的學校吧」。但是，他所遇到的「女兒」是會讀心的超能力者、「妻子」則是暗殺者！為了互相的利益而成為家庭，決定在隱藏真實身分的情況下共同生活的 3 人。世界的和平就託付即將發生一系列事件的暫定的家庭…？'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '進擊的巨人 The Final Season':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/attack2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=19849", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['《進擊的巨人》的故事描述百年前世界莫名出現神秘的巨人怪物，不斷殘忍食人，人類幾乎無法與之對抗，最後人類建造了三道寬 3 公尺、高 50 公尺的高聳圍牆，百年來未有巨人攻破，人們漸漸習慣牆內的生活，麻木於和平，害怕冒險與改變，直到 845 年，最外層的瑪利亞之牆，被身高超過 60m 的超大型巨人，踢破城牆，無數巨人湧入城鎮，親眼見到母親被巨人一口咬碎的慘劇的艾連，發誓要消滅所有巨人。最後一季的劇情，主要是在描述艾倫一行人在發現了牆外不只有巨人，更有另一個發達許多的國家「瑪雷」後，將正式與人類開戰。故事時間軸將跳到了巨人 13 年任期將滿的五至六年後，新的瑪雷戰士不只已開始選拔，帕拉迪島上的艾倫更因為擁有始祖巨人，即將和世界各國展開前所未有的戰爭。'], style={'marginTop': '25px'}, className='infotext')], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '無職轉生，到了異世界就拿出真本事':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/musyoku2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=20620", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['《無職轉生 ~到了異世界就拿出真本事~》是在小說投稿網站「小説家になろう」進行發表，累積人氣獲得第一名的冒險奇幻小說。故事描述著被趕出家門的 34 歲的無職處男的尼特族，因遭遇車禍而失去生命。在保有前世記憶的狀況下，轉生到了異世界。在這個劍與魔法的世界獲得第二次人生的他，反省自己的過去，並決定這次一定要認真地過活。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == 'Re：從零開始的異世界生活 第二季':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/re02.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=16344", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['我一定會救你的。菜月昴擊敗了魔女教的主教-貝特魯吉烏斯·羅曼尼康帝的“懶惰”，並重新開始了在愛蜜莉雅的職業生涯。兩人在克服艱難的告別後終於安定下來，但這是新動蕩的開始。前所未有的絕望危機，無情的現實在襲擊。這個男孩再次面臨著可怕的命運。從王都帶著避難村民歸還的昴與愛蜜莉雅，與女僕法蘭黛莉卡會談後決定前往「聖域」一探究竟。然而愛蜜莉雅卻在踏入聖域的瞬間昏迷，醒來後更被告知已無法離開聖域。被迫進行「試煉」的愛蜜莉雅與意外獲得「試煉」資格的昴面對陸續降臨的危機。昴必須在困境中找出正確選擇，拯救被束縛在禁書庫中四百年的精靈，締結永遠的契約。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '86－不存在的戰區－':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/862.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=22245", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['聖瑪格諾利亞共和國為了應對鄰國的無人機「Legion」侵略，成功研發出同型武器，不再需要靠著人命堆疊的戰爭終於來臨。是的──表面上確實如此。然而，位於共和國全八十五個行政區之外的「不存在的第 86 區」中，一群少年少女正以「有人駕駛的無人機」之姿，日夜奮戰不懈。率領一群年輕人出生入死的少年──辛，與身處遙遠後方，透過特殊通訊指揮他們作戰的「指揮管制官」少女──蕾娜。兩人壯烈而悲傷的戰鬥與離別的故事，就此揭開序幕──！'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '鬼滅之刃 遊郭篇':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/kimetsu2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=26850", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['日本大正時代，名叫竈門炭治郎的平凡農村少年，靠著賣炭來維持一家的生計。某天他下山去賣炭，回家時天色已暗，好心的三郎爺爺便留他住了一晚。隔天他回到家卻發現家人全都遭到殘殺，只剩禰豆子身體還有餘溫，然而她似乎變得跟平常不太一樣？為了尋求拯救妹妹的方法，炭治郎踏上了斬鬼的冒險旅程。而炭治郎等人在結束無限列車的任務後迎來了下個任務。跟隨著鬼殺隊最頂尖劍士《柱》的其中一人音柱・宇髓天元，炭治郎等人來到鬼棲息的遊郭。新的戰鬥就此揭開序幕！'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '輝夜姬想讓人告白～天才們的戀愛頭腦戰～ 第二季':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/kaguya2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=15298", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['在備受期待的菁英就讀的秀知院學園，在學生會裡相遇的副會長·四宮輝夜與會長白銀御行對彼此都有好感，但兩人的自尊心都不允許自己就這樣向對方告白，就在這樣的情況下僵持了半年——完全不夠坦率的兩人，認為自己只要先告白就輸了，每天想的都是「設法讓對方先告白」。就這樣直到今天，輝夜與白銀使盡渾身解數的戀愛頭腦戰仍在持續著。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '機動戰士鋼彈 水星的魔女 Season 2':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/suisei2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=33292", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['在星元122年——眾多企業擴展到宇宙並構築巨大經濟圈的時代有一名少女．蘇蕾塔，自邊境地區「水星」，轉來至MS產業的最大企業「貝納里特集團」旗下所經營的「阿斯提卡西亞高等專門學園」。作為米奧琳涅的未婚夫、作為鋼彈公司的一員，度過了充滿相遇和刺激的學園生活。從恐怖攻擊事件過去了兩個星期，蘇萊塔在學校期待與米奧琳涅的重逢，每天過著充實的生活；另一方面，米奧琳涅留在貝納里特集團總部，守護著父親的狀況。種種的新困難向兩人襲來，讓她們不得不做出抉擇。少女們將懷著各自的情感，面對鋼彈帶來的強大詛咒。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '叫我對大哥 (TV版)':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/ore2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=23349", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['以 おぷうのきょうだい所著漫畫為原著改編的動畫《老子是、津島（暫譯，俺、つしま）》，描述一位實際上是老婆婆、卻被稱為「老爺爺」（田中真弓配音演出）的老人，與眾多貓咪日常的漫畫，並以某天忽然出現在老爺爺家庭院的一隻貓「津島（大塚明夫配音演出）」為中心。預定將推出的動畫作品由 青木純執導，動畫公司則交由曾推出有《劇場版 角落小夥伴 繪本中的秘密》的 Fanworks 與 SPACE NEKO COMPANY 聯手製作。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '汪汪與喵喵':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/dogcat2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=29892", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['《汪汪與喵喵》是漫畫作家-松本英吉老師創作之作品這部動畫小品就由汪汪跟喵喵，兩隻都想養的貪心主人的故事來說起。故事圍繞在瘋狂向主人撒嬌超可愛的汪汪與雖然看起來很兇但又無法討厭牠的喵喵只要和他們在一起每天都超開心的日常生活。那你是貓派還是狗派呢？'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == '鬼滅之刃 刀匠村篇':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/kimetsuSwordsmithVillage2.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=33295", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['自從上弦之陸·墮姬和妓夫太郎被斬殺後導致上弦的位置出現空缺的緣故，因此猗窩座和其他上弦成員都被無慘召喚到無限城內，無慘面對上弦出現空缺的問題感到震怒並且覺得上弦成員應該要盡心極力地找出「藍色彼岸花」與殲滅鬼殺隊的職責，於是他指派上弦之肆·半天狗和上弦之伍·玉壺前往某個地點去執行任務。另一方面，在蝴蝶屋療傷長達兩個月的炭治郎得知鋼鐵塜不再給自己一把新刀的消息，因此他在蝴蝶屋的寺內清、中原澄與高田菜穗的建議下前往刀匠村再次請求鋼鐵塜幫忙打造新刀，當炭治郎抵達遇刀匠村遇到戀柱·甘露寺蜜璃和霞柱·時透無一郎以及不死川玄彌。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        elif df.iloc[selected_rows[0]][0] == 'IDOLiSH7 - 偶像星願 - Third BEAT！':
            info = html.Div([html.Div(html.A([html.Img(src='assets/images/IDOLiSH72.png')], href="https://ani.gamer.com.tw/animeVideo.php?sn=23368", target="_blank"), className='infoimage'), html.Div([html.H1([df.iloc[selected_rows[0]][0]], style={'color': 'rgba(255, 208, 0, 0.89'}), html.H3([f'監督：{df.iloc[selected_rows[0]][6]}'], style={'color': 'rgba(0, 238, 255, 0.842', 'marginTop': '25px'}), html.H3([f'製作公司：{df.iloc[selected_rows[0]][7]}'], style={'color': 'rgba(0, 238, 255, 0.842'}),
                             html.H3(['改編自由 BANDAI NAMCO Online 發行、並由漫畫家 種村有菜人擔任人物原案設定的手機遊戲，電視動畫《IDOLiSH7 - 偶像星願 -》描繪 7 位充滿個性的偶像，共組團體「IDOLiSH7」後在舞台上與同為偶像團體的「TRIGGER」等人競爭、逐漸成長的軌跡。'], style={'marginTop': '25px'})], style={'padding': '15px'})], className='info')
        else:
            info = dbc.ModalHeader(dbc.ModalTitle(
                "尚未更新資料"), class_name='infotitle')
        return info, True
    return None, False

selected_row = None
page_current = 0