SELECT 
    Company,
    Keyword,
    COUNT(*) as Mention_Count,
    ROUND(AVG(Confidence), 4) as Avg_AI_Confidence,
    Context_Snippet
FROM esg_reporting
WHERE Greenwashing_Risk = 'High'
  AND Keyword IN ('Scope 3', 'emissions reduced', 'carbon neutral')
GROUP BY Company, Keyword, Context_Snippet
ORDER BY Mention_Count DESC;

SELECT 
    Company,
    Keyword,
    SUM(Frequency) as Total_Mentions,
    SUM(CASE WHEN Sentiment = 'POSITIVE' THEN 1 ELSE 0 END) as Positive_Tone_Count,
    SUM(CASE WHEN Sentiment = 'NEGATIVE' THEN 1 ELSE 0 END) as Negative_Tone_Count,
    ROUND(CAST(SUM(CASE WHEN Sentiment = 'POSITIVE' THEN 1 ELSE 0 END) AS FLOAT) / 
          COUNT(*), 2) as Positivity_Ratio
FROM esg_reporting
GROUP BY Company, Keyword
ORDER BY Total_Mentions DESC;

SELECT 
    Company,
    Page_Number,
    Keyword,
    Sentiment,
    Context_Snippet
FROM esg_reporting
WHERE Confidence > 0.98
ORDER BY Page_Number ASC
LIMIT 10;