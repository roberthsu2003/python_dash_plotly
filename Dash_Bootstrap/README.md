# Dash Bootstrap

## 安裝

```
pip install dash-bootstrap-components
```


## Bootstrap 有各種主題可以直接套用(theme)

```python
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Alert(
    "Hello, Bootstrap!", className="m-5"
)

if __name__ == "__main__":
    app.run_server()
```


