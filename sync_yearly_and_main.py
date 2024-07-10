import pandas as pd

# Assumes that statistics_by_year.csv should supersede statistics.csv.

df = pd.read_csv("statistics_by_year.csv")
dfs = []

MIN_YEAR = 2018
MAX_YEAR = 2029

for time_period in range(MIN_YEAR, MAX_YEAR + 1):
    time_period_df = df[["name", "unit", "reference", str(time_period)]].rename(columns={str(time_period): "value"})
    time_period_df["time_period"] = time_period
    dfs.append(time_period_df)

main_df = pd.concat(dfs)
main_df = main_df[main_df.value.notnull()]
main_df.to_csv("statistics.csv", index=False)

main_df = pd.read_csv("statistics.csv")

# Then convert back to ensure consistency.

pivot = main_df.pivot_table(index=["name", "unit", "reference"], columns="time_period", values="value", dropna=False).reset_index()
for year in range(MIN_YEAR, MAX_YEAR + 1):
    if year not in pivot.columns:
        pivot[year] = None
pivot = pivot[["name", "unit", "reference"] + list(range(MIN_YEAR, MAX_YEAR + 1))]
pivot.index.name = "index"
# Drop all rows with all NaN values.
pivot = pivot.dropna(how="all", subset=list(range(MIN_YEAR, MAX_YEAR + 1)))
pivot = pivot.sort_values(["reference", "unit", 2025], ascending=False)
pivot.to_csv("statistics_by_year.csv", index=False)