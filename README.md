# NCUA Credit Union Call Report Data Processor

This project provides tools for downloading and processing National Credit Union Administration (NCUA) quarterly call report data. It includes functionality for downloading historical data files, extracting them, and processing them into a consolidated dataset with readable column names.

## Features

- Download NCUA call report data for specified date ranges
- Automatic extraction of downloaded ZIP files
- Processing of raw data files with column name mapping
- Consolidation of multiple quarters of data into a single dataset
- Handling of special characters and standardization of column names

## Requirements

```
python >= 3.6
Poetry >= 1.4.0
```

## Installation

1. Clone this repository:
```bash
git clone [https://github.com/LupaLupa10/ncua-call-report.git]
cd ncua-data-report
```

2. Install dependencies using Poetry:
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

The following dependencies will be installed automatically:
- pandas
- requests
- beautifulsoup4

## Project Structure

```
ncua-data-processor/
├── pyproject.toml          # Poetry configuration file
├── poetry.lock            # Poetry lock file
├── download_ncua_data.py  # Data downloading script
├── process_ncua_data.py   # Data processing script
├── ncua_data/            # Downloaded data directory
│   └── YYYY-QQ/         # Year-Quarter subfolders
└── ncua_combined_data.csv # Output combined dataset
```

## Usage

### 1. Downloading Data

The `download_ncua_data.py` script handles downloading and extracting NCUA call report data:

```python
# Activate Poetry environment first
poetry shell

# Then run the script
python download_ncua_data.py
```

Or run directly using Poetry:
```bash
poetry run python download_ncua_data.py
```

### 2. Processing Data

The `process_ncua_data.py` script processes the downloaded data:

```python
# Using Poetry shell
poetry shell
python process_ncua_data.py

# Or directly with Poetry
poetry run python process_ncua_data.py
```

## Key Functions

### Download Module (`download_ncua_data.py`)

- `get_download_links(start_year, start_quarter, end_year, end_quarter)`: Scrapes download links from NCUA website
- `download_and_extract(file_info)`: Downloads and extracts ZIP files
- `list_downloaded_files()`: Lists all extracted files by period

### Processing Module (`process_ncua_data.py`)

- `read_acctdesc_mapping(acctdesc_path)`: Creates mapping dictionary from AcctDesc.txt
- `map_acct_columns(data, mapping_dict)`: Applies column name mapping
- `process_fs_file(file_path, mapping_dict)`: Processes individual FS files
- `process_all_ncua_data(base_path)`: Processes all data files across all periods

## Output Data Format

The processed data includes the following additions to the original NCUA data:

- `year`: The year of the report
- `quarter`: The quarter of the report
- `source_file`: Original filename
- Column names are cleaned and mapped to readable names based on AcctDesc.txt

## Error Handling

The scripts include comprehensive error handling:
- Network errors during downloads
- File extraction errors
- Data processing errors
- Missing or corrupt files

Errors are logged to the console with descriptive messages.

## Notes

- The NCUA website may have rate limiting; the download script includes a 2-second delay between downloads
- Large datasets may require significant memory during processing
- Column mapping depends on AcctDesc.txt files in each period folder

