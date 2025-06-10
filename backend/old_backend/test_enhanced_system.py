#!/usr/bin/env python3

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# Import our enhanced modules
from enhanced_website_scraper import EnhancedWebsiteScraper
from multi_source_data_collector import MultiSourceDataCollector
from adaptive_research_agent import AdaptiveResearchAgent
from flexible_pipeline import FlexibleSubnetAnalysisPipeline

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_enhanced_system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EnhancedSystemTester:
    """
    Comprehensive testing system for the enhanced scraping pipeline
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'detailed_results': {}
        }
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        logger.info("🚀 Starting Enhanced Scraping System Test Suite")
        
        # Test 1: Component Tests
        await self.test_enhanced_website_scraper()
        await self.test_multi_source_collector()
        await self.test_adaptive_research_agent()
        
        # Test 2: Integration Tests
        await self.test_flexible_pipeline()
        
        # Test 3: Real-world Tests
        await self.test_apex_subnet_analysis()
        await self.test_chutes_subnet_analysis()
        
        # Test 4: Edge Cases
        await self.test_edge_cases()
        
        # Generate test report
        self.generate_test_report()
    
    async def test_enhanced_website_scraper(self):
        """Test the AI-enhanced website scraper"""
        logger.info("🔍 Testing Enhanced Website Scraper...")
        
        try:
            scraper = EnhancedWebsiteScraper()
            
            # Test with Apex (known issue case)
            result = scraper.scrape_subnet_website(
                'https://www.macrocosmos.ai', 
                'Apex'
            )
            
            # Validate results
            success = (
                result.get('status') == 'success' and
                'ai_analysis' in result and
                'enhanced_team_info' in result
            )
            
            self._record_test_result('enhanced_website_scraper', success, result)
            
            if success:
                logger.info("✅ Enhanced Website Scraper: PASSED")
                logger.info(f"   - Team members found: {result.get('enhanced_team_info', {}).get('team_members_found', 0)}")
                logger.info(f"   - AI confidence: {result.get('enhanced_team_info', {}).get('ai_confidence', 'Unknown')}")
            else:
                logger.error("❌ Enhanced Website Scraper: FAILED")
                logger.error(f"   - Error: {result.get('error', 'Unknown')}")
        
        except Exception as e:
            logger.error(f"❌ Enhanced Website Scraper: EXCEPTION - {e}")
            self._record_test_result('enhanced_website_scraper', False, {'error': str(e)})
    
    async def test_multi_source_collector(self):
        """Test the multi-source data collector"""
        logger.info("📊 Testing Multi-Source Data Collector...")
        
        try:
            collector = MultiSourceDataCollector()
            
            # Test subnet info for Apex
            subnet_info = {
                'name': 'Apex',
                'netuid': 1,
                'sources': {
                    'website': 'https://www.macrocosmos.ai',
                    'github': 'https://github.com/macrocosm-os/prompting'
                }
            }
            
            result = await collector.collect_comprehensive_data(subnet_info)
            
            # Validate results
            success = (
                'data_sources' in result and
                'team_information' in result and
                'confidence_scores' in result
            )
            
            self._record_test_result('multi_source_collector', success, result)
            
            if success:
                logger.info("✅ Multi-Source Collector: PASSED")
                logger.info(f"   - Data sources: {result.get('data_sources', [])}")
                logger.info(f"   - Team size estimate: {result.get('team_information', {}).get('estimated_size', 0)}")
            else:
                logger.error("❌ Multi-Source Collector: FAILED")
            
            await collector.close()
        
        except Exception as e:
            logger.error(f"❌ Multi-Source Collector: EXCEPTION - {e}")
            self._record_test_result('multi_source_collector', False, {'error': str(e)})
    
    async def test_adaptive_research_agent(self):
        """Test the adaptive research agent"""
        logger.info("🧠 Testing Adaptive Research Agent...")
        
        try:
            agent = AdaptiveResearchAgent(self.api_key)
            
            # Mock subnet data for testing
            subnet_data = {
                'data_sources': ['website', 'github'],
                'team_information': {
                    'estimated_size': 5,
                    'team_members': [{'username': 'test_user', 'contributions': 10}]
                },
                'company_information': {
                    'mission': 'Test mission',
                    'technology_focus': 'AI/ML'
                },
                'confidence_scores': {
                    'team_confidence': 'medium',
                    'company_confidence': 'low'
                }
            }
            
            research_goals = ["Identify key team members", "Understand business model"]
            
            result = await agent.conduct_adaptive_research(subnet_data, research_goals)
            
            # Validate results
            success = (
                'analysis_metadata' in result and
                result.get('status') != 'failed'
            )
            
            self._record_test_result('adaptive_research_agent', success, result)
            
            if success:
                logger.info("✅ Adaptive Research Agent: PASSED")
                logger.info(f"   - Queries executed: {result.get('analysis_metadata', {}).get('research_queries_executed', 0)}")
                logger.info(f"   - Average confidence: {result.get('analysis_metadata', {}).get('average_confidence', 0):.2f}")
            else:
                logger.error("❌ Adaptive Research Agent: FAILED")
                logger.error(f"   - Error: {result.get('error', 'Unknown')}")
        
        except Exception as e:
            logger.error(f"❌ Adaptive Research Agent: EXCEPTION - {e}")
            self._record_test_result('adaptive_research_agent', False, {'error': str(e)})
    
    async def test_flexible_pipeline(self):
        """Test the integrated flexible pipeline"""
        logger.info("🔧 Testing Flexible Pipeline Integration...")
        
        try:
            pipeline = FlexibleSubnetAnalysisPipeline(self.api_key)
            
            # Test with simple subnet
            subnet_info = {
                'name': 'TestSubnet',
                'netuid': 999,
                'description': 'Test subnet for pipeline validation',
                'sources': {
                    'website': 'https://example.com'
                }
            }
            
            result = await pipeline.analyze_subnet_comprehensive(subnet_info)
            
            # Validate results
            success = (
                'subnet_identity' in result and
                'analysis_metadata' in result and
                result.get('status') != 'failed'
            )
            
            self._record_test_result('flexible_pipeline', success, result)
            
            if success:
                logger.info("✅ Flexible Pipeline: PASSED")
                logger.info(f"   - Pipeline version: {result.get('analysis_metadata', {}).get('pipeline_version')}")
                logger.info(f"   - Analysis confidence: {result.get('analysis_metadata', {}).get('analysis_confidence', 0):.2f}")
            else:
                logger.error("❌ Flexible Pipeline: FAILED")
                logger.error(f"   - Error: {result.get('error', 'Unknown')}")
            
            await pipeline.close()
        
        except Exception as e:
            logger.error(f"❌ Flexible Pipeline: EXCEPTION - {e}")
            self._record_test_result('flexible_pipeline', False, {'error': str(e)})
    
    async def test_apex_subnet_analysis(self):
        """Test with the real Apex subnet (the original issue case)"""
        logger.info("🎯 Testing Apex Subnet Analysis (Original Issue)...")
        
        try:
            pipeline = FlexibleSubnetAnalysisPipeline(self.api_key)
            
            # Real Apex subnet data
            apex_subnet = {
                'name': 'Apex',
                'netuid': 1,
                'description': 'Decentralized AI development platform',
                'sources': {
                    'website': 'https://www.macrocosmos.ai',
                    'github': 'https://github.com/macrocosm-os/prompting',
                    'discord': 'https://discord.gg/macrocosmos'
                }
            }
            
            result = await pipeline.analyze_subnet_comprehensive(apex_subnet)
            
            # Check if we solved the original issue
            team_analysis = result.get('team_analysis', {})
            team_findings = team_analysis.get('comprehensive_findings', {})
            team_size = team_findings.get('estimated_size', 0)
            
            # Success criteria: We should find team information
            success = (
                result.get('status') != 'failed' and
                team_size > 0  # We expect to find some team indicators
            )
            
            self._record_test_result('apex_real_analysis', success, result)
            
            if success:
                logger.info("✅ Apex Analysis: PASSED - Issue Resolved!")
                logger.info(f"   - Team size found: {team_size}")
                logger.info(f"   - Data sources used: {result.get('data_collection_summary', {}).get('sources_used', [])}")
                logger.info(f"   - Team confidence: {team_analysis.get('confidence_assessment', {}).get('confidence_level', 'unknown')}")
                
                # Save detailed Apex results
                with open('apex_enhanced_analysis.json', 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info("   - Detailed results saved to apex_enhanced_analysis.json")
            else:
                logger.error("❌ Apex Analysis: FAILED - Issue NOT resolved")
                logger.error(f"   - Team size found: {team_size}")
                logger.error(f"   - Error: {result.get('error', 'No specific error')}")
            
            await pipeline.close()
        
        except Exception as e:
            logger.error(f"❌ Apex Analysis: EXCEPTION - {e}")
            self._record_test_result('apex_real_analysis', False, {'error': str(e)})
    
    async def test_chutes_subnet_analysis(self):
        """Test with Chutes subnet for comparison"""
        logger.info("🎲 Testing Chutes Subnet Analysis...")
        
        try:
            pipeline = FlexibleSubnetAnalysisPipeline(self.api_key)
            
            # Chutes subnet data (from your original analysis)
            chutes_subnet = {
                'name': 'Chutes',
                'netuid': 64,
                'description': 'Gaming and AI subnet',
                'sources': {
                    'website': 'https://chutes.ai',
                    'github': 'https://github.com/chutes-ai'
                }
            }
            
            result = await pipeline.analyze_subnet_comprehensive(chutes_subnet)
            
            success = result.get('status') != 'failed'
            
            self._record_test_result('chutes_analysis', success, result)
            
            if success:
                logger.info("✅ Chutes Analysis: PASSED")
                team_size = result.get('team_analysis', {}).get('comprehensive_findings', {}).get('estimated_size', 0)
                logger.info(f"   - Team size found: {team_size}")
            else:
                logger.error("❌ Chutes Analysis: FAILED")
            
            await pipeline.close()
        
        except Exception as e:
            logger.error(f"❌ Chutes Analysis: EXCEPTION - {e}")
            self._record_test_result('chutes_analysis', False, {'error': str(e)})
    
    async def test_edge_cases(self):
        """Test edge cases and error handling"""
        logger.info("⚠️ Testing Edge Cases...")
        
        edge_cases = [
            {
                'name': 'invalid_url',
                'subnet': {
                    'name': 'InvalidURL',
                    'sources': {'website': 'https://definitely-does-not-exist-12345.com'}
                }
            },
            {
                'name': 'empty_sources',
                'subnet': {
                    'name': 'EmptySources',
                    'sources': {}
                }
            }
        ]
        
        for case in edge_cases:
            try:
                pipeline = FlexibleSubnetAnalysisPipeline(self.api_key)
                result = await pipeline.analyze_subnet_comprehensive(case['subnet'])
                
                # For edge cases, we expect graceful failure handling
                success = 'error' in result or result.get('status') == 'failed'
                
                self._record_test_result(f"edge_case_{case['name']}", success, result)
                
                if success:
                    logger.info(f"✅ Edge Case {case['name']}: PASSED (graceful failure)")
                else:
                    logger.warning(f"⚠️ Edge Case {case['name']}: Unexpected success")
                
                await pipeline.close()
            
            except Exception as e:
                logger.info(f"✅ Edge Case {case['name']}: PASSED (expected exception: {str(e)[:50]}...)")
                self._record_test_result(f"edge_case_{case['name']}", True, {'expected_exception': str(e)})
    
    def _record_test_result(self, test_name: str, success: bool, result: Dict):
        """Record test result"""
        self.test_results['tests_run'] += 1
        if success:
            self.test_results['tests_passed'] += 1
        else:
            self.test_results['tests_failed'] += 1
        
        self.test_results['detailed_results'][test_name] = {
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'result_summary': {
                'status': result.get('status', 'unknown'),
                'error': result.get('error'),
                'data_sources': result.get('data_sources', []),
                'team_size': result.get('team_information', {}).get('estimated_size') or 
                           result.get('team_analysis', {}).get('comprehensive_findings', {}).get('estimated_size', 0)
            }
        }
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*60)
        logger.info("📋 ENHANCED SCRAPING SYSTEM TEST REPORT")
        logger.info("="*60)
        
        success_rate = (self.test_results['tests_passed'] / self.test_results['tests_run']) * 100
        
        logger.info(f"Tests Run: {self.test_results['tests_run']}")
        logger.info(f"Tests Passed: {self.test_results['tests_passed']}")
        logger.info(f"Tests Failed: {self.test_results['tests_failed']}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        
        logger.info("\nDetailed Results:")
        for test_name, result in self.test_results['detailed_results'].items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            team_size = result['result_summary']['team_size']
            sources = len(result['result_summary']['data_sources'])
            
            logger.info(f"  {status} {test_name}")
            if team_size > 0:
                logger.info(f"    └─ Team size: {team_size}, Sources: {sources}")
            elif result['result_summary']['error']:
                logger.info(f"    └─ Error: {result['result_summary']['error'][:50]}...")
        
        # Save detailed report
        with open('test_report.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        logger.info(f"\nDetailed test report saved to: test_report.json")
        
        # Final assessment
        if success_rate >= 80:
            logger.info("\n🎉 SYSTEM STATUS: READY FOR PRODUCTION")
        elif success_rate >= 60:
            logger.info("\n⚠️ SYSTEM STATUS: NEEDS MINOR IMPROVEMENTS")
        else:
            logger.info("\n🔧 SYSTEM STATUS: REQUIRES SIGNIFICANT WORK")

async def main():
    """Main test execution"""
    try:
        tester = EnhancedSystemTester()
        await tester.run_all_tests()
    except ValueError as e:
        logger.error(f"Configuration Error: {e}")
        logger.error("Please set OPENAI_API_KEY environment variable")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 