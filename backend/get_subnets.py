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

def get_subnet_identities() -> Optional[pd.DataFrame]:
    """
    Fetch subnet identity data from TaoStats API.
    Returns DataFrame with columns: netuid, subnet_name, description, subnet_url, github_repo, discord
    """
    url = "https://api.taostats.io/api/subnet/identity/v1"
    api_key = os.getenv('TAOSTATS_API_KEY')
    
    if not api_key:
        logger.error("TAOSTATS_API_KEY not found in environment variables")
        return None
    
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    
    try:
        logger.info("Fetching subnet identity data...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        raw_data = response.json()
        
        # Handle the API response structure with pagination
        if isinstance(raw_data, dict) and 'data' in raw_data:
            data = raw_data['data']
            logger.info(f"Successfully fetched data for {len(data)} subnets")
        elif isinstance(raw_data, list):
            data = raw_data
            logger.info(f"Successfully fetched data for {len(data)} subnets")
        else:
            logger.error(f"Unexpected API response structure: {type(raw_data)}")
            return None
        
        # Convert to DataFrame
        if not data:
            logger.warning("No subnet data found in API response")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Ensure we have the expected columns, handle missing ones
        expected_cols = ['netuid', 'subnet_name', 'description', 'subnet_url', 'github_repo', 'discord']
        
        # Create a mapping for any column name variations
        column_mapping = {
            'subnet_url': 'subnet_url',
            'github_repo': 'github_repo',
            'discord': 'discord'
        }
        
        for col in expected_cols:
            if col not in df.columns:
                df[col] = ''
                logger.warning(f"Column '{col}' not found in API response, setting to empty string")
        
        # Select only the columns we need
        df = df[expected_cols].copy()
        
        # Clean up data - handle null values
        df = df.fillna('')
        
        # Convert netuid to integer if it's not already
        if 'netuid' in df.columns:
            df['netuid'] = pd.to_numeric(df['netuid'], errors='coerce').fillna(0).astype(int)
        
        logger.info(f"Processed subnet identity data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching subnet identity data: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing subnet identity data: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_subnet_identities(df: pd.DataFrame, output_path: str = "results/subnet_identities.csv"):
    """Save subnet identities DataFrame to CSV file."""
    try:
        # Create results directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"Subnet identities saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving subnet identities: {e}")
        return False

if __name__ == "__main__":
    # Fetch subnet identity data
    subnet_df = get_subnet_identities()
    
    if subnet_df is not None and not subnet_df.empty:
        print("\nSubnet Identity Data:")
        print(subnet_df.head(10))
        print(f"\nTotal subnets: {len(subnet_df)}")
        
        # Save to CSV
        save_subnet_identities(subnet_df)
    else:
        print("Failed to fetch subnet identity data or no data available")

