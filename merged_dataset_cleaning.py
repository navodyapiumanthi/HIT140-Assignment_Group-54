import pandas as pd

df = pd.read_csv("merged_dataset.csv")


#drop duplicate rows
print("Duplicates before drop:", df.duplicated(keep="first").sum())
df = df.drop_duplicates(keep="first").reset_index(drop=True)

# datetime conversion
df["start_time_dt"] = pd.to_datetime(df["start_time"], errors="coerce", dayfirst=True)
df["time_dt"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)

#fill empty rows in time column
empty_time = df["time"].isna() | (df["time"].astype(str).str.strip() == "")
to_fill = empty_time & df["start_time_dt"].notna()

#ensuring column is datetime
df.loc[to_fill, "time"] = df.loc[to_fill, "start_time_dt"]
df["time"] = pd.to_datetime(df["time"], errors="coerce", dayfirst=True)
df["time_dt"] = df["time"]  # update time_dt after filling
print("Filled 'time' from start_time_dt:", to_fill.sum())

#ensures exact matches between start_time_dt and time_dt
both_present = df["start_time_dt"].notna() & df["time_dt"].notna()
exact_match = df["start_time_dt"] == df["time_dt"]
print("Exact matches between start_time_dt and time_dt:", (both_present & exact_match).sum())# Numeric conversion


#Fix out of range dates / typos 
def flip_date(ts: pd.Timestamp) -> pd.Timestamp:
    """Flip day and month if month > 5"""
    if pd.isna(ts) or ts.month <=5:
        return ts
    try:
        return ts.replace(month=ts.day, day=ts.month)
    except ValueError:
        return ts

df["time_dt"] = df["time_dt"].apply(flip_date)

map_to_scheme = {12:0, 1:1, 2:2, 3:3, 4:4, 5:5,}
df["month"] = df["time_dt"].dt.month.map(map_to_scheme).astype("Int64")


# mismatch in months and seasons
df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
df["season"] = df["month"].map({0:0, 1:0, 2:0, 3:1, 4:1, 5:1}).astype("Int64")


# Sorting
# Sort by season, month and then time
df["sort_dt"] = df["time_dt"].fillna(df["start_time_dt"])
df = df.sort_values(["season", "month", "sort_dt"], na_position="last").reset_index(drop=True)



df_out = df.drop(columns=["start_time_dt", "time_dt", "sort_dt"], errors="ignore")

# save merged with datetime formatting
df_out.to_csv("merged_dataset_sorted.csv", index=False, date_format="%d/%m/%Y %H:%M:%S")
print("\nSaved: merged_dataset_sorted.csv")


#Spit by season
winter = df_out[df_out["season"] == 0].reset_index(drop=True)
spring = df_out[df_out["season"] == 1].reset_index(drop=True)

#Train data 70/30

#Winter
train_winter = winter.sample(frac=0.7, random_state=42)
test_winter = winter.drop(train_winter.index).reset_index(drop=True)
train_winter = train_winter.reset_index(drop=True)

#Spring
train_spring = spring.sample(frac=0.7, random_state=42)
test_spring = spring.drop(train_spring.index).reset_index(drop=True)
train_spring = train_spring.reset_index(drop=True)

#save train and test data
train_winter.to_csv("train_winter_70.csv", index=False, date_format="%d/%m/%Y %H:%M:%S")
test_winter.to_csv("test_winter_30.csv",  index=False, date_format="%d/%m/%Y %H:%M:%S")
train_spring.to_csv("train_spring_70.csv", index=False, date_format="%d/%m/%Y %H:%M:%S")
test_spring.to_csv("test_spring_30.csv",  index=False, date_format="%d/%m/%Y %H:%M:%S")
