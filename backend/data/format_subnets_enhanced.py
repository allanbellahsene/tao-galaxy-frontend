import pandas as pd

# Load the CSV
input_path = 'data/subnets_enhanced.csv'
df = pd.read_csv(input_path)

# Function to split the "Subnet " column
def split_subnet(subnet_str):
    if pd.isna(subnet_str):
        return '', ''
    parts = subnet_str.split(':', 1)
    if len(parts) == 2:
        subnet_id = parts[0].strip()
        subnet_name = parts[1].strip()
    else:
        subnet_id = subnet_str.strip()
        subnet_name = ''
    return subnet_id, subnet_name

# Apply the function to create new columns
df[['Subnet ID', 'Subnet Name']] = df['Subnet '].apply(lambda x: pd.Series(split_subnet(x)))

# Save the new CSV
output_path = 'data/subnets_enhanced_with_ids.csv'
df.to_csv(output_path, index=False)

print(f"New CSV with 'Subnet ID' and 'Subnet Name' columns created: {output_path}") 