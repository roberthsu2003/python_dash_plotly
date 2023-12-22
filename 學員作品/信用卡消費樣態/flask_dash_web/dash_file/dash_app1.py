from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data
import plotly.express as px

dash1 = Dash(
    requests_pathname_prefix="/dash/app1/", external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash1.title = "信用卡消費樣態"
lastest_data = data.search_data(dataName="年齡層",tableName="age")


lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "年齡層", "信用卡交易筆數", "信用卡交易金額"]
)


dash1.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("各年齡層信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        dbc.DropdownMenu(
                            label="資料類別",
                            children=[
                                dbc.DropdownMenuItem(
                                    "首頁", href="/dash/index/",external_link=True
                                ),

                                dbc.DropdownMenuItem(
                                    "教育程度", href="/dash/app/", external_link=True
                                ),

                                dbc.DropdownMenuItem(
                                    "職業類別", href="/dash/app2/", external_link=True
                                ),

                                dbc.DropdownMenuItem(
                                    "性別", href="/dash/app3/", external_link=True
                                ),

                                dbc.DropdownMenuItem(
                                    "年收入", href="/dash/app4/", external_link=True
                                ),
                            ],
                            color="secondary",
                            style={"marginRight": "1rem"},
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("月份"),
                                dbc.Select(
                                    id="month",
                                    value="ALL",
                                    options=[
                                        {"label": "1月", "value": "1"},
                                        {"label": "2月", "value": "2"},
                                        {"label": "3月", "value": "3"},
                                        {"label": "4月", "value": "4"},
                                        {"label": "5月", "value": "5"},
                                        {"label": "6月", "value": "6"},
                                        {"label": "7月", "value": "7"},
                                        {"label": "8月", "value": "8"},
                                        {"label": "9月", "value": "9"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                    style={"marginRight": "1rem"},
                                ),
                            ],
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("地區"),
                                dbc.Select(
                                    id="area",
                                    value="ALL",
                                    options=[
                                        {"label": "臺北市", "value": "臺北市"},
                                        {"label": "新北市", "value": "新北市"},
                                        {"label": "桃園市", "value": "桃園市"},
                                        {"label": "臺中市", "value": "臺中市"},
                                        {"label": "臺南市", "value": "臺南市"},
                                        {"label": "高雄市", "value": "高雄市"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                    style={"marginRight": "1rem"},
                                ),
                            ],
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("產業別"),
                                dbc.Select(
                                    id="industry",
                                    value="ALL",
                                    options=[
                                        {"label": "食", "value": "食"},
                                        {"label": "衣", "value": "衣"},
                                        {"label": "住", "value": "住"},
                                        {"label": "行", "value": "行"},
                                        {"label": "文教康樂", "value": "文教康樂"},
                                        {"label": "百貨", "value": "百貨"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                    style={"marginRight": "1rem"},
                                ),
                            ],
                        ),
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("年齡層"),
                                dbc.Select(
                                    id="age",
                                    value="ALL",
                                    options=[
                                        {"label": "未滿20歲", "value": "未滿20歲"},
                                        {"label": "20(含)-25歲", "value": "20(含)-25歲"},
                                        {"label": "25(含)-30歲", "value": "25(含)-30歲"},
                                        {"label": "30(含)-35歲", "value": "30(含)-35歲"},
                                        {"label": "35(含)-40歲", "value": "35(含)-40歲"},
                                        {"label": "40(含)-45歲", "value": "40(含)-45歲"},
                                        {"label": "45(含)-50歲", "value": "45(含)-50歲"},
                                        {"label": "50(含)-55歲", "value": "50(含)-55歲"},
                                        {"label": "55(含)-60歲", "value": "55(含)-60歲"},
                                        {"label": "60(含)-65歲", "value": "60(含)-65歲"},
                                        {"label": "70(含)-75歲", "value": "70(含)-75歲"},
                                        {"label": "75(含)-80歲", "value": "75(含)-80歲"},
                                        {"label": "80(含)歲以上", "value": "80(含)歲以上"},
                                        {"label": "ALL", "value": "ALL"},
                                    ],
                                ),
                            ],
                        )
                    ],
                    className="d-flex justify-content-center",
                    style={"paddingTop": "2rem"},
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dash_table.DataTable(
                                    id="data",
                                    data=lastest_df.to_dict("records"),
                                    columns=[
                                        {"id": column, "name": column}
                                        for column in lastest_df.columns
                                    ],
                                    page_size=20,
                                    fixed_rows={"headers": True},
                                    style_table={
                                        "height": "300px",
                                        "overflowY": "auto",
                                    },
                                    style_cell={
                                        "text_align": "center",
                                    },
                                ),
                            ],
                            className="col text-center",
                        )
                    ],
                    className="row",
                    style={"paddingTop": "2rem"},
                ),
                html.Div([
                    html.Div(
                        [
                            dcc.Graph(id="graph", style={'flex': '5'}),
                            dcc.Graph(id="graph_sunburst", style={'flex': '5'}),
                        ], style={'display': 'flex', 'flexWrap': 'wrap', "paddingTop": "2rem"}),
                        dcc.Graph(id="graph_line"),
                        dcc.Graph(id="graph_bar"),
                    ],
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.P("來源："),
                                html.P("Data： 聯合信用卡處理中心Open API"),
                                html.P("Icon： Image by toffeomurice from Pixabay"),
                            ],
                            className="col",
                        )
                    ],
                    className="row",
                    style={
                        "paddingTop": "2rem",
                        "fontSize": "0.8rem",
                        "lineHeight": "0.3rem",
                    },
                ),
            ]
        )
    ],
    className="container-lg",
)


