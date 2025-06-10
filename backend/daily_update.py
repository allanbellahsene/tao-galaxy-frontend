#!/usr/bin/env python3
"""
Daily scheduler script for automatic subnet data updates.
This script can be run via cron or other scheduling systems.
"""

import logging
import sys
import os
from datetime import datetime
from update_subnet_data import main

# Configure logging for daily runs
def setup_daily_logging():
    """Setup logging configuration for daily runs."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"daily_update_{today}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def daily_update():
    """Run the daily subnet data update process."""
    logger = setup_daily_logging()
    
    logger.info("🚀 Starting daily subnet data update process...")
    logger.info(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Run the main update process
        exit_code = main()
        
        if exit_code == 0:
            logger.info("✅ Daily subnet data update completed successfully!")
            logger.info("📊 New data files saved in results/ and results/daily/")
            return 0
        else:
            logger.error("❌ Daily subnet data update failed!")
            return 1
            
    except Exception as e:
        logger.error(f"💥 Unexpected error during daily update: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(daily_update()) 