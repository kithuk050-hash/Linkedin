"""
LinkedIn Data Engineer Job Summary Report
Generates comprehensive table with India vs Outside India comparison
and required skillset details
"""

import requests
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from collections import defaultdict
import sys

load_dotenv()


class LinkedInDataEngineerAnalyzer:
    """Analyze Data Engineer jobs across India and International markets"""
    
    # Location mappings
    INDIA_CITIES = {
        "Bangalore": "South India",
        "Bengaluru": "South India",
        "Hyderabad": "South India",
        "Chennai": "South India",
        "Kochi": "South India",
        "Thiruvananthapuram": "South India",
        "Mumbai": "West India",
        "Pune": "West India",
        "Ahmedabad": "West India",
        "Vadodara": "West India",
        "Delhi": "North India",
        "Gurugram": "North India",
        "Gurgaon": "North India",
        "Noida": "North India",
        "Jaipur": "North India",
        "Kolkata": "East India",
        "Bhubaneswar": "East India",
    }
    
    COUNTRY_CODES = {
        "India": "in",
        "United States": "us",
        "United Kingdom": "gb",
        "Canada": "ca",
        "Singapore": "sg",
        "Germany": "de",
        "Australia": "au",
        "New Zealand": "nz",
    }
    
    def __init__(self, locations: List[str] = None, skills: List[str] = None):
        """Initialize analyzer"""
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = "https://www.linkedin.com/voyager/api"
        
        self.locations = locations or ["India", "United States", "United Kingdom", "Canada", "Singapore"]
        self.skills = skills or ["Python", "SQL", "Spark", "ETL", "Data Warehousing", "AWS", "Azure", "Hadoop", "Airflow"]
        self.keywords = "Data Engineer"
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        self.jobs = []
        self.stats = {
            "by_country": defaultdict(int),
            "by_region": defaultdict(int),
            "by_company": defaultdict(int),
            "by_job_level": defaultdict(int),
            "by_skills": defaultdict(int),
            "india_count": 0,
            "international_count": 0,
        }
    
    def get_location_code(self, location: str) -> str:
        """Get LinkedIn location code from country name"""
        return self.COUNTRY_CODES.get(location, location.lower()[:2])
    
    def search_jobs_by_location(self, location: str) -> List[Dict]:
        """Search jobs for a specific location"""
        try:
            location_code = self.get_location_code(location)
            url = f"{self.base_url}/jobs/search"
            
            params = {
                "keywords": self.keywords,
                "locationId": location_code,
                "experienceLevel": ["5", "6", "7"],
                "resultLimit": 100,
            }
            
            print(f"   🔍 Searching in {location}...", end=" ", flush=True)
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                jobs = response.json().get("elements", [])
                print(f"✓ Found {len(jobs)} jobs")
                return jobs
            else:
                print(f"✗ Error {response.status_code}")
                return []
        
        except Exception as e:
            print(f"✗ Error: {e}")
            return []
    
    def extract_skills_from_description(self, description: str) -> List[str]:
        """Extract mentioned skills from job description"""
        found_skills = []
        description_lower = description.lower()
        for skill in self.skills:
            if skill.lower() in description_lower:
                found_skills.append(skill)
        return found_skills
    
    def contains_required_skills(self, job_description: str) -> bool:
        """Check if job contains at least one required skill"""
        description_lower = job_description.lower()
        return any(skill.lower() in description_lower for skill in self.skills)
    
    def parse_job_details(self, job: Dict, location: str) -> Optional[Dict]:
        """Extract and parse job details"""
        try:
            description = job.get("description", "")
            
            if not self.contains_required_skills(description):
                return None
            
            job_location = job.get("location", location)
            country = self.extract_country(job_location, location)
            region = self.extract_region(job_location) if country == "India" else ""
            
            # Extract skills mentioned in this job
            mentioned_skills = self.extract_skills_from_description(description)
            
            parsed = {
                "job_id": job.get("id", ""),
                "job_title": job.get("title", "N/A"),
                "company_name": job.get("company", {}).get("name", "N/A"),
                "location": job_location,
                "country": country,
                "region": region,
                "job_level": job.get("seniority", [{}])[0].get("name", "N/A"),
                "job_type": job.get("type", "N/A"),
                "experience_required": "5+ years",
                "skills_mentioned": ", ".join(mentioned_skills),
                "description": description[:300],
                "posted_date": datetime.fromtimestamp(
                    int(job.get("postedDate", 0)) / 1000
                ).strftime("%Y-%m-%d") if job.get("postedDate") else "N/A",
                "url": f"https://www.linkedin.com/jobs/view/{job.get('id', '')}",
            }
            
            # Update statistics
            self.stats["by_country"][country] += 1
            if region:
                self.stats["by_region"][region] += 1
            self.stats["by_company"][parsed["company_name"]] += 1
            self.stats["by_job_level"][parsed["job_level"]] += 1
            
            if country == "India":
                self.stats["india_count"] += 1
            else:
                self.stats["international_count"] += 1
            
            # Track skills
            for skill in mentioned_skills:
                self.stats["by_skills"][skill] += 1
            
            return parsed
        
        except Exception as e:
            print(f"   ⚠️  Error parsing job: {e}")
            return None
    
    def extract_country(self, location: str, default: str = "") -> str:
        """Extract country from location"""
        for country in self.COUNTRY_CODES.keys():
            if country in location or country.lower() in location.lower():
                return country
        return default or "Other"
    
    def extract_region(self, location: str) -> str:
        """Extract region for India"""
        for city, region in self.INDIA_CITIES.items():
            if city in location or city.lower() in location.lower():
                return region
        return "Other"
    
    def generate_summary_table(self) -> pd.DataFrame:
        """Generate comprehensive summary table"""
        summary_data = []
        
        # Count by Country
        print("\n🌍 Generating Country Summary...")
        for country in self.locations:
            count = self.stats["by_country"].get(country, 0)
            location_type = "🇮🇳 India" if country == "India" else "🌎 International"
            summary_data.append({
                "Category": f"Country: {country}",
                "Type": location_type,
                "Count": count,
                "Percentage": f"{(count / len(self.jobs) * 100):.1f}%" if self.jobs else "0%"
            })
        
        # Summary by India vs International
        summary_data.append({
            "Category": "Region",
            "Type": "🇮🇳 INDIA",
            "Count": self.stats["india_count"],
            "Percentage": f"{(self.stats['india_count'] / len(self.jobs) * 100):.1f}%" if self.jobs else "0%"
        })
        
        summary_data.append({
            "Category": "Region",
            "Type": "🌎 OUTSIDE INDIA",
            "Count": self.stats["international_count"],
            "Percentage": f"{(self.stats['international_count'] / len(self.jobs) * 100):.1f}%" if self.jobs else "0%"
        })
        
        return pd.DataFrame(summary_data)
    
    def generate_skills_table(self) -> pd.DataFrame:
        """Generate required skills summary"""
        skills_data = []
        for skill, count in sorted(self.stats["by_skills"].items(), 
                                   key=lambda x: x[1], reverse=True):
            skills_data.append({
                "Required Skill": skill,
                "Job Postings": count,
                "Percentage": f"{(count / len(self.jobs) * 100):.1f}%" if self.jobs else "0%"
            })
        
        return pd.DataFrame(skills_data)
    
    def generate_regional_breakdown(self) -> pd.DataFrame:
        """Generate India regional breakdown"""
        regional_data = []
        for region, count in sorted(self.stats["by_region"].items(), 
                                    key=lambda x: x[1], reverse=True):
            regional_data.append({
                "Region": region,
                "Openings": count,
                "% of India": f"{(count / self.stats['india_count'] * 100):.1f}%" if self.stats['india_count'] > 0 else "0%"
            })
        
        return pd.DataFrame(regional_data)
    
    def generate_top_companies(self) -> pd.DataFrame:
        """Generate top hiring companies"""
        company_data = []
        for company, count in sorted(self.stats["by_company"].items(), 
                                     key=lambda x: x[1], reverse=True)[:15]:
            company_data.append({
                "Company": company,
                "Openings": count,
                "% of Total": f"{(count / len(self.jobs) * 100):.1f}%" if self.jobs else "0%"
            })
        
        return pd.DataFrame(company_data)
    
    def generate_job_level_breakdown(self) -> pd.DataFrame:
        """Generate job level breakdown"""
        level_data = []
        for level, count in sorted(self.stats["by_job_level"].items(), 
                                   key=lambda x: x[1], reverse=True):
            level_data.append({
                "Job Level": level,
                "Openings": count,
                "% of Total": f"{(count / len(self.jobs) * 100):.1f}%" if self.jobs else "0%"
            })
        
        return pd.DataFrame(level_data)
    
    def print_executive_summary(self):
        """Print executive summary with all tables"""
        if not self.jobs:
            print("❌ No jobs found")
            return
        
        print("\n" + "="*80)
        print("📊 LINKEDIN DATA ENGINEER JOBS - EXECUTIVE SUMMARY REPORT".center(80))
        print("="*80)
        
        print(f"\n✅ Total Jobs Found: {len(self.jobs)}")
        print(f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. Overview Table
        print("\n" + "-"*80)
        print("1️⃣  INDIA VS OUTSIDE INDIA - OVERVIEW".center(80))
        print("-"*80)
        overview_df = self.generate_summary_table()
        print(overview_df.to_string(index=False))
        
        # 2. Regional Breakdown for India
        if self.stats["india_count"] > 0:
            print("\n" + "-"*80)
            print("2️⃣  INDIA - REGIONAL BREAKDOWN".center(80))
            print("-"*80)
            regional_df = self.generate_regional_breakdown()
            print(regional_df.to_string(index=False))
        
        # 3. Required Skills
        print("\n" + "-"*80)
        print("3️⃣  REQUIRED SKILLSET SUMMARY".center(80))
        print("-"*80)
        skills_df = self.generate_skills_table()
        print(skills_df.to_string(index=False))
        
        # 4. Top Companies
        print("\n" + "-"*80)
        print("4️⃣  TOP HIRING COMPANIES".center(80))
        print("-"*80)
        companies_df = self.generate_top_companies()
        print(companies_df.to_string(index=False))
        
        # 5. Job Level
        print("\n" + "-"*80)
        print("5️⃣  JOB LEVEL DISTRIBUTION".center(80))
        print("-"*80)
        level_df = self.generate_job_level_breakdown()
        print(level_df.to_string(index=False))
        
        print("\n" + "="*80)
        print(f"🎯 Experience Required: 5+ years")
        print(f"🛠️  Skills Searched: {', '.join(self.skills)}")
        print("="*80)
    
    def save_detailed_report(self) -> str:
        """Save detailed report to Excel with multiple sheets"""
        if not self.jobs:
            print("❌ No jobs to save")
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_engineer_summary_{timestamp}.xlsx"
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Sheet 1: Summary Overview
                summary_df = self.generate_summary_table()
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Sheet 2: Skills Required
                skills_df = self.generate_skills_table()
                skills_df.to_excel(writer, sheet_name='Required Skills', index=False)
                
                # Sheet 3: India Regional Breakdown
                if self.stats["india_count"] > 0:
                    regional_df = self.generate_regional_breakdown()
                    regional_df.to_excel(writer, sheet_name='India Regions', index=False)
                
                # Sheet 4: Top Companies
                companies_df = self.generate_top_companies()
                companies_df.to_excel(writer, sheet_name='Top Companies', index=False)
                
                # Sheet 5: Job Level Distribution
                level_df = self.generate_job_level_breakdown()
                level_df.to_excel(writer, sheet_name='Job Levels', index=False)
                
                # Sheet 6: All Job Details
                jobs_df = pd.DataFrame(self.jobs)
                jobs_df.to_excel(writer, sheet_name='All Jobs', index=False)
            
            print(f"\n✅ Report saved to: {filename}")
            return filename
        
        except ImportError:
            print("⚠️  openpyxl not installed. Saving as CSV instead...")
            return self.save_to_csv()
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return ""
    
    def save_to_csv(self) -> str:
        """Save job details to CSV"""
        if not self.jobs:
            print("❌ No jobs to save")
            return ""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data_engineer_jobs_{timestamp}.csv"
        
        try:
            jobs_df = pd.DataFrame(self.jobs)
            jobs_df.to_csv(filename, index=False)
            print(f"✅ Jobs saved to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return ""
    
    def run(self) -> str:
        """Execute full analysis workflow"""
        print("\n" + "="*80)
        print("📊 LINKEDIN DATA ENGINEER JOB ANALYSIS".center(80))
        print("="*80)
        
        if not self.access_token:
            print("❌ LINKEDIN_ACCESS_TOKEN not found in .env file")
            print("📖 Please follow QUICK_START.md to setup your API token")
            return ""
        
        print(f"\n📋 Search Parameters:")
        print(f"   Keywords: {self.keywords}")
        print(f"   Experience: 5+ years")
        print(f"   Locations: {', '.join(self.locations)}")
        print(f"   Skills Tracked: {', '.join(self.skills)}")
        
        print(f"\n🚀 Starting analysis across {len(self.locations)} location(s)...\n")
        
        # Search all locations
        total_found = 0
        for location in self.locations:
            jobs = self.search_jobs_by_location(location)
            total_found += len(jobs)
            
            for job in jobs:
                parsed = self.parse_job_details(job, location)
                if parsed:
                    self.jobs.append(parsed)
        
        print(f"\n✅ Search complete. Found {total_found} total postings")
        print(f"✅ Filtered to {len(self.jobs)} jobs matching skills requirements")
        
        if self.jobs:
            # Generate reports
            self.print_executive_summary()
            self.save_detailed_report()
            self.save_to_csv()
        
        return filename if self.jobs else ""


def main():
    """Main entry point"""
    
    # Configure search parameters
    locations = ["India", "United States", "United Kingdom", "Canada", "Singapore"]
    skills = ["Python", "SQL", "Spark", "ETL", "Data Warehousing", "AWS", "Azure", "Hadoop", "Airflow", "BigQuery"]
    
    analyzer = LinkedInDataEngineerAnalyzer(locations=locations, skills=skills)
    analyzer.run()


if __name__ == "__main__":
    main()
