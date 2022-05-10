from turtle import pd
from dash import Dash,html,dcc
import pandas as pd
from plotly.express import data

app = Dash(__name__)
df = data.medals_long()
print(df.columns)
app.layout = html.Div(
    dcc.Checklist(
       df.nation.unique(),
       df.nation.unique()[0:2]
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)