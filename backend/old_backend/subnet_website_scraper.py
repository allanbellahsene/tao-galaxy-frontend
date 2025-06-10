import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubnetWebsiteScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
    
    def scrape_subnet_website(self, url: str, subnet_name: str = "") -> Dict:
        """
        Scrape a subnet website and extract information relevant to the 26 questions
        """
        try:
            logger.info(f"Scraping website: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract structured data
            website_data = {
                'url': url,
                'subnet_name': subnet_name,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'success',
                
                # Basic Information
                'title': self._extract_title(soup),
                'description': self._extract_description(soup),
                'mission': self._extract_mission(soup),
                
                # Team Information
                'team_info': self._extract_team_info(soup),
                'team_members': self._extract_team_members(soup),
                
                # Product/Problem Information
                'problem_statement': self._extract_problem_statement(soup),
                'solution': self._extract_solution(soup),
                'products': self._extract_products(soup),
                'revenue_model': self._extract_revenue_model(soup),
                
                # Communication/Marketing
                'social_links': self._extract_social_links(soup),
                'contact_info': self._extract_contact_info(soup),
                
                # Technical Information
                'github_links': self._extract_github_links(soup),
                'documentation_links': self._extract_documentation_links(soup),
                
                # Raw content for AI processing
                'clean_text': self._extract_clean_text(soup),
                'all_links': self._extract_all_links(soup, url),
                
                # Page structure analysis
                'has_about_section': self._has_section(soup, ['about', 'mission', 'vision']),
                'has_team_section': self._has_section(soup, ['team', 'founders', 'leadership']),
                'has_product_section': self._has_section(soup, ['product', 'solution', 'features']),
            }
            
            return website_data
            
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'subnet_name': subnet_name,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        # Fallback to h1
        h1_tag = soup.find('h1')
        if h1_tag:
            return h1_tag.get_text().strip()
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description from meta tags or first paragraph"""
        # Try meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc.get('content').strip()
        
        # Try og:description
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc.get('content').strip()
        
        # Fallback to first substantial paragraph
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 50:  # Substantial content
                return text
        
        return ""
    
    def _extract_mission(self, soup: BeautifulSoup) -> str:
        """Extract mission statement"""
        mission_keywords = ['mission', 'vision', 'purpose', 'goal', 'objective']
        
        # Look for sections with mission-related keywords
        for keyword in mission_keywords:
            # Check headings
            for tag in ['h1', 'h2', 'h3', 'h4']:
                headings = soup.find_all(tag)
                for heading in headings:
                    if keyword in heading.get_text().lower():
                        # Get next paragraph or div
                        next_elem = heading.find_next_sibling(['p', 'div'])
                        if next_elem:
                            return next_elem.get_text().strip()
            
            # Check for divs/sections with class containing keyword
            sections = soup.find_all(['div', 'section'], class_=re.compile(keyword, re.I))
            for section in sections:
                text = section.get_text().strip()
                if len(text) > 20:
                    return text[:500]  # Limit length
        
        return ""
    
    def _extract_team_info(self, soup: BeautifulSoup) -> Dict:
        """Extract team information"""
        team_info = {
            'has_team_section': False,
            'team_members_found': 0,
            'team_description': ""
        }
        
        team_keywords = ['team', 'founders', 'leadership', 'about us', 'who we are']
        
        for keyword in team_keywords:
            # Look for team sections
            sections = soup.find_all(['div', 'section'], class_=re.compile(keyword.replace(' ', ''), re.I))
            for section in sections:
                team_info['has_team_section'] = True
                team_info['team_description'] = section.get_text().strip()[:1000]
                break
            
            if team_info['has_team_section']:
                break
        
        return team_info
    
    def _extract_team_members(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract individual team member information"""
        team_members = []
        
        # Look for common team member patterns
        member_selectors = [
            '.team-member', '.founder', '.leadership-member',
            '[class*="team"]', '[class*="founder"]'
        ]
        
        for selector in member_selectors:
            members = soup.select(selector)
            for member in members:
                name = ""
                role = ""
                bio = ""
                
                # Extract name (usually in h3, h4, or strong)
                name_elem = member.find(['h3', 'h4', 'strong', '.name'])
                if name_elem:
                    name = name_elem.get_text().strip()
                
                # Extract role/title
                role_elem = member.find(['.role', '.title', '.position'])
                if role_elem:
                    role = role_elem.get_text().strip()
                
                # Extract bio
                bio_elem = member.find('p')
                if bio_elem:
                    bio = bio_elem.get_text().strip()
                
                if name:  # Only add if we found a name
                    team_members.append({
                        'name': name,
                        'role': role,
                        'bio': bio
                    })
        
        return team_members
    
    def _extract_problem_statement(self, soup: BeautifulSoup) -> str:
        """Extract problem statement or challenge description"""
        problem_keywords = ['problem', 'challenge', 'issue', 'pain point', 'why']
        
        for keyword in problem_keywords:
            # Look for headings with problem-related keywords
            for tag in ['h1', 'h2', 'h3']:
                headings = soup.find_all(tag)
                for heading in headings:
                    if keyword in heading.get_text().lower():
                        next_elem = heading.find_next_sibling(['p', 'div'])
                        if next_elem:
                            return next_elem.get_text().strip()
        
        return ""
    
    def _extract_solution(self, soup: BeautifulSoup) -> str:
        """Extract solution description"""
        solution_keywords = ['solution', 'how it works', 'approach', 'methodology']
        
        for keyword in solution_keywords:
            for tag in ['h1', 'h2', 'h3']:
                headings = soup.find_all(tag)
                for heading in headings:
                    if keyword in heading.get_text().lower():
                        next_elem = heading.find_next_sibling(['p', 'div'])
                        if next_elem:
                            return next_elem.get_text().strip()
        
        return ""
    
    def _extract_products(self, soup: BeautifulSoup) -> List[str]:
        """Extract product information"""
        products = []
        product_keywords = ['product', 'service', 'offering', 'feature']
        
        for keyword in product_keywords:
            sections = soup.find_all(['div', 'section'], class_=re.compile(keyword, re.I))
            for section in sections:
                text = section.get_text().strip()
                if len(text) > 20:
                    products.append(text[:300])
        
        return products
    
    def _extract_revenue_model(self, soup: BeautifulSoup) -> str:
        """Extract revenue model information"""
        revenue_keywords = ['revenue', 'monetization', 'business model', 'pricing']
        
        for keyword in revenue_keywords:
            for tag in ['h1', 'h2', 'h3']:
                headings = soup.find_all(tag)
                for heading in headings:
                    if keyword in heading.get_text().lower():
                        next_elem = heading.find_next_sibling(['p', 'div'])
                        if next_elem:
                            return next_elem.get_text().strip()
        
        return ""
    
    def _extract_social_links(self, soup: BeautifulSoup) -> Dict:
        """Extract social media links"""
        social_links = {}
        social_patterns = {
            'twitter': r'twitter\.com|x\.com',
            'discord': r'discord\.gg|discord\.com',
            'telegram': r't\.me|telegram\.org',
            'linkedin': r'linkedin\.com',
            'medium': r'medium\.com'
        }
        
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '').lower()
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href):
                    social_links[platform] = href
                    break
        
        return social_links
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information"""
        contact_info = {}
        
        # Look for email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        page_text = soup.get_text()
        emails = re.findall(email_pattern, page_text)
        if emails:
            contact_info['emails'] = list(set(emails))
        
        return contact_info
    
    def _extract_github_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract GitHub repository links"""
        github_links = []
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '')
            if 'github.com' in href.lower():
                github_links.append(href)
        
        return list(set(github_links))
    
    def _extract_documentation_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract documentation links"""
        doc_links = []
        links = soup.find_all('a', href=True)
        
        doc_keywords = ['docs', 'documentation', 'guide', 'tutorial', 'api']
        
        for link in links:
            href = link.get('href', '').lower()
            text = link.get_text().lower()
            
            if any(keyword in href or keyword in text for keyword in doc_keywords):
                doc_links.append(link.get('href'))
        
        return list(set(doc_links))
    
    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text content for AI processing"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text[:10000]  # Limit for AI processing
    
    def _extract_all_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all links from the page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href.startswith('/'):
                href = urljoin(base_url, href)
            links.append(href)
        
        return list(set(links))
    
    def _has_section(self, soup: BeautifulSoup, keywords: List[str]) -> bool:
        """Check if page has sections with specific keywords"""
        page_text = soup.get_text().lower()
        return any(keyword in page_text for keyword in keywords)

def test_chutes_scraping():
    """Test scraping Chutes website"""
    scraper = SubnetWebsiteScraper()
    
    # Test with Chutes website
    chutes_url = "https://chutes.ai"  # Assuming this is the URL
    
    result = scraper.scrape_subnet_website(chutes_url, "Chutes")
    
    if result['status'] == 'success':
        print("=== CHUTES WEBSITE SCRAPING RESULTS ===")
        print(f"Title: {result['title']}")
        print(f"Description: {result['description']}")
        print(f"Mission: {result['mission']}")
        print(f"Team Info: {result['team_info']}")
        print(f"Social Links: {result['social_links']}")
        print(f"GitHub Links: {result['github_links']}")
        print(f"Has About Section: {result['has_about_section']}")
        print(f"Has Team Section: {result['has_team_section']}")
        
        # Save results
        with open('chutes_website_data.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print("\nData saved to chutes_website_data.json")
    else:
        print(f"Error scraping Chutes website: {result.get('error')}")

if __name__ == "__main__":
    test_chutes_scraping()