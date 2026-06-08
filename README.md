# 高雄市計程車流量分析 — 特徵工程工具集

大四期間，參與計程車流量分析研究計畫，獨立開發的資料前處理模組。

## 專案背景

為建立計程車需求預測模型，需要對原始叫車紀錄補充外部特徵變數，包含時間屬性、地點性質、道路狀況與外部活動事件。

## 模組說明

### 1. 平常日 / 假日判斷 (`PythonProject5/`)
透過 Abstract API 查詢台灣國定假日，判斷每筆叫車時間是否為平常日。

- **輸入**：含叫車時間欄位的 Excel 檔
- **輸出**：新增 `X1: 1=平常日, 0=週六/週日/假日` 欄位
- **API**：[Abstract API — Holidays](https://app.abstractapi.com/api/holidays)

### 2. 上車地點類型分類 (`PythonProject2/`)
以 Google Maps Places API 自動判斷上車地點的性質，分為四類：

| 類別 | 說明 |
|---|---|
| 1 | 交通樞紐（捷運、火車站、機場）|
| 2 | 醫療 / 教育 / 政府機關 |
| 3 | 商圈 / 觀光景點 / 餐飲 |
| 4 | 住宅或其他 |

- `py.py`：混合查詢版（手動字典優先，再 fallback 至 API）
- `clean.py`：兩步查詢版（先取 Place ID，再查詳細 types）
- **API**：[Google Maps Places API](https://console.cloud.google.com/)

### 3. 最近主幹道計算 (`PythonProject6/`)
以 geopy 測地線距離演算法，計算每個上車地點座標到所有路段點的最短距離，找出最近主幹道，並串聯對應的車流速率資料。

- **輸入**：含座標的地點清單、路段幾何點位 CSV
- **輸出**：每個地點對應的最近路段名稱與距離（公尺）

### 4. 活動資訊爬蟲 (`PythonProject3/`)
批次搜尋活動關鍵字，自動取得 Google 搜尋結果網址與頁面標題，並針對失敗項目自動重新查詢。

- **輸入**：含活動查詢關鍵字的 Excel 檔
- **輸出**：補充 Google 搜尋結果網址與標題欄位

## 環境設定

```bash
pip install pandas requests geopy beautifulsoup4 googlesearch-python openpyxl
```

複製 `.env.example` 為 `.env` 並填入金鑰：

```bash
cp .env.example .env
```

## 技術棧

`Python` `pandas` `Google Maps Places API` `Abstract API` `geopy` `BeautifulSoup` `openpyxl`
