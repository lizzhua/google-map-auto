import os
import pandas as pd
import requests

# 設定檔案資訊
INPUT_FILE = "活頁簿2.xlsx"
SHEET_NAME = "2018.10-12月"
OUTPUT_FILE = "加上平常日判斷.xlsx"
API_KEY = os.getenv("ABSTRACT_API_KEY")

# 查詢整年台灣假日並建立假日集合（只查一次）
def get_holidays_for_year(year):
    url = f"https://holidays.abstractapi.com/v1/?api_key={API_KEY}&country=TW&year={year}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            holidays = response.json()
            return set(pd.to_datetime(h['date']).date() for h in holidays)
        else:
            print(f"假日查詢失敗：{year}，HTTP 錯誤碼 {response.status_code}")
            return set()
    except Exception as e:
        print(f"發生錯誤：{e}")
        return set()

# 查詢是否為平常日（比對假日集合）
def is_working_day(date_obj, holiday_set):
    return 0 if date_obj in holiday_set or date_obj.weekday() >= 5 else 1

# 執行流程
def main():
    df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME)
    df['叫車時間'] = pd.to_datetime(df['叫車時間'], errors='coerce')

    # 取得所有年份的假日資料
    years = df['叫車時間'].dt.year.dropna().unique()
    all_holidays = set()
    for y in years:
        all_holidays.update(get_holidays_for_year(int(y)))

    # 建立平常日判斷欄位
    df['X1:1=平常日, 0=週六/週日/假日'] = df['叫車時間'].dt.date.apply(lambda d: is_working_day(d, all_holidays))
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"已完成，輸出檔案為：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
