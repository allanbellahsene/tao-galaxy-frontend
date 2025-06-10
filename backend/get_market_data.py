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

def get_market_data() -> Optional[pd.DataFrame]:
    """
    Fetch market data from TaoStats dtao pool API.
    Returns DataFrame with columns: netuid, rank, market_cap, price, 
    price_change_1_day, price_change_1_week, price_change_1_month, tao_volume_24_hr
    """
    url = "https://api.taostats.io/api/dtao/pool/latest/v1?page=1"
    api_key = os.getenv('TAOSTATS_API_KEY')
    
    if not api_key:
        logger.error("TAOSTATS_API_KEY not found in environment variables")
        return None
    
    headers = {
        "accept": "application/json",
        "Authorization": api_key
    }
    
    try:
        logger.info("Fetching market data...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        raw_data = response.json()
        
        # Handle the API response structure with pagination
        if isinstance(raw_data, dict) and 'data' in raw_data:
            data = raw_data['data']
            logger.info(f"Successfully fetched market data for {len(data)} subnets")
        elif isinstance(raw_data, list):
            data = raw_data
            logger.info(f"Successfully fetched market data for {len(data)} subnets")
        else:
            logger.error(f"Unexpected API response structure: {type(raw_data)}")
            return None
        
        # Convert to DataFrame
        if not data:
            logger.warning("No market data found in API response")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Select only the columns we need
        columns_to_keep = [
            'netuid', 
            'rank', 
            'market_cap', 
            'price', 
            'price_change_1_day', 
            'price_change_1_week', 
            'price_change_1_month', 
            'tao_volume_24_hr'
        ]
        
        # Check if required columns exist, handle missing ones
        missing_cols = []
        for col in columns_to_keep:
            if col not in df.columns:
                missing_cols.append(col)
                if col in ['rank']:
                    df[col] = 0  # Default rank to 0
                elif col in ['market_cap', 'price', 'tao_volume_24_hr']:
                    df[col] = 0.0  # Default monetary values to 0
                elif col in ['price_change_1_day', 'price_change_1_week', 'price_change_1_month']:
                    df[col] = None  # Default price changes to None (will be handled later)
                else:
                    df[col] = ''
                
        if missing_cols:
            logger.warning(f"Missing columns in API response, using defaults: {missing_cols}")
        
        # Select only the columns we need
        df = df[columns_to_keep].copy()
        
        # Convert data types
        df['netuid'] = pd.to_numeric(df['netuid'], errors='coerce').fillna(0).astype(int)
        df['rank'] = pd.to_numeric(df['rank'], errors='coerce').fillna(0).astype(int)
        df['market_cap'] = pd.to_numeric(df['market_cap'], errors='coerce').fillna(0.0)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
        df['price_change_1_day'] = pd.to_numeric(df['price_change_1_day'], errors='coerce')
        df['price_change_1_week'] = pd.to_numeric(df['price_change_1_week'], errors='coerce')
        df['price_change_1_month'] = pd.to_numeric(df['price_change_1_month'], errors='coerce')
        df['tao_volume_24_hr'] = pd.to_numeric(df['tao_volume_24_hr'], errors='coerce').fillna(0.0)
        
        # Convert from rao to TAO (1 TAO = 1 billion rao)
        RAO_TO_TAO = 1e9
        df['market_cap'] = df['market_cap'] / RAO_TO_TAO
        df['tao_volume_24_hr'] = df['tao_volume_24_hr'] / RAO_TO_TAO
        
        logger.info(f"Converted market_cap and tao_volume_24_hr from rao to TAO")
        logger.info(f"Processed market data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching market data: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error processing market data: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_market_data(df: pd.DataFrame, output_path: str = "results/market_data.csv"):
    """Save market data DataFrame to CSV file."""
    try:
        # Create results directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"Market data saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving market data: {e}")
        return False

if __name__ == "__main__":
    # Fetch market data
    market_df = get_market_data()
    
    if market_df is not None and not market_df.empty:
        print("\nMarket Data:")
        print(market_df.head(10))
        print(f"\nTotal subnets: {len(market_df)}")
        
        # Show some summary stats
        print(f"\nMarket Summary:")
        print(f"Total Market Cap: ${market_df['market_cap'].sum():,.2f}")
        print(f"Average Price: ${market_df['price'].mean():.4f}")
        print(f"Total 24h Volume: {market_df['tao_volume_24_hr'].sum():,.0f} TAO")
        
        # Save to CSV
        save_market_data(market_df)
    else:
        print("Failed to fetch market data or no data available") 