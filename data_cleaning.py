import pandas as pd

# =============================
# LOAD DATA FROM THE /data FOLDER
# =============================

dalys_df = pd.read_excel("data/DALY5yearsallcountries.xlsx")
deaths_df = pd.read_excel("data/Deaths5yearsallcountries.xlsx")

pm25_2015 = pd.read_excel("data/pm2.5_2015.xlsx")
pm25_2016 = pd.read_excel("data/pm2.5_2016.xlsx")
pm25_2017 = pd.read_excel("data/pm2.5_2017.xlsx")
pm25_2018 = pd.read_excel("data/pm2.5_2018.xlsx")
pm25_2019 = pd.read_excel("data/pm2.5_2019.xlsx")
# =============================
# CLEANING THE AIR POLLUTION DATA (PM2.5)
# =============================

# Combine PM2.5 data across all years (2015–2019)
pm25_all = pd.concat([
    clean_pm25_data(pm25_2015, 2015),
    clean_pm25_data(pm25_2016, 2016),
    clean_pm25_data(pm25_2017, 2017),
    clean_pm25_data(pm25_2018, 2018),
    clean_pm25_data(pm25_2019, 2019)
])

# Drop rows with missing or invalid country names (like headers or metadata)
pollution_df = pm25_all[pd.notnull(pm25_all["Country"]) & pd.notnull(pm25_all["PM2.5"])].copy()

# Ensure correct column types
pollution_df["Year"] = pollution_df["Year"].astype(int)
pollution_df["PM2.5"] = pollution_df["PM2.5"].astype(float)

# Preview result
print(pollution_df.head())

pollution_df.to_csv("pollution_df.csv", index=False)

# =============================
# CLEANING THE HEALTH DATA (DALY + Death Rates)
# =============================

# Keep only rows where sex is Both and age group is All ages for both DALY and Death datasets
def clean_health_data(df, label):
    df = df[
        (df["Sex"] == "Both") &
        (df["Age group"] == "All ages")
    ].copy()
    df = df[["Country/ territory/ area", "Year", "GHE Cause", "Age-standardized rate"]]
    df.rename(columns={
        "Country/ territory/ area": "Country",
        "GHE Cause": "Cause",
        "Age-standardized rate": label
    }, inplace=True)
    return df

# Clean separately
dalys_df = clean_health_data(dalys_df, "DALY Rate")
deaths_df = clean_health_data(deaths_df, "Death Rate")

# Merge DALY and Death Rate data on Country, Year, and Disease Cause
health_df = pd.merge(dalys_df, deaths_df, on=["Country", "Year", "Cause"], how="inner")

# Preview result
print(health_df.head())

# OPTIONAL: Pivot version (e.g., diseases as columns)
# pivot_df = health_df.pivot_table(index=["Country", "Year"], columns="Cause", values="DALY Rate").reset_index()

health_df.to_csv("health_df.csv", index=False)
