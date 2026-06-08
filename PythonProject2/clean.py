import os
import pandas as pd
import requests
import time

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# 🚦 自動分類函數：依 types 分類
def classify_place(types_string):
    types = types_string.split(", ")
    if any(t in types for t in ["subway_station", "train_station", "bus_station", "transit_station", "airport"]):
        return 1  # 車站類
    elif any(t in types for t in ["hospital", "doctor", "school", "university", "post_office", "police", "city_hall", "local_government_office"]):
        return 2  # 醫療、教育、政府
    elif any(t in types for t in ["shopping_mall", "supermarket", "convenience_store", "restaurant", "lodging", "tourist_attraction", "park", "night_club"]):
        return 3  # 商業與觀光
    else:
        return 4  # 住家或其他

# 查 place_id
def get_place_id(address):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": address,
        "key": API_KEY
    }
    try:
        response = requests.get(url, params=params).json()
        results = response.get("results", [])
        if results:
            return results[0].get("place_id", "")
        else:
            return ""
    except Exception as e:
        print(f"[place_id 錯誤] {address} → {e}")
        return ""

# 查詳細資料
def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,types",
        "key": API_KEY
    }
    try:
        response = requests.get(url, params=params).json()
        result = response.get("result", {})
        name = result.get("name", "")
        addr = result.get("formatted_address", "")
        types = ", ".join(result.get("types", []))
        return name, addr, types
    except Exception as e:
        print(f"[details 錯誤] {place_id} → {e}")
        return "", "", ""

# 查詢主流程
def get_place_info(address):
    place_id = get_place_id(address)
    time.sleep(0.3)  # 控制查詢速度，避免 API 封鎖
    if place_id:
        name, addr, types = get_place_details(place_id)
        print(f"[查詢成功] {address} → {name}, {types}")
        return name, addr, types
    else:
        print(f"[查無結果] {address}")
        return "", "", ""

# 載入資料
df = pd.read_excel("標準化地址.xlsx")

# 查詢地點資訊
results = df["上車地點"].apply(lambda x: get_place_info(str(x)))

# 拆欄位
df["樓名"] = results.apply(lambda x: x[0])
df["標準地址"] = results.apply(lambda x: x[1])
df["地點類型"] = results.apply(lambda x: x[2])

# 自動分類
df["用途分類"] = df["地點類型"].apply(classify_place)

# 匯出
df.to_excel("樓名查詢結果_完整分類版.xlsx", index=False)
print("✅ 已完成查詢與分類，結果儲存為：樓名查詢結果_完整分類版.xlsx")
