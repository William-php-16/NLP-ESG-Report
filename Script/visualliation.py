import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px

# 1. Connect to the database and pull the aggregate data
conn = sqlite3.connect("C:\\Users\\user\\OneDrive\\ESG Project\\Output\\esg_portfolio.db")

query = """
SELECT 
    Company,
    Keyword,
    COUNT(*) as Total_Mentions,
    SUM(CASE WHEN Sentiment = 'POSITIVE' THEN 1 ELSE 0 END) as Positive_Count,
    ROUND(AVG(Confidence), 4) as Avg_AI_Confidence
FROM esg_reporting
GROUP BY Company, Keyword
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Calculate the Positivity Ratio (How often a keyword is discussed with a purely positive tone)
df['Positivity_Ratio'] = (df['Positive_Count'] / df['Total_Mentions']) * 100

# ---------------------------------------------------------
# VISUALIZATION 1: The Keyword Focus Bar Chart
# ---------------------------------------------------------
fig1 = px.bar(
    df, 
    x="Keyword", 
    y="Total_Mentions", 
    color="Company", 
    barmode="group",
    title="ESG Strategy Focus: Retail vs. Commodity vs. Cooperative",
    labels={"Total_Mentions": "Number of Mentions", "Keyword": "ESG Framework/Topic"},
    template="plotly_white"
)

# Show the interactive chart in VS Code
fig1.show()

# ---------------------------------------------------------
# VISUALIZATION 2: The Greenwashing Risk Matrix
# ---------------------------------------------------------
# This plots Volume of mentions vs. Positivity of tone. 
# High volume + 100% positive tone on difficult topics (like Scope 3) implies potential greenwashing.
fig2 = px.scatter(
    df, 
    x="Total_Mentions", 
    y="Positivity_Ratio", 
    color="Company", 
    size="Avg_AI_Confidence", # Dot size based on AI confidence
    hover_data=['Keyword'],   # Shows the keyword when you hover over the dot
    title="Greenwashing Risk Matrix (Volume vs. Tone)",
    labels={
        "Total_Mentions": "Discussion Volume (Mentions)", 
        "Positivity_Ratio": "Positivity Ratio (%)"
    },
    template="plotly_white"
)

# Customize the layout to make it look professional
fig2.update_layout(yaxis_range=[-5, 105])
fig2.show()

# ---------------------------------------------------------
# EXPORT FOR WEB
# ---------------------------------------------------------
# Save these interactive charts as HTML files
output_dir = Path("C:\\Users\\user\\OneDrive\\ESG Project\\Output\\Visual Figures")
output_dir.mkdir(parents=True, exist_ok=True)
fig1.write_html(output_dir / "chart_keyword_focus.html")
fig2.write_html(output_dir / "chart_risk_matrix.html")
print("Visualizations generated and saved as interactive HTML files!")