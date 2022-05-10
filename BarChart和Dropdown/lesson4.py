from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Restaurant tips by day of week'),
    dcc.Dropdown(
        id='dropdown',
        options=["Fri", "Sat", "Sun"],
        value = "Fri",
        clearable=False
    ),
    dcc.Graph(id="graph")
])

@app.callback(
    Output("graph","figure"),
    Input("dropdown","value")
)
def update_bar_chart(day):
    df = px.data.tips()
    mask = df["day"] == day
    fig = px.bar(
        df[mask],
        x="sex",
        y="total_bill",
        color="smoker",
        barmode="group"    
    )
    return fig

app.run_server(debug=True)
