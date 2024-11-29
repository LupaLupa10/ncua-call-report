import requests
from io import BytesIO
from zipfile import ZipFile
import os
from datetime import datetime
import time
from bs4 import BeautifulSoup


def get_download_links(start_year, start_quarter, end_year, end_quarter):
    """
    Scrape the download links from the NCUA quarterly data page for specific periods
    """
    url = "https://ncua.gov/analysis/credit-union-corporate-call-report-data/quarterly-data"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            if 'call-report-data' in a['href'] and a['href'].endswith('.zip'):
                parts = a['href'].split('-')
                if len(parts) >= 3:
                    year = parts[-2]
                    quarter = parts[-1].replace('.zip', '')
                    
                    if (int(year) > start_year or (int(year) == start_year and int(quarter) >= int(start_quarter))) and \
                       (int(year) < end_year or (int(year) == end_year and int(quarter) <= int(end_quarter))):
                        links.append({
                            'href': a['href'],
                            'text': a.text.strip(),
                            'year': year,
                            'quarter': quarter
                        })
        
        links.sort(key=lambda x: (x['year'], x['quarter']))
        return links
    
    except Exception as e:
        print(f"Error getting download links: {e}")
        return []

def download_and_extract(file_info):
    """
    Download and extract a single file directly to its period subfolder
    """
    base_url = "https://ncua.gov"
    full_url = base_url + file_info['href']
    period = f"{file_info['year']}-{file_info['quarter']}"
    
    # Create period-specific subfolder
    output_dir = os.path.join('ncua_data', period)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        print(f"Downloading {file_info['text']} ({period})...")
        response = requests.get(full_url, allow_redirects=True)
        response.raise_for_status()
        
        # Extract directly from memory
        with ZipFile(BytesIO(response.content)) as zip_file:
            # Get list of files in zip
            files = zip_file.namelist()
            # Extract all files to period subfolder
            zip_file.extractall(output_dir)
            print(f"Extracted files to {output_dir}: {', '.join(files)}")
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {period}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for {period}: {e}")
        return False

def download_specific_periods(start_year, start_quarter, end_year, end_quarter):
    """
    Download call reports for specific years and quarters
    """
    links = get_download_links(start_year, start_quarter, end_year, end_quarter)
    
    if not links:
        print("No download links found for specified period!")
        return
    
    print(f"Found {len(links)} files to download")
    
    for link in links:
        success = download_and_extract(link)
        if success:
            time.sleep(2)

def list_downloaded_files():
    """Print all extracted files by period"""
    print("\nExtracted data by period:")
    if os.path.exists('ncua_data'):
        for period in sorted(os.listdir('ncua_data')):
            period_dir = os.path.join('ncua_data', period)
            if os.path.isdir(period_dir):
                files = os.listdir(period_dir)
                print(f"\n{period}:")
                for f in sorted(files):
                    print(f"  - {f}")


if __name__ == "__main__":
    # Example: Download data from 2023Q1 to 2024Q1
    start_year = 2023
    start_quarter = "01"
    end_year = 2024
    end_quarter = "01"
    
    print(f"Starting NCUA call report data download for {start_year}Q{start_quarter} to {end_year}Q{end_quarter}...")
    download_specific_periods(start_year, start_quarter, end_year, end_quarter)
    list_downloaded_files()
    print("Download process completed!")