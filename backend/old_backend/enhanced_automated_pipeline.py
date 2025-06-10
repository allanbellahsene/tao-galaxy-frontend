#!/usr/bin/env python3
"""
Enhanced Automated Subnet Analysis Pipeline
Integrates the enhanced research agent with confidence scoring and human review capabilities
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_research_agent import EnhancedResearchAgent
from human_review_dashboard import HumanReviewDashboard
from scoring_agent import ScoringAgent
from subnets_basic_info import TaoStatsAPI
from subnet_website_scraper import SubnetWebsiteScraper
from source_verifier import SourceVerifier

logger = logging.getLogger(__name__)

class EnhancedAutomatedSubnetPipeline:
    """
    Enhanced automated pipeline with improved AI research and human review integration
    """
    
    def __init__(self, output_dir: str = "enhanced_pipeline_output", 
                 config_path: str = "research_config.yaml"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.taostats_api = TaoStatsAPI()
        self.website_scraper = SubnetWebsiteScraper()
        self.source_verifier = SourceVerifier()
        
        # Initialize enhanced AI agents
        self.research_agent = EnhancedResearchAgent(config_path=config_path)
        self.scoring_agent = ScoringAgent()
        
        # Initialize human review dashboard
        self.review_dashboard = HumanReviewDashboard(
            review_output_dir=str(self.output_dir / "human_review")
        )
        
        # Pipeline state tracking
        self.pipeline_state = {
            'started_at': datetime.now().isoformat(),
            'completed_phases': [],
            'current_phase': None,
            'errors': [],
            'warnings': [],
            'subnets_processed': 0,
            'human_review_required': 0,
            'high_confidence_results': 0
        }
        
        logger.info(f"Enhanced Pipeline initialized - output: {self.output_dir}")
    
    async def run_enhanced_pipeline(self, target_netuids: Optional[List[int]] = None,
                                  enable_human_review: bool = True) -> Dict:
        """
        Run the complete enhanced pipeline with human review integration
        """
        logger.info("Starting enhanced subnet analysis pipeline")
        
        try:
            # Phase 1: Fetch basic subnet data
            logger.info("Phase 1: Fetching subnet data from TaoStats")
            self.pipeline_state['current_phase'] = 'fetch_data'
            
            if target_netuids:
                subnets_data = []
                for netuid in target_netuids:
                    subnet = self.taostats_api.get_subnet_info(netuid)
                    if subnet:
                        subnets_data.append(subnet)
                logger.info(f"Fetched {len(subnets_data)} specific subnets")
            else:
                subnets_data = self.taostats_api.get_all_subnets()
                logger.info(f"Fetched {len(subnets_data)} total subnets")
            
            self._save_phase_output("phase_1_subnet_data.json", subnets_data)
            self.pipeline_state['completed_phases'].append('fetch_data')
            
            # Phase 2: Source verification and website scraping
            logger.info("Phase 2: Verifying sources and scraping websites")
            self.pipeline_state['current_phase'] = 'source_verification'
            
            verified_subnets = await self._phase_2_enhanced_verification(subnets_data)
            
            self._save_phase_output("phase_2_verified_sources.json", verified_subnets)
            self.pipeline_state['completed_phases'].append('source_verification')
            
            # Phase 3: Data normalization
            logger.info("Phase 3: Normalizing data structure")
            self.pipeline_state['current_phase'] = 'data_normalization'
            
            normalized_subnets = self._phase_3_enhanced_normalization(verified_subnets)
            
            self._save_phase_output("phase_3_normalized_data.json", normalized_subnets)
            self.pipeline_state['completed_phases'].append('data_normalization')
            
            # Phase 4: Enhanced AI research
            logger.info("Phase 4: Conducting enhanced AI research")
            self.pipeline_state['current_phase'] = 'ai_research'
            
            researched_subnets = await self._phase_4_enhanced_research(normalized_subnets)
            
            self._save_phase_output("phase_4_research_results.json", researched_subnets)
            self.pipeline_state['completed_phases'].append('ai_research')
            
            # Phase 5: AI scoring
            logger.info("Phase 5: Generating AI scores")
            self.pipeline_state['current_phase'] = 'ai_scoring'
            
            scored_subnets = await self._phase_5_enhanced_scoring(researched_subnets)
            
            self._save_phase_output("phase_5_scoring_results.json", scored_subnets)
            self.pipeline_state['completed_phases'].append('ai_scoring')
            
            # Phase 6: Human review processing (if enabled)
            if enable_human_review:
                logger.info("Phase 6: Processing human review requirements")
                self.pipeline_state['current_phase'] = 'human_review_processing'
                
                review_summary = self._phase_6_human_review_processing(scored_subnets)
                
                self._save_phase_output("phase_6_review_summary.json", review_summary)
                self.pipeline_state['completed_phases'].append('human_review_processing')
            
            # Phase 7: Final analysis compilation
            logger.info("Phase 7: Compiling final analysis")
            self.pipeline_state['current_phase'] = 'final_compilation'
            
            final_analysis = self._phase_7_final_compilation(scored_subnets, enable_human_review)
            
            self._save_phase_output("final_enhanced_analysis.json", final_analysis)
            self.pipeline_state['completed_phases'].append('final_compilation')
            
            # Generate pipeline summary
            pipeline_summary = self._generate_enhanced_summary(final_analysis)
            
            self.pipeline_state['current_phase'] = 'completed'
            logger.info("Enhanced pipeline completed successfully")
            
            return {
                'status': 'success',
                'pipeline_state': self.pipeline_state,
                'summary': pipeline_summary,
                'final_analysis': final_analysis,
                'output_directory': str(self.output_dir)
            }
            
        except Exception as e:
            logger.error(f"Enhanced pipeline failed: {e}")
            self.pipeline_state['errors'].append(str(e))
            self.pipeline_state['current_phase'] = 'failed'
            
            return {
                'status': 'failed',
                'error': str(e),
                'pipeline_state': self.pipeline_state,
                'output_directory': str(self.output_dir)
            }
    
    async def _phase_2_enhanced_verification(self, subnets_data: List[Dict]) -> List[Dict]:
        """
        Enhanced source verification with better error handling and metadata
        """
        verified_subnets = []
        
        for i, subnet in enumerate(subnets_data):
            logger.info(f"Verifying sources for subnet {subnet['netuid']}: {subnet['name']} ({i+1}/{len(subnets_data)})")
            
            try:
                # Extract sources from basic data
                taostats_sources = {
                    'website': subnet.get('website'),
                    'github': subnet.get('github'),
                    'discord': subnet.get('discord'),
                    'twitter': subnet.get('twitter')
                }
                
                # Scrape website if available
                website_data = {'status': 'no_website'}
                if taostats_sources.get('website'):
                    website_data = self.website_scraper.scrape_subnet_website(
                        taostats_sources['website'], 
                        subnet['name']
                    )
                    # Brief pause to be respectful
                    await asyncio.sleep(1)
                
                # Verify and merge sources
                verified_sources = self.source_verifier.verify_and_merge_sources(
                    taostats_sources, 
                    website_data
                )
                
                # Enhanced subnet data structure
                enhanced_subnet = {
                    **subnet,
                    'sources': verified_sources,
                    'website_raw': website_data,
                    'verification_metadata': {
                        'verified_at': datetime.now().isoformat(),
                        'sources_found': len([s for s in verified_sources.values() if s.get('url')]),
                        'website_scraped': website_data.get('status') == 'success',
                        'research_ready': self._assess_research_readiness(verified_sources, website_data)
                    }
                }
                
                verified_subnets.append(enhanced_subnet)
                
            except Exception as e:
                logger.error(f"Error verifying subnet {subnet['netuid']}: {e}")
                self.pipeline_state['errors'].append(f"Verification failed for subnet {subnet['netuid']}: {str(e)}")
                
                # Add subnet with error status
                verified_subnets.append({
                    **subnet,
                    'sources': {},
                    'website_raw': {'status': 'error', 'error': str(e)},
                    'verification_metadata': {
                        'verified_at': datetime.now().isoformat(),
                        'error': str(e),
                        'research_ready': False
                    }
                })
        
        return verified_subnets
    
    def _assess_research_readiness(self, sources: Dict, website_data: Dict) -> bool:
        """
        Assess if a subnet has enough data for meaningful AI research
        """
        # Must have at least one verified source
        verified_sources = [s for s in sources.values() if isinstance(s, dict) and s.get('url')]
        if not verified_sources:
            return False
        
        # Prefer websites with successful scraping
        if website_data.get('status') == 'success':
            return True
        
        # Or multiple verified sources
        if len(verified_sources) >= 2:
            return True
        
        return False
    
    def _phase_3_enhanced_normalization(self, verified_subnets: List[Dict]) -> List[Dict]:
        """
        Enhanced data normalization with research readiness assessment
        """
        normalized_subnets = []
        
        for subnet in verified_subnets:
            # Create enhanced normalized structure
            normalized_subnet = {
                'netuid': subnet['netuid'],
                'name': subnet['name'],
                'description': subnet.get('description', ''),
                'sources': subnet.get('sources', {}),
                'website_raw': subnet.get('website_raw', {}),
                'verification_metadata': subnet.get('verification_metadata', {}),
                'research_ready': subnet.get('verification_metadata', {}).get('research_ready', False),
                'normalization_metadata': {
                    'normalized_at': datetime.now().isoformat(),
                    'source_count': len([s for s in subnet.get('sources', {}).values() 
                                       if isinstance(s, dict) and s.get('url')]),
                    'has_website_content': subnet.get('website_raw', {}).get('status') == 'success'
                }
            }
            
            normalized_subnets.append(normalized_subnet)
        
        return normalized_subnets
    
    async def _phase_4_enhanced_research(self, normalized_subnets: List[Dict]) -> List[Dict]:
        """
        Enhanced AI research phase with confidence tracking
        """
        researched_subnets = []
        research_ready_count = len([s for s in normalized_subnets if s.get('research_ready', False)])
        
        logger.info(f"Conducting research on {research_ready_count} research-ready subnets")
        
        for i, subnet in enumerate(normalized_subnets):
            logger.info(f"Processing subnet {subnet['netuid']}: {subnet['name']} ({i+1}/{len(normalized_subnets)})")
            
            researched_subnet = subnet.copy()
            
            try:
                if not subnet.get('research_ready', False):
                    logger.warning(f"Skipping research for subnet {subnet['netuid']} - not research ready")
                    researched_subnet['research_results'] = {
                        'status': 'skipped',
                        'reason': 'insufficient_data_for_research',
                        'research_timestamp': datetime.now().isoformat()
                    }
                else:
                    # Conduct enhanced research
                    research_results = await self.research_agent.conduct_comprehensive_research(subnet)
                    researched_subnet['research_results'] = research_results
                    
                    # Track pipeline statistics
                    self.pipeline_state['subnets_processed'] += 1
                    
                    if research_results.get('analysis_metadata', {}).get('human_review_required', False):
                        self.pipeline_state['human_review_required'] += 1
                    
                    if research_results.get('analysis_metadata', {}).get('overall_confidence') == 'HIGH':
                        self.pipeline_state['high_confidence_results'] += 1
                    
                    # Rate limiting
                    await asyncio.sleep(2)
                
                researched_subnets.append(researched_subnet)
                
            except Exception as e:
                logger.error(f"Research failed for subnet {subnet['netuid']}: {e}")
                self.pipeline_state['errors'].append(f"Research failed for subnet {subnet['netuid']}: {str(e)}")
                
                researched_subnet['research_results'] = {
                    'status': 'failed',
                    'error': str(e),
                    'research_timestamp': datetime.now().isoformat()
                }
                researched_subnets.append(researched_subnet)
        
        return researched_subnets
    
    async def _phase_5_enhanced_scoring(self, researched_subnets: List[Dict]) -> List[Dict]:
        """
        Enhanced scoring phase that considers research confidence
        """
        scored_subnets = []
        
        for subnet in researched_subnets:
            scored_subnet = subnet.copy()
            
            try:
                research_results = subnet.get('research_results', {})
                
                if research_results.get('status') in ['completed']:
                    # Generate scores using research results
                    scores = await self.scoring_agent.generate_scores(subnet, research_results)
                    scored_subnet['scores'] = scores
                else:
                    # Create placeholder scores for subnets without research
                    scored_subnet['scores'] = {
                        'status': 'skipped',
                        'reason': 'no_research_data_available',
                        'overall_score': 1.0,
                        'confidence_level': 'NO_DATA',
                        'scoring_timestamp': datetime.now().isoformat()
                    }
                
                # Add analysis completion timestamp
                scored_subnet['analysis_completed_at'] = datetime.now().isoformat()
                
                scored_subnets.append(scored_subnet)
                
                # Brief pause for rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Scoring failed for subnet {subnet['netuid']}: {e}")
                self.pipeline_state['errors'].append(f"Scoring failed for subnet {subnet['netuid']}: {str(e)}")
                
                scored_subnet['scores'] = {
                    'status': 'failed',
                    'error': str(e),
                    'overall_score': 1.0,
                    'scoring_timestamp': datetime.now().isoformat()
                }
                scored_subnets.append(scored_subnet)
        
        return scored_subnets
    
    def _phase_6_human_review_processing(self, scored_subnets: List[Dict]) -> Dict:
        """
        Process subnets that require human review
        """
        logger.info("Processing human review requirements")
        
        # Extract research results for review processing
        research_results = []
        for subnet in scored_subnets:
            research_data = subnet.get('research_results', {})
            if research_data.get('status') == 'completed':
                research_results.append(research_data)
        
        # Process with human review dashboard
        review_summary = self.review_dashboard.process_research_results(research_results)
        
        logger.info(f"Human review summary: {review_summary['total_items_for_review']} items need review")
        
        return review_summary
    
    def _phase_7_final_compilation(self, scored_subnets: List[Dict], 
                                 human_review_enabled: bool) -> Dict:
        """
        Compile final analysis with enhanced metadata
        """
        # Sort subnets by overall score (descending)
        valid_scored_subnets = [s for s in scored_subnets 
                              if s.get('scores', {}).get('overall_score', 0) > 1]
        
        sorted_subnets = sorted(valid_scored_subnets, 
                              key=lambda x: x.get('scores', {}).get('overall_score', 0), 
                              reverse=True)
        
        # Generate analytics
        analytics = self._generate_enhanced_analytics(scored_subnets)
        
        final_analysis = {
            'analysis_metadata': {
                'generated_at': datetime.now().isoformat(),
                'pipeline_version': 'enhanced_v1.0',
                'total_subnets_analyzed': len(scored_subnets),
                'human_review_enabled': human_review_enabled,
                'confidence_distribution': analytics['confidence_distribution'],
                'research_quality_stats': analytics['research_quality'],
                'pipeline_performance': analytics['pipeline_performance']
            },
            'top_performing_subnets': sorted_subnets[:20],  # Top 20
            'all_subnets': sorted_subnets,
            'analytics': analytics,
            'human_review_summary': self.pipeline_state.get('human_review_summary', {}),
            'pipeline_state': self.pipeline_state
        }
        
        return final_analysis
    
    def _generate_enhanced_analytics(self, scored_subnets: List[Dict]) -> Dict:
        """
        Generate comprehensive analytics about the analysis results
        """
        analytics = {
            'confidence_distribution': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'NO_DATA': 0},
            'research_quality': {
                'research_ready_subnets': 0,
                'successfully_researched': 0,
                'high_quality_sources': 0,
                'human_review_required': 0
            },
            'pipeline_performance': {
                'total_processing_time': 0,
                'average_time_per_subnet': 0,
                'error_rate': 0,
                'success_rate': 0
            },
            'scoring_distribution': {
                'excellent_scores': 0,  # > 4.0
                'good_scores': 0,       # 3.0-4.0
                'average_scores': 0,    # 2.0-3.0
                'poor_scores': 0        # < 2.0
            }
        }
        
        total_subnets = len(scored_subnets)
        successful_analyses = 0
        
        for subnet in scored_subnets:
            # Research confidence distribution
            research_results = subnet.get('research_results', {})
            if research_results.get('status') == 'completed':
                confidence = research_results.get('analysis_metadata', {}).get('overall_confidence', 'NO_DATA')
                analytics['confidence_distribution'][confidence] += 1
                
                successful_analyses += 1
                
                if research_results.get('analysis_metadata', {}).get('human_review_required', False):
                    analytics['research_quality']['human_review_required'] += 1
            
            # Research readiness
            if subnet.get('research_ready', False):
                analytics['research_quality']['research_ready_subnets'] += 1
            
            if research_results.get('status') == 'completed':
                analytics['research_quality']['successfully_researched'] += 1
            
            # Source quality
            sources = subnet.get('sources', {})
            verified_sources = [s for s in sources.values() if isinstance(s, dict) and s.get('url')]
            if len(verified_sources) >= 2:
                analytics['research_quality']['high_quality_sources'] += 1
            
            # Scoring distribution
            scores = subnet.get('scores', {})
            overall_score = scores.get('overall_score', 0)
            
            if overall_score >= 4.0:
                analytics['scoring_distribution']['excellent_scores'] += 1
            elif overall_score >= 3.0:
                analytics['scoring_distribution']['good_scores'] += 1
            elif overall_score >= 2.0:
                analytics['scoring_distribution']['average_scores'] += 1
            else:
                analytics['scoring_distribution']['poor_scores'] += 1
        
        # Calculate performance metrics
        analytics['pipeline_performance']['success_rate'] = (successful_analyses / total_subnets * 100) if total_subnets > 0 else 0
        analytics['pipeline_performance']['error_rate'] = len(self.pipeline_state['errors']) / total_subnets * 100 if total_subnets > 0 else 0
        
        return analytics
    
    def _generate_enhanced_summary(self, final_analysis: Dict) -> Dict:
        """
        Generate enhanced pipeline execution summary
        """
        analytics = final_analysis['analytics']
        
        summary = {
            'execution_summary': {
                'total_subnets_processed': final_analysis['analysis_metadata']['total_subnets_analyzed'],
                'research_ready_subnets': analytics['research_quality']['research_ready_subnets'],
                'successfully_researched': analytics['research_quality']['successfully_researched'],
                'human_review_required': analytics['research_quality']['human_review_required'],
                'high_confidence_results': analytics['confidence_distribution']['HIGH'],
                'pipeline_errors': len(self.pipeline_state['errors']),
                'success_rate': f"{analytics['pipeline_performance']['success_rate']:.1f}%"
            },
            'quality_metrics': {
                'high_quality_sources': analytics['research_quality']['high_quality_sources'],
                'confidence_distribution': analytics['confidence_distribution'],
                'scoring_distribution': analytics['scoring_distribution']
            },
            'top_subnets': [
                {
                    'netuid': subnet['netuid'],
                    'name': subnet['name'],
                    'overall_score': subnet.get('scores', {}).get('overall_score', 0),
                    'confidence': subnet.get('research_results', {}).get('analysis_metadata', {}).get('overall_confidence', 'UNKNOWN')
                }
                for subnet in final_analysis['top_performing_subnets'][:10]
            ],
            'recommendations': self._generate_pipeline_recommendations(analytics)
        }
        
        return summary
    
    def _generate_pipeline_recommendations(self, analytics: Dict) -> List[str]:
        """
        Generate recommendations based on pipeline results
        """
        recommendations = []
        
        # Human review recommendations
        review_required = analytics['research_quality']['human_review_required']
        total_researched = analytics['research_quality']['successfully_researched']
        
        if review_required > 0:
            review_percentage = (review_required / total_researched * 100) if total_researched > 0 else 0
            recommendations.append(f"{review_required} subnets ({review_percentage:.1f}%) require human review")
        
        # Confidence recommendations
        high_confidence = analytics['confidence_distribution']['HIGH']
        if high_confidence == 0:
            recommendations.append("No high-confidence research results - consider improving data sources")
        elif high_confidence < total_researched * 0.3:
            recommendations.append("Low proportion of high-confidence results - verify source quality")
        
        # Scoring recommendations
        excellent_scores = analytics['scoring_distribution']['excellent_scores']
        if excellent_scores == 0:
            recommendations.append("No excellent scoring subnets identified - review scoring criteria")
        
        return recommendations
    
    def _save_phase_output(self, filename: str, data: Any):
        """Save phase output to file"""
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Phase output saved: {filename}")

# CLI interface
async def main():
    """Main CLI interface for enhanced pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Subnet Analysis Pipeline")
    parser.add_argument('--subnets', nargs='*', type=int, 
                       help='Specific subnet IDs to analyze')
    parser.add_argument('--config', default='research_config.yaml',
                       help='Research configuration file')
    parser.add_argument('--output-dir', default='enhanced_pipeline_output',
                       help='Output directory')
    parser.add_argument('--disable-human-review', action='store_true',
                       help='Disable human review processing')
    
    args = parser.parse_args()
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run pipeline
    pipeline = EnhancedAutomatedSubnetPipeline(
        output_dir=args.output_dir,
        config_path=args.config
    )
    
    result = await pipeline.run_enhanced_pipeline(
        target_netuids=args.subnets,
        enable_human_review=not args.disable_human_review
    )
    
    # Print summary
    if result['status'] == 'success':
        summary = result['summary']
        print("\n" + "="*60)
        print("ENHANCED PIPELINE EXECUTION SUMMARY")
        print("="*60)
        print(f"✅ Status: {result['status']}")
        print(f"📊 Subnets processed: {summary['execution_summary']['total_subnets_processed']}")
        print(f"🔬 Research ready: {summary['execution_summary']['research_ready_subnets']}")
        print(f"🤖 AI researched: {summary['execution_summary']['successfully_researched']}")
        print(f"👥 Human review needed: {summary['execution_summary']['human_review_required']}")
        print(f"🎯 High confidence: {summary['execution_summary']['high_confidence_results']}")
        print(f"📈 Success rate: {summary['execution_summary']['success_rate']}")
        
        print(f"\n📁 Output directory: {result['output_directory']}")
        
        if summary['recommendations']:
            print("\n💡 Recommendations:")
            for rec in summary['recommendations']:
                print(f"   • {rec}")
    else:
        print(f"\n❌ Pipeline failed: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main()) 