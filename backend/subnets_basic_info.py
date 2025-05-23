import requests
import json
from typing import Dict, List, Optional

class TaoStatsAPI:
    def __init__(self):
        self.api_base = "https://api.taostats.io/api"
        self.headers = {"accept": "application/json",
                        "Authorization": "tao-3707df3e-8ac5-47fb-8d6c-5a9fd7bc1875:c4a98c1b"}
    
    def get_all_subnets(self) -> List[Dict]:
        """Get all subnet identity data from taostats API"""
        url = f"{self.api_base}/subnet/identity/v1"
        
        try:
            print("Fetching all subnet data from TaoStats API...")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            subnets = data.get('data', [])
            
            print(f"Successfully fetched {len(subnets)} subnets")
            return subnets
            
        except requests.RequestException as e:
            print(f"Error fetching subnet data: {e}")
            return []
    
    def get_subnet_by_id(self, target_netuid: int) -> Optional[Dict]:
        """Get specific subnet data by netuid"""
        all_subnets = self.get_all_subnets()
        
        for subnet in all_subnets:
            if subnet.get('netuid') == target_netuid:
                return subnet
        
        print(f"Subnet with netuid {target_netuid} not found")
        return None
    
    def format_subnet_data(self, subnet: Dict) -> Dict:
        """Format subnet data for easier use"""
        return {
            'netuid': subnet.get('netuid'),
            'name': subnet.get('subnet_name'),
            'description': subnet.get('description'),
            'sources': {
                'github': subnet.get('github_repo'),
                'website': subnet.get('subnet_url'),
                'discord': subnet.get('discord'),
                'contact': subnet.get('subnet_contact')
            },
            'additional_info': subnet.get('additional'),
            'raw_data': subnet
        }

def main():
    # Initialize API client
    api = TaoStatsAPI()
    
    # Get all subnets
    all_subnets = api.get_all_subnets()
    
    if not all_subnets:
        print("Failed to fetch subnet data")
        return
    
    print(f"Processing {len(all_subnets)} subnets...")
    
    # Format all subnet data
    formatted_subnets = []
    subnet_list = []
    
    for subnet in all_subnets:
        formatted_data = api.format_subnet_data(subnet)
        formatted_subnets.append(formatted_data)
        if subnet.get('netuid') == 0:
            continue
        
        # Create simplified list entry
        subnet_list.append({
            'netuid': subnet.get('netuid'),
            'name': subnet.get('subnet_name'),
            'has_github': bool(subnet.get('github_repo')),
            'has_website': bool(subnet.get('subnet_url')),
            'has_discord': bool(subnet.get('discord')),
            'has_description': bool(subnet.get('description'))
        })
    
    # Save complete subnet data
    with open('all_subnets_data.json', 'w') as f:
        json.dump(formatted_subnets, f, indent=2)
    
    # Save subnet list
    with open('subnet_list.json', 'w') as f:
        json.dump(subnet_list, f, indent=2)
    
    print(f"\n=== SUMMARY ===")
    print(f"Total subnets: {len(all_subnets)}")
    print(f"Complete data saved to: all_subnets_data.json")
    print(f"Subnet list saved to: subnet_list.json")
    
    # Show statistics
    stats = {
        'with_github': sum(1 for s in subnet_list if s['has_github']),
        'with_website': sum(1 for s in subnet_list if s['has_website']),
        'with_discord': sum(1 for s in subnet_list if s['has_discord']),
        'with_description': sum(1 for s in subnet_list if s['has_description'])
    }
    
    print(f"\n=== STATISTICS ===")
    print(f"Subnets with GitHub: {stats['with_github']}")
    print(f"Subnets with Website: {stats['with_website']}")
    print(f"Subnets with Discord: {stats['with_discord']}")
    print(f"Subnets with Description: {stats['with_description']}")
    
    # Show first 10 subnets as sample
    print(f"\n=== FIRST 10 SUBNETS ===")
    for subnet in subnet_list[:10]:
        print(f"  {subnet['netuid']}: {subnet['name']} (GitHub: {subnet['has_github']}, Website: {subnet['has_website']})")
    
    # Show Chutes specifically
    chutes = next((s for s in formatted_subnets if s['netuid'] == 64), None)
    if chutes:
        print(f"\n=== CHUTES SUBNET (SN64) ===")
        print(f"Name: {chutes['name']}")
        print(f"Description: {chutes['description']}")
        print("Sources:")
        for source_type, url in chutes['sources'].items():
            if url:
                print(f"  {source_type}: {url}")
        
        sources = [url for url in chutes['sources'].values() if url]
        print(f"\nTotal sources for Chutes: {len(sources)}")
    else:
        print("\nChutes subnet (SN64) not found in data")

if __name__ == "__main__":
    main()