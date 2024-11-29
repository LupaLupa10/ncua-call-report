import pandas as pd
import os
import re
from pathlib import Path


def read_acctdesc_mapping(acctdesc_path: str) -> dict:
    """
    Read AcctDesc.txt and create mapping dictionary.
    """
    try:
        acct_df = pd.read_csv(acctdesc_path, quoting=1)
        mapping_dict = {}
        special_chars_pattern = re.compile(r'[ ()\/\\,.\-\'"]')
        
        for _, row in acct_df.iterrows():
            if pd.notna(row['Account']) and pd.notna(row['AcctName']):
                account_key = f"acct_{str(row['Account']).lower()}"
                acct_name = special_chars_pattern.sub('_', str(row['AcctName'])).lower()
                acct_name = re.sub(r'_+', '_', acct_name).strip('_')
                mapping_dict[account_key] = acct_name
                
        return mapping_dict
    except Exception as e:
        print(f"Error reading AcctDesc.txt: {e}")
        return {}

def map_acct_columns(data: pd.DataFrame, mapping_dict: dict) -> pd.DataFrame:
    """
    Map account columns using the mapping dictionary.
    """
    data.columns = data.columns.str.lower()
    acct_columns = [col for col in data.columns if 'acct_' in col]
    column_mapping = {}
    for col in acct_columns:
        if col in mapping_dict:
            column_mapping[col] = mapping_dict[col]
    data = data.rename(columns=column_mapping)
    return data

def process_fs_file(file_path: str, mapping_dict: dict) -> pd.DataFrame:
    """
    Process a single FS file and rename its columns using the mapping.
    """
    try:
        df = pd.read_csv(file_path)
        df = map_acct_columns(df, mapping_dict)
        path_parts = str(file_path).split(os.sep)
        year_qtr = path_parts[-2]  
        year, qtr = year_qtr.split('-')
        
        df['year'] = year
        df['quarter'] = qtr
        df['source_file'] = os.path.basename(file_path)
        
        return df
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return pd.DataFrame()

def process_all_ncua_data(base_path: str) -> pd.DataFrame:
    """
    Process all NCUA data files across all year-quarter folders.
    """
    all_folders = [f for f in Path(base_path).iterdir() if f.is_dir()]
    all_dfs = []
    
    for folder in all_folders:
        acctdesc_path = folder / 'AcctDesc.txt'
        if not acctdesc_path.exists():
            print(f"Warning: AcctDesc.txt not found in {folder}")
            continue
            
        mapping_dict = read_acctdesc_mapping(str(acctdesc_path))
        
        fs_files = folder.glob('FS*.txt')
        for fs_file in fs_files:
            print(f"Processing {fs_file}")
            df = process_fs_file(str(fs_file), mapping_dict)
            if not df.empty:
                all_dfs.append(df)
    
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()


if __name__ == '__main__':
    base_path = 'ncua_data'
    combined_data = process_all_ncua_data(base_path)
    
    if not combined_data.empty:
        output_path = 'ncua_combined_data.csv'
        combined_data.to_csv(output_path, index=False)
        print(f"\nProcessing complete. Combined data saved to {output_path}")
        print(f"Total rows: {len(combined_data)}")
        print("\nSample of unique files processed:")
        print(combined_data['source_file'].unique()[:5])
    else:
        print("No data was processed successfully.")
    
    df = pd.read_csv('ncua_combined_data.csv')
    print(df.head())
    print(df.columns)