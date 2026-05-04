# LinkedIn Data Engineer Job Scraper - Complete Setup Guide

## 📋 What You Have

You now have a complete LinkedIn job scraping solution with 5+ files:

### 🎯 Core Files

1. **linkedin_job_scraper.py** (8.4 KB)
   - Basic scraper for beginners
   - Search for Data Engineer jobs
   - Filter by 5+ years experience
   - Output: CSV file

2. **linkedin_job_scraper_enhanced.py** (11 KB)
   - Advanced scraper with multi-location support
   - Better filtering and analytics
   - Detailed reporting by region, country, company
   - Recommended for production use

3. **test_setup.py** (7.3 KB)
   - Verify your setup before running scraper
   - Check credentials, packages, files, API connection
   - Diagnose issues automatically

### 📚 Configuration Files

4. **.env.example** (278 B)
   - Template for API credentials
   - Copy to `.env` and fill in your tokens

5. **requirements_linkedin_scraper.txt** (52 B)
   - Python package dependencies
   - Install with: `pip install -r requirements_linkedin_scraper.txt`

### 📖 Documentation

6. **LINKEDIN_SCRAPER_README.md** (Full detailed guide)
7. **QUICK_START.md** (5-minute setup)
8. **SETUP_GUIDE.md** (This file - comprehensive overview)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Get LinkedIn API Credentials

1. Go to https://www.linkedin.com/developers
2. Click **Create app** (or use existing)
3. Go to **Auth** tab
4. Copy your **Access Token**

### Step 2: Setup Configuration

```bash
cd /Users/kishore/Desktop/spark-expectations

# Create .env file
cp .env.example .env

# Edit and add your Access Token
# Use VS Code: code .env
# Or terminal: nano .env
```

Add to `.env`:
```
LINKEDIN_ACCESS_TOKEN=your_actual_token_here
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
```

### Step 3: Verify Setup

```bash
python test_setup.py
```

Expected output:
```
✅ Environment (.env) - PASS
✅ Python Packages - PASS
✅ Scraper Files - PASS
✅ Imports - PASS
✅ LinkedIn API Connection - PASS

🎉 ALL CHECKS PASSED!
```

### Step 4: Run Scraper

**Basic version:**
```bash
python linkedin_job_scraper.py
```

**Enhanced version (recommended):**
```bash
python linkedin_job_scraper_enhanced.py
```

### Step 5: View Results

```bash
# File is created: data_engineer_jobs_YYYYMMDD_HHMMSS.csv

# Open in Excel (macOS)
open data_engineer_jobs_*.csv

# Or view with Python
python -c "import pandas as pd; print(pd.read_csv('data_engineer_jobs_*.csv'))"
```

---

## 📊 What Data You Get

### CSV Columns

```
job_id              - LinkedIn Job ID
job_title           - Position title (e.g., "Senior Data Engineer")
company_name        - Company name
location            - City/location
country             - Country (India, USA, etc.)
region              - Region (for India: South, West, North, East)
job_level           - Seniority level
job_type            - Full-time, Contract, etc.
experience_required - Minimum experience (5+ years)
required_skills     - Python, SQL, Spark, ETL, etc.
description         - Job description (first 300 chars)
posted_date         - When posted (YYYY-MM-DD)
url                 - Direct LinkedIn job URL
```

### Example Output

```
job_title: "Senior Data Engineer"
company_name: "Tech Company India"
location: "Bangalore, Karnataka, India"
country: "India"
region: "South India"
experience_required: "5+ years"
url: "https://www.linkedin.com/jobs/view/12345678"
```

---

## 🎯 Features Comparison

| Feature | Basic Scraper | Enhanced Scraper |
|---------|---------------|------------------|
| Single location search | ✅ | ✅ |
| Multi-location search | ❌ | ✅ |
| Skill filtering | Basic | Advanced |
| Regional analysis | ❌ | ✅ (India) |
| Company statistics | ❌ | ✅ |
| Job level breakdown | ❌ | ✅ |
| Error handling | Basic | Comprehensive |
| Analytics export | CSV only | CSV + DataFrame |
| Documentation | Moderate | Extensive |

---

## 🔧 Advanced Usage

### Search Multiple Locations

Edit `linkedin_job_scraper_enhanced.py`:

```python
locations = ["India", "United States", "Singapore", "United Kingdom"]
```

### Add/Change Skills

```python
skills = ["Python", "SQL", "Spark", "Apache Kafka", "AWS"]
```

### Change Job Title

```python
self.keywords = "Data Scientist"  # or "Machine Learning Engineer"
```

### Customize Experience Level

```python
# In the search params:
"experienceLevel": ["5", "6", "7"],  # Change to [3, 4, 5] for 3+ years
```

---

## 📝 File Structure

