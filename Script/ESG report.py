# 1. Import Libraries
import pdfplumber
import pandas as pd
import re

# 2. Define file paths and keywords
# Update this path to match exactly where your file is saved
pdf_path = r"C:\Users\user\OneDrive\ESG Project\Data Raw\jde-peets-annual-report-2025.pdf"

# These are the concrete actions vs. buzzwords we want to track
esg_keywords = [
    "Scope 3", 
    "regenerative agriculture", 
    "circular economy", 
    "emissions reduced",
    "carbon neutral",
    "small farmers",
    "deforestation",
    "fair trade"
]

extracted_data = []

# 3. Open the PDF and extract text
print("Opening PDF...")
with pdfplumber.open(pdf_path) as pdf:
    # For testing, just look at the first 50 pages to save time. 
    # Later, you can change this to look at the specific "Sustainability Statements" pages.
    for i, page in enumerate(pdf.pages[:165-179]):
        text = page.extract_text()
        
        if text:
            # Clean the text (remove extra line breaks)
            clean_text = text.replace('\n', ' ')
            
            # 4. Search for our keywords on this page
            for keyword in esg_keywords:
                # Count how many times the keyword appears on the page (case-insensitive)
                count = len(re.findall(keyword, clean_text, re.IGNORECASE))
                
                if count > 0:
                    match = re.search(keyword, clean_text, re.IGNORECASE)
                    start = max(0, match.start() - 100)
                    end = min(len(clean_text), match.end() + 100)
                    snippet = clean_text[start:end]

                    extracted_data.append({
                        "Company": "JDE Peet's",
                        "Page_Number": i + 1,
                        "Keyword": keyword,
                        "Frequency": count,
                        "Context_Snippet": snippet
                    })

# 5. Convert findings to a structured DataFrame
df_esg = pd.DataFrame(extracted_data)

# Display the first few rows
print(df_esg.head())

# 6. Save to CSV for Phase 2 (SQL)
if df_esg.empty:
    print("Warning: No keywords found in the first 50 pages.")
else:
    df_esg.to_csv(r"C:\Users\user\OneDrive\ESG Project\Output\jde_peets_esg_keywords.csv", index=False)
    print("Extraction complete and saved to CSV!")