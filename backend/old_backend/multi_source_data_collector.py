import requests
import json
import logging
import time
from typing import Dict, List, Optional, Tuple
import asyncio
import aiohttp
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class DataSource:
    name: str
    priority: int
    confidence: float
    data: Dict

class MultiSourceDataCollector:
    """
    Collect subnet information from multiple sources with intelligent fallback
    """
    
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.github_api_base = "https://api.github.com"
        self.timeout = 10
    
    async def collect_comprehensive_data(self, subnet_info: Dict) -> Dict:
        """
        Collect data from multiple sources and intelligently merge results
        """
        sources_data = []
        
        # Source 1: Website scraping (primary)
        if subnet_info.get('sources', {}).get('website'):
            website_data = await self._collect_website_data(subnet_info)
            if website_data:
                sources_data.append(DataSource("website", 1, 0.9, website_data))
        
        # Source 2: GitHub analysis (high confidence for technical projects)
        if subnet_info.get('sources', {}).get('github'):
            github_data = await self._collect_github_data(subnet_info)
            if github_data:
                sources_data.append(DataSource("github", 2, 0.8, github_data))
        
        # Source 3: Social media analysis
        social_data = await self._collect_social_media_data(subnet_info)
        if social_data:
            sources_data.append(DataSource("social_media", 3, 0.6, social_data))
        
        # Source 4: Blockchain/registry data
        registry_data = await self._collect_registry_data(subnet_info)
        if registry_data:
            sources_data.append(DataSource("registry", 4, 0.7, registry_data))
        
        # Source 5: Search engine results
        search_data = await self._collect_search_results(subnet_info)
        if search_data:
            sources_data.append(DataSource("search", 5, 0.5, search_data))
        
        # Intelligently merge all sources
        merged_data = self._intelligent_merge(sources_data, subnet_info)
        
        return merged_data
    
    async def _collect_github_data(self, subnet_info: Dict) -> Optional[Dict]:
        """
        Comprehensive GitHub analysis for team and project information
        """
        try:
            github_url = subnet_info.get('sources', {}).get('github', '')
            if not github_url:
                return None
            
            # Extract owner and repo from GitHub URL
            repo_match = re.search(r'github\.com/([^/]+)/([^/]+)', github_url)
            if not repo_match:
                return None
            
            owner, repo = repo_match.groups()
            
            # Collect multiple GitHub data points
            github_data = {
                'repository_info': await self._get_github_repo_info(owner, repo),
                'contributors': await self._get_github_contributors(owner, repo),
                'organization_info': await self._get_github_org_info(owner),
                'recent_activity': await self._get_github_activity(owner, repo),
                'readme_content': await self._get_github_readme(owner, repo)
            }
            
            # Analyze GitHub data for team information
            team_analysis = self._analyze_github_team_data(github_data)
            github_data['team_analysis'] = team_analysis
            
            return github_data
            
        except Exception as e:
            logger.error(f"GitHub data collection failed: {e}")
            return None
    
    async def _get_github_repo_info(self, owner: str, repo: str) -> Dict:
        """Get basic repository information"""
        try:
            url = f"{self.github_api_base}/repos/{owner}/{repo}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.warning(f"Failed to get repo info: {e}")
        return {}
    
    async def _get_github_contributors(self, owner: str, repo: str) -> List[Dict]:
        """Get repository contributors"""
        try:
            url = f"{self.github_api_base}/repos/{owner}/{repo}/contributors"
            async with self.session.get(url) as response:
                if response.status == 200:
                    contributors = await response.json()
                    
                    # Get detailed info for top contributors
                    detailed_contributors = []
                    for contributor in contributors[:10]:  # Limit to top 10
                        user_info = await self._get_github_user_info(contributor['login'])
                        if user_info:
                            detailed_contributors.append({
                                **contributor,
                                'profile': user_info
                            })
                    
                    return detailed_contributors
        except Exception as e:
            logger.warning(f"Failed to get contributors: {e}")
        return []
    
    async def _get_github_user_info(self, username: str) -> Dict:
        """Get detailed user information"""
        try:
            url = f"{self.github_api_base}/users/{username}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.warning(f"Failed to get user info for {username}: {e}")
        return {}
    
    async def _get_github_org_info(self, owner: str) -> Dict:
        """Get organization information if owner is an org"""
        try:
            url = f"{self.github_api_base}/orgs/{owner}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    org_info = await response.json()
                    
                    # Get organization members
                    members_url = f"{self.github_api_base}/orgs/{owner}/members"
                    async with self.session.get(members_url) as members_response:
                        if members_response.status == 200:
                            org_info['members'] = await members_response.json()
                    
                    return org_info
        except Exception as e:
            logger.warning(f"Failed to get org info: {e}")
        return {}
    
    async def _get_github_activity(self, owner: str, repo: str) -> Dict:
        """Get recent repository activity"""
        try:
            # Get recent commits
            commits_url = f"{self.github_api_base}/repos/{owner}/{repo}/commits"
            async with self.session.get(commits_url + "?per_page=10") as response:
                commits = await response.json() if response.status == 200 else []
            
            # Get recent releases
            releases_url = f"{self.github_api_base}/repos/{owner}/{repo}/releases"
            async with self.session.get(releases_url + "?per_page=5") as response:
                releases = await response.json() if response.status == 200 else []
            
            return {
                'recent_commits': commits,
                'recent_releases': releases,
                'activity_score': self._calculate_activity_score(commits, releases)
            }
        except Exception as e:
            logger.warning(f"Failed to get activity data: {e}")
        return {}
    
    async def _get_github_readme(self, owner: str, repo: str) -> str:
        """Get repository README content"""
        try:
            url = f"{self.github_api_base}/repos/{owner}/{repo}/readme"
            async with self.session.get(url) as response:
                if response.status == 200:
                    readme_data = await response.json()
                    # Decode base64 content
                    import base64
                    content = base64.b64decode(readme_data['content']).decode('utf-8')
                    return content
        except Exception as e:
            logger.warning(f"Failed to get README: {e}")
        return ""
    
    def _analyze_github_team_data(self, github_data: Dict) -> Dict:
        """
        Analyze GitHub data to extract team insights
        """
        analysis = {
            'estimated_team_size': 0,
            'team_members': [],
            'organization_type': 'individual',
            'development_activity': 'unknown',
            'team_confidence': 'low'
        }
        
        # Analyze contributors
        contributors = github_data.get('contributors', [])
        if contributors:
            analysis['estimated_team_size'] = len([c for c in contributors if c.get('contributions', 0) > 5])
            analysis['team_members'] = [
                {
                    'username': c['login'],
                    'contributions': c.get('contributions', 0),
                    'profile': c.get('profile', {})
                }
                for c in contributors[:10]
            ]
        
        # Check if it's an organization
        org_info = github_data.get('organization_info', {})
        if org_info:
            analysis['organization_type'] = 'organization'
            analysis['estimated_team_size'] = max(
                analysis['estimated_team_size'],
                len(org_info.get('members', []))
            )
        
        # Assess development activity
        activity = github_data.get('recent_activity', {})
        activity_score = activity.get('activity_score', 0)
        if activity_score > 0.7:
            analysis['development_activity'] = 'high'
        elif activity_score > 0.3:
            analysis['development_activity'] = 'medium'
        else:
            analysis['development_activity'] = 'low'
        
        # Determine confidence level
        if org_info and contributors:
            analysis['team_confidence'] = 'high'
        elif contributors and len(contributors) > 3:
            analysis['team_confidence'] = 'medium'
        else:
            analysis['team_confidence'] = 'low'
        
        return analysis
    
    async def _collect_social_media_data(self, subnet_info: Dict) -> Optional[Dict]:
        """
        Collect information from social media and communication platforms
        """
        try:
            social_data = {}
            sources = subnet_info.get('sources', {})
            
            # Twitter/X analysis (if available)
            twitter_url = self._extract_twitter_url(sources)
            if twitter_url:
                social_data['twitter'] = await self._analyze_twitter_profile(twitter_url)
            
            # Discord analysis (if available)
            discord_info = sources.get('discord')
            if discord_info:
                social_data['discord'] = await self._analyze_discord_info(discord_info)
            
            # LinkedIn analysis (if available)
            linkedin_url = self._extract_linkedin_url(sources)
            if linkedin_url:
                social_data['linkedin'] = await self._analyze_linkedin_profile(linkedin_url)
            
            return social_data if social_data else None
            
        except Exception as e:
            logger.error(f"Social media data collection failed: {e}")
            return None
    
    async def _collect_registry_data(self, subnet_info: Dict) -> Optional[Dict]:
        """
        Collect data from blockchain registries and subnet databases
        """
        try:
            # This would integrate with Bittensor registry, TaoStats, etc.
            registry_data = {
                'taostats_data': await self._get_taostats_data(subnet_info),
                'bittensor_registry': await self._get_bittensor_registry_data(subnet_info),
                'subnet_metrics': await self._get_subnet_metrics(subnet_info)
            }
            
            return registry_data
            
        except Exception as e:
            logger.error(f"Registry data collection failed: {e}")
            return None
    
    async def _collect_search_results(self, subnet_info: Dict) -> Optional[Dict]:
        """
        Collect information from search engine results and news
        """
        try:
            subnet_name = subnet_info.get('name', '')
            search_queries = [
                f'"{subnet_name}" bittensor team',
                f'"{subnet_name}" founders blockchain',
                f'"{subnet_name}" AI subnet developers'
            ]
            
            search_data = {}
            for query in search_queries:
                results = await self._search_web(query)
                if results:
                    search_data[query] = results
            
            return search_data if search_data else None
            
        except Exception as e:
            logger.error(f"Search data collection failed: {e}")
            return None
    
    def _intelligent_merge(self, sources_data: List[DataSource], subnet_info: Dict) -> Dict:
        """
        Intelligently merge data from multiple sources based on confidence and priority
        """
        merged = {
            'subnet_info': subnet_info,
            'data_sources': [s.name for s in sources_data],
            'collection_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'team_information': {},
            'company_information': {},
            'confidence_scores': {},
            'source_analysis': {}
        }
        
        # Sort sources by priority and confidence
        sources_data.sort(key=lambda x: (x.priority, -x.confidence))
        
        # Merge team information with confidence weighting
        team_info = self._merge_team_information(sources_data)
        merged['team_information'] = team_info
        
        # Merge company information
        company_info = self._merge_company_information(sources_data)
        merged['company_information'] = company_info
        
        # Calculate overall confidence scores
        confidence_scores = self._calculate_confidence_scores(sources_data, team_info, company_info)
        merged['confidence_scores'] = confidence_scores
        
        return merged
    
    def _merge_team_information(self, sources_data: List[DataSource]) -> Dict:
        """Merge team information from multiple sources"""
        team_info = {
            'estimated_size': 0,
            'team_members': [],
            'leadership': [],
            'size_indicators': [],
            'confidence_level': 'unknown'
        }
        
        size_estimates = []
        all_members = []
        
        for source in sources_data:
            if source.name == 'github':
                github_team = source.data.get('team_analysis', {})
                size_estimates.append((github_team.get('estimated_team_size', 0), source.confidence))
                all_members.extend(github_team.get('team_members', []))
            
            elif source.name == 'website':
                website_team = source.data.get('enhanced_team_info', {})
                if website_team.get('team_members_found', 0) > 0:
                    size_estimates.append((website_team['team_members_found'], source.confidence))
        
        # Calculate weighted average team size
        if size_estimates:
            weighted_sum = sum(size * conf for size, conf in size_estimates)
            total_confidence = sum(conf for _, conf in size_estimates)
            team_info['estimated_size'] = int(weighted_sum / total_confidence) if total_confidence > 0 else 0
        
        team_info['team_members'] = all_members
        
        return team_info
    
    def _merge_company_information(self, sources_data: List[DataSource]) -> Dict:
        """Merge company information from multiple sources"""
        company_info = {
            'mission': '',
            'products': [],
            'technology_focus': '',
            'development_status': 'unknown'
        }
        
        for source in sources_data:
            if source.name == 'website':
                website_company = source.data.get('enhanced_company_info', {})
                if website_company.get('mission') and not company_info['mission']:
                    company_info['mission'] = website_company['mission']
                if website_company.get('technology_focus'):
                    company_info['technology_focus'] = website_company['technology_focus']
            
            elif source.name == 'github':
                github_repo = source.data.get('repository_info', {})
                if github_repo.get('description') and not company_info['mission']:
                    company_info['mission'] = github_repo['description']
        
        return company_info
    
    def _calculate_confidence_scores(self, sources_data: List[DataSource], 
                                   team_info: Dict, company_info: Dict) -> Dict:
        """Calculate overall confidence scores for the analysis"""
        scores = {
            'overall_confidence': 'low',
            'team_confidence': 'low',
            'company_confidence': 'low',
            'data_quality': 'poor'
        }
        
        # Calculate based on number of sources and their confidence
        source_count = len(sources_data)
        avg_confidence = sum(s.confidence for s in sources_data) / source_count if source_count > 0 else 0
        
        if source_count >= 3 and avg_confidence > 0.7:
            scores['overall_confidence'] = 'high'
        elif source_count >= 2 and avg_confidence > 0.5:
            scores['overall_confidence'] = 'medium'
        
        # Team confidence based on information availability
        if team_info.get('estimated_size', 0) > 0:
            scores['team_confidence'] = 'medium' if team_info['estimated_size'] > 5 else 'low'
            if len(team_info.get('team_members', [])) > 3:
                scores['team_confidence'] = 'high'
        
        return scores
    
    # Helper methods for specific platform analysis would go here...
    def _extract_twitter_url(self, sources: Dict) -> Optional[str]:
        """Extract Twitter URL from sources"""
        # Implementation for Twitter URL extraction
        return sources.get('twitter') or sources.get('x')
    
    def _extract_linkedin_url(self, sources: Dict) -> Optional[str]:
        """Extract LinkedIn URL from sources"""
        return sources.get('linkedin')
    
    def _calculate_activity_score(self, commits: List, releases: List) -> float:
        """Calculate development activity score"""
        # Simple scoring based on recent activity
        commit_score = min(len(commits) / 10, 1.0)  # Normalize to 0-1
        release_score = min(len(releases) / 5, 1.0)  # Normalize to 0-1
        return (commit_score + release_score) / 2
    
    async def close(self):
        """Close the session"""
        await self.session.close()

# Additional helper functions would be implemented here for specific platforms 