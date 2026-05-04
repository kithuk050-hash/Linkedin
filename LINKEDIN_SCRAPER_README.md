# LinkedIn Data Engineer Job Scraper

A Python script to fetch Data Engineer job openings from LinkedIn API with 5+ years of experience requirements. Organizes jobs by country and region within India.

## Features

✅ Search for Data Engineer positions with 5+ years experience  
✅ Filter by required skills: Python, SQL, Spark, ETL, Data Warehousing  
✅ Support for multiple locations (India + international)  
✅ Regional breakdown for Indian jobs  
✅ CSV export with organized data  
✅ Summary statistics by country and region  

---

## Prerequisites

- Python 3.8+
- LinkedIn Developer Account
- LinkedIn API Access Token

---

## Step 1: Get LinkedIn API Credentials

### Option A: LinkedIn Official API (Recommended for Production)

1. Go to https://www.linkedin.com/developers
2. Sign in with your LinkedIn account
3. Click **Create app**
4. Fill in the required fields:
   - **App name**: e.g., "Data Engineer Job Scraper"
   - **LinkedIn Page**: Select or create one
   - **App logo**: Upload an image
   - **Legal agreement**: Accept terms
5. Go to **Auth** tab and copy:
   - `Client ID`
   - `Client Secret`
6. Generate **Access Token**:
   - Click "Auth" → "Generate access token"
   - Or set up OAuth 2.0 for production use

### Option B: Using LinkedIn OAuth 2.0

For production, implement OAuth 2.0 flow:
```
1. User logs in via LinkedIn
2. App receives authorization code
3. Exchange code for access token
4. Use token to make API requests
```

---

## Step 2: Setup Environment

### Clone/Copy Files

```bash
cd /Users/kishore/Desktop/spark-expectations

# Copy the example .env file
cp .env.example .env
```

### Update .env with Your Credentials

Edit `.env` and add your LinkedIn credentials:

```bash
LINKEDIN_CLIENT_ID=your_actual_client_id
LINKEDIN_CLIENT_SECRET=your_actual_client_secret
LINKEDIN_ACCESS_TOKEN=your_actual_access_token
```

⚠️ **Important**: Never commit `.env` to GitHub (it's in `.gitignore`)

---

## Step 3: Install Dependencies

```bash
pip install -r requirements_linkedin_scraper.txt
```

Or install individually:

```bash
pip install requests python-dotenv pandas
```

---

## Step 4: Run the Scraper

### Basic Usage

```bash
python linkedin_job_scraper.py
```

### Expected Output

```
============================================================
   LinkedIn Data Engineer Job Scraper
   Experience: 5+ years | Skills: Python, SQL, Spark, ETL
============================================================
✅ LinkedIn credentials loaded

🔍 Searching for 'Data Engineer' jobs in India...
   Experience: 5+ years
   Required Skills: Python, SQL, Spark, ETL, Data Warehousing

✅ Found 47 job openings

📋 Processing 47 jobs...

✅ Jobs saved to 'data_engineer_jobs_20240503_143022.csv'
   Total jobs: 47

📊 Summary by Country:
   India: 35 jobs
   United States: 8 jobs
   Singapore: 2 jobs
   United Kingdom: 2 jobs

📍 Summary by Region (India):
   South India: 15 jobs
   West India: 12 jobs
   North India: 8 jobs
```

---

## Step 5: View Results

The script generates a CSV file: `data_engineer_jobs_YYYYMMDD_HHMMSS.csv`

### CSV Columns

| Column | Description |
|--------|-------------|
| `job_id` | LinkedIn Job ID |
| `job_title` | Position title |
| `company_name` | Company name |
| `location` | City/Location |
| `country` | Country |
| `region` | Region (for India) |
| `job_level` | Seniority level |
| `job_type` | Full-time, Contract, etc. |
| `experience_required` | 5+ years |
| `required_skills` | Python, SQL, Spark, ETL, etc. |
| `description` | Job description (first 200 chars) |
| `posted_date` | When job was posted |
| `url` | LinkedIn job posting URL |

### Open in Excel

```bash
# macOS
open data_engineer_jobs_*.csv

# Linux
xdg-open data_engineer_jobs_*.csv

# Windows
start data_engineer_jobs_*.csv
```

---

## Advanced Usage

### Modify Search Parameters

Edit `linkedin_job_scraper.py` and change these values:

```python
self.keywords = "Data Engineer"  # Job title
self.locations = ["India", "United States"]  # Add more locations
self.skills = ["Python", "SQL", "Spark"]  # Add/remove skills
```

### Add More Countries

Update the `extract_country()` method:

```python
def extract_country(self, location: str) -> str:
    if "India" in location:
        return "India"
    elif "Germany" in location:
        return "Germany"
    # Add more...
```

---

## Limitations & Considerations

⚠️ **LinkedIn API Restrictions**:
- Official API has rate limits (check LinkedIn docs)
- Some job data may be limited based on your app permissions
- Requires approval for certain endpoints

⚠️ **Terms of Service**:
- Respect LinkedIn's ToS regarding scraping
- Don't republish data without permission
- Use only for personal/research purposes

### Alternative Approaches

If LinkedIn API access is limited:

1. **LinkedIn Job Board UI Scraping** (not recommended - violates ToS)
2. **Job APIs**:
   - Jooble API
   - RemoteOK API
   - GitHub Jobs API
   - Indeed API
3. **Manual Download**: Export jobs from LinkedIn's Job Search manually

---

## Troubleshooting

### Error: "Missing LinkedIn credentials"

**Solution**: Ensure `.env` file exists and has the correct credentials:

```bash
cat .env  # Verify content
```

### Error: "API returned 403 Forbidden"

**Solution**: Your access token may be expired or have insufficient permissions:
1. Generate a new access token from LinkedIn Developer Portal
2. Update `.env` file
3. Try again

### Error: "Connection timeout"

**Solution**: LinkedIn API may be temporarily unavailable:
1. Wait a few minutes and retry
2. Check your internet connection
3. Verify API endpoint URL

### No jobs returned

**Solution**: Search criteria might be too restrictive:
1. Check job keywords
2. Verify location codes (use LinkedIn UI to confirm)
3. Adjust experience level filter

---

## Next Steps

1. ✅ Get LinkedIn API credentials
2. ✅ Setup `.env` file
3. ✅ Run the scraper
4. ✅ View CSV results
5. **Optional**: Integrate with database, dashboards, or automation

---

## Support

For LinkedIn API issues, visit:
- LinkedIn Developer Docs: https://learn.microsoft.com/en-us/linkedin/
- LinkedIn Support: https://www.linkedin.com/help

For script issues, check the code comments or create an issue.

---

## License

This script is for educational purposes. Ensure compliance with LinkedIn's Terms of Service.
