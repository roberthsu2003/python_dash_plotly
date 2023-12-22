import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from dash import dash_table

df = pd.read_csv('dash_file/list.csv')
data=df.to_dict("records")

#111111111111111111111111111111111111111111111111111111111111111111111以固體或液體物質自殺及自為中毒
def generate_pie_chart_drug():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["以固體或液體物質自殺及自為中毒"],
                marker=dict(colors=[
                                "#D22B2B",
                                "#C41E3A",
                                "#F88379",
                                "#d62728",
                                "#DC143C",
                                "#FF3131",
                                "#D2042D",
                                "#EE4B2B",
                                "#811331",
                                "#C04000",
                                "#E35335",
                                "#A52A2A",
                                "#FA8072",
                                "#E3735E",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_drug():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="以固體或液體物質自殺及自為中毒",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                    "#D22B2B",
                    "#C41E3A",
                    "#F88379",
                    "#d62728",
                    "#DC143C",
                    "#FF3131",
                    "#D2042D",
                    "#EE4B2B",
                    "#811331",
                    "#C04000",
                    "#E35335",
                    "#A52A2A",
                    "#FA8072",
                    "#E3735E",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_drug():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["以固體或液體物質自殺及自為中毒"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart
#22222222222222222222222222222222222222222222222222222222222222222222222222以氣體及蒸汽自殺及自為中毒
def generate_pie_chart_air():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["以氣體及蒸汽自殺及自為中毒"],
                marker=dict(colors=[
                                "#FFAC1C",
                                "#CD7F32",
                                "#DAA06D",
                                "#CC5500",
                                "#E97451",
                                "#E3963E",
                                "#F28C28",
                                "#D27D2D",
                                "#B87333",
                                "#FF7F50",
                                "#DAA520",
                                "#C04000",
                                "#CC7722",
                                "#FFA500",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_air():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="以氣體及蒸汽自殺及自為中毒",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                    "#FFAC1C",
                    "#CD7F32",
                    "#DAA06D",
                    "#CC5500",
                    "#E97451",
                    "#E3963E",
                    "#F28C28",
                    "#D27D2D",
                    "#B87333",
                    "#FF7F50",
                    "#DAA520",
                    "#C04000",
                    "#CC7722",
                    "#FFA500",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_air():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["以氣體及蒸汽自殺及自為中毒"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart
#33333333333333333333333333333333333333333333333333333333333333333333333333333333333吊死、勒死及窒息之自殺及自傷
def generate_pie_chart_hang():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["吊死、勒死及窒息之自殺及自傷"],
                marker=dict(colors=[
                                "#EADDCA",
                                "#FFBF00",
                                "#FBCEB1",
                                "#FFDB58",
                                "#E1C16E",
                                "#FFFF8F",
                                "#FFC000",
                                "#DAA520",
                                "#F8DE7E",
                                "#E4D00A",
                                "#F0E68C",
                                "#FADA5E",
                                "#FFDEAD",
                                "#FFD700",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_hang():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="吊死、勒死及窒息之自殺及自傷",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                                "#EADDCA",
                                "#FFBF00",
                                "#FBCEB1",
                                "#FFDB58",
                                "#E1C16E",
                                "#FFFF8F",
                                "#FFC000",
                                "#DAA520",
                                "#F8DE7E",
                                "#E4D00A",
                                "#F0E68C",
                                "#FADA5E",
                                "#FFDEAD",
                                "#FFD700",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_hang():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["吊死、勒死及窒息之自殺及自傷"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart
#444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444溺水 (淹死)自殺及自傷
def generate_pie_chart_drown():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["溺水 (淹死)自殺及自傷"],
                marker=dict(colors=[
                                "#4F7942",
                                "#228b22",
                                "#57b754",
                                "#7ddb7c",
                                "#4dae4b",
                                "#355E3B",
                                "#74d272",
                                "#44a541",
                                "#399c37",
                                "#87e586",
                                "#61c05e",
                                "#6ac968",
                                "#2e942d",
                                "#90ee90",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_drown():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="溺水 (淹死)自殺及自傷",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                                "#4F7942",
                                "#228b22",
                                "#57b754",
                                "#7ddb7c",
                                "#4dae4b",
                                "#355E3B",
                                "#74d272",
                                "#44a541",
                                "#399c37",
                                "#87e586",
                                "#61c05e",
                                "#6ac968",
                                "#2e942d",
                                "#90ee90",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_drown():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["溺水 (淹死)自殺及自傷"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart
#55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555鎗砲及爆炸物自殺及自傷
def generate_pie_chart_gun():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["鎗砲及爆炸物自殺及自傷"],
                marker=dict(colors=[
                                "#b6d0e2",
                                "#9cc2e0",
                                "#82b4dd",
                                "#69a5db",
                                "#5096d9",
                                "#3686d6",
                                "#1776d2",
                                "#0066cd",
                                "#0056c6",
                                "#0044be",
                                "#0031b4",
                                "#0818a8",
                                "#A7C7E7",
                                "#0096FF",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_gun():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="鎗砲及爆炸物自殺及自傷",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                                "#b6d0e2",
                                "#9cc2e0",
                                "#82b4dd",
                                "#69a5db",
                                "#5096d9",
                                "#3686d6",
                                "#1776d2",
                                "#0066cd",
                                "#0056c6",
                                "#0044be",
                                "#0031b4",
                                "#0818a8",
                                "#A7C7E7",
                                "#0096FF",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_gun():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["鎗砲及爆炸物自殺及自傷"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart
#66666666666666666666666666666666666666666666666666666666666666666666666666666666666666666切穿工具自殺及自傷
def generate_pie_chart_cut():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["切穿工具自殺及自傷"],
                marker=dict( colors=[
                                "#2c56ef",
                                "#2a3cfa",
                                "#4700ff",
                                "#3f00ff",
                                "#4f00ff",
                                "#5500ff",
                                "#5c00ff",
                                "#6200ff",
                                "#6700ff",
                                "#6c00ff",
                                "#7100ff",
                                "#7b00ff",
                                "#7600ff",
                                "#7f00ff",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_cut():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="切穿工具自殺及自傷",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                                "#2c56ef",
                                "#2a3cfa",
                                "#4700ff",
                                "#3f00ff",
                                "#4f00ff",
                                "#5500ff",
                                "#5c00ff",
                                "#6200ff",
                                "#6700ff",
                                "#6c00ff",
                                "#7100ff",
                                "#7b00ff",
                                "#7600ff",
                                "#7f00ff",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_cut():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["切穿工具自殺及自傷"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart
#7777777777777777777777777777777777777777777777777777777777777777777777777777777777777777由高處跳下自殺及自傷
def generate_pie_chart_jump():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["由高處跳下自殺及自傷"],
                marker=dict(colors=[
                                "#da70d6",
                                "#d268ce",
                                "#c95fc6",
                                "#c157be",
                                "#b94eb6",
                                "#b145ae",
                                "#a83ca6",
                                "#a0339e",
                                "#982a97",
                                "#901f8f",
                                "#881288",
                                "#850d85",
                                "#830683",
                                "#800080",
                            ])
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_jump():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="由高處跳下自殺及自傷",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                                "#da70d6",
                                "#d268ce",
                                "#c95fc6",
                                "#c157be",
                                "#b94eb6",
                                "#b145ae",
                                "#a83ca6",
                                "#a0339e",
                                "#982a97",
                                "#901f8f",
                                "#881288",
                                "#850d85",
                                "#830683",
                                "#800080",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_jump():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["由高處跳下自殺及自傷"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart

#8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888其他及未明示之方式自殺及自傷
def generate_pie_chart_other():
    return dcc.Graph(
        id="suicide-pie-chart",
        figure=go.Figure(
            data=[go.Pie(
                labels=df["年度"],
                values=df["其他及未明示之方式自殺及自傷"],
                marker=dict(colors=[
                                "#71797e",
                                "#767d82",
                                "#737b80",
                                "#787f84",
                                "#7f858a",
                                "#868c8f",
                                "#8d9295",
                                "#94999b",
                                "#9b9fa1",
                                "#a3a6a7",
                                "#aaacae",
                                "#b1b3b4",
                                "#b9b9ba",
                                "#c0c0c0",
                            ],)
            )],
            layout=go.Layout(
                title="圓餅圖",
                width=595,
                height=595,
                margin=dict(l=30, r=20, b=20, t=120),
                showlegend=True,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            )
        ).update_layout(title_x=0.5),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate bar chart
def generate_bar_chart_other():
    return dcc.Graph(
        id="suicide-bar-chart",
        figure=px.bar(
            df,
            x="年度",
            y="其他及未明示之方式自殺及自傷",
            title="長條圖",
                color=[
                    "98",
                    "99",
                    "100",
                    "101",
                    "102",
                    "103",
                    "104",
                    "105",
                    "106",
                    "107",
                    "108",
                    "109",
                    "110",
                    "111",
                ],
                color_discrete_sequence=[
                                "#71797e",
                                "#767d82",
                                "#737b80",
                                "#787f84",
                                "#7f858a",
                                "#868c8f",
                                "#8d9295",
                                "#94999b",
                                "#9b9fa1",
                                "#a3a6a7",
                                "#aaacae",
                                "#b1b3b4",
                                "#b9b9ba",
                                "#c0c0c0",
                ],
        ).update_layout(title_x=0.5,paper_bgcolor="#FCFAF2"),
        style={"width": "595px", "height": "595px"}
    )

# Function to generate line charts
def generate_line_chart_other():
    updated_chart = dcc.Graph(
        id=f"suicide-line-chart_a",
        figure={
            "data": [
                go.Scatter(
                    x=df["年度"],
                    y=df["其他及未明示之方式自殺及自傷"],
                    mode="lines+markers",
                )
            ],
            "layout": go.Layout(
                width=1200,  # 調整寬度
                height=595,
                margin=dict(l=100, r=20, b=20, t=120),
                showlegend=False,
                paper_bgcolor="#FCFAF2",  # 透明背景
                plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
            ),
        },
    )
    return updated_chart


# 提取方法描述列以获取方法名称
methods = df.columns[1:]
# 将所有方法的年度加总
sum_df = df[methods].sum()

def total_pie():
    return dcc.Graph(
            id="suicide-pie-chart",
            figure=px.pie(
                names=methods,
                values=sum_df.values,
                title="各自殺方法年度總數圓餅圖",
                color=methods,
                color_discrete_sequence=[
                    "#66327C",
                    "#8F77B5",
                    "#B481BB",
                    "#7B90D2",
                    "#9467bd",
                    "#986DB2",
                    "#9B90C2",
                    "#211E55",
                    "#B28FCE",
                    "#7B90D2",
                ],  # 修改为不同的颜色
            ).update_layout(
            width=595,
            height=595,
            margin=dict(l=30, r=20, b=20, t=120),
            showlegend=True,
            paper_bgcolor="#FCFAF2",  # 透明背景
            plot_bgcolor="rgba(0,0,0,0)",  # 透明背景
        ),
            style={"width": "595px", "height": "595px"},  # 设置宽度、高度和浮动位置
        )

def total_bar():
    return dcc.Graph(
            id="suicide-bar-chart",
            figure=px.bar(
                y=sum_df.values,
                title="各自殺方法年度總數長條圖",
                labels={"x": "自殺方法", "y": "年度總數"},
                color=methods,
                color_discrete_sequence=[
                    "#66327C",
                    "#8F77B5",
                    "#B481BB",
                    "#7B90D2",
                    "#9467bd",
                    "#986DB2",
                    "#9B90C2",
                    "#211E55",
                    "#B28FCE",
                    "#7B90D2",
                ],  # 修改为不同的颜色
            ).update_layout(paper_bgcolor="#FCFAF2"),
            style={
                "width": "595px",
                "height": "595px",
            },  # 设置宽度、高度和浮动位置
        )

def total_line():
    custom_labels = [
        "固體/液體中毒",
        "氣體/蒸汽中毒",
        "吊死、勒死及窒息",
        "溺水 (淹死)",
        "鎗砲/爆炸物自殺",
        "切穿自殺",
        "跳樓自殺",
        "其他"
    ]

    return dcc.Graph(
        id="suicide-line-chart",
        figure=go.Figure(
            data=[go.Scatter(
                x=methods,
                y=sum_df.values,
                mode="lines+markers",
                marker=dict(
                    color=[
                        "#66327C",
                        "#8F77B5",
                        "#B481BB",
                        "#7B90D2",
                        "#9467bd",
                        "#986DB2",
                        "#9B90C2",
                        "#211E55",
                        "#B28FCE",
                        "#7B90D2",
                    ]
                ),
            )],
            layout=dict(
                title="各自殺方法年度總數折線圖",
                xaxis=dict(title="自殺方法"),
                yaxis=dict(title="年度總數"),
                width=1200,
                height=600,
                paper_bgcolor="#FCFAF2"
            ),
        ).update_xaxes(ticktext=custom_labels, tickvals=methods),
        style={"width": "300px", "height": "300px", 'padding-bottom': '310px'},
    )

def total_list():
    return dash_table.DataTable(
        id="suicide-methods-table",
        columns=[
            {"name": "年度", "id": "年度"},
            {"name":  "服毒自殺", "id": "以固體或液體物質自殺及自為中毒"},
            {"name": "以氣體自殺", "id": "以氣體及蒸汽自殺及自為中毒"},
            {"name": "窒息式自殺", "id": "吊死、勒死及窒息之自殺及自傷"},
            {"name": "用水自殺", "id": "溺水 (淹死)自殺及自傷"},
            {"name": "吞槍自殺", "id": "鎗砲及爆炸物自殺及自傷"},
            {"name": "切穿工具自殺及自傷", "id": "切穿工具自殺及自傷"},
            {"name": "由高處跳下自殺及自傷", "id": "由高處跳下自殺及自傷"},
            {"name": "其他及未明示之方式自殺及自傷", "id": "其他及未明示之方式自殺及自傷"},
        ],
        data=df.to_dict("records"),
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},  # Apply the style to odd rows
                'backgroundColor': '#FCFAF2',  # Set the background color for odd rows
            }
        ],)

