# -*- coding: utf-8 -*-
import pandas as pd
from geopy.distance import geodesic

# 讀入地址經緯度（已經查好的）
points_df = pd.read_excel("查詢結果_含鄰近主幹道.xlsx")

# 讀入路段點資料
roads_df = pd.read_csv("kaohsiung_road_geometries.csv")

# 計算每個地點到所有路段點的最短距離
output = []
for _, p in points_df.iterrows():
    p_coord = (p['緯度'], p['經度'])
    roads_df['距離'] = roads_df.apply(lambda r: geodesic(p_coord, (r['lat'], r['lon'])).meters, axis=1)
    min_row = roads_df.loc[roads_df['距離'].idxmin()]
    output.append({
        '地址': p['上車地點'],
        '緯度': p['緯度'],
        '經度': p['經度'],
        '最近路段': min_row['路段'],
        '距離（公尺）': min_row['距離']
    })

# 輸出結果
out = pd.DataFrame(output)
out.to_csv("nearest_road_from_excel_points.csv", index=False)
print("\nSaved to nearest_road_from_excel_points.csv")
