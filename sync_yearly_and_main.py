import pandas as pd

# Assumes that statistics_by_year.csv should supersede statistics.csv.

df = pd.read_csv("statistics_by_year.csv")
dfs = []

for time_period in range(2024, 2030):
    time_period_df = df[["name", "unit", str(time_period)]].rename(columns={str(time_period): "value"})
    time_period_df["time_period"] = time_period
    dfs.append(time_period_df)

main_df = pd.concat(dfs)
main_df.to_csv("statistics.csv", index=False)

# Then convert back to ensure consistency.

pivot = main_df.pivot_table(index=["name", "unit"], columns="time_period", values="value").reset_index()
pivot.index.name = "index"
pivot.to_csv("statistics_by_year.csv", index=False)