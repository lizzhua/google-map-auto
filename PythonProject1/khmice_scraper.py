import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.klook.com/zh-TW/blog/kaohsiung-exhibition"
headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 找出文章中的標題（假設使用 <h2> 做為活動區塊標題）
headers = soup.find_all("h2")

data = []

for h in headers:
    name = h.text.strip()
    # 往下找下一段文字作為說明（如果有）
    next_para = h.find_next_sibling("p")
    desc = next_para.text.strip() if next_para else ""
    data.append({
        "活動名稱": name,
        "活動簡介": desc,
        "來源平台": "Klook 高雄展覽推薦"
    })

df = pd.DataFrame(data)
print(df)
