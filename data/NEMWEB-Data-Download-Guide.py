import streamlit as st
import pandas as pd

st.title("How to Download Data from NEMWEB in Batch")
st.markdown('''
This guide focuses exclusively on how to write Python code to download various types of data from the 
Australian Energy Market Operator's (AEMO) National Electricity Market Web (NEMWEB) in batch.
''')

st.warning('''
**Disclaimer**:
- The information provided here is for educational purposes only.
- Always check the terms of use and licensing agreements on the AEMO website before downloading data.
- Be respectful of the AEMO servers and avoid overwhelming them with too many requests.
''', icon="⚠️")

st.header("1. Setup Environment")
st.markdown('''
First, you'll need to set up your environment with the necessary libraries and directories:
```python
import requests
import os
import time
import zipfile

# Define directories to store files
data_dir = 'data/aemo_data'
os.makedirs(data_dir, exist_ok=True)

# Define regions in the National Electricity Market (NEM)
regions = ['NSW1', 'QLD1', 'SA1', 'TAS1', 'VIC1']

# Setup headers for HTTP requests to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
```
''')

st.markdown('''
The `headers` dictionary is used to mimic a browser when making HTTP requests to the AEMO website. This can help avoid issues with servers that block requests from non-browser clients. 
You can also use a random user-agent to further mimic a browser and avoid being blocked by the server:

```python
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.84'
]

def get_random_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }

# Usage
headers = get_random_headers()
```
''')

st.header("2. Downloading Price and Demand Data")
st.markdown('''
AEMO provides a special direct CSV download service for price and demand data, which follows a different URL pattern than the MMS Data Model. This is one of the most commonly used datasets and is available in a simpler format.

### Understanding the Price and Demand API

The Price and Demand data is provided through a dedicated API that follows this URL pattern:
```
https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{YEARMONTH}_{REGION}.csv
```

Where:
- `{YEARMONTH}`: Year and month in YYYYMM format (e.g., 202401 for January 2024)
- `{REGION}`: Region code (NSW1, QLD1, SA1, TAS1, VIC1)

### Code for Batch Downloading

This code loops through years, months, and regions to download all price and demand data:

```python
# Base URL template for price and demand data
base_url = "https://aemo.com.au/aemo/data/nem/priceanddemand/PRICE_AND_DEMAND_{}_{}.csv"

# Loop through years and months
for year in range(2019, 2025):
    for month in range(1, 13):
        month_str = f"{year}{month:02d}"
        
        # Skip future months in current year
        if year == 2024 and month > 12:
            continue
            
        for region in regions:
            filename = f"data/aemo_data/PRICE_AND_DEMAND_{month_str}_{region}.csv"
            
            # Skip if file already exists
            if os.path.exists(filename):
                print(f"Skipping {filename} - already exists")
                continue
                
            url = base_url.format(month_str, region)
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")
            
            # Wait to avoid overwhelming the server
            time.sleep(1)
```

### What's in the Price and Demand Data?

Each downloaded CSV file contains:
- `SETTLEMENTDATE`: Date and time of the trading interval
- `TOTALDEMAND`: Total electricity demand in MW
- `RRP`: Regional Reference Price in $/MWh (the spot price for that region)
- `PERIODTYPE`: Trading interval type (typically 5-minute or 30-minute periods)

This provides a comprehensive dataset of electricity prices and demand across all regions of the National Electricity Market, which is valuable for analysing trends, price volatility, and demand patterns.

Output files will be named like:
- `PRICE_AND_DEMAND_201901_NSW1.csv` (NSW data for January 2019)
- `PRICE_AND_DEMAND_201901_QLD1.csv` (QLD data for January 2019)
etc.
''')

