import os
import pandas as pd
import requests
import time

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# ✅ 自定義特殊地點字典（補足查不到的情況）
manual_dict = {
    "高鐵左營": 1,
    "台鐵高雄": 1,
    "捷運三多": 1,
    "捷運美麗島": 1,
    "長庚醫院": 2,
    "高雄醫學大學": 2,
    "國泰中正廣場": 3,
    "義享天地": 3,
    "夢時代": 3,
    "瑞豐夜市": 3,
    "85大樓": 3,
    "美術館": 3
}

# ✅ 分類規則
def classify_place(place_types):
    if any(pt in place_types for pt in ["airport", "bus_station", "subway_station", "train_station", "transit_station"]):
        return 1
    elif any(pt in place_types for pt in ["hospital", "school", "university", "post_office", "police", "city_hall", "local_government_office"]):
        return 2
    elif any(pt in place_types for pt in ["shopping_mall", "convenience_store", "supermarket", "lodging", "tourist_attraction", "restaurant", "park"]):
        return 3
    else:
        return 4

# ✅ Google Places Text Search API 查詢
def get_place_type_textsearch(address):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": address,
        "key": API_KEY
    }
    try:
        response = requests.get(url, params=params).json()
        results = response.get("results", [])
        if results:
            place_types = results[0].get("types", [])
            print(f"[API] {address} → {place_types}")
            return classify_place(place_types)
        else:
            print(f"[API] {address} → 無結果")
            return 4
    except Exception as e:
        print(f"[ERROR] 查詢失敗：{address}, 錯誤：{e}")
        return 4

# ✅ 判斷是否出現在手動表中
def check_manual(address):
    for keyword, cat in manual_dict.items():
        if keyword in address:
            print(f"[手動] {address} → {keyword} → 分類 {cat}")
            return cat
    return None

# ✅ 綜合判斷（先查字典，再查 API）
def hybrid_classify(address):
    address = str(address)
    manual_result = check_manual(address)
    if manual_result is not None:
        return manual_result
    time.sleep(0.3)  # 加一點延遲避免 API 鎖住
    return get_place_type_textsearch(address)

# ✅ 載入資料
df = pd.read_excel("活頁簿1.xlsx")

# ✅ 執行分類
df["地點分類"] = df["上車地點"].apply(hybrid_classify)

# ✅ 匯出結果
df.to_excel("分類後.xlsx", index=False)
print("✅ 分類完成，結果已匯出為『分類後.xlsx』")
