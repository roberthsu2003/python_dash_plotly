## Scater和RangeSlider
- 以點表示的圖表

```python
import plotly.express as px
fig = px.scatter(x=[0,1,2,3,4], y=[0,1,4,9,16])
fig.show()
```

![](./images/pic1.png)

```python
#x and y使用DataFrame Columns
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df, x = 'sepal_width', y='sepal_length')
fig.show()
```

![](./images/pic2.png)

![](./images/pic3.png)

## 設定點大小和顏色

```python
import plotly.express as px
df = px.data.iris()
fig = px.scatter(df,
                x="sepal_width",
                y="sepal_length",
                color="species",
                size="petal_length",
                hover_data=['petal_width']
)
fig.show()
```

![](./images/pic4.png)

