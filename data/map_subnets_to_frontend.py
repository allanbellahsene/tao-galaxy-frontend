import json
import re
from collections import defaultdict

# Helper to slugify category names
def slugify(name):
    return re.sub(r'[^a-z0-9]+', '', name.lower().replace(' ', ''))

# Load the JSON
with open('data/subnets_enhanced_with_ids.json', 'r') as f:
    subnets = json.load(f)

# Group subnets by category
categories = defaultdict(list)
for subnet in subnets:
    category = subnet.get('Category') or 'Uncategorized'
    categories[category].append(subnet)

# Build the frontend data structure
frontend_categories = []
for cat_name, subnets_list in categories.items():
    safe_cat_name = cat_name or 'Uncategorized'
    # Calculate total market cap for the category
    market_cap_total = sum(float(s.get('Clean_Market_Cap', 0) or 0) for s in subnets_list)
    # Map subnets to frontend structure
    mapped_subnets = []
    for s in subnets_list:
        mapped_subnets.append({
            'id': s.get('Subnet ID', ''),
            'name': s.get('Subnet Name', ''),
            'description': s.get('Description', ''),
            'status': 'active',  # or infer from data if available
            'marketCap': float(s.get('Clean_Market_Cap', 0) or 0),
            'emissions': float(s.get('Clean_Emission', 0) or 0),
            'weeklyChange': float(s.get('Price_Change_24h', 0) or 0),
            'validators': int(s.get('Validators', 0) or 0),
            'age': int(s.get('Age', 0) or 0),
            'metrics': []  # Add metrics if available
        })
    frontend_categories.append({
        'id': slugify(safe_cat_name),
        'name': safe_cat_name,
        'description': '',  # Optionally fill in
        'marketCapTotal': market_cap_total,
        'subnets': mapped_subnets
    })

# Save to JSON
with open('data/subnets_frontend_ready.json', 'w') as f:
    json.dump(frontend_categories, f, indent=2)

print('Frontend-ready JSON created: data/subnets_frontend_ready.json') 