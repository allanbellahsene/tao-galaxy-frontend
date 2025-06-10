import asyncio
import json
import logging
import os
import time
from typing import Dict, List, Optional
from enhanced_website_scraper import EnhancedWebsiteScraper
from multi_source_data_collector import MultiSourceDataCollector
from adaptive_research_agent import AdaptiveResearchAgent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FlexibleSubnetAnalysisPipeline:
    """
    Enhanced pipeline that combines multiple data collection and analysis approaches
    """
    
    def __init__(self, openai_api_key: str):
        self.enhanced_scraper = EnhancedWebsiteScraper()
        self.multi_source_collector = MultiSourceDataCollector()
        self.adaptive_agent = AdaptiveResearchAgent(openai_api_key)
        self.results_cache = {}
    
    async def analyze_subnet_comprehensive(self, subnet_info: Dict, 
                                         research_goals: Optional[List[str]] = None) -> Dict:
        """
        Comprehensive subnet analysis using all available enhanced methods
        """
        try:
            subnet_name = subnet_info.get('name', 'Unknown')
            logger.info(f"Starting comprehensive analysis for {subnet_name}")
            
            # Step 1: Enhanced multi-source data collection
            logger.info("Phase 1: Multi-source data collection...")
            comprehensive_data = await self.multi_source_collector.collect_comprehensive_data(subnet_info)
            
            # Step 2: Enhanced website scraping (if needed)
            website_url = subnet_info.get('sources', {}).get('website')
            if website_url and self._should_enhance_website_data(comprehensive_data):
                logger.info("Phase 2: Enhanced website analysis...")
                enhanced_website_data = self.enhanced_scraper.scrape_subnet_website(website_url, subnet_name)
                comprehensive_data = self._merge_website_data(comprehensive_data, enhanced_website_data)
            
            # Step 3: Adaptive research analysis
            logger.info("Phase 3: Adaptive research analysis...")
            if not research_goals:
                research_goals = self._generate_default_research_goals(subnet_info)
            
            research_analysis = await self.adaptive_agent.conduct_adaptive_research(
                comprehensive_data, research_goals
            )
            
            # Step 4: Create final comprehensive report
            logger.info("Phase 4: Generating final report...")
            final_report = self._create_comprehensive_report(
                subnet_info, comprehensive_data, research_analysis
            )
            
            # Cache results for potential reuse
            self.results_cache[subnet_name] = final_report
            
            logger.info(f"Analysis complete for {subnet_name}")
            return final_report
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed for {subnet_info.get('name', 'Unknown')}: {e}")
            return self._create_error_report(subnet_info, str(e))
    
    async def batch_analyze_subnets(self, subnet_list: List[Dict], 
                                  max_concurrent: int = 3) -> Dict:
        """
        Analyze multiple subnets concurrently with rate limiting
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def analyze_single(subnet_info):
            async with semaphore:
                try:
                    result = await self.analyze_subnet_comprehensive(subnet_info)
                    return subnet_info.get('name', 'Unknown'), result
                except Exception as e:
                    logger.error(f"Failed to analyze {subnet_info.get('name', 'Unknown')}: {e}")
                    return subnet_info.get('name', 'Unknown'), self._create_error_report(subnet_info, str(e))
        
        logger.info(f"Starting batch analysis of {len(subnet_list)} subnets...")
        
        # Execute all analyses concurrently
        tasks = [analyze_single(subnet) for subnet in subnet_list]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Compile results
        batch_results = {
            'analysis_summary': {
                'total_subnets': len(subnet_list),
                'successful_analyses': 0,
                'failed_analyses': 0,
                'batch_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'subnet_analyses': {},
            'batch_insights': {}
        }
        
        for result in results:
            if isinstance(result, Exception):
                batch_results['analysis_summary']['failed_analyses'] += 1
                continue
            
            subnet_name, analysis = result
            if analysis.get('status') != 'failed':
                batch_results['analysis_summary']['successful_analyses'] += 1
                batch_results['subnet_analyses'][subnet_name] = analysis
            else:
                batch_results['analysis_summary']['failed_analyses'] += 1
                batch_results['subnet_analyses'][subnet_name] = analysis
        
        # Generate batch insights
        batch_results['batch_insights'] = self._generate_batch_insights(batch_results['subnet_analyses'])
        
        logger.info(f"Batch analysis complete: {batch_results['analysis_summary']['successful_analyses']} successful, {batch_results['analysis_summary']['failed_analyses']} failed")
        
        return batch_results
    
    def _should_enhance_website_data(self, comprehensive_data: Dict) -> bool:
        """
        Determine if enhanced website scraping is needed
        """
        # Check if website data is missing or low quality
        confidence_scores = comprehensive_data.get('confidence_scores', {})
        
        # Always enhance if we have low confidence in team or company data
        if confidence_scores.get('team_confidence', 'low') == 'low':
            return True
        if confidence_scores.get('company_confidence', 'low') == 'low':
            return True
        
        # Check if website was a data source but provided limited information
        if 'website' in comprehensive_data.get('data_sources', []):
            team_info = comprehensive_data.get('team_information', {})
            if team_info.get('estimated_size', 0) == 0:
                return True
        
        return False
    
    def _merge_website_data(self, comprehensive_data: Dict, enhanced_website_data: Dict) -> Dict:
        """
        Intelligently merge enhanced website data with existing comprehensive data
        """
        if enhanced_website_data.get('status') != 'success':
            return comprehensive_data
        
        # Merge enhanced team information
        if enhanced_website_data.get('enhanced_team_info'):
            existing_team = comprehensive_data.get('team_information', {})
            enhanced_team = enhanced_website_data['enhanced_team_info']
            
            # Use enhanced data if it provides more information
            if enhanced_team.get('team_members_found', 0) > existing_team.get('estimated_size', 0):
                comprehensive_data['team_information']['estimated_size'] = enhanced_team['team_members_found']
                comprehensive_data['team_information']['enhanced_website_analysis'] = enhanced_team
        
        # Merge AI analysis if available
        if enhanced_website_data.get('ai_analysis'):
            comprehensive_data['enhanced_ai_analysis'] = enhanced_website_data['ai_analysis']
        
        # Update data sources
        if 'website_enhanced' not in comprehensive_data.get('data_sources', []):
            comprehensive_data['data_sources'].append('website_enhanced')
        
        return comprehensive_data
    
    def _generate_default_research_goals(self, subnet_info: Dict) -> List[str]:
        """
        Generate default research goals based on subnet information
        """
        goals = [
            "Identify the core team members and their professional backgrounds",
            "Understand the project's mission and value proposition",
            "Assess the development activity and project maturity",
            "Evaluate the business model and sustainability"
        ]
        
        # Add specific goals based on available information
        if subnet_info.get('sources', {}).get('github'):
            goals.append("Analyze the technical approach and code quality")
        
        if subnet_info.get('sources', {}).get('discord'):
            goals.append("Assess community engagement and support")
        
        return goals
    
    def _create_comprehensive_report(self, subnet_info: Dict, 
                                   comprehensive_data: Dict, 
                                   research_analysis: Dict) -> Dict:
        """
        Create a comprehensive final report combining all analysis results
        """
        report = {
            'subnet_identity': {
                'name': subnet_info.get('name', 'Unknown'),
                'netuid': subnet_info.get('netuid'),
                'description': subnet_info.get('description', ''),
                'sources': subnet_info.get('sources', {})
            },
            'data_collection_summary': {
                'sources_used': comprehensive_data.get('data_sources', []),
                'collection_timestamp': comprehensive_data.get('collection_timestamp'),
                'data_quality': comprehensive_data.get('confidence_scores', {})
            },
            'team_analysis': {
                'comprehensive_findings': comprehensive_data.get('team_information', {}),
                'research_insights': research_analysis.get('team_analysis', {}),
                'confidence_assessment': self._assess_team_confidence(comprehensive_data, research_analysis)
            },
            'company_analysis': {
                'comprehensive_findings': comprehensive_data.get('company_information', {}),
                'research_insights': research_analysis.get('company_analysis', {}),
                'confidence_assessment': self._assess_company_confidence(comprehensive_data, research_analysis)
            },
            'technical_analysis': self._extract_technical_insights(comprehensive_data),
            'executive_summary': research_analysis.get('executive_summary', {}),
            'recommendations': self._generate_recommendations(comprehensive_data, research_analysis),
            'analysis_metadata': {
                'pipeline_version': '2.0_enhanced',
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'analysis_confidence': self._calculate_overall_confidence(comprehensive_data, research_analysis)
            }
        }
        
        return report
    
    def _assess_team_confidence(self, comprehensive_data: Dict, research_analysis: Dict) -> Dict:
        """Assess confidence in team analysis"""
        confidence_factors = []
        overall_score = 0.0
        
        # Factor 1: Data source diversity
        sources = comprehensive_data.get('data_sources', [])
        if len(sources) >= 3:
            confidence_factors.append("Multiple data sources available")
            overall_score += 0.3
        elif len(sources) >= 2:
            confidence_factors.append("Limited data sources")
            overall_score += 0.2
        
        # Factor 2: Team size evidence
        team_size = comprehensive_data.get('team_information', {}).get('estimated_size', 0)
        if team_size > 0:
            confidence_factors.append(f"Team size estimated: {team_size}")
            overall_score += 0.4
        
        # Factor 3: Research analysis confidence
        research_confidence = research_analysis.get('analysis_metadata', {}).get('average_confidence', 0.0)
        if research_confidence > 0.7:
            confidence_factors.append("High research analysis confidence")
            overall_score += 0.3
        elif research_confidence > 0.4:
            confidence_factors.append("Medium research analysis confidence")
            overall_score += 0.2
        
        return {
            'overall_score': min(overall_score, 1.0),
            'confidence_level': 'high' if overall_score > 0.7 else 'medium' if overall_score > 0.4 else 'low',
            'contributing_factors': confidence_factors
        }
    
    def _assess_company_confidence(self, comprehensive_data: Dict, research_analysis: Dict) -> Dict:
        """Assess confidence in company analysis"""
        confidence_factors = []
        overall_score = 0.0
        
        # Similar to team assessment but focused on company information
        company_info = comprehensive_data.get('company_information', {})
        
        if company_info.get('mission'):
            confidence_factors.append("Mission statement identified")
            overall_score += 0.4
        
        if company_info.get('technology_focus'):
            confidence_factors.append("Technology focus identified")
            overall_score += 0.3
        
        # Add research analysis factors
        research_confidence = research_analysis.get('analysis_metadata', {}).get('average_confidence', 0.0)
        overall_score += research_confidence * 0.3
        
        return {
            'overall_score': min(overall_score, 1.0),
            'confidence_level': 'high' if overall_score > 0.7 else 'medium' if overall_score > 0.4 else 'low',
            'contributing_factors': confidence_factors
        }
    
    def _extract_technical_insights(self, comprehensive_data: Dict) -> Dict:
        """Extract technical insights from GitHub and other sources"""
        technical_insights = {
            'development_activity': 'unknown',
            'code_quality_indicators': [],
            'technology_stack': [],
            'project_maturity': 'unknown'
        }
        
        # Analyze GitHub data if available
        github_sources = [source for source in comprehensive_data.get('data_sources', []) if 'github' in source]
        if github_sources:
            # Extract GitHub-specific insights
            # This would be implemented based on the GitHub data structure
            technical_insights['development_activity'] = 'active'  # Placeholder
        
        return technical_insights
    
    def _generate_recommendations(self, comprehensive_data: Dict, research_analysis: Dict) -> Dict:
        """Generate actionable recommendations based on the analysis"""
        recommendations = {
            'data_improvement': [],
            'research_priorities': [],
            'risk_considerations': [],
            'investment_considerations': []
        }
        
        # Data improvement recommendations
        confidence_scores = comprehensive_data.get('confidence_scores', {})
        if confidence_scores.get('team_confidence', 'low') == 'low':
            recommendations['data_improvement'].append("Seek additional team information through LinkedIn or direct contact")
        
        if confidence_scores.get('company_confidence', 'low') == 'low':
            recommendations['data_improvement'].append("Research company mission and business model more thoroughly")
        
        # Research priorities based on gaps
        missing_categories = comprehensive_data.get('missing_data_categories', [])
        for category in missing_categories:
            recommendations['research_priorities'].append(f"Investigate {category} through additional sources")
        
        return recommendations
    
    def _calculate_overall_confidence(self, comprehensive_data: Dict, research_analysis: Dict) -> float:
        """Calculate overall analysis confidence score"""
        factors = []
        
        # Data source factor
        source_count = len(comprehensive_data.get('data_sources', []))
        source_factor = min(source_count / 3, 1.0)  # Normalize to max 3 sources
        factors.append(source_factor * 0.3)
        
        # Confidence scores factor
        confidence_scores = comprehensive_data.get('confidence_scores', {})
        avg_confidence = sum([
            0.8 if conf == 'high' else 0.5 if conf == 'medium' else 0.2
            for conf in confidence_scores.values()
            if isinstance(conf, str)
        ]) / max(len(confidence_scores), 1)
        factors.append(avg_confidence * 0.4)
        
        # Research analysis factor
        research_conf = research_analysis.get('analysis_metadata', {}).get('average_confidence', 0.0)
        factors.append(research_conf * 0.3)
        
        return sum(factors)
    
    def _generate_batch_insights(self, subnet_analyses: Dict) -> Dict:
        """Generate insights across multiple subnet analyses"""
        insights = {
            'common_patterns': [],
            'data_quality_trends': {},
            'team_size_distribution': {},
            'confidence_distribution': {}
        }
        
        if not subnet_analyses:
            return insights
        
        # Analyze patterns across subnets
        team_sizes = []
        confidences = []
        
        for subnet_name, analysis in subnet_analyses.items():
            if analysis.get('status') == 'failed':
                continue
            
            # Collect team sizes
            team_size = analysis.get('team_analysis', {}).get('comprehensive_findings', {}).get('estimated_size', 0)
            if team_size > 0:
                team_sizes.append(team_size)
            
            # Collect confidence scores
            confidence = analysis.get('analysis_metadata', {}).get('analysis_confidence', 0.0)
            confidences.append(confidence)
        
        # Generate distribution insights
        if team_sizes:
            insights['team_size_distribution'] = {
                'average': sum(team_sizes) / len(team_sizes),
                'min': min(team_sizes),
                'max': max(team_sizes),
                'sample_size': len(team_sizes)
            }
        
        if confidences:
            insights['confidence_distribution'] = {
                'average': sum(confidences) / len(confidences),
                'high_confidence_count': len([c for c in confidences if c > 0.7]),
                'low_confidence_count': len([c for c in confidences if c < 0.4])
            }
        
        return insights
    
    def _create_error_report(self, subnet_info: Dict, error: str) -> Dict:
        """Create standardized error report"""
        return {
            'subnet_identity': {
                'name': subnet_info.get('name', 'Unknown'),
                'netuid': subnet_info.get('netuid')
            },
            'status': 'failed',
            'error': error,
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_metadata': {
                'pipeline_version': '2.0_enhanced',
                'analysis_confidence': 0.0
            }
        }
    
    async def close(self):
        """Clean up resources"""
        await self.multi_source_collector.close()

# Usage example and testing functions
async def test_enhanced_pipeline():
    """Test the enhanced pipeline with sample data"""
    
    # Example subnet data (similar to Apex structure)
    sample_subnet = {
        'name': 'Apex',
        'netuid': 1,
        'description': 'Decentralized AI development platform',
        'sources': {
            'website': 'https://www.macrocosmos.ai',
            'github': 'https://github.com/macrocosm-os/prompting',
            'discord': 'https://discord.gg/macrocosmos'
        }
    }
    
    # Initialize pipeline
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    pipeline = FlexibleSubnetAnalysisPipeline(api_key)
    
    try:
        # Test single subnet analysis
        print("Testing enhanced subnet analysis...")
        result = await pipeline.analyze_subnet_comprehensive(sample_subnet)
        
        print(f"Analysis complete for {sample_subnet['name']}")
        print(f"Overall confidence: {result['analysis_metadata']['analysis_confidence']:.2f}")
        print(f"Data sources used: {result['data_collection_summary']['sources_used']}")
        
        # Save results
        with open('enhanced_analysis_result.json', 'w') as f:
            json.dump(result, f, indent=2)
        
        print("Results saved to enhanced_analysis_result.json")
        
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        await pipeline.close()

if __name__ == "__main__":
    asyncio.run(test_enhanced_pipeline()) 