@dash1.callback(
    Output("data", "data"),
    [Input("area", "value"), Input("month", "value"), Input("industry", "value"), Input("age", "value")],
)
def update_table(selected_area, selected_month, selected_industry, selected_age):
    filtered_data = [
        row
        for row in lastest_data
        if (selected_area == "ALL" or row[2] == selected_area)
        and (selected_month == "ALL" or str(row[1]) == selected_month)
        and (selected_industry == "ALL" or row[3] == selected_industry)
        and (selected_age == "ALL" or row[4] == selected_age)
    ]

    update_df = pd.DataFrame(
        filtered_data, columns=["年", "月", "地區", "產業別", "年齡層", "信用卡交易筆數", "信用卡交易金額"]
    )
    return update_df.to_dict("records")

@dash1.callback(
    Output("graph", "figure"),
    [Input("industry","value"),Input("age","value")]
)
def update_pie_chart(selected_value, selected_age_value):
    global lastest_df
    if selected_value == "ALL":
        industry_sum = lastest_df.groupby('產業別')['信用卡交易金額'].sum().reset_index()
        fig = px.pie(industry_sum, values='信用卡交易金額', names='產業別', title='各產業別信用卡交易金額分布', height=500)
    else:
        if selected_age_value != "ALL":
            filtered_df = lastest_df[lastest_df['產業別'] == f'{selected_value}']
            fig = px.pie(filtered_df, values='信用卡交易金額', names='年齡層',title=f'{selected_value} / {selected_age_value} 信用卡交易金額占比', height=500)
            highlight_age = selected_age_value
            fig.update_traces(
                marker=dict(colors=['rgba(1,87,155,0.2)' if age != highlight_age else '' for age in fig.data[0]['labels']]),
            )
        else:
            filtered_df = lastest_df[lastest_df['產業別'] == f'{selected_value}']
            fig = px.pie(filtered_df, values='信用卡交易金額', names='年齡層', title=f'{selected_value} / 各年齡層信用卡交易金額分布', height=500)
    return fig
    
@dash1.callback(
    Output("graph_line", "figure"),
    Input("age","value")
)
def update_line_chart(selected_age):
    global lastest_df
    if selected_age == "ALL":
        monthly_total = lastest_df.groupby(['年', '月', '年齡層'])['信用卡交易金額'].sum().reset_index()
        fig = px.line(monthly_total, x="月", y="信用卡交易金額", color="年齡層", title='各年齡層每月信用卡交易金額趨勢', markers=True, height=450)
    else:
        monthly_total = lastest_df.groupby(['年', '月', '年齡層'])['信用卡交易金額'].sum().reset_index()
        filtered_df = monthly_total[monthly_total['年齡層'] == f'{selected_age}']
        fig = px.line(filtered_df, x="月", y="信用卡交易金額", color="年齡層", title=f'{selected_age}每月信用卡交易金額趨勢', markers=True, height=450)
    return fig

