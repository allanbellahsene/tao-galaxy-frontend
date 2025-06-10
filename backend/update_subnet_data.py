#!/usr/bin/env python3
"""
Main script to update comprehensive subnet data by fetching from TaoStats API and merging datasets.
Includes daily historical data saving and comprehensive market data enrichment.
"""

import sys
import os
from merge_subnet_data import merge_subnet_data, save_merged_data, save_daily_data, display_comprehensive_summary
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to update comprehensive subnet data."""
    logger.info("Starting comprehensive subnet data update process...")
    
    try:
        # Merge comprehensive subnet data from multiple sources
        merged_df = merge_subnet_data()
        
        if merged_df is not None:
            # Display comprehensive summary
            display_comprehensive_summary(merged_df)
            
            # Save current merged data (latest)
            csv_success = save_merged_data(merged_df, "results/merged_subnet_data.csv")
            
            # Save daily historical data with date-based filenames
            daily_success = save_daily_data(merged_df)
            
            # Save as JSON for frontend use
            json_path = "results/merged_subnet_data.json"
            try:
                merged_df.to_json(json_path, orient='records', indent=2, date_format='iso')
                json_success = True
                logger.info(f"Data saved as JSON to {json_path}")
            except Exception as e:
                logger.error(f"Error saving JSON: {e}")
                json_success = False
            
            # Report results
            if csv_success and json_success and daily_success:
                logger.info("✅ Comprehensive subnet data update completed successfully!")
                logger.info("📊 Data includes: Identity, Statistics (% emissions), Market Data")
                logger.info("📅 Daily historical files saved for data continuity")
                return 0
            else:
                logger.error("❌ Some files failed to save")
                return 1
        else:
            logger.error("❌ Failed to merge comprehensive subnet data")
            return 1
            
    except Exception as e:
        logger.error(f"❌ Unexpected error in main process: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())