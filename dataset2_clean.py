import pandas as pd

#file loading and checking 
df2 = pd.read_csv("Dataset 2.csv")

print(df2.info())
print(df2.head())
print(df2.isna().sum())

#data conversion
df2["start_time"] = pd.to_datetime(df2["time"], errors="coerce")

dum_cols = ["hours_after_sunset", "bat_landing_number",
            "food_availability", "rat_minutes", "rat_arrival_number"]

for col in dum_cols:
    df2[col] = pd.to_numeric(df2[col], errors="coerce")
    
#missing values
df2 = df2.dropna(subset=["hours_after_sunset", "food_availability",
                        "rat_minutes", "rat_arrival_number"])

#invalid values
before = len(df2)

df2 = df2[df2["hours_after_sunset"] >= 0] #bats are nocturnal
df2 = df2[df2["bat_landing_number"] >= 0] #cannot be negative
df2 = df2[df2["rat_arrival_number"] >= 0] #cannot be negative
df2 = df2[df2["rat_minutes"] >= 0] #cannot be negative
df2 = df2[df2["rat_minutes"] <=30] #max 30 minutes
df2 = df2[df2["food_availability"] >=0] #only 0 and 1 allowed

print(f"Rows removed due to invalid values: {before - len(df2)}")

# counts are integers

df2["bat_landing_number"] = df2["bat_landing_number"].astype(int)
df2["rat_arrival_number"] = df2["rat_arrival_number"].astype(int)

# investigation variable
df2["rat_present"] = (df2["rat_minutes"] > 0).astype(int)

# cleaning log
print("\n--- CLEANING LOG ---")
print("Rows after cleaning:", len(df2))
print("Rat present (0/1):", df2["rat_present"].value_counts(dropna=False).to_dict())

print("\nNumeric summaries:")
print(df2[["hours_after_sunset", "bat_landing_number", 
        "food_availability", "rat_minutes", "rat_arrival_number"]].describe())

# save cleaned data
df2.to_csv("Dataset2_clean.csv", index=False)
print("\nSaved: Dataset2_clean.csv")