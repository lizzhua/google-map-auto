import pandas as pd

print("1104496 廖幸茹")

df = pd.read_csv("data.csv")

diff = df['q2_qty'] - df['q1_qty']

print(diff.to_string(index=True))

