import pandas as pd
import requests

df = pd.read_csv("subnets.csv")

def extract_subnet_number(subnet_str):
    try:
        # Extract the number after "SN"
        parts = subnet_str.split(":")
        number_part = parts[0].strip()
        number = int(''.join(filter(str.isdigit, number_part)))
        return number
    except:
        return None
    

df['netuid'] = df['Subnet '].apply(extract_subnet_number)

headers = {
        "accept": "application/json",
        "Authorization": "tao-3707df3e-8ac5-47fb-8d6c-5a9fd7bc1875:c4a98c1b"
}

def fetch_subnet_data():
    url = "https://api.taostats.io/api/subnet/latest/v1"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

subnet_data = fetch_subnet_data()

# Create a mapping dictionary for quick lookup
subnet_map = {item['netuid']: item for item in subnet_data}

# Function to fetch price data from the pools endpoint
def fetch_pool_data():
    url = "https://api.taostats.io/api/dtao/pool/latest/v1"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching pool data: {response.status_code}")
        return []

print("Fetching pool data from TaoStats API...")
pool_data = fetch_pool_data()

pool_map = {item['netuid']: item for item in pool_data}

df['Emission'] = None
df['Emission_Percentage'] = None
df['Current_Price'] = None
df['Price_Change_24h'] = None
df['Market_Cap'] = None
df['Symbol'] = None
df["Circulating_Supply"] = None

# Total emission across all subnets
total_emission = sum(float(subnet['emission']) for subnet in subnet_data if 'emission' in subnet)

# Calculate and add the data for each subnet
for index, row in df.iterrows():
    netuid = row['netuid']
    
    # Add emission data
    if netuid is not None and netuid in subnet_map:
        subnet_info = subnet_map[netuid]
        
        if 'emission' in subnet_info:
            emission_value = float(subnet_info['emission'])
            df.at[index, 'Emission'] = emission_value
            
            # Calculate emission percentage
            percentage = (emission_value / total_emission) * 100
            df.at[index, 'Emission_Percentage'] = f"{percentage:.2f}%"
    
    # Add price data
    if netuid is not None and netuid in pool_map:
        pool_info = pool_map[netuid]
        
        if 'price' in pool_info:
            df.at[index, 'Current_Price'] = pool_info['price']
        
        if 'price_change_1_day' in pool_info:
            df.at[index, 'Price_Change_24h'] = pool_info['price_change_1_day']
        
        if 'market_cap' in pool_info:
            df.at[index, 'Market_Cap'] = pool_info['market_cap']
            
        if 'symbol' in pool_info:
            df.at[index, 'Symbol'] = pool_info['symbol']

        if 'total_alpha' in pool_info:
            df.at[index, 'Circulating_Supply'] = pool_info['total_alpha']

# Clean and prepare the data
def clean_numeric(value):
    if pd.isna(value):
        return 0
    if isinstance(value, str):
        return float(value.replace('%', ''))
    return float(value)

# Clean price, emission, and market cap columns
df['Clean_Price'] = df['Current_Price'].apply(lambda x: clean_numeric(x) if not pd.isna(x) else 0)
df['Clean_Emission'] = df['Emission_Percentage'].apply(lambda x: clean_numeric(x) if not pd.isna(x) else 0)

df["Clean_Market_Cap"] = ( df["Circulating_Supply"].astype(float) / 10**9 ) * df["Clean_Price"].astype(float) * 367

print(df.head())

df.to_csv('subnets_enhanced.csv', index=False)
