import dash_mantine_components as dmc
from dash import Dash, _dash_renderer
from dash import html, Output, Input, callback
import pandas as pd
from dash_iconify import DashIconify
import os
_dash_renderer._set_react_version("18.2.0")

app = Dash(external_stylesheets=dmc.styles.ALL)

data = [["4", "簡介"],["1", "工單查詢"], ["2", "工廠工站查詢"], ["3", "員工編號查詢"],]

df = pd.read_csv('整合後檔案.csv')
df2 = pd.read_csv('Factoryworkstation.csv')
df3 = pd.read_csv('virtual_data_with_permissions.csv')
selected_data_1 = [{'value':value,'label':value} for value in df.Date.unique()]
selected_data_2 = [{'value': value, 'label': value} for value in df2.Plant.unique()]
selected_data_3 = [{'value': value, 'label': value} for value in df3.ID.unique()]

app.layout = dmc.MantineProvider(

 dmc.AppShell(
    [
        dmc.AppShellHeader(
                dmc.NavLink(
                    label="職能發展學院",
                    leftSection=DashIconify(icon="tabler:gauge"),
                    active=True,
                    variant="filled",
                    color="orange",
                    id="school_icon",
                    h=70,
                    href='/',
                    refresh=True                                    
                ),
                h=70         
        
            ),
        dmc.AppShellMain(
            children=[ dmc.Container(        
                    dmc.Title(f"風扇良率判定及相關資料查詢系統", order=2),
                    fluid=True,
                    ta='center',
                    my=30  
                ),
                dmc.Flex(
                         [
            html.Div(
                        [#選單欄位
                            dmc.RadioGroup(
                                children=dmc.Group([dmc.Radio(l, value=k) for k, l in data], my=10),
                                id="radiogroup-simple",
                                value="4",
                                label="請選擇模式",
                                size="md",
                                mb=10,
                                style={
                                                "width": 500,
                                                "margin": "0 auto",  # 居中對齊
                                }

                            ),        
                                dmc.Select(
                                    label="請選擇",
                                    placeholder="請選擇1個",
                                    id="dropdown-selection",
                                    value="",
                                    data=selected_data_1,
                                    w=200,
                                    mb=10,
                                ),
                                
                            
                        ]
                    ),
                        dmc.Box([
                                        dmc.Text(
                                            id="radio-output",
                                            style={
                                                "width": 700,
                                                "maxWidth": "1000px",
                                                "margin": "0 auto",  # 居中對齊
                                            },
                                        )
                                    ],
                                    style={"padding": "20px"},  # 外框填充
                                ),

                          ],
                                                        

                                            )
        ]),
    ],
    header={"height": 70},
    padding="xl",    
    style={}

)
)


@callback(
    Output("dropdown-selection", "data"),
    Input("radiogroup-simple", "value"),
)
def update_dropdown(radio_value):
    # **紅色修改部分：根據 Radio 值返回不同選單內容**
    if radio_value == "1":
        return [{'value': value, 'label': value} for value in df.Date.unique()]
    elif radio_value == "2":
        return [{'value': value, 'label': value} for value in df2.Plant.unique()]
    elif radio_value == "3":
        return [{'value': value, 'label': value} for value in df3.ID.unique()]





@callback(

        Output("radio-output", "children"), 
        Input("radiogroup-simple", "value"),
        Input("dropdown-selection", "value"))