st.header("3. Downloading from MMS Data Model")
st.markdown('''
The Market Management System (MMS) Data Model is AEMO's comprehensive repository of electricity market data. It contains detailed information on dispatch, pricing, generation, bidding, and more. This section explains how to download the DISPATCH_UNIT_SCADA data, which provides actual generation output for each unit in the market.

### Understanding DISPATCH_UNIT_SCADA Data

DISPATCH_UNIT_SCADA is one of the most valuable datasets in the MMS Data Model. It contains:
- Real-time SCADA (Supervisory Control and Data Acquisition) readings for each generating unit
- Data at 5-minute resolution (dispatch intervals)
- Actual output values in MW
- Data for all registered generators in the NEM

This data allows you to analyze:
- Actual generator output vs. capacity
- Renewable generation patterns
- Generator availability and outages
- Response to price signals

### Downloading DISPATCH_UNIT_SCADA Data

The code below handles:
1. Different URL formats before and after August 2024
2. File downloading and extraction
3. Proper renaming of extracted CSV files

```python
base_mms_url = "http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{}/MMSDM_{}_{}/MMSDM_Historical_Data_SQLLoader/DATA/{}.zip"

def download_dispatch_unit_scada_data(base_mms_url):
    """
    Downloads DISPATCH_UNIT_SCADA data from NEMWEB for specified years and months.
    This function handles the URL format change that occurred in August 2024.
    """
    for year in range(2024, 2026):
        for month in range(1, 13):
            month_str = f"{year}{month:02d}"
            # Skip future months/years
            if year >= 2024 and month > 12:
                continue
                
            # URL format changes in August 2024
            if (year == 2024 and month >= 8) or year >= 2025:
                filename = f"PUBLIC_ARCHIVE%23DISPATCH_UNIT_SCADA%23FILE01%23{month_str}010000"
            else:
                filename = f"PUBLIC_DVD_DISPATCH_UNIT_SCADA_{month_str}010000"
                
            url = base_mms_url.format(year, year, f"{month:02d}", filename)

            zipname = f"data/aemo_data/DISPATCH_UNIT_SCADA_{month_str}.zip"
            csvname = f"data/aemo_data/DISPATCH_UNIT_SCADA_{month_str}.csv"

            try:
                if not os.path.exists(zipname):
                    print(f"Downloading {url}")
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    with open(zipname, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {zipname}")
                else:
                    print(f"Skipping {zipname} - already exists")

                if not os.path.exists(csvname):
                    # Unzip the file and rename the CSV file
                    with zipfile.ZipFile(zipname, 'r') as zip_ref:
                        zip_ref.extractall("data/aemo_data")
                    print(f"Unzipped {zipname}")

                    # Rename the CSV file - converting URL encoding (%23) to actual hash symbols (#)
                    filename = filename.replace('%23', '#')
                    os.rename(f"data/aemo_data/{filename}.CSV", csvname)
                    print(f"Renamed to {csvname}")
                else:
                    print(f"Skipping {csvname} - already exists")
                    
                # Be polite to the server
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")

# Call the function
download_dispatch_unit_scada_data(base_mms_url)
```

### Downloading Interconnector Data

Similarly, you can download interconnector flow data (DISPATCHINTERCONNECTORRES), which shows the electricity flow between different regions of the NEM:

```python
def download_dispatch_interconnectors_data(base_mms_url):
    """
    Downloads DISPATCHINTERCONNECTORRES data from NEMWEB, which contains
    interconnector flow information between NEM regions.
    """
    table = "DISPATCHINTERCONNECTORRES"

    for year in range(2024, 2026):
        for month in range(1, 13):
            month_str = f"{year}{month:02d}"
            if year >= 2024 and month > 12:
                continue
                
            if (year == 2024 and month >= 8) or year >= 2025:
                filename = f"PUBLIC_ARCHIVE%23{table}%23FILE01%23{month_str}010000"
            else:
                filename = f"PUBLIC_DVD_{table}_{month_str}010000"
                
            url = base_mms_url.format(year, year, f"{month:02d}", filename)

            zipname = f"data/aemo_data/{table}_{month_str}.zip"
            csvname = f"data/aemo_data/{table}_{month_str}.csv"

            # Download logic same as above function
            # ...
```

### File Format Notes

The downloaded files are in CSV format but have some specific formatting:
1. The first line contains metadata
2. The last line contains a summary count
3. The actual data has columns like SETTLEMENTDATE, DUID, SCADAVALUE, etc.

When processing this data later, you may want to skip the first and last lines:
```python
import pandas as pd
# Example of reading the file correctly
df = pd.read_csv("data/aemo_data/DISPATCH_UNIT_SCADA_202401.csv", skiprows=1, skipfooter=1, engine='python')
```
''')

