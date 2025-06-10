import re
import logging
from typing import Dict, List, Set, Optional
from urllib.parse import urlparse, urljoin
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

class SourceVerifier:
    """
    Verifies and merges source URLs from Taostats and website scraping
    """
    
    def __init__(self):
        # Known source types and their matching patterns
        self.source_patterns = {
            'github': [
                r'github\.com',
                r'github\.io'
            ],
            'discord': [
                r'discord\.gg',
                r'discord\.com/invite',
                r'discordapp\.com/invite'
            ],
            'twitter': [
                r'twitter\.com',
                r'x\.com'
            ],
            'telegram': [
                r't\.me',
                r'telegram\.org'
            ],
            'linkedin': [
                r'linkedin\.com'
            ],
            'medium': [
                r'medium\.com'
            ],
            'documentation': [
                r'docs\.',
                r'documentation',
                r'gitbook\.io',
                r'notion\.site',
                r'readme\.io',
                r'/docs',
                r'/documentation'
            ],
            'whitepaper': [
                r'\.pdf',
                r'whitepaper',
                r'paper\.pdf',
                r'wp\.pdf'
            ],
            'website': [
                r'https?://'
            ]
        }
    
    def verify_and_merge_sources(self, taostats_sources: Dict, website_data: Dict) -> Dict:
        """
        Compare Taostats sources with website-discovered sources and merge them
        """
        logger.info("Starting source verification and merging")
        
        # Initialize verified sources structure
        verified_sources = {}
        
        # Extract all links from website data
        website_links = self._extract_website_links(website_data)
        
        # Process Taostats sources
        taostats_links = self._normalize_taostats_sources(taostats_sources)
        
        # Get all unique source types
        all_source_types = set(taostats_links.keys()) | set(website_links.keys())
        
        for source_type in all_source_types:
            taostats_url = taostats_links.get(source_type)
            website_urls = website_links.get(source_type, [])
            
            # Determine the status and best URL
            verified_source = self._verify_source_type(source_type, taostats_url, website_urls)
            
            if verified_source:
                verified_sources[source_type] = verified_source
        
        logger.info(f"Verified {len(verified_sources)} source types")
        return verified_sources
    
    def _extract_website_links(self, website_data: Dict) -> Dict[str, List[str]]:
        """Extract and categorize links from website scraping data"""
        categorized_links = {}
        
        if website_data.get('status') != 'success':
            return categorized_links
        
        # Collect all links from different parts of website data
        all_links = []
        
        # Add specific link types from website data
        if 'github_links' in website_data:
            all_links.extend(website_data['github_links'])
        
        if 'social_links' in website_data:
            for platform, url in website_data['social_links'].items():
                all_links.append(url)
        
        if 'documentation_links' in website_data:
            all_links.extend(website_data['documentation_links'])
        
        if 'all_links' in website_data:
            all_links.extend(website_data['all_links'])
        
        # Categorize links by type
        for link in all_links:
            if not link or not isinstance(link, str):
                continue
                
            link = link.strip()
            if not link.startswith('http'):
                continue
            
            # Determine link type
            source_type = self._categorize_link(link)
            if source_type:
                if source_type not in categorized_links:
                    categorized_links[source_type] = []
                categorized_links[source_type].append(link)
        
        # Deduplicate lists
        for source_type in categorized_links:
            categorized_links[source_type] = list(set(categorized_links[source_type]))
        
        return categorized_links
    
    def _normalize_taostats_sources(self, sources: Dict) -> Dict[str, str]:
        """Normalize Taostats sources into standard format"""
        normalized = {}
        
        # Map Taostats keys to our standard source types
        key_mapping = {
            'github': 'github',
            'website': 'website', 
            'discord': 'discord',
            'contact': 'contact',
            'subnet_url': 'website'
        }
        
        for key, value in sources.items():
            if not value:
                continue
                
            # Use mapped key or original key
            source_type = key_mapping.get(key, key)
            
            # Additional categorization for unclear sources
            if source_type == 'contact' and value:
                # Try to categorize contact URLs
                categorized_type = self._categorize_link(value)
                if categorized_type:
                    source_type = categorized_type
            
            normalized[source_type] = value
        
        return normalized
    
    def _categorize_link(self, url: str) -> Optional[str]:
        """Categorize a URL into a source type"""
        url_lower = url.lower()
        
        for source_type, patterns in self.source_patterns.items():
            for pattern in patterns:
                if re.search(pattern, url_lower):
                    return source_type
        
        return None
    
    def _verify_source_type(self, source_type: str, taostats_url: Optional[str], website_urls: List[str]) -> Optional[Dict]:
        """
        Verify a specific source type and determine the best URL and status
        """
        # Clean inputs
        taostats_url = taostats_url.strip() if taostats_url else None
        website_urls = [url.strip() for url in website_urls if url and url.strip()]
        
        # Remove duplicates and empty strings
        website_urls = list(set([url for url in website_urls if url]))
        
        if not taostats_url and not website_urls:
            return None
        
        # Determine status and best URL
        if taostats_url and website_urls:
            # Check if taostats URL matches any website URL
            matches = self._find_url_matches(taostats_url, website_urls)
            
            if matches:
                return {
                    'url': taostats_url,  # Use taostats as primary if it matches
                    'status': 'both',
                    'taostats_url': taostats_url,
                    'website_urls': website_urls,
                    'match_confidence': max(matches.values())
                }
            else:
                # URLs don't match - flag discrepancy
                return {
                    'url': taostats_url,  # Default to taostats
                    'status': 'both',  # Both sources have URLs but different
                    'taostats_url': taostats_url,
                    'website_urls': website_urls,
                    'discrepancy': True,
                    'match_confidence': 0.0
                }
        
        elif taostats_url and not website_urls:
            return {
                'url': taostats_url,
                'status': 'taostats_only',
                'taostats_url': taostats_url,
                'website_urls': []
            }
        
        elif not taostats_url and website_urls:
            return {
                'url': website_urls[0],  # Use first website URL
                'status': 'website_only',
                'taostats_url': None,
                'website_urls': website_urls
            }
        
        return None
    
    def _find_url_matches(self, taostats_url: str, website_urls: List[str]) -> Dict[str, float]:
        """
        Find matches between taostats URL and website URLs
        Returns dict of website_url: confidence_score
        """
        matches = {}
        
        for website_url in website_urls:
            confidence = self._calculate_url_similarity(taostats_url, website_url)
            if confidence > 0.8:  # High confidence threshold
                matches[website_url] = confidence
        
        return matches
    
    def _calculate_url_similarity(self, url1: str, url2: str) -> float:
        """Calculate similarity between two URLs"""
        # Simple domain-based comparison
        try:
            domain1 = urlparse(url1).netloc.lower()
            domain2 = urlparse(url2).netloc.lower()
            
            # Remove www prefix for comparison
            domain1 = domain1.replace('www.', '')
            domain2 = domain2.replace('www.', '')
            
            # Exact domain match
            if domain1 == domain2:
                return 1.0
            
            # Subdomain match (e.g., docs.example.com vs example.com)
            if domain1 in domain2 or domain2 in domain1:
                return 0.9
            
            # Similarity-based matching
            similarity = SequenceMatcher(None, domain1, domain2).ratio()
            return similarity
            
        except Exception:
            # Fallback to string similarity
            return SequenceMatcher(None, url1.lower(), url2.lower()).ratio()
    
    def create_initial_sources(self, taostats_sources: Dict) -> Dict:
        """Create initial sources structure when no website data is available"""
        verified_sources = {}
        
        normalized_sources = self._normalize_taostats_sources(taostats_sources)
        
        for source_type, url in normalized_sources.items():
            if url and url.strip():
                verified_sources[source_type] = {
                    'url': url.strip(),
                    'status': 'taostats_only',
                    'taostats_url': url.strip(),
                    'website_urls': []
                }
        
        return verified_sources
    
    def generate_verification_summary(self, verified_sources: Dict) -> Dict:
        """Generate a summary of the source verification process"""
        summary = {
            'total_sources': len(verified_sources),
            'both_sources': 0,
            'taostats_only': 0,
            'website_only': 0,
            'discrepancies': 0,
            'source_types': list(verified_sources.keys()),
            'health_score': 0.0
        }
        
        for source_type, source_data in verified_sources.items():
            status = source_data.get('status', 'unknown')
            
            if status == 'both':
                summary['both_sources'] += 1
                if source_data.get('discrepancy', False):
                    summary['discrepancies'] += 1
            elif status == 'taostats_only':
                summary['taostats_only'] += 1
            elif status == 'website_only':
                summary['website_only'] += 1
        
        # Calculate health score (percentage of verified sources)
        if summary['total_sources'] > 0:
            verified_count = summary['both_sources']
            summary['health_score'] = round((verified_count / summary['total_sources']) * 100, 1)
        
        return summary

