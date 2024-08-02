import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import base64

# Load data
file_path = '/Users/jesshuang/Documents/GitHub/__11304_python_2024_tvdi__/homework/專案/快樂專案WEB_13黃靖雯_15王愷立_07林見恆/World Happiness Report_new.csv'

if os.path.exists(file_path):
    data = pd.read_csv(file_path)
    print(data.head())
else:
    print(f"File not found: {file_path}")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define column alternatives
column_alternatives = {
    'Life Ladder': "誰最快樂",
    'Log GDP Per Capita': "經濟發展",
    'Social Support': "人際關係",
    'Healthy Life Expectancy At Birth': "健康醫療",
    'Freedom To Make Life Choices': "身心自由",
    'Generosity': "慷慨助人",
    'Perceptions Of Corruption': "社會腐敗",
    'Positive Affect': "正面情緒",
    'Negative Affect': "負面情緒",
    'Confidence In National Government': "政治信心"
}

# Define messages
messages = {
    'Life Ladder': "好吧 🙂\n\n🇺🇸🇨🇦🇦🇺🇳🇿\n美加紐澳地區看起來最快樂！\n\n緊追在後的是西歐 🌍 以及\n拉丁美洲及加勒比海地區 🌎",
    'Log GDP Per Capita': "💰\n  錢不是萬能的\n\n 雖然此數據顯示\nGDP 是 #1 影響快樂的指標 - \n\n拉丁美洲及加勒比海地區證明了\n不用最經濟富裕也能活得快樂！🤠",
    'Social Support': "👨‍👩‍👧‍👦\n 人際關係\n\n 擁有健全的社會人際互助是此數據\n顯示 #3 影響快樂的指標 - \n\n此處並非指「社會福利制度」，而是「當遇到人生中困難挫折，是否有可以信任的人給予支持幫助」🥹",
    'Healthy Life Expectancy At Birth': "🩺\n  沒錯！健康很重要\n\n 肝不好，人生就是黑白的～\n有進步的醫療水平，能預期腳長壽命是此數據顯示 #4 影響快樂的指標！",
    'Freedom To Make Life Choices': "🤸🏽‍♀️\n身心自由\n\n能夠自由決定人生及工作方向是此指標中顯示 #2 重要影響快樂的指標！\n\n可以發現連快樂指數低的地區，嚮往自由的標準也相當高～ 🌿",
    'Generosity': "❤️‍🩹\n慷慨助人\n施比受更有福\n\n儘管不是所有人都有餘力助人，此處資料顯示，能滿足自身需求並有額外能力已捐款或志工方式幫助他人，能有效提升快樂程度。☺️",
    'Perceptions Of Corruption': "🤑\n沒人喜歡腐敗\n\n不過此處資料顯示，社會的腐敗程度並無直接重大影響人民快樂程度！",
    'Positive Affect': "😁\n 正面情緒\n\n感受到正面情緒如：\n「滿足」、「興奮」、「愉悅」的頻率。\n\n此處資料顯示較分散，\n說明人們情緒波動受各國不同文化民情影響，較不適合直接代表快樂程度。",
    'Negative Affect': "😣\n 負面情緒\n\n感受到負面情緒如：\n「沮喪」、「生氣」、「難過」的頻率。\n\n此處資料顯示較分散，\n說明人們情緒波動受各國不同文化民情影響，較不適合直接代表快樂程度。",
    'Confidence In National Government': "📡\n 政治信心\n\n雖然政治議題無所不在，此處資料有趣地顯示，人民對國民政府的信心度並無重大影響其快樂程度。"
}

# Load and encode image
img_path = "/Users/jesshuang/Documents/GitHub/__11304_python_2024_tvdi__/homework/專案/快樂專案WEB_13黃靖雯_15王愷立_07林見恆/img.png"
encoded_image = base64.b64encode(open(img_path, 'rb').read()).decode('ascii')

# Define the layout
app.layout = html.Div([
    html.H1("The Happiness Project 人生快樂專案", style={'textAlign': 'center'}),
    html.H2("什麼使你「快樂」？", style={'textAlign': 'center'}),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'display': 'block', 'margin': 'auto'}),
    html.H2("看看世界各地怎麼說", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': v, 'value': k} for k, v in column_alternatives.items()],
        value='Life Ladder',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Graph(id='happiness-scatter'),
    html.Div(id='message-box', style={'textAlign': 'center', 'whiteSpace': 'pre-line'})
])

# Define callback to update graph
@app.callback(
    [Output('happiness-scatter', 'figure'),
     Output('message-box', 'children')],
    [Input('column-dropdown', 'value')]
)
def update_graph(selected_column):
    fig = px.scatter(data, x=selected_column, y='Life Ladder', color='Region',
                     title=f'Life Ladder vs {column_alternatives[selected_column]}',
                     labels={'Life Ladder': 'Life Ladder', selected_column: column_alternatives[selected_column]})
    
    return fig, messages[selected_column]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)