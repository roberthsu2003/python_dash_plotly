
## 1. 使用Plotly圖表元件

- 了解Figure物件
- 資料屬性
- 版面屬性
- 學習figure追蹤和增加它們
- 不同方式轉換figures

## 所需要的套件
- Figure類別為於plotly套件內的graph_objects模內
- Dash
- Dash HTML Components
- Dash Core Components
- Dash Bootstrap Components
- Jupyter Dash
- pandas

## 了解Figure 物件

- Plotly是一個小而完整的資料視覺系統
- 有超過50種以上的圖表類型
- 支援2D,3D,3軸,地圖...
- 每個圖表有很多細節的設定
- Figue有2個主要的物件組合,data和layout

```python
import plotly.graph_objects as go
fig = go.Figure()
fig.add_scatter(x=[1, 2, 3, ], y=[4, 2, 3])
fig.add_scatter(x=[1, 2, 3, 4], y=[4, 5, 2, 3])
fig.layout.title = '這是表單抬頭'
fig.layout.xaxis.title = '這是 X-axis title'
fig.layout.yaxis.title = '這是 Y-axis title'
fig.show()
```

### 將Figure物件轉換為html頁面

```python
#上官網查詢 plotly.graphic_object.figure內write_html()資料

fig.write_html('html_plot.html',
                config={'toImageButtonOptions':
                    {'format':'svg'}
                }
)
```

### 將Figure物件轉換為圖片

```python
fig.write_image('path/to/image_file.svg', height=600, width=850)
```



	
	
	