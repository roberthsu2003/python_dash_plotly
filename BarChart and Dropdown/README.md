## Dropdown component

```
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
    html.Div(id='dd-output-container')
])


@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)

```

![](./images/pic1.png)

#### options and value的屬性各種操作法

```python
dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC')
``` 

```python
dcc.Dropdown(
   options=['New York City', 'Montreal', 'San Francisco'],
   value='Montreal'
)
```

```python
dcc.Dropdown(
   options=[
       {'label': 'New York City', 'value': 'New York City'},
       {'label': 'Montreal', 'value': 'Montreal'},
       {'label': 'San Francisco', 'value': 'San Francisco'},
   ],
   value='Montreal'
)
```

```python
dcc.Dropdown(
   options={
        'New York City': 'New York City',
        'Montreal': 'Montreal',
        'San Francisco': 'San Francisco'
   },
   value='Montreal'
)
```

### 可多值選取的Dropdown

```python
from dash import Dash,dcc,html

dcc.Dropdown(
    ['New York City', 'Montreal', 'San Francisco'],
    ['Montreal', 'San Francisco'],
    multi=True
)

app = Dash(__name__)
app.layout = html.Div(
    dcc.Dropdown(
    ['New York City', 'Montreal', 'San Francisco'],
    ['Montreal', 'San Francisco'],
    multi=True
)
)
if __name__ == '__main__':
    app.run_server(debug=True)
```

![](./images/pic2.png)

### 提示文字

```python
from dash import dcc

dcc.Dropdown(
    ['New York City', 'Montreal', 'San Francisco'],
    placeholder="Select a city",
)
```

![](./images/pic3.png)

### 關閉Dropdown

```python
from dash import dcc

dcc.Dropdown(
    ['New York City', 'Montreal', 'San Francisco'],
    disabled=True
)
```

### 關閉部份選項

```python
dcc.Dropdown([
        {'label': 'New York City', 'value': 'NYC', 'disabled': True},
        {'label': 'Montreal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF', 'disabled': True}])
```

### 使用Pandas提供資料

```python
from dash import Dash, dcc, html, Input, Output
from plotly.express import data
import pandas as pd

df =  data.medals_long()
print(df)

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(df.nation.unique(), id='pandas-dropdown-2'),
    html.Div(id='pandas-output-container-2')
])


@app.callback(
    Output('pandas-output-container-2', 'children'),
    Input('pandas-dropdown-2', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)

```

### 整合Bar Char

```python
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

```

![](./images/pic4.png)

