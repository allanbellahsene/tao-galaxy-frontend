import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from subnets_basic_info import TaoStatsAPI
from subnet_website_scraper import SubnetWebsiteScraper
from source_verifier import SourceVerifier
from research_agent import ResearchAgent
from scoring_agent import ScoringAgent

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutomatedSubnetPipeline:
    """
    Main orchestrator for the automated Bittensor subnet analysis pipeline
    """
    
    def __init__(self, output_dir: str = "pipeline_output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.taostats_api = TaoStatsAPI()
        self.website_scraper = SubnetWebsiteScraper()
        self.source_verifier = SourceVerifier()
        self.research_agent = ResearchAgent()
        self.scoring_agent = ScoringAgent()
        
        # Pipeline state
        self.pipeline_state = {
            'phase': 'initialized',
            'started_at': None,
            'completed_phases': [],
            'current_subnet': None,
            'total_subnets': 0,
            'processed_subnets': 0,
            'errors': []
        }
    
    async def run_full_pipeline(self, target_netuids: Optional[List[int]] = None) -> Dict:
        """
        Run the complete automated pipeline for all or specified subnets
        """
        logger.info("Starting automated subnet analysis pipeline")
        self.pipeline_state['started_at'] = datetime.now().isoformat()
        
        try:
            # Phase 1: Ingest Taostats Data
            logger.info("Phase 1: Ingesting Taostats data")
            self.pipeline_state['phase'] = 'ingesting_taostats'
            subnets_data = await self._phase_1_ingest_taostats(target_netuids)
            
            # Phase 2: Verify & Complete Sources
            logger.info("Phase 2: Verifying and completing sources")
            self.pipeline_state['phase'] = 'verifying_sources'
            verified_subnets = await self._phase_2_verify_sources(subnets_data)
            
            # Phase 3: Normalize & Store
            logger.info("Phase 3: Normalizing and storing data")
            self.pipeline_state['phase'] = 'normalizing_data'
            normalized_subnets = await self._phase_3_normalize_store(verified_subnets)
            
            # Phase 4: Deep Research & Scoring
            logger.info("Phase 4: Deep research and scoring")
            self.pipeline_state['phase'] = 'research_scoring'
            researched_subnets = await self._phase_4_research_score(normalized_subnets)
            
            # Phase 5: Generate Final Dataset
            logger.info("Phase 5: Generating final dataset")
            self.pipeline_state['phase'] = 'finalizing'
            final_dataset = await self._phase_5_finalize(researched_subnets)
            
            self.pipeline_state['phase'] = 'completed'
            logger.info("Pipeline completed successfully!")
            
            return {
                'status': 'success',
                'pipeline_state': self.pipeline_state,
                'final_dataset_path': str(self.output_dir / 'final_subnet_analysis.json'),
                'summary': self._generate_pipeline_summary(final_dataset)
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self.pipeline_state['phase'] = 'failed'
            self.pipeline_state['errors'].append(str(e))
            return {
                'status': 'failed',
                'error': str(e),
                'pipeline_state': self.pipeline_state
            }
    
    async def _phase_1_ingest_taostats(self, target_netuids: Optional[List[int]]) -> List[Dict]:
        """Phase 1: Fetch all subnet data from Taostats API"""
        logger.info("Fetching subnet data from Taostats API")
        
        all_subnets = self.taostats_api.get_all_subnets()
        
        if target_netuids:
            # Filter to specific subnets if requested
            all_subnets = [s for s in all_subnets if s.get('netuid') in target_netuids]
            logger.info(f"Filtered to {len(all_subnets)} target subnets")
        
        self.pipeline_state['total_subnets'] = len(all_subnets)
        
        # Format and save raw Taostats data
        formatted_subnets = []
        for subnet in all_subnets:
            formatted_data = self.taostats_api.format_subnet_data(subnet)
            formatted_subnets.append(formatted_data)
        
        # Save Phase 1 output
        output_path = self.output_dir / 'phase_1_taostats_data.json'
        with open(output_path, 'w') as f:
            json.dump(formatted_subnets, f, indent=2)
        
        self.pipeline_state['completed_phases'].append('taostats_ingestion')
        logger.info(f"Phase 1 complete: {len(formatted_subnets)} subnets processed")
        
        return formatted_subnets
    
    async def _phase_2_verify_sources(self, subnets_data: List[Dict]) -> List[Dict]:
        """Phase 2: Scrape websites and verify source URLs"""
        logger.info("Starting source verification phase")
        
        verified_subnets = []
        
        for i, subnet in enumerate(subnets_data):
            self.pipeline_state['current_subnet'] = subnet.get('netuid')
            self.pipeline_state['processed_subnets'] = i
            
            logger.info(f"Processing subnet {subnet['netuid']}: {subnet['name']} ({i+1}/{len(subnets_data)})")
            
            try:
                # Extract website URL from Taostats sources
                website_url = subnet['sources'].get('website')
                
                if not website_url:
                    logger.warning(f"No website URL for subnet {subnet['netuid']}")
                    verified_subnet = subnet.copy()
                    verified_subnet['website_data'] = {'status': 'no_website'}
                    verified_subnet['verified_sources'] = self.source_verifier.create_initial_sources(subnet['sources'])
                    verified_subnets.append(verified_subnet)
                    continue
                
                # Scrape the website
                website_data = self.website_scraper.scrape_subnet_website(
                    website_url, 
                    subnet['name']
                )
                
                # Verify and merge sources
                verified_sources = self.source_verifier.verify_and_merge_sources(
                    taostats_sources=subnet['sources'],
                    website_data=website_data
                )
                
                # Create enhanced subnet data
                verified_subnet = subnet.copy()
                verified_subnet['website_data'] = website_data
                verified_subnet['verified_sources'] = verified_sources
                verified_subnet['source_verification_summary'] = self.source_verifier.generate_verification_summary(verified_sources)
                
                verified_subnets.append(verified_subnet)
                
                # Rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing subnet {subnet['netuid']}: {e}")
                self.pipeline_state['errors'].append(f"Subnet {subnet['netuid']}: {str(e)}")
                
                # Add subnet with error status
                error_subnet = subnet.copy()
                error_subnet['website_data'] = {'status': 'error', 'error': str(e)}
                error_subnet['verified_sources'] = self.source_verifier.create_initial_sources(subnet['sources'])
                verified_subnets.append(error_subnet)
        
        # Save Phase 2 output
        output_path = self.output_dir / 'phase_2_verified_sources.json'
        with open(output_path, 'w') as f:
            json.dump(verified_subnets, f, indent=2)
        
        self.pipeline_state['completed_phases'].append('source_verification')
        logger.info(f"Phase 2 complete: {len(verified_subnets)} subnets processed")
        
        return verified_subnets
    
    async def _phase_3_normalize_store(self, verified_subnets: List[Dict]) -> List[Dict]:
        """Phase 3: Normalize data structure and create unified sources object"""
        logger.info("Starting data normalization phase")
        
        normalized_subnets = []
        
        for subnet in verified_subnets:
            try:
                # Create normalized structure
                normalized_subnet = {
                    'netuid': subnet['netuid'],
                    'name': subnet['name'],
                    'description': subnet['description'],
                    
                    # Unified sources with verification status
                    'sources': subnet['verified_sources'],
                    
                    # Raw data preservation
                    'taostats_raw': subnet['raw_data'],
                    'website_raw': subnet.get('website_data', {}),
                    
                    # Verification metadata
                    'source_verification': subnet.get('source_verification_summary', {}),
                    
                    # Prepared for research phase
                    'research_ready': True if subnet.get('website_data', {}).get('status') == 'success' else False,
                    
                    # Processing metadata
                    'processed_at': datetime.now().isoformat(),
                    'pipeline_version': '1.0'
                }
                
                normalized_subnets.append(normalized_subnet)
                
            except Exception as e:
                logger.error(f"Error normalizing subnet {subnet['netuid']}: {e}")
                self.pipeline_state['errors'].append(f"Normalization error for subnet {subnet['netuid']}: {str(e)}")
        
        # Save Phase 3 output
        output_path = self.output_dir / 'phase_3_normalized_data.json'
        with open(output_path, 'w') as f:
            json.dump(normalized_subnets, f, indent=2)
        
        self.pipeline_state['completed_phases'].append('data_normalization')
        logger.info(f"Phase 3 complete: {len(normalized_subnets)} subnets normalized")
        
        return normalized_subnets
    
    async def _phase_4_research_score(self, normalized_subnets: List[Dict]) -> List[Dict]:
        """Phase 4: Run AI research and scoring agents"""
        logger.info("Starting research and scoring phase")
        
        researched_subnets = []
        
        for i, subnet in enumerate(normalized_subnets):
            logger.info(f"Researching subnet {subnet['netuid']}: {subnet['name']} ({i+1}/{len(normalized_subnets)})")
            
            try:
                # Skip research if not ready (no successful website scraping)
                if not subnet.get('research_ready', False):
                    logger.warning(f"Skipping research for subnet {subnet['netuid']} - not research ready")
                    researched_subnet = subnet.copy()
                    researched_subnet['research_results'] = {'status': 'skipped', 'reason': 'not_research_ready'}
                    researched_subnet['scores'] = {'status': 'skipped', 'reason': 'no_research_data'}
                    researched_subnets.append(researched_subnet)
                    continue
                
                # Run research agent
                research_results = await self.research_agent.conduct_research(subnet)
                
                # Run scoring agent
                scores = await self.scoring_agent.generate_scores(subnet, research_results)
                
                # Create final subnet data
                researched_subnet = subnet.copy()
                researched_subnet['research_results'] = research_results
                researched_subnet['scores'] = scores
                researched_subnet['analysis_completed_at'] = datetime.now().isoformat()
                
                researched_subnets.append(researched_subnet)
                
                # Rate limiting for API calls
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error researching subnet {subnet['netuid']}: {e}")
                self.pipeline_state['errors'].append(f"Research error for subnet {subnet['netuid']}: {str(e)}")
                
                # Add subnet with error status
                error_subnet = subnet.copy()
                error_subnet['research_results'] = {'status': 'error', 'error': str(e)}
                error_subnet['scores'] = {'status': 'error', 'error': str(e)}
                researched_subnets.append(error_subnet)
        
        # Save Phase 4 output
        output_path = self.output_dir / 'phase_4_research_scores.json'
        with open(output_path, 'w') as f:
            json.dump(researched_subnets, f, indent=2)
        
        self.pipeline_state['completed_phases'].append('research_scoring')
        logger.info(f"Phase 4 complete: {len(researched_subnets)} subnets analyzed")
        
        return researched_subnets
    
    async def _phase_5_finalize(self, researched_subnets: List[Dict]) -> List[Dict]:
        """Phase 5: Generate final dataset for dashboard"""
        logger.info("Finalizing dataset for dashboard")
        
        final_dataset = []
        
        for subnet in researched_subnets:
            # Create dashboard-ready format
            dashboard_subnet = {
                'netuid': subnet['netuid'],
                'name': subnet['name'],
                'description': subnet['description'],
                
                # Key metrics for dashboard
                'verified_sources_count': len([s for s in subnet['sources'].values() if s.get('status') == 'both']),
                'website_available': subnet.get('research_ready', False),
                'has_github': bool(subnet['sources'].get('github', {}).get('url')),
                'has_documentation': bool(subnet['sources'].get('documentation', {}).get('url')),
                
                # Research summary
                'research_status': subnet.get('research_results', {}).get('status', 'unknown'),
                'scoring_status': subnet.get('scores', {}).get('status', 'unknown'),
                
                # Scores for display
                'scores': subnet.get('scores', {}),
                
                # Source verification summary
                'source_health': self._calculate_source_health(subnet['sources']),
                
                # Links for dashboard
                'primary_links': self._extract_primary_links(subnet['sources']),
                
                # Last updated
                'last_updated': subnet.get('analysis_completed_at', subnet.get('processed_at'))
            }
            
            final_dataset.append(dashboard_subnet)
        
        # Save final dataset
        output_path = self.output_dir / 'final_subnet_analysis.json'
        with open(output_path, 'w') as f:
            json.dump(final_dataset, f, indent=2)
        
        # Also save complete data for reference
        complete_output_path = self.output_dir / 'complete_subnet_data.json'
        with open(complete_output_path, 'w') as f:
            json.dump(researched_subnets, f, indent=2)
        
        self.pipeline_state['completed_phases'].append('finalization')
        logger.info(f"Phase 5 complete: Final dataset ready with {len(final_dataset)} subnets")
        
        return final_dataset
    
    def _calculate_source_health(self, sources: Dict) -> Dict:
        """Calculate source health metrics"""
        total_sources = len(sources)
        verified_sources = len([s for s in sources.values() if s.get('status') == 'both'])
        missing_sources = len([s for s in sources.values() if s.get('status') == 'taostats_only'])
        new_sources = len([s for s in sources.values() if s.get('status') == 'website_only'])
        
        health_score = (verified_sources / total_sources * 100) if total_sources > 0 else 0
        
        return {
            'total_sources': total_sources,
            'verified_sources': verified_sources,
            'missing_sources': missing_sources,
            'new_sources': new_sources,
            'health_score': round(health_score, 1)
        }
    
    def _extract_primary_links(self, sources: Dict) -> Dict:
        """Extract primary links for dashboard display"""
        primary_links = {}
        
        priority_sources = ['website', 'github', 'discord', 'twitter', 'documentation']
        
        for source_type in priority_sources:
            if source_type in sources and sources[source_type].get('url'):
                primary_links[source_type] = sources[source_type]['url']
        
        return primary_links
    
    def _generate_pipeline_summary(self, final_dataset: List[Dict]) -> Dict:
        """Generate summary statistics for the pipeline run"""
        total_subnets = len(final_dataset)
        research_ready = len([s for s in final_dataset if s['website_available']])
        with_github = len([s for s in final_dataset if s['has_github']])
        
        avg_source_health = sum(s['source_health']['health_score'] for s in final_dataset) / total_subnets if total_subnets > 0 else 0
        
        return {
            'total_subnets_processed': total_subnets,
            'research_ready_subnets': research_ready,
            'subnets_with_github': with_github,
            'average_source_health': round(avg_source_health, 1),
            'pipeline_errors': len(self.pipeline_state['errors']),
            'execution_time': self._calculate_execution_time()
        }
    
    def _calculate_execution_time(self) -> str:
        """Calculate total pipeline execution time"""
        if self.pipeline_state['started_at']:
            start_time = datetime.fromisoformat(self.pipeline_state['started_at'])
            duration = datetime.now() - start_time
            return str(duration)
        return "unknown"

# CLI interface for running the pipeline
async def main():
    """Main entry point for running the automated pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Bittensor Subnet Analysis Pipeline")
    parser.add_argument("--subnets", nargs="+", type=int, help="Specific subnet IDs to process")
    parser.add_argument("--output-dir", default="pipeline_output", help="Output directory for results")
    
    args = parser.parse_args()
    
    pipeline = AutomatedSubnetPipeline(output_dir=args.output_dir)
    
    result = await pipeline.run_full_pipeline(target_netuids=args.subnets)
    
    print("\n" + "="*50)
    print("PIPELINE EXECUTION SUMMARY")
    print("="*50)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 