from turtle import pd
from dash import Dash,html,dcc
import pandas as pd
from plotly.express import data

app = Dash(__name__)
df = data.medals_long()
print(df.columns)
app.layout = html.Div(
    dcc.Checklist(
       df.columns,
       df.columns[0:2].values
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)