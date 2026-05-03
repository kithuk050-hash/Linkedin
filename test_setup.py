"""
LinkedIn Scraper - Setup Verification & Test Script
Use this to verify your configuration before running the full scraper
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def check_environment():
    """Check if .env file exists and has required variables"""
    print("\n" + "="*60)
    print("🔍 ENVIRONMENT CHECK".center(60))
    print("="*60)
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file found")
    else:
        print("❌ .env file NOT found")
        print("   Create it: cp .env.example .env")
        return False
    
    # Check credentials
    required_vars = [
        "LINKEDIN_ACCESS_TOKEN",
        "LINKEDIN_CLIENT_ID",
        "LINKEDIN_CLIENT_SECRET"
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if value and value != "your_actual_client_id":
            print(f"✅ {var:30} configured")
        else:
            print(f"❌ {var:30} NOT configured or is placeholder")
            missing.append(var)
    
    return len(missing) == 0


def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n" + "="*60)
    print("📦 PYTHON PACKAGES CHECK".center(60))
    print("="*60)
    
    required_packages = [
        ("requests", "HTTP requests"),
        ("dotenv", "Environment variables"),
        ("pandas", "Data analysis"),
        ("csv", "CSV handling (built-in)"),
    ]
    
    all_installed = True
    for package_name, description in required_packages:
        try:
            if package_name == "dotenv":
                __import__("dotenv")
            elif package_name == "csv":
                __import__("csv")
            else:
                __import__(package_name)
            print(f"✅ {package_name:20} {description}")
        except ImportError:
            print(f"❌ {package_name:20} NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n📝 Install missing packages:")
        print("   pip install -r requirements_linkedin_scraper.txt")
    
    return all_installed


def check_files():
    """Check if scraper files exist"""
    print("\n" + "="*60)
    print("📁 FILES CHECK".center(60))
    print("="*60)
    
    files_to_check = [
        ("linkedin_job_scraper.py", "Basic scraper"),
        ("linkedin_job_scraper_enhanced.py", "Enhanced scraper"),
        (".env", "Configuration"),
        ("requirements_linkedin_scraper.txt", "Dependencies"),
        ("LINKEDIN_SCRAPER_README.md", "Documentation"),
    ]
    
    all_exist = True
    for filename, description in files_to_check:
        if Path(filename).exists():
            print(f"✅ {filename:40} {description}")
        else:
            print(f"❌ {filename:40} NOT found")
            all_exist = False
    
    return all_exist


def test_imports():
    """Test if imports work"""
    print("\n" + "="*60)
    print("🧪 IMPORT TEST".center(60))
    print("="*60)
    
    try:
        print("Testing: import requests... ", end="", flush=True)
        import requests
        print("✅")
    except ImportError:
        print("❌ Failed")
        return False
    
    try:
        print("Testing: import dotenv... ", end="", flush=True)
        from dotenv import load_dotenv
        print("✅")
    except ImportError:
        print("❌ Failed")
        return False
    
    try:
        print("Testing: import pandas... ", end="", flush=True)
        import pandas
        print("✅")
    except ImportError:
        print("❌ Failed")
        return False
    
    try:
        print("Testing: import csv... ", end="", flush=True)
        import csv
        print("✅")
    except ImportError:
        print("❌ Failed")
        return False
    
    return True


def test_linkedin_connection():
    """Test LinkedIn API connection"""
    print("\n" + "="*60)
    print("🌐 LINKEDIN API CONNECTION TEST".center(60))
    print("="*60)
    
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    if not access_token or access_token == "your_access_token_here":
        print("⏭️  Skipping (access token not configured)")
        return None
    
    try:
        import requests
        
        url = "https://www.linkedin.com/voyager/api/jobs/search"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        params = {
            "keywords": "Data Engineer",
            "locationId": "in",
            "resultLimit": 1
        }
        
        print("Attempting connection to LinkedIn API...")
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            print("✅ Successfully connected to LinkedIn API!")
            data = response.json()
            jobs_count = len(data.get("elements", []))
            print(f"✅ API response valid ({jobs_count} jobs returned)")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed (401)")
            print("   Your access token may be expired or invalid")
            return False
        elif response.status_code == 403:
            print("❌ Permission denied (403)")
            print("   Your token may not have job search permissions")
            return False
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
    
    except requests.exceptions.Timeout:
        print("❌ Connection timeout")
        print("   LinkedIn API may be unavailable")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error")
        print("   Check your internet connection")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def print_summary(results):
    """Print summary of all checks"""
    print("\n" + "="*60)
    print("📋 SUMMARY".center(60))
    print("="*60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r is True)
    
    status_map = {
        True: "✅ PASS",
        False: "❌ FAIL",
        None: "⏭️  SKIP"
    }
    
    for check_name, result in results.items():
        print(f"{status_map[result]:8} {check_name}")
    
    print("\n" + "-"*60)
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED! Ready to run scraper.".center(60))
        print("\nNext: python linkedin_job_scraper_enhanced.py".center(60))
    else:
        failed = sum(1 for r in results.values() if r is False)
        if failed > 0:
            print(f"⚠️  {failed} CHECKS FAILED - Fix issues before running scraper".center(60))
    
    print("="*60 + "\n")


def main():
    """Run all checks"""
    print("\n" + "🚀 LINKEDIN SCRAPER - SETUP VERIFICATION 🚀".center(60))
    
    results = {
        "Environment (.env)": check_environment(),
        "Python Packages": check_python_packages(),
        "Scraper Files": check_files(),
        "Imports": test_imports(),
        "LinkedIn API Connection": test_linkedin_connection(),
    }
    
    print_summary(results)
    
    return 0 if all(v is not False for v in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