st.header("4. Creating a Generalized Download Function")
st.markdown('''
Instead of creating separate functions for each table, we can build a more flexible and reusable solution with a generalized download function. This approach allows you to download any table from the NEMWEB MMS Data Model with a single function call.

### Advantages of a Generalized Approach

1. **Code reusability**: Write the download logic once and use it for any table
2. **Flexibility**: Easily specify different date ranges for different tables
3. **Maintainability**: Centralized error handling and logging
4. **Configurability**: Customize behavior with parameters

### The Generalized Download Function

```python
def download_nemweb_table_data(table_name, years_range, months_range, output_dir="data/aemo_data", 
                              delay=1, overwrite=False):
    """
    Generic function to download any table from NEMWEB MMS Data Model
    
    Args:
        table_name (str): The name of the table to download (e.g., "DISPATCHLOAD")
        years_range (tuple): Start and end years (inclusive), e.g., (2023, 2024)
        months_range (tuple): Start and end months (inclusive), e.g., (1, 12)
        output_dir (str): Directory to save downloaded files
        delay (int): Seconds to wait between downloads to avoid overwhelming the server
        overwrite (bool): Whether to overwrite existing files
    
    Returns:
        dict: Summary of download results with counts of successful and failed downloads
    """
    base_mms_url = "http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{}/MMSDM_{}_{}/MMSDM_Historical_Data_SQLLoader/DATA/{}.zip"
    
    start_year, end_year = years_range
    start_month, end_month = months_range
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Track results
    results = {
        "successful": 0,
        "skipped": 0,
        "failed": 0,
        "failed_urls": []
    }
    
    print(f"Starting download of {table_name} data from {start_year}-{start_month} to {end_year}-{end_month}")
    
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # Skip months outside the specified range
            if (year == start_year and month < start_month) or (year == end_year and month > end_month):
                continue
                
            # Format the month string (e.g., 202401)
            month_str = f"{year}{month:02d}"
            
            # Determine the correct filename format based on date
            # URL format changed in August 2024
            if (year == 2024 and month >= 8) or year >= 2025:
                filename = f"PUBLIC_ARCHIVE%23{table_name}%23FILE01%23{month_str}010000"
            else:
                filename = f"PUBLIC_DVD_{table_name}_{month_str}010000"
                
            # Construct the full URL
            url = base_mms_url.format(year, year, f"{month:02d}", filename)

            # Define output filenames
            zipname = os.path.join(output_dir, f"{table_name}_{month_str}.zip")
            csvname = os.path.join(output_dir, f"{table_name}_{month_str}.csv")

            try:
                # Check if files already exist
                if os.path.exists(csvname) and not overwrite:
                    print(f"Skipping {csvname} - already exists")
                    results["skipped"] += 1
                    continue
                
                # Download the zip file
                if not os.path.exists(zipname) or overwrite:
                    print(f"Downloading {url}")
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    with open(zipname, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {zipname}")
                
                # Extract the CSV file
                with zipfile.ZipFile(zipname, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
                print(f"Unzipped {zipname}")

                # Rename the CSV file
                csv_original = os.path.join(output_dir, f"{filename.replace('%23', '#')}.CSV")
                if os.path.exists(csv_original):
                    os.rename(csv_original, csvname)
                    print(f"Renamed to {csvname}")
                    results["successful"] += 1
                else:
                    print(f"Warning: Could not find expected CSV file {csv_original}")
                    results["failed"] += 1
                    results["failed_urls"].append(url)
                    
                # Optional: Remove the zip file to save space
                # os.remove(zipname)
                    
                # Be polite to the server
                time.sleep(delay)
                
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")
                results["failed"] += 1
                results["failed_urls"].append(url)
    
    # Print summary
    print(f"Download summary for {table_name}:")
    print(f"  Successfully downloaded: {results['successful']}")
    print(f"  Skipped (already exist): {results['skipped']}")
    print(f"  Failed: {results['failed']}")
    
    return results
```

### Advanced Usage Examples

The function can be used in various ways to suit different needs:

1. **Download a full year of data:**
```python
# Download all DISPATCHLOAD data for 2023
download_nemweb_table_data("DISPATCHLOAD", (2023, 2023), (1, 12))
```

2. **Download a specific time period:**
```python
# Download DISPATCHPRICE data from July 2023 to February 2024
download_nemweb_table_data("DISPATCHPRICE", (2023, 2024), (7, 2))
```

3. **Download with custom settings:**
```python
# Download with a longer delay and overwrite existing files
download_nemweb_table_data("BIDDAYOFFER_D", (2024, 2024), (1, 6), 
                          delay=2, overwrite=True)
```

4. **Download multiple tables:**
```python
# Define tables and corresponding time periods
tables_to_download = [
    {"name": "DISPATCHLOAD", "years": (2023, 2024), "months": (1, 12)},
    {"name": "DISPATCHPRICE", "years": (2023, 2024), "months": (1, 12)},
    {"name": "DISPATCHINTERCONNECTORRES", "years": (2024, 2024), "months": (1, 6)}
]

# Download all tables
for table in tables_to_download:
    download_nemweb_table_data(
        table["name"], table["years"], table["months"]
    )
```

This generalized function provides a flexible foundation that you can adapt to your specific needs for downloading any data from the NEMWEB MMS Data Model.
''')