@dash1.callback(
    Output("graph_bar", "figure"),
    Input("area","value")
)
def update_bar_chart(selected_area):
    global lastest_df
    if selected_area == "ALL":
        region_sum = lastest_df.groupby('地區')['信用卡交易金額'].sum().reset_index()
        fig = px.bar(region_sum, x='地區', y='信用卡交易金額', title='各地區信用卡交易金額', height=450)
    else:
        region_sum = lastest_df.groupby('地區')['信用卡交易金額'].sum().reset_index()
        fig = px.bar(region_sum, x='地區', y='信用卡交易金額', title=f'{selected_area}信用卡交易金額', height=450)
        highlighted_region = selected_area
        fig.update_traces(marker_color=['rgba(1,87,155,0.2)' if region != highlighted_region else 'blue' for region in region_sum['地區']])
    return fig

@dash1.callback(
    Output("graph_sunburst", "figure"),
    [Input("month","value"),Input("area","value"),Input("industry","value")]
)
def update_sunburst_chart(selected_mon,selected_ar,selected_ind):
    global lastest_df
    if selected_mon == "ALL" and selected_ar == "ALL" and selected_ind == "ALL":
        fig = px.sunburst(lastest_df, path=['年', '月', '地區', '產業別', '年齡層'], values='信用卡交易金額', title='2023年各年齡層信用卡交易分布', height=500)
    elif selected_mon != "ALL" and selected_ar == "ALL" and selected_ind == "ALL":
        filtered_df = lastest_df[lastest_df['月'].astype(str) == selected_mon]
        fig = px.sunburst(filtered_df, path=['月', '地區', '產業別', '年齡層'], values='信用卡交易金額',title=f'{selected_mon}月信用卡交易分布', height=500)
    elif (selected_mon == "ALL" and selected_ar != "ALL" and selected_ind == "ALL"):
        filtered_df = lastest_df[lastest_df['地區'] == selected_ar]
        fig = px.sunburst(filtered_df, path=['地區', '產業別', '年齡層'], values='信用卡交易金額',title=f'{selected_ar}信用卡交易分布', height=500)
    elif (selected_mon == "ALL" and selected_ar != "ALL" and selected_ind != "ALL"):
        filtered_df = lastest_df[(lastest_df['地區'] == selected_ar) & (lastest_df['產業別'] == selected_ind)]
        fig = px.sunburst(filtered_df, path=['地區', '產業別', '年齡層'], values='信用卡交易金額',title=f'{selected_ar} / {selected_ind} 信用卡交易分布', height=500)
    elif selected_mon != "ALL" and selected_ar != "ALL" and selected_ind == "ALL":
        filtered_df = lastest_df[(lastest_df['月'].astype(str) == selected_mon) & (lastest_df['地區'] == selected_ar)]
        print(filtered_df)
        fig = px.sunburst(filtered_df, path=['地區', '產業別', '年齡層'], values='信用卡交易金額',title=f'{selected_mon}月 / {selected_ar} 信用卡交易分布', height=500)
    elif selected_mon != "ALL" and selected_ar == "ALL" and selected_ind != "ALL":
        filtered_df = lastest_df[(lastest_df['月'].astype(str) == selected_mon) & (lastest_df['產業別'] == selected_ind)]
        fig = px.sunburst(filtered_df, path=['月', '產業別', '年齡層'], values='信用卡交易金額',title=f'{selected_mon}月 / {selected_ind} 信用卡交易分布', height=500)
    elif selected_mon != "ALL" and selected_ar != "ALL" and selected_ind != "ALL":
        filtered_df = lastest_df[(lastest_df['月'].astype(str) == selected_mon) & (lastest_df['地區'] == selected_ar) & (lastest_df['產業別'] == selected_ind)]
        fig = px.sunburst(filtered_df, path=['地區', '產業別', '年齡層'], values='信用卡交易金額',title=f'{selected_mon}月 / {selected_ar} / {selected_ind} / 各年齡層信用卡交易分布', height=500)
    return fig