```
spark-expectations/
├── linkedin_job_scraper.py              (Basic scraper)
├── linkedin_job_scraper_enhanced.py     (Advanced scraper)
├── test_setup.py                         (Setup verification)
├── .env.example                          (Config template)
├── requirements_linkedin_scraper.txt     (Dependencies)
├── LINKEDIN_SCRAPER_README.md           (Full documentation)
├── QUICK_START.md                        (5-min setup)
├── SETUP_GUIDE.md                        (This file)
└── data_engineer_jobs_*.csv             (Generated results)
```

---

## ⚡ Troubleshooting

### Problem: "LINKEDIN_ACCESS_TOKEN not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# If not found:
cp .env.example .env

# Edit and add token
nano .env  # or use VS Code
```

### Problem: "API returned 403 Forbidden"

**Solution:**
1. Your token is expired or invalid
2. Generate new token from LinkedIn Developer Portal
3. Update `.env` with new token
4. Run: `python test_setup.py`

### Problem: "No jobs found"

**Solution:**
1. Check if token is valid: `python test_setup.py`
2. Try different keywords
3. Check location codes
4. Verify API permissions

### Problem: "Connection timeout"

**Solution:**
1. Check internet connection
2. LinkedIn API may be down
3. Try again in a few minutes
4. Check firewall/proxy settings

---

## 📈 What's Next?

After getting your data:

### 1. **Analyze Results**
```python
import pandas as pd

df = pd.read_csv('data_engineer_jobs_*.csv')
print(df.groupby('country').size())
print(df.groupby('region').size())
print(df['company_name'].value_counts().head(10))
```

### 2. **Create Visualizations**
```python
import matplotlib.pyplot as plt

df['country'].value_counts().plot(kind='bar')
plt.title('Jobs by Country')
plt.show()
```

### 3. **Export to Database**
```python
import sqlite3

conn = sqlite3.connect('jobs.db')
df.to_sql('data_engineer_jobs', conn, if_exists='replace')
```

### 4. **Create Dashboard**
- Use Tableau, PowerBI, or Streamlit
- Visualize jobs by location, company, skills
- Track trends over time

### 5. **Schedule Periodic Runs**
```bash
# Run scraper daily
crontab -e
# Add: 0 9 * * * cd /Users/kishore/Desktop/spark-expectations && python linkedin_job_scraper_enhanced.py
```

---

## 📚 Documentation Files

1. **QUICK_START.md** → Start here (5 mins)
2. **SETUP_GUIDE.md** → This file (comprehensive)
3. **LINKEDIN_SCRAPER_README.md** → Full reference guide
4. **Code comments** → Read the `.py` files for detailed explanations

---

## 🔐 Security Notes

⚠️ **Important:**
- Never commit `.env` to Git (it contains secrets)
- `.env` should be in `.gitignore` (already is if using standard Python setup)
- Don't share your Access Token
- Keep credentials private

---

## 🎓 Learning Resources

### LinkedIn API
- https://learn.microsoft.com/en-us/linkedin/
- https://www.linkedin.com/developers/

### Python Libraries Used
- **requests**: HTTP requests → https://requests.readthedocs.io/
- **python-dotenv**: Environment variables → https://python-dotenv.readthedocs.io/
- **pandas**: Data analysis → https://pandas.pydata.org/
- **csv**: CSV handling → https://docs.python.org/3/library/csv.html

### Data Analysis
- Pandas Tutorial: https://pandas.pydata.org/docs/user_guide/
- Matplotlib: https://matplotlib.org/
- Streamlit: https://streamlit.io/

---

## 📞 Support

### If You Get Stuck

1. **Check test results**: `python test_setup.py`
2. **Read error messages carefully** - they usually tell you what's wrong
3. **Check the documentation files**
4. **Review code comments** in the `.py` files

### Common Issues

- Token expired → Generate new one
- No jobs found → Verify search parameters
- API error 403 → Check token permissions
- Import error → Run `pip install -r requirements_linkedin_scraper.txt`

---

## ✅ Checklist

Before running:

- [ ] Got LinkedIn API Access Token
- [ ] Created `.env` file with credentials
- [ ] Installed dependencies: `pip install -r requirements_linkedin_scraper.txt`
- [ ] Ran setup verification: `python test_setup.py`
- [ ] Read this guide and QUICK_START.md

Ready? 🚀

```bash
python linkedin_job_scraper_enhanced.py
```

---

## 📞 Next Steps

1. **Setup**: Follow steps above ✅
2. **Verify**: Run `python test_setup.py`
3. **Execute**: Run `python linkedin_job_scraper_enhanced.py`
4. **Analyze**: Open generated CSV file
5. **Extend**: Add your own features/analysis

---

**Happy Scraping! 🎉**

*For detailed technical documentation, see LINKEDIN_SCRAPER_README.md*
