# Comparative Supply Chain & Greenwashing Sentiment Analysis

A Python and SQL pipeline that compares ESG disclosure quality across three major Dutch F&B companies — Ahold Delhaize, JDE Peet's, and Royal FrieslandCampina — and flags potential greenwashing through NLP-based sentiment analysis of their 2024–2025 annual reports.

---

## Background

ESG reporting has grown from a voluntary exercise into a regulatory expectation, yet the gap between what companies claim and what they can verify remains wide. This project was built to surface that gap programmatically. By extracting high-signal ESG keywords from official annual reports and running sentiment and confidence scoring on the surrounding context, the pipeline identifies passages where positive ESG language is used without measurable backing — the hallmark of greenwashing risk.

The three companies were chosen because they sit at different points of the same agri-food supply chain: Ahold Delhaize (retail), JDE Peet's (branded consumer goods), and Royal FrieslandCampina (upstream dairy and ingredients). Comparing their disclosures side by side reveals how sustainability narratives shift across the value chain.

---

## How It Works

1. **Extraction** — `ESG report.py` reads each annual report PDF and scans for a defined keyword list (Scope 3, deforestation, regenerative agriculture, circular economy, fair trade).
2. **NLP Scoring** — `nlp_sentiment.py` runs each keyword passage through a transformer-based sentiment classifier, returning a sentiment label (POSITIVE / NEGATIVE) and a confidence score.
3. **Database** — `SQLpush.py` pushes all results into a local SQLite database (`esg_portfolio.db`) for querying.
4. **Analysis** — `AnalystProject.sql` aggregates mention counts, sentiment splits, and greenwashing risk flags by company and keyword.
5. **Visualisation** — `visualliation.py` generates the interactive HTML charts; `ESG_Report.pdf` is the compiled one-page summary.

---

## Key Findings

- **Scope 3 emissions dominate Ahold Delhaize's disclosure** with 115 total mentions — the highest single-keyword count in the dataset. Despite the volume, 37.7% of those mentions carry high greenwashing risk, meaning the claims are aspirational rather than performance-verified.

- **JDE Peet's leads on deforestation volume** (109 mentions), consistent with its coffee and tea sourcing exposure. Its greenwashing risk share is the highest of the three (38.6%), concentrated in regenerative agriculture claims. A balanced 50/50 sentiment split suggests the company is still building credibility around these topics.

- **Royal FrieslandCampina shows the most conservative disclosure profile** — 27 total instances, the lowest high-risk share (29.6%), and the lowest average model confidence (90.1%). This may reflect tighter editorial control or genuinely narrower sustainability scope in the 2025 report.

- **Regenerative agriculture is the riskiest keyword category across all three companies.** It appears in forward-looking, aspirational contexts with little quantitative backing attached — making it the most scrutinised claim type for sustainability auditors and investors.

| Company | Total Mentions | Positive Sentiment | High-Risk Share | Avg. Confidence |
|---|---|---|---|---|
| Ahold Delhaize | 150 | 45.3% | 37.7% | 93.7% |
| JDE Peet's | 233 | 50.0% | 38.6% | 92.4% |
| Royal FrieslandCampina | 77 | 48.1% | 29.6% | 90.1% |

---

## Project Structure

```
ESG Project/
├── Data Raw/               ← Source annual report PDFs
├── Data Clean/             ← Aggregated CSVs for analysis
├── Output/                 ← NLP results, keyword CSVs, report, charts
│   └── Visual Figures/     ← Interactive HTML charts
├── Script/                 ← All pipeline scripts and SQL
└── README.md
```

---

## Data: Quick Access

### Raw Input (Annual Reports)
| Company | File |
|---|---|
| Ahold Delhaize | [ad-annual-report-2025-interactive.pdf](Data%20Raw/ad-annual-report-2025-interactive.pdf) |
| JDE Peet's | [jde-peets-annual-report-2025.pdf](Data%20Raw/jde-peets-annual-report-2025.pdf) |
| Royal FrieslandCampina | [Annual-Report_2025_Royal-FrieslandCampina-NV.pdf](Data%20Raw/Annual-Report_2025_Royal-FrieslandCampina-NV.pdf) |

### Clean / Aggregated Data
| File | Contents |
|---|---|
| [Company, Keyword, Mention Count, Avg AI Confidence](Data%20Clean/Company%2CKeyword%2CMention_Count%2CAvg_AI_Con.csv) | Mention totals and average model confidence per keyword |
| [Company, Keyword, Total Mentions, Positive %](Data%20Clean/Company%2CKeyword%2CTotal_Mentions%2CPositive_.csv) | Sentiment summary by company and keyword |
| [Company, Page, Keyword, Sentiment, Confidence](Data%20Clean/Company%2CPage_Number%2CKeyword%2CSentiment%2CCo.csv) | Full row-level NLP output |

### Output Files
| File | Contents |
|---|---|
| [ahold_delhaize_nlp_results.csv](Output/ahold_delhaize_nlp_results.csv) | Full NLP results — Ahold Delhaize |
| [jde_peets_nlp_results.csv](Output/jde_peets_nlp_results.csv) | Full NLP results — JDE Peet's |
| [royal_frieslandcampina_nlp_results.csv](Output/royal_frieslandcampina_nlp_results.csv) | Full NLP results — Royal FrieslandCampina |
| [ahold_delhaize_esg_keywords.csv](Output/ahold_delhaize_esg_keywords.csv) | Keyword extraction — Ahold Delhaize |
| [jde_peets_esg_keywords.csv](Output/jde_peets_esg_keywords.csv) | Keyword extraction — JDE Peet's |
| [royal_frieslandcampina_esg_keywords.csv](Output/royal_frieslandcampina_esg_keywords.csv) | Keyword extraction — Royal FrieslandCampina |
| [esg_portfolio.db](Output/esg_portfolio.db) | SQLite database — all results |
| [ESG_Report.pdf](Output/ESG_Report.pdf) | One-page visual summary report |

### Visual Figures
| File | Contents |
|---|---|
| [chart_keyword_focus.html](Output/Visual%20Figures/chart_keyword_focus.html) | Interactive keyword focus chart |
| [chart_risk_matrix.html](Output/Visual%20Figures/chart_risk_matrix.html) | Interactive greenwashing risk matrix |

---

## Scripts
| Script | Purpose |
|---|---|
| [ESG report.py](Script/ESG%20report.py) | PDF extraction and keyword scanning |
| [nlp_sentiment.py](Script/nlp_sentiment.py) | NLP sentiment scoring pipeline |
| [SQLpush.py](Script/SQLpush.py) | Push results to SQLite database |
| [AnalystProject.sql](Script/AnalystProject.sql) | Aggregation and risk queries |
| [visualliation.py](Script/visualliation.py) | Chart generation |