st.header("5. Understanding NEMWEB URL Patterns")
st.markdown('''
To effectively download data from NEMWEB, it's important to understand the URL patterns used by AEMO. This allows you to construct valid download links programmatically.

### NEMWEB MMS Data Model URL Structure

The MMS Data Model follows this general pattern:
```
http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{YEAR}/MMSDM_{YEAR}_{MONTH}/MMSDM_Historical_Data_SQLLoader/DATA/{FILENAME}.zip
```

Where:
- `{YEAR}`: Four-digit year (e.g., 2024)
- `{MONTH}`: Two-digit month (e.g., 01 for January)
- `{FILENAME}`: The specific file identifier, which follows different patterns based on time periods

### Filename Patterns

For data before August 2024:
```
PUBLIC_DVD_{TABLE_NAME}_{YEARMONTH}010000
```

For data from August 2024 onwards:
```
PUBLIC_ARCHIVE%23{TABLE_NAME}%23FILE01%23{YEARMONTH}010000
```

Note that `%23` is the URL encoding for the hash symbol (#). When working with the actual filenames after downloading, you'll need to replace this with actual # characters.

### Example URLs

For January 2024 DISPATCHLOAD data:
```
http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2024/MMSDM_2024_01/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHLOAD_202401010000.zip
```

For October 2024 DISPATCHLOAD data:
```
http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2024/MMSDM_2024_10/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_ARCHIVE%23DISPATCHLOAD%23FILE01%23202410010000.zip
```

Understanding these patterns is essential for constructing valid URLs programmatically, especially when you're downloading data that spans across different time periods where formats might change.
''')

