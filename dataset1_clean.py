import pandas as pd 

df = pd.read_csv("Dataset 1.csv")

#file checking

print(df.info())
print(df.head())
print(df.isna().sum())


df["habit_raw"] = df["habit"].astype(str) #raw habit column for later use

#data conversion
df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
df["sunset_time"] = pd.to_datetime(df["sunset_time"], errors="coerce")
df["rat_period_start"] = pd.to_datetime(df["rat_period_start"], errors="coerce")
df["rat_period_end"] = pd.to_datetime(df["rat_period_end"], errors="coerce")

df["bat_landing_to_food"] = pd.to_numeric(df["bat_landing_to_food"], errors="coerce")
df["seconds_after_rat_arrival"] = pd.to_numeric(df["seconds_after_rat_arrival"], errors="coerce")
df["hours_after_sunset"] = pd.to_numeric(df["hours_after_sunset"], errors="coerce")
df["risk"] = pd.to_numeric(df["risk"], errors="coerce")
df["reward"] = pd.to_numeric(df["reward"], errors="coerce")

#missing values
df = df.dropna(subset=["risk", "reward"]) #remove rows with missing values from these columns

df["habit"] = df["habit"].fillna("unknown") #missing data will be filled with "unknown"

#formatting
df["habit"] = df["habit"].astype(str).str.strip().str.lower() #standardise habit values
df["habit"] = df["habit"].replace({"bat_figiht": "bat_fight"}) #correcting a typo




#invalid habit values
df = df[~df["habit"].str.contains(r"\d", na=False)]

df = df[df["risk"].isin([0,1]) &df["reward"].isin([0,1])]

#habit groups
df["habit_simple"] = "other"

df.loc[df["habit"].str.contains("fast", na=False), "habit_simple"] = "fast"
df.loc[df["habit"].str.contains("pick", na=False), "habit_simple"] = "pick"
df.loc[df["habit"].str.contains("bat",  na=False), "habit_simple"] = "bat"
df.loc[df["habit"].str.contains("rat",  na=False), "habit_simple"] = "rat" 

#new fight column
df["fight"] = df["habit_raw"].str.lower().str.contains("fight", na=False).astype(int)

#update habit column to use simplified groups
df["habit"] = df["habit_simple"]
df = df.drop(columns=["habit_simple"]) #drop the temporary column

#negative values in numeric columns
numeric_cols = ["bat_landing_to_food", "seconds_after_rat_arrival", "hours_after_sunset"] #time cannot be negative, bats are nocturnal
for col in numeric_cols:
    if col in df.columns:
        before = len(df)
        df = df[df[col] >= 0]
        removed = before - len(df)
        print(f"Removed {removed} rows with negative values in {col}")
        

#cleaning log
print("\n--- CLEANING LOG ---")
print("Rows after cleaning:", len(df))

# Key label distributions
print("Risk (0/1):", df["risk"].value_counts(dropna=False).to_dict())
print("Reward (0/1):", df["reward"].value_counts(dropna=False).to_dict())

# Habit summary (both raw distinct and simplified groups)

if "habit_simple" in df.columns:
    print("Habit groups (simple):",
        df["habit_simple"].value_counts(dropna=False).to_dict())

# Fight flag summary 
print("Fight flag (0/1):", df["fight"].value_counts(dropna=False).to_dict())

# Optional: quick peek at timing for sanity
print("\nTiming summaries:")
print(df[["bat_landing_to_food", "seconds_after_rat_arrival", "hours_after_sunset"]].describe())

# Save cleaned dataset for the team
df.to_csv("Dataset1_clean.csv", index=False)
print("\nSaved: Dataset1_clean.csv")
