import requests
import pandas as pd
import os
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_subnet_latest_stats() -> Optional[pd.DataFrame]:
    """
    Fetch latest subnet statistics from TaoStats API.
    Returns DataFrame with columns: netuid, emission, active (renamed from subtoken_enabled), timestamp
    """
    url = "https://api.taostats.io/api/subnet/latest/v1"
    api_key = os.getenv('TAOSTATS_API_KEY')
    
    if not api_key:
        logger.error("TAOSTATS_API_KEY not found in environment variables")
        return None
    
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    
    try:
        logger.info("Fetching latest subnet statistics...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        raw_data = response.json()
        
        # Handle the API response structure with pagination
        if isinstance(raw_data, dict) and 'data' in raw_data:
            data = raw_data['data']
            logger.info(f"Successfully fetched latest stats for {len(data)} subnets")
        elif isinstance(raw_data, list):
            data = raw_data
            logger.info(f"Successfully fetched latest stats for {len(data)} subnets")
        else:
            logger.error(f"Unexpected API response structure: {type(raw_data)}")
            return None
        
        # Convert to DataFrame
        if not data:
            logger.warning("No subnet statistics data found in API response")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Select only the columns we need and rename
        columns_to_keep = {
            'netuid': 'netuid',
            'emission': 'emission', 
            'subtoken_enabled': 'active',
            'timestamp': 'timestamp'
        }
        
        # Check if required columns exist, handle missing ones
        missing_cols = []
        for col in columns_to_keep.keys():
            if col not in df.columns:
                missing_cols.append(col)
                if col == 'subtoken_enabled':
                    df[col] = False  # Default to False for active status
                elif col == 'emission':
                    df[col] = 0.0  # Default emission to 0
                elif col == 'timestamp':
                    df[col] = datetime.now().isoformat()  # Default to current time
                else:
                    df[col] = ''
                
        if missing_cols:
            logger.warning(f"Missing columns in API response, using defaults: {missing_cols}")
        
        # Select and rename columns
        df = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep).copy()
        
        # Convert emission to numeric
        df['emission'] = pd.to_numeric(df['emission'], errors='coerce').fillna(0.0)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Ensure active is boolean
        df['active'] = df['active'].astype(bool)
        
        # Convert netuid to integer
        df['netuid'] = pd.to_numeric(df['netuid'], errors='coerce').fillna(0).astype(int)
        
        logger.info(f"Processed subnet statistics: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching subnet statistics: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing subnet statistics: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_subnet_stats(df: pd.DataFrame, output_path: str = "results/subnet_stats.csv"):
    """Save subnet statistics DataFrame to CSV file."""
    try:
        # Create results directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"Subnet statistics saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving subnet statistics: {e}")
        return False

if __name__ == "__main__":
    # Fetch subnet statistics
    stats_df = get_subnet_latest_stats()
    
    if stats_df is not None and not stats_df.empty:
        print("\nSubnet Statistics Data:")
        print(stats_df.head(10))
        print(f"\nTotal subnets: {len(stats_df)}")
        
        # Show some summary stats
        print(f"\nEmission Summary:")
        print(f"Total Emission: {stats_df['emission'].sum():.2f}")
        print(f"Average Emission: {stats_df['emission'].mean():.4f}")
        print(f"Active Subnets: {stats_df['active'].sum()}")
        
        # Save to CSV
        save_subnet_stats(stats_df)
    else:
        print("Failed to fetch subnet statistics or no data available")