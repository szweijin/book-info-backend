# Book Search API

## 專案簡介
Book Search API 是一個以 Flask + SQLAlchemy 建構的後端 RESTful API，提供書籍資料的新增、查詢等功能。  
此專案已部署於 Google Cloud Run，並使用 PostgreSQL 作為資料庫。

## 主要技術
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- PostgreSQL
- Google Cloud Run
- Docker
- Flasgger (Swagger API 文件)

## 環境變數設定

請在專案根目錄建立 `.env` 檔案，範例如下：

```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
```
可參考 .env.example 作為範本。


## 本地開發環境設定
1. 建議使用虛擬環境

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```
2. 安裝依賴套件

```bash
pip install -r requirements.txt
```
3. 建立資料庫並匯入假資料（可選）
```bash
python seed_data.py
```
4. 啟動 Flask 開發伺服器
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```
Windows PowerShell：
```powershell
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
flask run
```

## Docker 環境
1. 建立 Docker 映像
```bash
docker build -t book-api .
```
2. 使用 Docker Compose 啟動服務
```bash
docker-compose up -d
```
## 部署
- 後端已部署於 Google Cloud Run，並連接外部 Cloud SQL 資料庫。
- CI/CD 設定在 `.github/workflows/deploy.yml`，當推送至 main 分支時自動部署。

## API 文件
Swagger UI 可在 `/apidocs/`路徑查看。
例如：http://localhost:5000/apidocs/

## 常見指令
- 建立資料庫表格
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```
- 匯入假資料
```bash
python seed_data.py
```