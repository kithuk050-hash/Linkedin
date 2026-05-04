# Quick Start Guide - LinkedIn Job Scraper

## 5-Minute Setup

### Step 1: Get Your LinkedIn API Token (5 mins)

1. Go to https://www.linkedin.com/developers
2. Sign in with LinkedIn
3. Click **Create app** → Fill form → Submit
4. Go to **Auth** tab
5. Copy your **Access Token** (or generate one)

### Step 2: Setup Files (1 min)

```bash
cd /Users/kishore/Desktop/spark-expectations

# Create .env file with your token
cp .env.example .env

# Edit .env and add your Access Token
# Use: nano .env  or  vim .env  or open in VS Code
```

### Step 3: Install & Run (2 mins)

```bash
# Install dependencies
pip install -r requirements_linkedin_scraper.txt

# Run the basic scraper
python linkedin_job_scraper.py

# OR run the enhanced version
python linkedin_job_scraper_enhanced.py
```

### Step 4: View Results (1 min)

```bash
# A CSV file is created: data_engineer_jobs_YYYYMMDD_HHMMSS.csv

# Open in Excel (macOS)
open data_engineer_jobs_*.csv

# Or view with Python
python -c "import pandas as pd; df = pd.read_csv('data_engineer_jobs_*.csv'); print(df)"
```

---

## What You'll Get

📊 **CSV with these columns:**
- Job ID & Title
- Company Name
- Location (City & Country)
- Region (for India)
- Experience Required (5+ years)
- Job Type (Full-time, Contract, etc.)
- Required Skills
- Job Description
- Posted Date
- Direct LinkedIn URL

---

## File Overview

| File | Purpose |
|------|---------|
| `linkedin_job_scraper.py` | Basic scraper (easy to understand) |
| `linkedin_job_scraper_enhanced.py` | Advanced scraper (multi-location, analytics) |
| `.env.example` | Template for credentials |
| `requirements_linkedin_scraper.txt` | Python dependencies |
| `LINKEDIN_SCRAPER_README.md` | Full documentation |

---

## Troubleshooting

### ❌ "Missing LINKEDIN_ACCESS_TOKEN"

**Fix**: 
1. Check if `.env` file exists: `ls -la .env`
2. Edit it: `nano .env`
3. Add token and save

### ❌ "403 Forbidden Error"

**Fix**:
1. Go to LinkedIn Developer Portal
2. Generate a new Access Token
3. Update `.env` and retry

### ❌ "No jobs returned"

**Fix**:
1. Verify your token is valid
2. Try with "India" first (easier to find jobs)
3. Check if your token has job search permissions

---

## Next Steps

1. ✅ Setup credentials
2. ✅ Run scraper
3. ✅ Export to Excel
4. **Optional**: 
   - Import into database
   - Create dashboard with results
   - Set up scheduled jobs
   - Integrate with other tools

---

## API Rate Limits

- LinkedIn API: ~100 jobs per search
- Rate limit: ~300 requests/min (check your app settings)
- For more data: Make multiple searches with different filters

---

## Support

- LinkedIn Docs: https://learn.microsoft.com/en-us/linkedin/
- Python Errors: Check script comments
- Questions: Review LINKEDIN_SCRAPER_README.md

---

**Ready?** Run: `python linkedin_job_scraper_enhanced.py` 🚀
