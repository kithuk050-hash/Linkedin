"""
Demo version - Shows sample output without needing API token
Run this to see what the final report will look like
"""

import pandas as pd
from datetime import datetime
from io import StringIO
import os

def generate_demo_report():
    """Generate demo report with sample data"""
    
    # Sample Data
    jobs_sample = [
        {"job_id": "1", "job_title": "Data Engineer", "company_name": "Google", "country": "India", "region": "South India", "skills_mentioned": "Python, SQL, Spark"},
        {"job_id": "2", "job_title": "Senior Data Engineer", "company_name": "Microsoft", "country": "United States", "region": "", "skills_mentioned": "Python, SQL, Spark, AWS"},
        {"job_id": "3", "job_title": "Data Engineer", "company_name": "Amazon", "country": "India", "region": "West India", "skills_mentioned": "Python, SQL, ETL"},
        {"job_id": "4", "job_title": "Data Engineer", "company_name": "Netflix", "country": "United States", "region": "", "skills_mentioned": "Python, Scala, Kafka"},
        {"job_id": "5", "job_title": "Data Engineer", "company_name": "Flipkart", "country": "India", "region": "South India", "skills_mentioned": "Python, SQL, Hadoop"},
    ]
    
    # Sample Statistics
    print("\n" + "="*80)
    print("📊 LINKEDIN DATA ENGINEER JOBS - EXECUTIVE SUMMARY REPORT (SAMPLE)".center(80))
    print("="*80)
    
    print(f"\n✅ Total Jobs Found: 375")
    print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Overview Table
    print("\n" + "-"*80)
    print("1️⃣  INDIA VS OUTSIDE INDIA - OVERVIEW".center(80))
    print("-"*80)
    overview_data = {
        "Category": ["Country: India", "Country: United States", "Country: United Kingdom", "Region", "Region"],
        "Type": ["🇮🇳 India", "🌎 International", "🌎 International", "🇮🇳 INDIA", "🌎 OUTSIDE INDIA"],
        "Count": [245, 95, 35, 245, 130],
        "Percentage": ["65.3%", "25.3%", "9.3%", "65.3%", "34.7%"]
    }
    overview_df = pd.DataFrame(overview_data)
    print(overview_df.to_string(index=False))
    
    # 2. India Regional Breakdown
    print("\n" + "-"*80)
    print("2️⃣  INDIA - REGIONAL BREAKDOWN".center(80))
    print("-"*80)
    regional_data = {
        "Region": ["South India", "West India", "North India", "East India"],
        "Openings": [98, 87, 45, 15],
        "% of India": ["40.0%", "35.5%", "18.4%", "6.1%"]
    }
    regional_df = pd.DataFrame(regional_data)
    print(regional_df.to_string(index=False))
    
    # 3. Required Skills
    print("\n" + "-"*80)
    print("3️⃣  REQUIRED SKILLSET SUMMARY".center(80))
    print("-"*80)
    skills_data = {
        "Required Skill": ["Python", "SQL", "Spark", "AWS", "ETL", "Data Warehousing", "Azure", "Hadoop", "Airflow", "BigQuery"],
        "Job Postings": [285, 278, 185, 167, 145, 128, 95, 78, 65, 58],
        "Percentage": ["76.0%", "74.1%", "49.3%", "44.5%", "38.7%", "34.1%", "25.3%", "20.8%", "17.3%", "15.5%"]
    }
    skills_df = pd.DataFrame(skills_data)
    print(skills_df.to_string(index=False))
    
    # 4. Top Companies
    print("\n" + "-"*80)
    print("4️⃣  TOP HIRING COMPANIES".center(80))
    print("-"*80)
    companies_data = {
        "Company": ["Google", "Amazon", "Microsoft", "Flipkart", "Jio", "Goldman Sachs", "McKinsey", "Infosys", "TCS", "IBM"],
        "Openings": [28, 24, 22, 18, 15, 14, 12, 11, 10, 9],
        "% of Total": ["7.5%", "6.4%", "5.9%", "4.8%", "4.0%", "3.7%", "3.2%", "2.9%", "2.7%", "2.4%"]
    }
    companies_df = pd.DataFrame(companies_data)
    print(companies_df.to_string(index=False))
    
    # 5. Job Level
    print("\n" + "-"*80)
    print("5️⃣  JOB LEVEL DISTRIBUTION".center(80))
    print("-"*80)
    level_data = {
        "Job Level": ["Senior", "Mid-Level", "Lead", "Principal", "Staff"],
        "Openings": [165, 142, 48, 15, 5],
        "% of Total": ["44.0%", "37.9%", "12.8%", "4.0%", "1.3%"]
    }
    level_df = pd.DataFrame(level_data)
    print(level_df.to_string(index=False))
    
    print("\n" + "="*80)
    print(f"🎯 Experience Required: 5+ years")
    print(f"🛠️  Skills Searched: Python, SQL, Spark, ETL, Data Warehousing, AWS, Azure, Hadoop, Airflow, BigQuery")
    print("="*80)
    
    # Save as Excel
    print("\n💾 Saving Excel Report...")
    try:
        with pd.ExcelWriter("data_engineer_summary_DEMO.xlsx", engine='openpyxl') as writer:
            overview_df.to_excel(writer, sheet_name='Summary', index=False)
            regional_df.to_excel(writer, sheet_name='India Regions', index=False)
            skills_df.to_excel(writer, sheet_name='Required Skills', index=False)
            companies_df.to_excel(writer, sheet_name='Top Companies', index=False)
            level_df.to_excel(writer, sheet_name='Job Levels', index=False)
        
        print("✅ Demo Excel report saved: data_engineer_summary_DEMO.xlsx")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_demo_report()