st.header("6. Downloading Static Reference Data")
st.markdown('''
In addition to time-series data, AEMO provides important static reference data that helps interpret and enrich the time-series information. These reference datasets include information about registered participants, generators, and other market entities.

### NEM Registration and Exemption List

The NEM Registration and Exemption List contains comprehensive information about all registered generators, including:
- Generator names and locations
- Technology types and fuel sources
- Registered capacities
- Classification (scheduled, semi-scheduled, non-scheduled)
- Owner/participant

This reference data is essential for correctly interpreting generator data and understanding the market composition.

```python
# Download NEM Registration and Exemption List
registration_url = "https://www.aemo.com.au/-/media/files/electricity/nem/participant_information/nem-registration-and-exemption-list.xlsx"
registration_filename = "data/aemo_data/NEM_Registration_and_Exemption_List.xlsx"

try:
    response = requests.get(registration_url, headers=headers)
    response.raise_for_status()
    with open(registration_filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {registration_filename}")
except requests.exceptions.RequestException as e:
    print(f"Failed to download {registration_url}: {e}")
```

### Network Outage Data

The NETWORK_OUTAGEDETAIL table provides information about planned and unplanned outages in the transmission network:

```python
# Download network outage data
outage_detail_url = "https://nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2025/MMSDM_2025_01/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_ARCHIVE%23NETWORK_OUTAGEDETAIL%23FILE01%23202501010000.zip"
outage_detail_zipname = "data/aemo_data/NETWORK_OUTAGEDETAIL_202501.zip"

try:
    response = requests.get(outage_detail_url, headers=headers)
    response.raise_for_status()
    with open(outage_detail_zipname, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {outage_detail_zipname}")

    # Unzip the file
    with zipfile.ZipFile(outage_detail_zipname, 'r') as zip_ref:
        zip_ref.extractall("data/aemo_data")
    print(f"Unzipped {outage_detail_zipname}")
except requests.exceptions.RequestException as e:
    print(f"Failed to download {outage_detail_url}: {e}")
```

### Other Important Reference Data

Other valuable static reference datasets available from AEMO include:

1. **List of Regional Boundaries**: 
```python
regional_boundaries_url = "https://www.aemo.com.au/-/media/files/electricity/nem/data/nem-region-boundaries.xlsx"
```

2. **Interconnector Capabilities**:
```python
interconnector_capabilities_url = "https://www.aemo.com.au/-/media/files/electricity/nem/security_and_reliability/congestion-information/2019/interconnector-capabilities.pdf"
```

3. **Marginal Loss Factors (MLFs)**:
```python
mlf_url = "https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/market-operations/loss-factors-and-regional-boundaries"
# Note: This page has links to different MLF spreadsheets that need to be extracted programmatically
```

These reference datasets can be particularly useful when analysing transmission flows, constraints, and price differences between regions.
''')

