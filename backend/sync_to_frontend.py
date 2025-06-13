import pandas as pd
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Category mapping based on existing frontend structure
CATEGORY_MAP = {
    "AI & Machine Learning": {
        "id": "ai-&-machine-learning",
        "name": "AI & Machine Learning", 
        "description": "",
        "subnets": [1, 2, 3, 4, 5, 9, 11, 15, 16, 17, 19, 20, 21, 22, 23, 29, 35, 36, 37, 38, 39, 41, 45, 46, 47, 54, 56, 58, 59, 60, 61, 62, 70, 80, 84, 85, 87, 88, 93, 94]
    },
    "Core Infrastructure": {
        "id": "core-infrastructure",
        "name": "Core Infrastructure",
        "description": "",
        "subnets": [7, 12, 26, 27, 49, 51, 63, 64, 65, 75, 81, 91]
    },
    "Data Services": {
        "id": "data-services", 
        "name": "Data Services",
        "description": "",
        "subnets": [6, 13, 18, 24, 30, 33, 40, 42, 44, 48, 50, 52, 55, 57]
    },
    "DeFi & Trading": {
        "id": "defi-&-trading",
        "name": "DeFi & Trading", 
        "description": "",
        "subnets": [8, 10, 53]
    },
    "Scientific Computing": {
        "id": "scientific-computing",
        "name": "Scientific Computing",
        "description": "",
        "subnets": [25, 43, 68, 76]
    },
    "Security & Trust": {
        "id": "security-&-trust",
        "name": "Security & Trust",
        "description": "",
        "subnets": [32, 34, 66]
    },
    "Uncategorized": {
        "id": "uncategorized",
        "name": "Uncategorized", 
        "description": "",
        "subnets": [14, 28, 31, 67, 69, 71, 72, 73, 74, 77, 78, 79, 82, 83, 86, 89, 90, 92, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]
    }
}

def safe_float(value, default=0.0):
    """Safely convert value to float, return default if conversion fails."""
    if pd.isna(value) or value == "" or value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    """Safely convert value to int, return default if conversion fails."""
    if pd.isna(value) or value == "" or value is None:
        return default
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

def safe_string(value, default=""):
    """Safely convert value to string, return default if None or empty."""
    if pd.isna(value) or value is None:
        return default
    return str(value).strip()

def get_subnet_category(subnet_id: int) -> str:
    """Get category for a subnet ID."""
    for category_name, category_info in CATEGORY_MAP.items():
        if subnet_id in category_info["subnets"]:
            return category_name
    return "Uncategorized"  # Default category

def transform_subnet_data(df: pd.DataFrame) -> List[Dict]:
    """Transform backend CSV data into frontend JSON structure."""
    logger.info("Transforming subnet data for frontend...")
    
    # Group subnets by category
    categories = {}
    
    for _, row in df.iterrows():
        subnet_id = safe_int(row['Subnet ID'])
        
        # Skip SN0 (Root subnet) as it's not shown in the frontend
        if subnet_id == 0:
            continue
            
        category_name = get_subnet_category(subnet_id)
        
        # Create subnet object with enriched fields but maintaining original structure
        subnet = {
            "id": f"SN{subnet_id}",
            "name": safe_string(row['Subnet Name'], f"Unknown"),
            "description": safe_string(row['Description']),
            "status": "active" if safe_string(row['Active']).lower() == 'true' else "inactive",
            "marketCap": safe_float(row['Market Cap']),
            "emissions": safe_float(row['Emission']),
            "weeklyChange": safe_float(row['Price Change 1 Week']),
            "validators": 0,  # Keep original structure
            "age": safe_int(row['Days Since Registration']),
            "metrics": [],  # Keep original structure
            # Enhanced fields from our backend (optional fields)
            "website": safe_string(row['Website']),
            "github": safe_string(row['Github']),
            "discord": safe_string(row['Discord']),
            "registrationDate": safe_string(row['Registration Date']),
            "daysSinceRegistration": safe_int(row['Days Since Registration']),
            "rank": safe_int(row['Rank']),
            "price": safe_float(row['Price']),
            "priceChange1Day": safe_float(row['Price Change 1 Day']),
            "priceChange1Month": safe_float(row['Price Change 1 Month']),
            "taoVolume24hr": safe_float(row['TAO Volume 24hr']),
            "timestamp": safe_string(row['Timestamp'])
        }
        
        # Initialize category if not exists
        if category_name not in categories:
            category_info = CATEGORY_MAP[category_name]
            categories[category_name] = {
                "id": category_info["id"],
                "name": category_info["name"],
                "description": category_info["description"],
                "marketCapTotal": 0.0,
                "subnets": []
            }
        
        # Add subnet to category
        categories[category_name]["subnets"].append(subnet)
        categories[category_name]["marketCapTotal"] += subnet["marketCap"]
    
    # Convert to list format expected by frontend
    result = []
    for category in categories.values():
        # Sort subnets by emissions (descending) to match original order
        category["subnets"].sort(key=lambda x: x["emissions"], reverse=True)
        result.append(category)
    
    # Sort categories by total market cap (descending) to match original order
    result.sort(key=lambda x: x["marketCapTotal"], reverse=True)
    
    logger.info(f"Transformed {sum(len(cat['subnets']) for cat in result)} subnets into {len(result)} categories")
    return result

def sync_to_frontend() -> bool:
    """Main function to sync backend data to frontend JSON."""
    try:
        logger.info("Starting backend to frontend sync...")
        
        # Read backend CSV data
        csv_path = "results/merged_subnet_data.csv"
        logger.info(f"Reading data from {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Transform data
        frontend_data = transform_subnet_data(df)
        
        # Write to frontend JSON file
        output_path = "../frontend/public/subnets_frontend_ready.json"
        logger.info(f"Writing transformed data to {output_path}")
        
        with open(output_path, 'w') as f:
            json.dump(frontend_data, f, indent=2)
        
        # Also create a backup with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"results/frontend_data_backup_{timestamp}.json"
        with open(backup_path, 'w') as f:
            json.dump(frontend_data, f, indent=2)
        
        logger.info("✅ Frontend sync completed successfully!")
        
        # Display summary
        total_subnets = sum(len(cat['subnets']) for cat in frontend_data)
        active_subnets = sum(len([s for s in cat['subnets'] if s['status'] == 'active']) for cat in frontend_data)
        total_market_cap = sum(cat['marketCapTotal'] for cat in frontend_data)
        
        print(f"\n📊 Sync Summary:")
        print(f"   Total Subnets: {total_subnets}")
        print(f"   Active Subnets: {active_subnets}")
        print(f"   Categories: {len(frontend_data)}")
        print(f"   Total Market Cap: ${total_market_cap:,.2f}")
        print(f"   Output: {output_path}")
        print(f"   Backup: {backup_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during sync: {str(e)}")
        return False

if __name__ == "__main__":
    success = sync_to_frontend()
    if not success:
        exit(1) 