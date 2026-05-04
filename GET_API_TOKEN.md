# 🚀 Setup Guide - Get Your LinkedIn API Token

This guide will help you get your **LinkedIn Access Token** in 5 minutes.

## Why Do You Need This?

Your Data Engineer job analysis script needs a LinkedIn API token to fetch real job data.

## Step 1: Create a LinkedIn Developer Account

1. Go to: **https://www.linkedin.com/developers/apps**
2. Sign in with your LinkedIn account (create one if needed)
3. Click **Create app**

## Step 2: Fill in the Application Details

Complete the form with:
- **App name**: `Data Engineer Analyzer` (or any name)
- **LinkedIn Page**: Select your LinkedIn page or create one
- **App description**: `Analyze Data Engineer job market trends`
- **App logo**: Upload any image (optional)
- **Legal agreement**: Check the box
- Click **Create app**

## Step 3: Get Your Access Token

### Option A: Quick Access Token (Recommended)
1. Go to the app you just created
2. Click on the **Auth** tab
3. Look for **User tokens** section
4. Click **Request access** or use existing token
5. Copy your **Access Token**

### Option B: Generate Access Token
1. In the **Auth** tab
2. Scroll to "Access tokens"
3. Click **Generate token**
4. Copy the token

⚠️ **IMPORTANT**: Your token is sensitive! Never share it publicly.

## Step 4: Add Token to Your .env File

1. Open the `.env` file in your editor:
   ```bash
   cd /Users/kishore/Desktop/linkedin
   nano .env
   # Or open in VS Code
   ```

2. Replace the placeholder with your actual token:
   ```
   LINKEDIN_ACCESS_TOKEN=your_actual_token_here_1234567890abcdef
   ```

3. Save the file (Ctrl+O, Enter, Ctrl+X for nano)

Example .env file:
```
# LinkedIn API Credentials
# Get these from: https://www.linkedin.com/developers

LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_ACCESS_TOKEN=AQEaR_d4F5x8KmL2ZvXpQw...
```

## Step 5: Run Your Analysis

Now you're ready to run the complete analysis!

```bash
cd /Users/kishore/Desktop/linkedin

# Run the analysis
python3 data_engineer_summary.py
```

## What Will Happen?

1. ✅ Script will search LinkedIn for Data Engineer jobs
2. ✅ Search locations: India, USA, UK, Canada, Singapore
3. ✅ Filter by required skills: Python, SQL, Spark, AWS, ETL, etc.
4. ✅ Collect 5+ years experience positions
5. ✅ Generate beautiful summary tables
6. ✅ Create Excel report: `data_engineer_summary_YYYYMMDD_HHMMSS.xlsx`
7. ✅ Create CSV backup: `data_engineer_jobs_YYYYMMDD_HHMMSS.csv`

## Output Files

### 📊 Excel Report (Recommended)
```
data_engineer_summary_YYYYMMDD_HHMMSS.xlsx
├── Summary Sheet → India vs Outside India overview
├── Required Skills Sheet → Top skills and percentages
├── India Regions Sheet → South/North/West/East breakdown
├── Top Companies Sheet → Companies with most openings
├── Job Levels Sheet → Senior/Mid/Lead distribution
└── All Jobs Sheet → Complete job listings
```

### 📋 CSV Report
```
data_engineer_jobs_YYYYMMDD_HHMMSS.csv
(All job details for further analysis)
```

## Customization

Want to change search parameters? Edit `data_engineer_summary.py`:

### Change Locations
Find the `main()` function and modify:
```python
locations = ["India", "United States", "Canada", "Australia"]
```

### Change Required Skills
```python
skills = ["Python", "Java", "Scala", "Kafka"]
```

### Change Experience Level
Search for `"5", "6", "7"` in the code (means 5+ years)

## Troubleshooting

### ❌ "LINKEDIN_ACCESS_TOKEN not found"
- Make sure `.env` file exists in `/Users/kishore/Desktop/linkedin/`
- Make sure it has `LINKEDIN_ACCESS_TOKEN=your_token_here`
- Restart the terminal/Python after editing

### ❌ "Connection timeout"
- Check your internet connection
- LinkedIn API might be rate limiting - try again in 5 minutes

### ❌ "No results found"
- Token might be invalid/expired - generate a new one
- Try with different locations or skills

### ❌ "ImportError: No module named 'openpyxl'"
```bash
pip3 install openpyxl pandas requests python-dotenv
```

## Need More Help?

1. **Quick Overview**: Read [DATA_ENGINEER_SUMMARY_GUIDE.md](DATA_ENGINEER_SUMMARY_GUIDE.md)
2. **Sample Output**: Run `python3 demo_report.py` to see example
3. **LinkedIn API Docs**: https://learn.microsoft.com/en-us/linkedin/

## First Time Setup Checklist

- [ ] LinkedIn Developer Account Created
- [ ] App Created at https://www.linkedin.com/developers/apps
- [ ] Access Token Generated
- [ ] Token Added to `.env` file
- [ ] Dependencies Installed: `pip3 install -r requirements_linkedin_scraper.txt`
- [ ] Run Demo: `python3 demo_report.py`
- [ ] Run Full Analysis: `python3 data_engineer_summary.py`

---

**You're all set! 🎉**

Ready to analyze the Data Engineer job market? Run:
```bash
python3 data_engineer_summary.py
```