st.header("7. Most Valuable Tables in NEMWEB")
st.markdown('''
The NEMWEB MMS Data Model contains hundreds of tables, but certain tables are particularly valuable for electricity market analysis. Here's an overview of the most commonly used tables, what they contain, and what you can use them for:

| Table Name | Description | Use Cases | Data Frequency |
|------------|-------------|-----------|----------------|
| DISPATCHLOAD | Dispatch load for each unit | Generator output analysis, bid compliance | 5-minute |
| DISPATCHPRICE | Regional reference price | Price analysis, market events | 5-minute |
| DISPATCHREGIONSUM | Regional summary (demand, price, etc.) | Regional analysis, demand forecasting | 5-minute |
| DISPATCH_UNIT_SCADA | Actual unit output from SCADA | Real output vs. dispatch targets, generator performance | 5-minute |
| DISPATCHINTERCONNECTORRES | Interconnector flow data | Inter-regional analysis, constraint impacts | 5-minute |
| DUDETAILSUMMARY | Dispatch unit details | Generator static information | Infrequent updates |
| GENCONDATA | Generator constraint data | Constraint analysis, generator limitations | When changed |
| MARKETNOTICEDATA | Market notices | Market events, outages, interventions | As published |
| BIDDAYOFFER_D | Day ahead bid offers | Bidding strategy analysis | Daily |
| DISPATCHCONSTRAINT | Constraint solutions | Network constraint analysis | 5-minute |
| NETWORK_OUTAGEDETAIL | Network outage details | Transmission outage analysis | As published |
| ROOFTOPPV_ACTUAL | Estimated rooftop PV generation | Distributed generation analysis | 5-minute |
| BIDPEROFFER_D | Price band offers | Detailed bidding analysis | Daily |
| DISPATCHCASESOLUTION | Full dispatch case solutions | Detailed market operation analysis | 5-minute |
| TRADINGREGIONSUM | Trading interval regional summary | Settlement analysis | 30-minute |

### Choosing the Right Tables

When deciding which tables to download, consider:

1. **Analysis Purpose**:
   - For price analysis: DISPATCHPRICE, DISPATCHREGIONSUM
   - For generator analysis: DISPATCHLOAD, DISPATCH_UNIT_SCADA
   - For network analysis: DISPATCHINTERCONNECTORRES, DISPATCHCONSTRAINT
   - For bidding analysis: BIDDAYOFFER_D, BIDPEROFFER_D

2. **Data Volume**:
   - 5-minute tables (like DISPATCHLOAD) will be much larger than daily tables
   - Consider downloading a small sample first to estimate storage requirements

3. **Related Tables**:
   - Many analyses require joining multiple tables
   - For example, generator analysis typically requires DISPATCHLOAD, DISPATCH_UNIT_SCADA, and DUDETAILSUMMARY

4. **Time Period**:
   - Recent data (last 1-2 years) is most useful for current market analysis
   - Historical data can be useful for pattern analysis or studying specific events

Note: The availability of data may vary depending on the time period. Older tables might have different formats or naming conventions.
''')

