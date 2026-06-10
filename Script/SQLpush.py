import pandas as pd
import sqlite3

# 1. Connect to SQLite (This creates the database file in your main folder)
db_path = r"C:\Users\user\OneDrive\ESG Project\Output\esg_portfolio.db"
conn = sqlite3.connect(db_path)

print("Reading CSV files...")
# 2. Load the NLP results CSVs
# (Assuming you ran the NLP script for all three companies)
df_ad = pd.read_csv(r"C:\Users\user\OneDrive\ESG Project\Output\ahold_delhaize_nlp_results.csv")
df_jde = pd.read_csv(r"C:\Users\user\OneDrive\ESG Project\Output\jde_peets_nlp_results.csv")
df_rfc = pd.read_csv(r"C:\Users\user\OneDrive\ESG Project\Output\royal_frieslandcampina_nlp_results.csv")

# Combine them into one master dataframe if you have all three
print("Combining data...")
df_master = pd.concat([df_ad, df_jde, df_rfc], ignore_index=True)

print("Pushing combined data to the database...")
df_master.to_sql("esg_reporting", conn, if_exists="replace", index=False)

print(f"Success! Inserted {len(df_master)} total rows into the database.")
print("\nRow breakdown by company:")
print(df_master['Company'].value_counts())

conn.close()