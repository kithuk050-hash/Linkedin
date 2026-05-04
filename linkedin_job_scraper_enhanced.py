"""
Enhanced LinkedIn Job Scraper with Multi-Location Support
Fetch Data Engineer jobs with filtering by experience, skills, location
"""

import requests
import json
import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()


class EnhancedLinkedInJobScraper:
    """Enhanced LinkedIn job scraper with advanced filtering"""
    
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
        """
        Initialize scraper with custom locations and skills
        
        Args:
            locations: List of countries/regions to search
            skills: List of required skills
        """
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.base_url = "https://www.linkedin.com/voyager/api"
        
        # Custom parameters
        self.locations = locations or ["India"]
        self.skills = skills or ["Python", "SQL", "Spark", "ETL", "Data Warehousing"]
        self.keywords = "Data Engineer"
        self.experience_level = "5"  # 5+ years
        
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
                "experienceLevel": ["5", "6", "7"],  # 5+ years
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
    
    def contains_required_skills(self, job_description: str) -> bool:
        """Check if job contains at least one required skill"""
        description_lower = job_description.lower()
        return any(skill.lower() in description_lower for skill in self.skills)
    
    def parse_job_details(self, job: Dict, location: str) -> Optional[Dict]:
        """Extract and parse job details"""
        try:
            description = job.get("description", "")
            
            # Filter by required skills
            if not self.contains_required_skills(description):
                return None
            
            job_location = job.get("location", location)
            country = self.extract_country(job_location, location)
            region = self.extract_region(job_location) if country == "India" else ""
            
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
                "required_skills": ", ".join(self.skills),
                "description": description[:300],
                "posted_date": datetime.fromtimestamp(
                    int(job.get("postedDate", 0)) / 1000
                ).strftime("%Y-%m-%d") if job.get("postedDate") else "N/A",
                "url": f"https://www.linkedin.com/jobs/view/{job.get('id', '')}",
            }
            
            # Update stats
            self.stats["by_country"][country] += 1
            if region:
                self.stats["by_region"][region] += 1
            self.stats["by_company"][parsed["company_name"]] += 1
            self.stats["by_job_level"][parsed["job_level"]] += 1
            
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
    
    def save_to_csv(self, filename: Optional[str] = None) -> str:
        """Save jobs to CSV file"""
        if not self.jobs:
            print("❌ No jobs to save")
            return ""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_engineer_jobs_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = list(self.jobs[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.jobs)
            
            print(f"\n✅ Saved {len(self.jobs)} jobs to '{filename}'")
            return filename
        
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return ""
    
    def generate_analytics(self) -> pd.DataFrame:
        """Generate analytics DataFrame"""
        if not self.jobs:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.jobs)
        return df
    
    def print_detailed_summary(self):
        """Print detailed summary with analytics"""
        if not self.jobs:
            return
        
        print("\n" + "="*60)
        print("📊 DETAILED SUMMARY".center(60))
        print("="*60)
        
        print(f"\n📈 Total Jobs Found: {len(self.jobs)}")
        
        print("\n🌍 By Country:")
        for country, count in sorted(self.stats["by_country"].items(), 
                                     key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.jobs)) * 100
            print(f"   {country:20} {count:3} jobs ({percentage:5.1f}%)")
        
        print("\n📍 By Region (India Only):")
        for region, count in sorted(self.stats["by_region"].items(), 
                                    key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.jobs)) * 100
            print(f"   {region:20} {count:3} jobs ({percentage:5.1f}%)")
        
        print("\n🏢 Top 10 Companies:")
        for company, count in sorted(self.stats["by_company"].items(), 
                                     key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {company:30} {count:3} openings")
        
        print("\n💼 By Job Level:")
        for level, count in sorted(self.stats["by_job_level"].items(), 
                                   key=lambda x: x[1], reverse=True):
            print(f"   {level:20} {count:3} jobs")
        
        print("\n✅ Required Skills: " + ", ".join(self.skills))
        print("✅ Experience Required: 5+ years")
        print("="*60)
    
    def run(self) -> str:
        """Execute full scraping workflow"""
        print("\n" + "="*60)
        print("   ENHANCED LINKEDIN DATA ENGINEER JOB SCRAPER".center(60))
        print("="*60)
        
        if not self.access_token:
            print("❌ LINKEDIN_ACCESS_TOKEN not found in .env")
            return ""
        
        print(f"\n📋 Search Parameters:")
        print(f"   Keywords: {self.keywords}")
        print(f"   Experience: {self.experience_level}+ years")
        print(f"   Locations: {', '.join(self.locations)}")
        print(f"   Skills: {', '.join(self.skills)}")
        
        print(f"\n🚀 Starting search across {len(self.locations)} location(s)...\n")
        
        # Search all locations
        total_found = 0
        for location in self.locations:
            jobs = self.search_jobs_by_location(location)
            total_found += len(jobs)
            
            # Parse and filter jobs
            for job in jobs:
                parsed = self.parse_job_details(job, location)
                if parsed:
                    self.jobs.append(parsed)
        
        print(f"\n✅ Search complete. Found {total_found} total postings")
        print(f"✅ Filtered to {len(self.jobs)} jobs matching skills requirements\n")
        
        # Save and generate reports
        filename = self.save_to_csv()
        self.print_detailed_summary()
        
        return filename


def main():
    """Main entry point with example usage"""
    
    # Example 1: Search India only
    # locations = ["India"]
    
    # Example 2: Search India and US
    locations = ["India"]
    
    skills = ["Python", "SQL", "Spark", "ETL", "Data Warehousing"]
    
    scraper = EnhancedLinkedInJobScraper(locations=locations, skills=skills)
    csv_file = scraper.run()
    
    # Optional: Generate analytics
    if csv_file:
        print(f"\n💾 Load results with: pd.read_csv('{csv_file}')")


if __name__ == "__main__":
    main()
