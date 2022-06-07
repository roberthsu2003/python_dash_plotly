# 使用github部署至heroku

### 1. 專案內建立Procfile

```
web: gunicorn index:server
```

### 2. 在主程式app下方建立server

```
server = app.server
``` 

### 3. 下載和安裝git

### 4. 建立一個私人的github專案,並建立一個專案資料夾

### 5.將專案copy至此資料夾

```
$ git init
$ git add .
$ git commit -m "first commit"
$ git branch -M main
$ git remote add origin https:xxxxxxxxx.git
$ git push -u origin main
```

### 5.使用pycharm建立有venv01的虛擬環境
### 6.專案資料夾安裝python 套件

```
$ pip install plotly
$ pip install pandas
$ pip install requests
$ pip install dash-bootstrap-components
$ pip install gunicorn
```

### 7.建立requirements.txt

```
$ pip freeze > requirements.txt
```

### 8. 刪除虛擬環境
### 7. 建立Heroku專案
### 8. 設定專案使用github連線
