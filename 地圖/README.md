## 地圖
### 支援
- Mapbox Maps
- Geo maps

### Mapbox Maps
- tile-base maps

#### Mapbox Maps支援的圖表
- px.scatter_mapbox
- px.line_mapbox
- px.choropleth_mapbox
- px.density_mapbox
- go.Scattermapbox
- go.Choroplethmapbox
- go.Densitymapbox

#### 使用Mapbox Map有時而要申請免費的Mapbox token
- 如果基礎地圖有參考到(layout.mapbox.style)Mapbox service就要申請
- 如果沒有參考到Mapbox service就可以不用申請

#### 基礎地圖(layout.mapbox.style)
##### 不需要token
- white-bg
- open-street-map
- carto-positron
- carto-darkmatter
- stamen-terrain
- stamen-toner
- stamen-watercolor

##### 需要token
- basic
- streets
- outdoors
- light
- dark
- satellite
- satellite-streets

#### OpenStreetMap

```python

```

### Geo maps
- outline-base maps

#### Geo maps支援的圖表
- px.scatter_geo
- px.line_geo
- px.choropleth
- go.Scattergeo
- go.Choropleth



