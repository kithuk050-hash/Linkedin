# Data Engineer Job Summary - Quick Guide

## What This Does

This script generates a **comprehensive one-page summary table** showing:

✅ **India vs Outside India Comparison**
- Total job openings in India
- Total job openings outside India
- Breakdown by country

✅ **Regional Breakdown (India Only)**
- Openings by Indian region (South, North, West, East, etc.)

✅ **Required Skillset Summary**
- Top 10+ in-demand skills
- % of jobs requiring each skill

✅ **Top Hiring Companies**
- Companies with most Data Engineer openings

✅ **Job Level Distribution**
- Breakdown by seniority level

## Quick Start

### Step 1: Setup (if not already done)
```bash
cd /Users/kishore/Desktop/linkedin

# Install dependencies
pip install -r requirements_linkedin_scraper.txt

# Add openpyxl for Excel reports
pip install openpyxl

# Create .env with your LinkedIn API token
cp .env.example .env
# Edit .env and add your LINKEDIN_ACCESS_TOKEN
```

### Step 2: Run the Analysis
```bash
python data_engineer_summary.py
```

### Step 3: View Results
The script will:
1. 📊 Print a beautiful summary table in the terminal
2. 📁 Save an Excel file: `data_engineer_summary_YYYYMMDD_HHMMSS.xlsx`
3. 📋 Save a CSV file: `data_engineer_jobs_YYYYMMDD_HHMMSS.csv`

## Output Files

### 1. Excel Report (Recommended)
Multiple sheets:
- **Summary**: India vs Outside India overview
- **Required Skills**: All skills tracked with percentages
- **India Regions**: Regional breakdown
- **Top Companies**: Top 15 hiring companies
- **Job Levels**: Seniority distribution
- **All Jobs**: Detailed job listings

### 2. CSV File
Complete job details for further analysis in Excel, Pandas, etc.

## Sample Output Preview

```
================================================================================
                         INDIA VS OUTSIDE INDIA - OVERVIEW
================================================================================
Category            Type           Count  Percentage
Country: India      🇮🇳 India      245    65.0%
Country: US         🌎 International 95   25.3%
Region              🇮🇳 INDIA      245    65.0%
Region              🌎 OUTSIDE INDIA 130   35.0%

================================================================================
                           REQUIRED SKILLSET SUMMARY
================================================================================
Required Skill      Job Postings  Percentage
Python              185           49.3%
SQL                 178           47.4%
Spark               156           41.6%
AWS                 134           35.7%
ETL                 128           34.1%
...
```

## Customization

Edit the main() function in `data_engineer_summary.py` to:

### Change locations
```python
locations = ["India", "United States", "Canada", "Australia"]
```

### Change skills
```python
skills = ["Python", "Java", "Scala", "Kafka", "Flink"]
```

### Adjust experience level
Search for `"5", "6", "7"` in the code and modify accordingly

## Troubleshooting

- **LINKEDIN_ACCESS_TOKEN error**: Make sure .env file has your token
- **Connection error**: Check internet connection
- **Rate limit**: LinkedIn API has limits; try again in a few minutes
- **No results**: Try adjusting locations or skills

## Need Help?

Refer to:
- QUICK_START.md - API token setup
- SETUP_GUIDE.md - Detailed setup guide
- LINKEDIN_SCRAPER_README.md - API documentation
