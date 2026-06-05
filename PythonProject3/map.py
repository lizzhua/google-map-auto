import pandas as pd
from googlesearch import search
import time
import requests
from bs4 import BeautifulSoup

# 原始資料（含失敗的）讀入
df = pd.read_excel("活動查詢結果_含標題_日期判斷.xlsx")

# 篩出需要重新查詢的資料
fail_query = df["Google搜尋結果"].isin(["錯誤", "無結果"])
fail_title = df["搜尋結果標題"].isin(["無標題", "標題擷取失敗", "", None])
to_retry = df[fail_query | fail_title].copy()

# 用來更新資料用的索引
retry_indices = to_retry.index

# 搜尋 Google（重查網址）
def search_google(query):
    try:
        results = list(search(query, lang="zh-tw", num_results=1))
        return results[0] if results else "無結果"
    except Exception:
        return "錯誤"

# 擷取標題（重查標題）
def get_page_title(url):
    try:
        if not url.startswith("http"):
            return "無法取得標題"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        return soup.title.string.strip() if soup.title else "無標題"
    except Exception:
        return "標題擷取失敗"

# 重新查詢流程
new_urls, new_titles = [], []
for i, row in to_retry.iterrows():
    query = row["活動查詢關鍵字"]

    url = search_google(query)
    title = get_page_title(url)

    new_urls.append(url)
    new_titles.append(title)

    print(f"🔁 重新查詢 {i}：{query}")
    print(f"🌐 網址：{url}")
    print(f"📄 標題：{title}")
    time.sleep(2)  # 避免封鎖

# 回填回原始資料
df.loc[retry_indices, "Google搜尋結果"] = new_urls
df.loc[retry_indices, "搜尋結果標題"] = new_titles

# 匯出結果
df.to_excel("活動查詢結果_重新查詢後.xlsx", index=False)
print("✅ 已完成！結果儲存為：活動查詢結果_重新查詢後.xlsx")
