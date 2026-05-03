"""
LinkedIn Job Scraper - Fetch Data Engineer jobs with 5+ years experience
Supports India and international locations
Output: CSV file with job details organized by region/country
"""

import requests
import json
import csv
from datetime import datetime
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LinkedInJobScraper:
    """Scrape job openings from LinkedIn API"""
    
    def __init__(self):
        # LinkedIn API credentials (set these in .env file)
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
        self.access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        
        # Base URL for LinkedIn API
        self.base_url = "https://www.linkedin.com/voyager/api"
        
        # Job search parameters
        self.keywords = "Data Engineer"
        self.experience_level = "5"  # 5+ years
        self.locations = ["India"]  # Can be expanded
        self.skills = ["Python", "SQL", "Spark", "ETL", "Data Warehousing"]
        
        # Headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        self.jobs = []
    
    def validate_credentials(self) -> bool:
        """Validate LinkedIn API credentials"""
        if not all([self.client_id, self.client_secret, self.access_token]):
            print("❌ Missing LinkedIn credentials. Set LINKEDIN_ACCESS_TOKEN in .env file")
            return False
        print("✅ LinkedIn credentials loaded")
        return True
    
    def search_jobs(self) -> List[Dict]:
        """
        Search for Data Engineer jobs using LinkedIn API
        Note: This uses the Jobs Search endpoint
        """
        try:
            # LinkedIn Jobs Search API endpoint
            url = f"{self.base_url}/jobs/search"
            
            params = {
                "keywords": self.keywords,
                "locationId": "in",  # India
                "experienceLevel": ["5", "6", "7"],  # 5+ years experience
                "resultLimit": 100,
                "start": 0
            }
            
            print(f"\n🔍 Searching for '{self.keywords}' jobs in {self.locations[0]}...")
            print(f"   Experience: {self.experience_level}+ years")
            print(f"   Required Skills: {', '.join(self.skills)}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("elements", [])
                print(f"✅ Found {len(jobs)} job openings")
                return jobs
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                return []
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return []
    
    def parse_job_details(self, job: Dict) -> Dict:
        """Extract relevant job details"""
        try:
            return {
                "job_id": job.get("id", "N/A"),
                "job_title": job.get("title", "N/A"),
                "company_name": job.get("company", {}).get("name", "N/A"),
                "location": job.get("location", "N/A"),
                "country": self.extract_country(job.get("location", "")),
                "region": self.extract_region(job.get("location", "")),
                "job_level": job.get("level", "N/A"),
                "job_type": job.get("employmentType", "N/A"),
                "experience_required": "5+ years",
                "description": job.get("description", "N/A")[:200],  # First 200 chars
                "posted_date": job.get("postedDate", "N/A"),
                "url": f"https://www.linkedin.com/jobs/view/{job.get('id', '')}",
                "required_skills": ", ".join(self.skills)
            }
        except Exception as e:
            print(f"⚠️  Error parsing job: {e}")
            return None
    
    def extract_country(self, location: str) -> str:
        """Extract country from location string"""
        if "India" in location:
            return "India"
        elif "United States" in location or "USA" in location:
            return "United States"
        elif "United Kingdom" in location:
            return "United Kingdom"
        elif "Singapore" in location:
            return "Singapore"
        elif "Canada" in location:
            return "Canada"
        elif "Germany" in location:
            return "Germany"
        else:
            return location.split(",")[-1].strip() if "," in location else "Other"
    
    def extract_region(self, location: str) -> str:
        """Extract region from location"""
        india_regions = {
            "Bangalore": "South India",
            "Hyderabad": "South India",
            "Chennai": "South India",
            "Kochi": "South India",
            "Mumbai": "West India",
            "Pune": "West India",
            "Delhi": "North India",
            "Gurugram": "North India",
            "Noida": "North India",
            "Kolkata": "East India",
            "Bhubaneswar": "East India",
        }
        
        for city, region in india_regions.items():
            if city in location:
                return region
        
        return "Other"
    
    def save_to_csv(self, filename: str = "data_engineer_jobs.csv"):
        """Save job data to CSV file"""
        if not self.jobs:
            print("❌ No jobs to save. Please run search_jobs() first.")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    "job_id", "job_title", "company_name", "location", "country", "region",
                    "job_level", "job_type", "experience_required", "required_skills",
                    "description", "posted_date", "url"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.jobs)
            
            print(f"\n✅ Jobs saved to '{filename}'")
            print(f"   Total jobs: {len(self.jobs)}")
            
            # Print summary by country
            self.print_summary()
        
        except Exception as e:
            print(f"❌ Error saving to CSV: {e}")
    
    def print_summary(self):
        """Print summary statistics"""
        if not self.jobs:
            return
        
        print("\n📊 Summary by Country:")
        country_count = {}
        region_count = {}
        
        for job in self.jobs:
            country = job.get("country", "Other")
            region = job.get("region", "Other")
            country_count[country] = country_count.get(country, 0) + 1
            region_count[region] = region_count.get(region, 0) + 1
        
        for country, count in sorted(country_count.items(), key=lambda x: x[1], reverse=True):
            print(f"   {country}: {count} jobs")
        
        print("\n📍 Summary by Region (India):")
        for region, count in sorted(region_count.items(), key=lambda x: x[1], reverse=True):
            if region != "Other":
                print(f"   {region}: {count} jobs")
    
    def run(self):
        """Execute the full scraping workflow"""
        print("=" * 60)
        print("   LinkedIn Data Engineer Job Scraper")
        print("   Experience: 5+ years | Skills: Python, SQL, Spark, ETL")
        print("=" * 60)
        
        if not self.validate_credentials():
            return
        
        # Search for jobs
        jobs = self.search_jobs()
        
        if jobs:
            # Parse and filter jobs
            print(f"\n📋 Processing {len(jobs)} jobs...")
            for job in jobs:
                parsed = self.parse_job_details(job)
                if parsed:
                    self.jobs.append(parsed)
            
            # Save to CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_engineer_jobs_{timestamp}.csv"
            self.save_to_csv(filename)
        else:
            print("\n⚠️  No jobs found. Check your credentials and search parameters.")


def main():
    """Main entry point"""
    scraper = LinkedInJobScraper()
    scraper.run()


if __name__ == "__main__":
    main()
