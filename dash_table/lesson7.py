from dash import Dash, dash_table
import pandas as pd
from collections import OrderedDict

app = Dash(__name__)

data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(
    OrderedDict([(name, col_data * 10) for (name, col_data) in data.items()])
)

app.layout = dash_table.DataTable(
    data = df.to_dict('records'),
    columns = [{'id':c, 'name':c} for c in df.columns],
    fixed_rows={'headers':True},
    style_table={'height':400} #default to 500
)

if __name__ == "__main__":
    app.run_server(debug=True)