def choose_framework(R_value,D_Value):
    if R_value == "1":
        dff = df[df.Date == D_Value]
        diff = dff[['Date','OrderID','Product','Prediction','Confidence']]
        diff['Confidence'] = diff['Confidence'].apply(lambda x: f"{x:.3f}")
        elements = diff.to_dict('records')
        rows = [
        dmc.TableTr(
            [   dmc.TableTd(element["Date"]),
                dmc.TableTd(element["OrderID"]),
                dmc.TableTd(element["Product"]),
                dmc.TableTd(element["Prediction"]),
                dmc.TableTd(element["Confidence"]),
            ]
        )
        for element in elements
        ]

        head = dmc.TableThead(
            dmc.TableTr(
                [   dmc.TableTh("日期"),
                    dmc.TableTh("工單號碼"),
                    dmc.TableTh("產品料號"),
                    dmc.TableTh("判定結果"),
                    dmc.TableTh("評估指數"),
                ]
            )
        )
        body = dmc.TableTbody(rows)
        caption = dmc.TableCaption("工單詳細清單")


        return dmc.LineChart(
    h=300,
    dataKey="date",
    data=elements,
    series = [
        {"name": "Confidence", "color": "blue.6"},
    ],
    curveType="linear",
    tickLine="xy",
    withXAxis=False,
    withDots=False,
),dmc.Table([head, body, caption])
    

    elif R_value == "2":
        dff2 = df2[df2.Plant == D_Value]
        diff2 = dff2[['Plant','Workstation Code',"Code",'Step Name (English)','Step Name (Chinese)']]
        elements = diff2.to_dict(orient='records')
        rows = [
        dmc.TableTr(
            [
                dmc.TableTd(element["Plant"]),
                dmc.TableTd(element["Workstation Code"]),
                dmc.TableTd(element["Code"]),
                dmc.TableTd(element["Step Name (English)"]),
                dmc.TableTd(element["Step Name (Chinese)"]),
            ]
        )
        for element in elements
        ]

        head = dmc.TableThead(
            dmc.TableTr(
                [
                    dmc.TableTh("廠區"),
                    dmc.TableTh("車間"),
                    dmc.TableTh("工站名稱"),
                    dmc.TableTh("工站完整名稱(英文)"),
                    dmc.TableTh("工站完整名稱(中文)"),
                ]
            )
        )
        body = dmc.TableTbody(rows)
        caption = dmc.TableCaption("廠區工站查詢")
        return dmc.Table([head, body, caption])
    elif R_value == "3":
        dff3 = df3[df3.ID == D_Value]
        diff3 = dff3[['ID','姓名','權限代號']]
        elements = diff3.to_dict(orient='records')
        rows = [
        dmc.TableTr(
            [
                dmc.TableTd(element["ID"]),
                dmc.TableTd(element["姓名"]),
                dmc.TableTd(element["權限代號"]),
            ]
        )
        for element in elements
        ]

        head = dmc.TableThead(
            dmc.TableTr(
                [
                    dmc.TableTh("ID"),
                    dmc.TableTh("姓名"),
                    dmc.TableTh("權限代號"),
                ]
            )
        )
        body = dmc.TableTbody(rows)
        caption = dmc.TableCaption("員工查詢")
        return dmc.Table([head, body, caption])
    if R_value == "4":

        return                     dmc.Text(
                        [
                            dmc.Mark("這是一個基於 'Dash' 和 'Mantine Components' 的前端應用程式，用於實現風扇良率判定及相關資料查詢系統。"),                            
                            dmc.Space(h=20),
                            dmc.Text("功能簡介", fw=900,size="xl"),
                            dmc.Text('1.多模式選擇查詢', fw=700),
                            dmc.Text('系統提供三種主要查詢模式：'),
                            dmc.Text('工單查詢：按日期檢索工單資訊，包括產品料號、判定結果及評估指數。'),
                            dmc.Text('工廠工站查詢：按廠區檢索工站資訊，包括工站代碼、步驟名稱（中英對照）。'),
                            dmc.Text('員工編號查詢：根據員工 ID 檢索個人姓名及權限代號。'),
                            dmc.Space(h=20),
                            dmc.Text('2.數據視覺化', fw=700),
                            dmc.Text('使用 Mantine 提供的 UI 組件來展示資料表格，讓查詢結果清晰直觀。'),
                            dmc.Text('工單查詢模式下，提供 Confidence 值的折線圖視覺化，幫助快速判定關鍵指標。'),
                            dmc.Space(h=20),
                            dmc.Text('3.高效資料篩選與互動', fw=700),
                            dmc.Text('依據用戶選擇的查詢模式動態更新選單，僅顯示相關的篩選條件。'),
                            dmc.Text('互動式選單與顯示區域無縫結合，點擊或選擇後即可即時更新查詢結果。'),
                            dmc.Space(h=20),
                            dmc.Text('4.介面友好', fw=700),
                            dmc.Text('使用 Mantine 的AppShell組件實現統一的頁面佈局：'),
                            dmc.Text('頂部導航欄標註應用名稱，方便用戶快速返回首頁。'),
                            dmc.Text('中心化設計讓主要功能模組居中顯示，提高用戶體驗。'),
                            dmc.Text('支援多語言顯示（如中文與英文的工站名稱）。'),
                            dmc.Space(h=20),
                            dmc.Text('技術特點', fw=900,size="xl"),
                            dmc.Text('前端技術', fw=700),
                            dmc.Text('應用使用 Dash 和 Dash Mantine Components 框架構建，確保靈活的頁面組件及優異的樣式支援。'),
                            dmc.Space(h=20),
                            dmc.Text('數據處理', fw=700),
                            dmc.Text('從 CSV 文件載入多組數據，基於 pandas 高效過濾與處理。'),
                            dmc.Text('將處理後的資料轉換為字典和表格結構，用於視覺化展示。'),
                            dmc.Space(h=20),
                            dmc.Text('響應式設計', fw=700),
                            dmc.Text('基於用戶選擇的模式，系統自動切換相關的選項與結果。'),
                            dmc.Text('使用回調函數實現多組件間的動態交互。'),
                            dmc.Space(h=20),
                            dmc.Text('適用場景', fw=900,size="xl"),
                            dmc.Text('製造業中，用於查詢生產工單、工廠工站資料以及員工相關資訊。'),
                            dmc.Text('提供良率分析及數據支持，幫助用戶快速做出決策。'),
                            dmc.Text('適合需要高效數據篩選和視覺化的業務場景。'),
                            dmc.Space(h=20),
                            dmc.Text('組員:廖庭鋒,林采橘,郭子睿(哈哈哥)'),
                              
                            
                        ]
                    )

if __name__ == "__main__":
    #使用 Render 提供的埠號，若不存在則預設為 8050
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=True, host="0.0.0.0", port=port)
        # app.run(debug=True)