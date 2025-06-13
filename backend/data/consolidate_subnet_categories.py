import json
from collections import defaultdict

# Mapping from granular to consolidated categories
CATEGORY_MAP = {
    # Core Infrastructure
    'Infrastructure': 'Core Infrastructure',
    'Compute': 'Core Infrastructure',
    'Storage': 'Core Infrastructure',
    'Compute, Infrastructure': 'Core Infrastructure',
    'Data Pipeline, Storage': 'Core Infrastructure',
    'Infrastructure, Security': 'Core Infrastructure',
    'Compute, Generative AI': 'Core Infrastructure',
    'DeFi, Infrastructure': 'Core Infrastructure',
    'Computeinfrastructure': 'Core Infrastructure',
    # AI & Machine Learning
    'Generative AI': 'AI & Machine Learning',
    'Decentralized Training': 'AI & Machine Learning',
    'Model development': 'AI & Machine Learning',
    'AI powered tool': 'AI & Machine Learning',
    'AI Agent': 'AI & Machine Learning',
    'Decentralized Training, Model development': 'AI & Machine Learning',
    'Model development, Predictive systems': 'AI & Machine Learning',
    'Fine-tuning': 'AI & Machine Learning',
    # DeFi & Trading
    'DeFi': 'DeFi & Trading',
    'Alpha Trade Exchange': 'DeFi & Trading',
    'EfficientFrontier': 'DeFi & Trading',
    'Sturdy': 'DeFi & Trading',
    'PTN': 'DeFi & Trading',
    # Data Services
    'Data Pipeline': 'Data Services',
    'Predictive systems': 'Data Services',
    'Data Pipeline, Predictive systems': 'Data Services',
    'Data Pipeline, Storage': 'Data Services',
    # Security & Trust
    'Deepfake detection': 'Security & Trust',
    'Security': 'Security & Trust',
    'FakeNews': 'Security & Trust',
    # Scientific Computing
    'DeSci': 'Scientific Computing',
    'Protein Folding': 'Scientific Computing',
    'Nova': 'Scientific Computing',
    'Safescan': 'Scientific Computing',
    'Graphite': 'Scientific Computing',
    # Uncategorized
    None: 'Uncategorized',
    '': 'Uncategorized',
    'Uncategorized': 'Uncategorized',
    'Unknown': 'Uncategorized',
}

def consolidate_category(cat):
    if not cat or cat.strip() == '' or cat.strip().lower() == 'none':
        return 'Uncategorized'
    # Try direct match
    if cat in CATEGORY_MAP:
        return CATEGORY_MAP[cat]
    # Try splitting on comma and mapping each part
    for part in cat.split(','):
        part = part.strip()
        if part in CATEGORY_MAP:
            return CATEGORY_MAP[part]
    # Fallback: return as-is (or 'Uncategorized')
    return 'Uncategorized'

# Load the JSON
with open('data/subnets_enhanced_with_ids.json') as f:
    subnets = json.load(f)

# Group subnets by consolidated category
categories = defaultdict(list)
for subnet in subnets:
    orig_cat = subnet.get('Category')
    new_cat = consolidate_category(orig_cat)
    categories[new_cat].append(subnet)

# Prepare frontend-ready structure
frontend_categories = []
for cat_name, subnets in categories.items():
    market_cap_total = sum(s.get('Clean_Market_Cap', 0) or 0 for s in subnets)
    frontend_categories.append({
        'id': cat_name.lower().replace(' ', '-'),
        'name': cat_name,
        'description': '',
        'marketCapTotal': market_cap_total,
        'subnets': [
            {
                'id': s.get('Subnet ID'),
                'name': s.get('Subnet Name'),
                'description': s.get('Description'),
                'status': 'active',
                'marketCap': s.get('Clean_Market_Cap', 0) or 0,
                'emissions': s.get('Clean_Emission', 0) or 0,
                'weeklyChange': s.get('Price_Change_24h', 0) or 0,
                'validators': 0,
                'age': 0,
                'metrics': [],
            }
            for s in subnets
        ]
    })

# Sort categories by market cap descending
frontend_categories.sort(key=lambda c: c['marketCapTotal'], reverse=True)

# Write to output JSON
with open('frontend/public/subnets_frontend_ready.json', 'w') as f:
    json.dump(frontend_categories, f, indent=2)

print('Consolidated categories written to frontend/public/subnets_frontend_ready.json') 