# Utility functions for testing and debugging
def test_source_verification():
    """Test the source verification functionality"""
    verifier = SourceVerifier()
    
    # Sample Taostats sources
    taostats_sources = {
        'github': 'https://github.com/example/repo',
        'website': 'https://example.com',
        'discord': 'https://discord.gg/abc123'
    }
    
    # Sample website data
    website_data = {
        'status': 'success',
        'github_links': ['https://github.com/example/repo', 'https://github.com/example/docs'],
        'social_links': {
            'discord': 'https://discord.gg/abc123',
            'twitter': 'https://twitter.com/example'
        },
        'all_links': [
            'https://example.com',
            'https://docs.example.com',
            'https://example.com/whitepaper.pdf'
        ]
    }
    
    # Run verification
    verified_sources = verifier.verify_and_merge_sources(taostats_sources, website_data)
    summary = verifier.generate_verification_summary(verified_sources)
    
    print("=== SOURCE VERIFICATION TEST ===")
    print(f"Verified Sources: {len(verified_sources)}")
    print(f"Summary: {summary}")
    
    for source_type, source_data in verified_sources.items():
        print(f"\n{source_type.upper()}:")
        print(f"  URL: {source_data['url']}")
        print(f"  Status: {source_data['status']}")
        print(f"  Taostats: {source_data.get('taostats_url', 'None')}")
        print(f"  Website: {source_data.get('website_urls', [])}")

if __name__ == "__main__":
    test_source_verification() 