import pandas as pd
import os
import logging
from typing import Optional
from datetime import datetime
from get_subnets import get_subnet_identities
from get_subnet_stats import get_subnet_latest_stats
from get_market_data import get_market_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def merge_subnet_data() -> Optional[pd.DataFrame]:
    """
    Merge subnet identity, statistics, and market data into a comprehensive dataset.
    Returns DataFrame with columns: Timestamp, Subnet ID, Subnet Name, Description, 
    Emission (as %), Active, Website, Github, Discord, Registration Date, Days Since Registration,
    Rank, Market Cap, Price, Price Change 1 Day, Price Change 1 Week, Price Change 1 Month, TAO Volume 24hr
    """
    logger.info("Starting comprehensive subnet data merge process...")
    
    # Fetch identity data
    identity_df = get_subnet_identities()
    if identity_df is None:
        logger.error("Failed to fetch subnet identity data")
        return None
    
    # Fetch statistics data
    stats_df = get_subnet_latest_stats()
    if stats_df is None:
        logger.error("Failed to fetch subnet statistics data")
        return None
    
    # Fetch market data
    market_df = get_market_data()
    if market_df is None:
        logger.error("Failed to fetch market data")
        return None
    
    logger.info(f"Identity data: {len(identity_df)} subnets")
    logger.info(f"Statistics data: {len(stats_df)} subnets")
    logger.info(f"Market data: {len(market_df)} subnets")
    
    # Convert emissions to percentages BEFORE merging
    total_emission = stats_df['emission'].sum()
    if total_emission > 0:
        stats_df['emission'] = (stats_df['emission'] / total_emission * 100).round(4)
        logger.info(f"Converted emissions to percentages (total was: {total_emission})")
    else:
        logger.warning("Total emission is 0, keeping absolute values")
    
    # Start with identity data as the base
    merged_df = identity_df.copy()
    
    # Merge with statistics data
    merged_df = pd.merge(
        merged_df,
        stats_df,
        on='netuid',
        how='outer',
        suffixes=('', '_stats')
    )
    
    # Merge with market data
    merged_df = pd.merge(
        merged_df,
        market_df,
        on='netuid',
        how='outer',
        suffixes=('', '_market')
    )
    
    logger.info(f"Final merged data: {len(merged_df)} subnets")
    
    # Create the final column mapping to match the desired output format
    final_column_mapping = {
        'timestamp': 'Timestamp',
        'netuid': 'Subnet ID',
        'subnet_name': 'Subnet Name',
        'description': 'Description',
        'emission': 'Emission',
        'active': 'Active',
        'subnet_url': 'Website',
        'github_repo': 'Github',
        'discord': 'Discord',
        'registration_timestamp': 'Registration Date',
        'days_since_registration': 'Days Since Registration',
        'rank': 'Rank',
        'market_cap': 'Market Cap',
        'price': 'Price',
        'price_change_1_day': 'Price Change 1 Day',
        'price_change_1_week': 'Price Change 1 Week',
        'price_change_1_month': 'Price Change 1 Month',
        'tao_volume_24_hr': 'TAO Volume 24hr'
    }
    
    # Ensure all required columns exist
    for original_col in final_column_mapping.keys():
        if original_col not in merged_df.columns:
            if original_col == 'timestamp':
                merged_df[original_col] = datetime.now()
            elif original_col in ['emission', 'market_cap', 'price', 'tao_volume_24_hr']:
                merged_df[original_col] = 0.0
            elif original_col in ['price_change_1_day', 'price_change_1_week', 'price_change_1_month']:
                merged_df[original_col] = None
            elif original_col in ['rank', 'days_since_registration']:
                merged_df[original_col] = 0
            elif original_col in ['active']:
                merged_df[original_col] = False
            elif original_col in ['registration_timestamp']:
                merged_df[original_col] = None
            else:
                merged_df[original_col] = ''
    
    # Select and rename columns
    final_columns = list(final_column_mapping.keys())
    merged_df = merged_df[final_columns].rename(columns=final_column_mapping)
    
    # Fill missing values appropriately
    merged_df['Timestamp'] = merged_df['Timestamp'].fillna(datetime.now())
    merged_df['Subnet Name'] = merged_df['Subnet Name'].fillna('Unknown')
    merged_df['Description'] = merged_df['Description'].fillna('')
    merged_df['Emission'] = merged_df['Emission'].fillna(0.0)
    merged_df['Active'] = merged_df['Active'].fillna(False)
    merged_df['Website'] = merged_df['Website'].fillna('')
    merged_df['Github'] = merged_df['Github'].fillna('')
    merged_df['Discord'] = merged_df['Discord'].fillna('')
    merged_df['Days Since Registration'] = merged_df['Days Since Registration'].fillna(0)
    merged_df['Rank'] = merged_df['Rank'].fillna(0)
    merged_df['Market Cap'] = merged_df['Market Cap'].fillna(0.0)
    merged_df['Price'] = merged_df['Price'].fillna(0.0)
    merged_df['TAO Volume 24hr'] = merged_df['TAO Volume 24hr'].fillna(0.0)
    # Note: Price change columns and Registration Date can remain as NaN for subnets without data
    
    # Sort by Subnet ID
    merged_df = merged_df.sort_values('Subnet ID').reset_index(drop=True)
    
    logger.info(f"Final comprehensive dataset: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
    
    return merged_df

def save_merged_data(df: pd.DataFrame, output_path: str = "results/merged_subnet_data.csv"):
    """Save merged subnet data to CSV file."""
    try:
        # Create results directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        logger.info(f"Merged subnet data saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving merged subnet data: {e}")
        return False

def save_daily_data(df: pd.DataFrame, base_dir: str = "results/daily"):
    """Save daily historical data with date-based filename."""
    try:
        # Create daily directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        # Generate date-based filename
        today = datetime.now().strftime("%Y-%m-%d")
        csv_filename = f"subnet_data_{today}.csv"
        json_filename = f"subnet_data_{today}.json"
        
        csv_path = os.path.join(base_dir, csv_filename)
        json_path = os.path.join(base_dir, json_filename)
        
        # Save CSV
        df.to_csv(csv_path, index=False)
        logger.info(f"Daily data saved to {csv_path}")
        
        # Save JSON
        df.to_json(json_path, orient='records', indent=2, date_format='iso')
        logger.info(f"Daily data saved to {json_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error saving daily data: {e}")
        return False

def display_comprehensive_summary(df: pd.DataFrame):
    """Display a comprehensive summary of the merged data."""
    print("\n" + "="*80)
    print("COMPREHENSIVE SUBNET DATA SUMMARY")
    print("="*80)
    
    print(f"\nTotal Subnets: {len(df)}")
    print(f"Active Subnets: {df['Active'].sum()}")
    print(f"Inactive Subnets: {(~df['Active']).sum()}")
    
    print(f"\nEmission Distribution (%):")
    print(f"Total Percentage: {df['Emission'].sum():.2f}%")
    print(f"Average Emission: {df['Emission'].mean():.4f}%")
    print(f"Max Emission: {df['Emission'].max():.4f}%")
    
    print(f"\nMarket Data:")
    print(f"Total Market Cap: ${df['Market Cap'].sum():,.2f}")
    print(f"Average Price: ${df['Price'].mean():.4f}")
    print(f"Total 24h Volume: {df['TAO Volume 24hr'].sum():,.0f} TAO")
    
    # Show registration statistics
    valid_days = df['Days Since Registration'].replace(0, None).dropna()
    if not valid_days.empty:
        print(f"\nRegistration Statistics:")
        print(f"Oldest subnet: {valid_days.max():.0f} days old")
        print(f"Newest subnet: {valid_days.min():.0f} days old")
        print(f"Average age: {valid_days.mean():.1f} days")
        print(f"Subnets with registration data: {len(valid_days)}")
    
    # Count subnets with various data fields
    print(f"\nData Completeness:")
    print(f"Subnets with Website: {(df['Website'] != '').sum()}")
    print(f"Subnets with Github: {(df['Github'] != '').sum()}")
    print(f"Subnets with Discord: {(df['Discord'] != '').sum()}")
    print(f"Subnets with Market Data: {(df['Market Cap'] > 0).sum()}")
    print(f"Subnets with Registration Data: {(df['Days Since Registration'] > 0).sum()}")
    
    # Show top 10 by emission percentage
    print(f"\nTop 10 Subnets by Emission (%):")
    top_subnets = df.nlargest(10, 'Emission')[['Subnet ID', 'Subnet Name', 'Emission', 'Active', 'Days Since Registration']]
    print(top_subnets.to_string(index=False))
    
    # Show top 10 by market cap
    print(f"\nTop 10 Subnets by Market Cap:")
    top_market_cap = df.nlargest(10, 'Market Cap')[['Subnet ID', 'Subnet Name', 'Market Cap', 'Price', 'Days Since Registration']]
    print(top_market_cap.to_string(index=False))
    
    # Show first few rows
    print(f"\nFirst 5 rows of comprehensive data:")
    display_cols = ['Subnet ID', 'Subnet Name', 'Emission', 'Active', 'Days Since Registration', 'Market Cap']
    print(df[display_cols].head().to_string(index=False))

if __name__ == "__main__":
    # Merge comprehensive subnet data
    merged_df = merge_subnet_data()
    
    if merged_df is not None:
        # Display comprehensive summary
        display_comprehensive_summary(merged_df)
        
        # Save current merged data
        save_merged_data(merged_df)
        
        # Save daily historical data
        save_daily_data(merged_df)
        
        # Also save as JSON for potential frontend use
        json_output_path = "results/merged_subnet_data.json"
        try:
            merged_df.to_json(json_output_path, orient='records', indent=2, date_format='iso')
            logger.info(f"Merged subnet data also saved as JSON to {json_output_path}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            
    else:
        print("Failed to merge comprehensive subnet data")