st.header("8. Advanced Downloading Techniques")
st.markdown('''
When downloading large amounts of data from NEMWEB, you may want to employ more advanced techniques to improve efficiency, reliability, and organisation.

### Chunked Downloads for Large Files

For very large files, downloading in chunks prevents memory issues and allows for download resumption:

```python
def download_large_file(url, local_filename, chunk_size=8192):
    """
    Downloads a large file in chunks to avoid memory issues.
    
    Args:
        url (str): URL to download
        local_filename (str): Path to save the file
        chunk_size (int): Size of each chunk in bytes
        
    Returns:
        str: Path to the downloaded file
    """
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        
        print(f"Downloading {url} to {local_filename}")
        print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
        
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size): 
                if chunk:  # Filter out keep-alive chunks
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Print progress
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"Progress: {percent:.1f}% ({downloaded / (1024 * 1024):.1f} MB)", end='\\r')
        
        print(f"\\nCompleted download of {local_filename}")
    return local_filename
```

### Parallel Downloads for Multiple Files

To dramatically speed up downloading multiple files, you can use parallel processing:

```python
from concurrent.futures import ThreadPoolExecutor
import time
import random

def download_file(url_filename_tuple):
    """
    Download a single file, suitable for use with ThreadPoolExecutor
    
    Args:
        url_filename_tuple (tuple): (url, filename) to download
        
    Returns:
        dict: Status of the download operation
    """
    url, filename = url_filename_tuple
    result = {
        "url": url,
        "filename": filename,
        "success": False,
        "error": None
    }
    
    if os.path.exists(filename) and not overwrite:
        print(f"Skipping {filename} - already exists")
        result["success"] = True
        result["skipped"] = True
        return result
    
    try:
        # Add a small random delay to avoid hammering the server
        time.sleep(random.uniform(0.5, 1.5))
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
            
        print(f"Downloaded {filename}")
        result["success"] = True
        return result
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        result["error"] = str(e)
        return result

def parallel_download(url_filename_list, max_workers=3, overwrite=False):
    """
    Download multiple files in parallel
    
    Args:
        url_filename_list (list): List of (url, filename) tuples
        max_workers (int): Maximum number of concurrent downloads
        overwrite (bool): Whether to overwrite existing files
        
    Returns:
        list: Results for each download attempt
    """
    print(f"Starting parallel download of {len(url_filename_list)} files with {max_workers} workers")
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_file, item): item for item in url_filename_list}
        
        for future in futures.as_completed(future_to_url):
            url, filename = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing {url}: {e}")
                results.append({
                    "url": url,
                    "filename": filename,
                    "success": False,
                    "error": str(e)
                })
    
    # Summarize results
    successes = sum(1 for r in results if r["success"])
    failures = len(results) - successes
    
    print(f"Download summary: {successes} successful, {failures} failed")
    
    return results
```

### Example Usage of Parallel Downloading

Here's how you can use parallel downloading to fetch multiple months of data quickly:

```python
# Example: Download DISPATCHPRICE data for all of 2023 in parallel
base_url = "http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2023/MMSDM_2023_{}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHPRICE_2023{}010000.zip"
output_dir = "data/aemo_data"

# Create a list of URL and filename pairs
download_list = []
for month in range(1, 13):
    month_str = f"{month:02d}"
    url = base_url.format(month_str, month_str)
    filename = os.path.join(output_dir, f"DISPATCHPRICE_2023{month_str}.zip")
    download_list.append((url, filename))

# Download with 4 parallel workers
results = parallel_download(download_list, max_workers=4)
```

### Organising Downloads by Data Type and Date

For better organisation, especially when downloading many tables, consider structuring your downloads by table type and date range:

```python
def organize_nemweb_downloads(base_dir="data/nemweb"):
    """
    Creates an organized directory structure for NEMWEB downloads
    
    Args:
        base_dir (str): Base directory for all downloads
        
    Returns:
        dict: Dictionary of paths for different types of data
    """
    # Create main category directories
    categories = {
        "dispatch": os.path.join(base_dir, "dispatch"),
        "bidding": os.path.join(base_dir, "bidding"),
        "constraints": os.path.join(base_dir, "constraints"),
        "interconnectors": os.path.join(base_dir, "interconnectors"),
        "reference": os.path.join(base_dir, "reference"),
        "misc": os.path.join(base_dir, "misc")
    }
    
    # Create all directories
    for category, path in categories.items():
        os.makedirs(path, exist_ok=True)
        
        # Create year subdirectories
        for year in range(2019, 2025):
            year_path = os.path.join(path, str(year))
            os.makedirs(year_path, exist_ok=True)
    
    print(f"Created organized directory structure in {base_dir}")
    return categories
```

### Data Download Logging

For large download operations, implementing logging helps track progress and troubleshoot issues:

```python
import logging
import datetime

def setup_download_logging(log_dir="logs"):
    """
    Sets up logging for download operations
    
    Args:
        log_dir (str): Directory to store log files
        
    Returns:
        logging.Logger: Configured logger
    """
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a unique log filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"nemweb_download_{timestamp}.log")
    
    # Configure logger
    logger = logging.getLogger("nemweb_downloader")
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Started NEMWEB download session at {datetime.datetime.now()}")
    return logger
```

These advanced techniques will help you build a robust, efficient system for downloading and managing large amounts of NEMWEB data.
''')

