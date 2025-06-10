import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import logging
import openai
import os

logger = logging.getLogger(__name__)

class EnhancedWebsiteScraper:
    """
    Enhanced website scraper with AI-powered content understanding
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 15
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def scrape_subnet_website(self, url: str, subnet_name: str = "") -> Dict:
        """
        Multi-strategy website scraping with AI-powered content analysis
        """
        try:
            # Step 1: Normalize and validate URL
            normalized_url = self._normalize_url(url)
            
            # Step 2: Multi-attempt scraping with different strategies
            website_data = self._multi_strategy_scrape(normalized_url, subnet_name)
            
            if website_data['status'] == 'success':
                # Step 3: AI-powered content analysis
                website_data = self._ai_enhanced_analysis(website_data)
                
                # Step 4: Discover and analyze additional pages
                website_data = self._discover_additional_content(website_data, normalized_url)
            
            return website_data
            
        except Exception as e:
            logger.error(f"Enhanced scraping failed for {url}: {e}")
            return self._create_error_response(url, subnet_name, str(e))
    
    def _normalize_url(self, url: str) -> str:
        """
        Intelligent URL normalization and validation
        """
        if not url:
            raise ValueError("Empty URL provided")
        
        # Remove common prefixes/suffixes that might interfere
        url = url.strip().rstrip('/')
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            # Try HTTPS first (more common and secure)
            test_urls = [f"https://{url}", f"http://{url}"]
            
            for test_url in test_urls:
                try:
                    response = requests.head(test_url, timeout=5, allow_redirects=True)
                    if response.status_code < 400:
                        return test_url
                except:
                    continue
            
            # Default to HTTPS if both fail
            return f"https://{url}"
        
        return url
    
    def _multi_strategy_scrape(self, url: str, subnet_name: str) -> Dict:
        """
        Attempt multiple scraping strategies with exponential backoff
        """
        strategies = [
            self._standard_scrape,
            self._javascript_aware_scrape,
            self._mobile_user_agent_scrape
        ]
        
        for i, strategy in enumerate(strategies):
            try:
                logger.info(f"Attempting strategy {i+1} for {url}")
                result = strategy(url, subnet_name)
                if result['status'] == 'success':
                    return result
                
                # Brief delay between strategies
                time.sleep(1)
                
            except Exception as e:
                logger.warning(f"Strategy {i+1} failed for {url}: {e}")
                continue
        
        # All strategies failed
        return self._create_error_response(url, subnet_name, "All scraping strategies failed")
    
    def _standard_scrape(self, url: str, subnet_name: str) -> Dict:
        """Standard scraping approach"""
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'url': url,
            'subnet_name': subnet_name,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success',
            'method': 'standard',
            'soup': soup,
            'raw_html': str(soup),
            'clean_text': self._extract_clean_text(soup)
        }
    
    def _javascript_aware_scrape(self, url: str, subnet_name: str) -> Dict:
        """
        Scraping for JavaScript-heavy sites (would need selenium/playwright)
        For now, just a different user agent approach
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'url': url,
            'subnet_name': subnet_name,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success',
            'method': 'javascript_aware',
            'soup': soup,
            'raw_html': str(soup),
            'clean_text': self._extract_clean_text(soup)
        }
    
    def _mobile_user_agent_scrape(self, url: str, subnet_name: str) -> Dict:
        """Mobile user agent scraping"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
        }
        response = requests.get(url, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        return {
            'url': url,
            'subnet_name': subnet_name,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success',
            'method': 'mobile',
            'soup': soup,
            'raw_html': str(soup),
            'clean_text': self._extract_clean_text(soup)
        }
    
    def _ai_enhanced_analysis(self, website_data: Dict) -> Dict:
        """
        Use AI to extract information that pattern matching might miss
        """
        try:
            clean_text = website_data.get('clean_text', '')[:8000]  # Limit for API
            
            # AI-powered information extraction
            analysis_prompt = f"""
            Analyze this website content for a blockchain/AI project called "{website_data['subnet_name']}".
            
            Extract the following information:
            
            1. TEAM INFORMATION:
               - Number of team members (count any mentions of specific people, roles, job postings)
               - Team member names and roles
               - Leadership information
               - Company size indicators (hiring, office mentions, etc.)
               
            2. COMPANY DETAILS:
               - Mission/vision statements
               - Product descriptions
               - Technology focus
               - Business model hints
               
            3. CONTACT/SOCIAL:
               - Email addresses
               - Social media links
               - Contact forms
               
            4. EVIDENCE QUALITY:
               - Rate the evidence quality for each finding (High/Medium/Low)
               - Note any indirect evidence (job postings = team growth, etc.)
            
            Website content:
            {clean_text}
            
            Respond in JSON format with extracted information and confidence levels.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at analyzing website content to extract business and team information. Always respond in valid JSON format."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1
            )
            
            ai_analysis = json.loads(response.choices[0].message.content)
            website_data['ai_analysis'] = ai_analysis
            
            # Merge AI findings with traditional scraping
            website_data = self._merge_ai_traditional_data(website_data)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            website_data['ai_analysis'] = {'error': str(e), 'status': 'failed'}
        
        return website_data
    
    def _discover_additional_content(self, website_data: Dict, base_url: str) -> Dict:
        """
        Discover and analyze additional relevant pages
        """
        soup = website_data.get('soup')
        if not soup:
            return website_data
        
        # Common team/about page patterns
        team_page_patterns = [
            '/team', '/about', '/about-us', '/founders', '/leadership',
            '/people', '/staff', '/crew', '/our-team', '/meet-the-team',
            '/careers', '/jobs', '/join-us'
        ]
        
        additional_pages = []
        
        # Find links to potential team pages
        all_links = soup.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', '').lower()
            link_text = link.get_text().lower()
            
            # Check if link seems team-related
            if any(pattern in href or pattern in link_text for pattern in team_page_patterns):
                full_url = urljoin(base_url, link.get('href'))
                if self._is_same_domain(base_url, full_url):
                    additional_pages.append(full_url)
        
        # Scrape additional pages (limit to prevent infinite crawling)
        website_data['additional_pages'] = {}
        for page_url in additional_pages[:3]:  # Limit to 3 additional pages
            try:
                page_data = self._standard_scrape(page_url, website_data['subnet_name'])
                if page_data['status'] == 'success':
                    # AI analysis for additional page
                    page_data = self._ai_enhanced_analysis(page_data)
                    website_data['additional_pages'][page_url] = page_data
            except Exception as e:
                logger.warning(f"Failed to scrape additional page {page_url}: {e}")
        
        return website_data
    
    def _merge_ai_traditional_data(self, website_data: Dict) -> Dict:
        """
        Intelligently merge AI analysis with traditional scraping results
        """
        ai_data = website_data.get('ai_analysis', {})
        
        # Enhanced team information
        team_info = {
            'has_team_section': bool(ai_data.get('team_information', {}).get('team_members')),
            'team_members_found': len(ai_data.get('team_information', {}).get('team_members', [])),
            'team_description': ai_data.get('team_information', {}).get('description', ''),
            'company_size_indicators': ai_data.get('team_information', {}).get('size_indicators', []),
            'ai_confidence': ai_data.get('team_information', {}).get('confidence', 'Unknown')
        }
        
        # Enhanced company information
        company_info = {
            'mission': ai_data.get('company_details', {}).get('mission', ''),
            'products': ai_data.get('company_details', {}).get('products', []),
            'technology_focus': ai_data.get('company_details', {}).get('technology', ''),
            'business_model': ai_data.get('company_details', {}).get('business_model', '')
        }
        
        # Update website data with enhanced information
        website_data.update({
            'enhanced_team_info': team_info,
            'enhanced_company_info': company_info,
            'traditional_extraction_enhanced': True
        })
        
        return website_data
    
    def _extract_clean_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text from soup object"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs are from the same domain"""
        try:
            domain1 = urlparse(url1).netloc.lower()
            domain2 = urlparse(url2).netloc.lower()
            return domain1 == domain2
        except:
            return False
    
    def _create_error_response(self, url: str, subnet_name: str, error: str) -> Dict:
        """Create standardized error response"""
        return {
            'url': url,
            'subnet_name': subnet_name,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'error',
            'error': error,
            'ai_analysis': {'status': 'not_attempted'},
            'additional_pages': {}
        } 