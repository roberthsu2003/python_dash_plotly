from dash import Dash, Input, Output, callback, dash_table
import pandas as pd
import dash_bootstrap_components as dbc

df = pd.read_csv('https://git.io/Juf1t')
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Label('Click a cell in the table:'),
    dash_table.DataTable(df.to_dict('records'),[{"name":i, "id":i} for i in df.columns],id='tb1'),
    dbc.Alert(id='tbl_out')
])

@callback(
    Output('tbl_out','children'),
    Input('tb1','active_cell')
)
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the Table"

if __name__ == "__main__":
    app.run_server(debug=True)