st.header("9. Best Practices and Ethical Considerations")
st.markdown('''
When downloading data from NEMWEB, it's important to follow best practices and ethical considerations to ensure you're being a good data citizen and avoiding potential issues.

### Respect the Data Source

AEMO provides this data as a public service, so it's important to be respectful:

- **Include delays between requests**: Always add a delay between requests (1-2 seconds is typically sufficient)
- **Limit concurrent connections**: Avoid making too many parallel requests (3-5 maximum is reasonable)
- **Download during off-peak hours**: For large batch downloads, consider running your scripts during nights or weekends

### Error Handling and Reliability

Robust error handling ensures you can recover from failures:

- **Implement retries**: Add retry logic for failed downloads with exponential backoff
- **Log errors**: Keep detailed logs of any failures for troubleshooting
- **Resume capability**: Design your code to resume from where it left off if interrupted

### Data Storage and Management

Proper data management saves time and resources:

- **Compress older files**: Consider compressing data you don't actively use
- **Use a database**: For frequent analysis, import data into a database like PostgreSQL
- **Implement data versioning**: Keep track of when data was downloaded and any modifications
- **Validate downloads**: Check file integrity and contents after downloading

### Terms of Use Compliance

AEMO data is subject to terms of use:

- **Review AEMO's terms**: Check AEMO's website for current terms of use
- **Attribution**: When publishing analysis based on this data, properly attribute AEMO as the source
- **Non-commercial limitations**: Be aware of any limitations on commercial use of the data

### Sample Code: Ethically Sound Downloader

Here's a sample implementation that incorporates these best practices:

```python
def ethical_nemweb_download(table_name, year, month, output_dir="data/aemo_data", 
                           max_retries=3, retry_delay=5, respect_delay=2):
    """
    Downloads data from NEMWEB with ethical considerations built in
    
    Args:
        table_name (str): Table to download
        year (int): Year to download
        month (int): Month to download
        output_dir (str): Directory to save downloaded files
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Base delay between retries (will increase exponentially)
        respect_delay (int): Delay between requests to respect the server
    """
    month_str = f"{year}{month:02d}"
    
    # Determine the correct filename format
    if (year == 2024 and month >= 8) or year >= 2025:
        filename = f"PUBLIC_ARCHIVE%23{table_name}%23FILE01%23{month_str}010000"
    else:
        filename = f"PUBLIC_DVD_{table_name}_{month_str}010000"
    
    url = f"http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{year}/MMSDM_{year}_{month:02d}/MMSDM_Historical_Data_SQLLoader/DATA/{filename}.zip"
    zipname = os.path.join(output_dir, f"{table_name}_{month_str}.zip")
    csvname = os.path.join(output_dir, f"{table_name}_{month_str}.csv")
    
    # Skip if already downloaded
    if os.path.exists(csvname):
        print(f"File already exists: {csvname}")
        return {"status": "skipped", "reason": "file_exists"}
    
    # Try to download with retries
    for attempt in range(max_retries):
        try:
            # Respect the server with a delay
            time.sleep(respect_delay)
            
            print(f"Downloading {url} (Attempt {attempt+1}/{max_retries})")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(zipname, 'wb') as f:
                f.write(response.content)
            
            # Unzip and rename
            with zipfile.ZipFile(zipname, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            
            # Rename the CSV file
            actual_filename = filename.replace('%23', '#')
            os.rename(os.path.join(output_dir, f"{actual_filename}.CSV"), csvname)
            
            print(f"Successfully downloaded and processed {csvname}")
            return {"status": "success", "file": csvname}
            
        except requests.exceptions.RequestException as e:
            print(f"Download failed: {e}")
            
            # Exponential backoff
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Max retries reached. Failed to download {url}")
                return {"status": "failed", "reason": str(e)}
```
''')

# Footer
st.markdown("---")
st.markdown('''
### Additional Resources

- [AEMO Data Dashboard](https://aemo.com.au/en/energy-systems/electricity/national-electricity-market-nem/data-nem)
- [NEMWEB Portal](https://nemweb.com.au/)
- [MMS Data Model Report](https://www.aemo.com.au/-/media/files/electricity/nem/it-systems-and-change/mms-data-model/mms-data-model-report.pdf)
- [AEMO NEMWeb File Formats Reference](https://nemweb.com.au/Reports/Current/nemweb_file_formats.pdf)

Data provided by the Australian Energy Market Operator (AEMO) via NEMWEB.  
This guide is for educational purposes only.
''')