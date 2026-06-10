# 1. Import Libraries
import pandas as pd
from transformers import pipeline
try:
    from IPython.display import display
except ImportError:
    display = print

# 2. Load the data from Phase 1
# Make sure this matches the filename you saved earlier
data_path = r"C:\Users\user\OneDrive\ESG Project\Output\jde_peets_esg_keywords.csv"
df_esg = pd.read_csv(data_path)

# 3. Initialize the NLP Pipeline
print("Downloading and loading the AI model (this may take a minute)...")
# We are using a standard, fast sentiment analysis model from Hugging Face
sentiment_analyzer = pipeline("sentiment-analysis")

# 4. Define a function to process the text
def analyze_greenwashing_risk(text):
    # The AI model has a limit of 512 tokens (words/subwords) per chunk
    # We truncate the text to ensure it doesn't crash the model
    truncated_text = str(text)[:500] 
    
    # Run the AI model
    result = sentiment_analyzer(truncated_text)[0]
    sentiment = result['label']       # POSITIVE or NEGATIVE
    confidence = result['score']      # 0.0 to 1.0
    
    # Flagging Logic:
    # If a company is talking about a serious issue like "Scope 3 emissions" 
    # but the AI detects a 99% POSITIVE sentiment, that is a red flag for 
    # greenwashing (glossing over the harsh reality of emissions).
    risk_flag = "High" if (sentiment == "POSITIVE" and confidence > 0.90) else "Low"
    
    return pd.Series([sentiment, confidence, risk_flag])

# 5. Apply the AI model to our extracted snippets
print("Analyzing text snippets for sentiment...")
df_esg[['Sentiment', 'Confidence', 'Greenwashing_Risk']] = df_esg['Context_Snippet'].apply(analyze_greenwashing_risk)

# 6. View the results
print(df_esg.head(10))

# 7. Save the enriched data for SQL Phase
df_esg.to_csv(r"C:\Users\user\OneDrive\ESG Project\Output\jde_peets_nlp_results.csv", index=False)
print("NLP Analysis complete! Data is ready for SQL.")