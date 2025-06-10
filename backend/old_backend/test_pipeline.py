#!/usr/bin/env python3
"""
Test script for the automated subnet analysis pipeline
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automated_pipeline import AutomatedSubnetPipeline

async def test_pipeline_demo():
    """
    Run a demo of the pipeline with a few test subnets
    """
    print("="*60)
    print("BITTENSOR SUBNET ANALYSIS PIPELINE - DEMO")
    print("="*60)
    
    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY environment variable not set!")
        print("   The pipeline will run but AI research and scoring will be skipped.")
        print("   To enable full functionality, set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    # Initialize pipeline
    pipeline = AutomatedSubnetPipeline(output_dir="demo_output")
    
    print("🚀 Starting pipeline demo...")
    print(f"📁 Output directory: demo_output/")
    print()
    
    # Test with a few specific subnets (including ones we know have websites)
    test_subnets = [1, 5, 11, 19, 27, 64]  # Mix of different subnet types
    
    print(f"🎯 Testing with subnets: {test_subnets}")
    print()
    
    try:
        # Run the pipeline
        result = await pipeline.run_full_pipeline(target_netuids=test_subnets)
        
        print("✅ Pipeline completed!")
        print()
        print("="*60)
        print("EXECUTION SUMMARY")
        print("="*60)
        
        if result['status'] == 'success':
            summary = result['summary']
            print(f"📊 Total subnets processed: {summary['total_subnets_processed']}")
            print(f"🌐 Research-ready subnets: {summary['research_ready_subnets']}")
            print(f"📝 Subnets with GitHub: {summary['subnets_with_github']}")
            print(f"🔗 Average source health: {summary['average_source_health']}%")
            print(f"⚠️  Pipeline errors: {summary['pipeline_errors']}")
            print(f"⏱️  Execution time: {summary['execution_time']}")
            print()
            
            # Show phase completion
            completed_phases = result['pipeline_state']['completed_phases']
            print("📋 Completed phases:")
            for phase in completed_phases:
                print(f"   ✓ {phase}")
            print()
            
            # Show output files
            print("📄 Generated files:")
            output_files = [
                "phase_1_taostats_data.json",
                "phase_2_verified_sources.json", 
                "phase_3_normalized_data.json",
                "phase_4_research_scores.json",
                "final_subnet_analysis.json"
            ]
            
            for filename in output_files:
                filepath = f"demo_output/{filename}"
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"   📄 {filename} ({size:,} bytes)")
            
            print()
            print("🎉 Demo completed successfully!")
            print("👀 Check the demo_output/ directory for detailed results")
            
        else:
            print("❌ Pipeline failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            if result.get('pipeline_state', {}).get('errors'):
                print("Detailed errors:")
                for error in result['pipeline_state']['errors']:
                    print(f"   - {error}")
    
    except Exception as e:
        print(f"❌ Demo failed with exception: {e}")
        import traceback
        traceback.print_exc()

async def test_individual_components():
    """
    Test individual pipeline components
    """
    print("\n" + "="*60)
    print("INDIVIDUAL COMPONENT TESTS")
    print("="*60)
    
    # Test 1: TaoStats API
    print("🧪 Testing TaoStats API connection...")
    try:
        from subnets_basic_info import TaoStatsAPI
        api = TaoStatsAPI()
        subnets = api.get_all_subnets()
        print(f"   ✅ Successfully fetched {len(subnets)} subnets")
    except Exception as e:
        print(f"   ❌ TaoStats API test failed: {e}")
    
    # Test 2: Website Scraper
    print("\n🧪 Testing website scraper...")
    try:
        from subnet_website_scraper import SubnetWebsiteScraper
        scraper = SubnetWebsiteScraper()
        # Test with a reliable website
        result = scraper.scrape_subnet_website("https://httpbin.org/html", "Test Site")
        if result['status'] == 'success':
            print("   ✅ Website scraper working")
        else:
            print(f"   ⚠️  Website scraper test inconclusive: {result.get('status')}")
    except Exception as e:
        print(f"   ❌ Website scraper test failed: {e}")
    
    # Test 3: Source Verifier
    print("\n🧪 Testing source verifier...")
    try:
        from source_verifier import SourceVerifier
        verifier = SourceVerifier()
        
        # Test with sample data
        sample_taostats = {'github': 'https://github.com/test', 'website': 'https://test.com'}
        sample_website = {
            'status': 'success',
            'github_links': ['https://github.com/test'],
            'all_links': ['https://test.com', 'https://docs.test.com']
        }
        
        verified = verifier.verify_and_merge_sources(sample_taostats, sample_website)
        summary = verifier.generate_verification_summary(verified)
        print(f"   ✅ Source verifier working - {summary['total_sources']} sources processed")
    except Exception as e:
        print(f"   ❌ Source verifier test failed: {e}")
    
    # Test 4: AI Components (if API key available)
    if os.getenv('OPENAI_API_KEY'):
        print("\n🧪 Testing AI components...")
        try:
            from research_agent import ResearchAgent
            from scoring_agent import ScoringAgent
            
            # Just test initialization
            research_agent = ResearchAgent()
            scoring_agent = ScoringAgent()
            print("   ✅ AI components initialized successfully")
        except Exception as e:
            print(f"   ❌ AI components test failed: {e}")
    else:
        print("\n⚠️  Skipping AI component tests (no OpenAI API key)")

def print_setup_instructions():
    """
    Print setup instructions for users
    """
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    print()
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Set up OpenAI API key (optional but recommended):")
    print("   export OPENAI_API_KEY='your-api-key-here'")
    print()
    print("3. Run the full pipeline:")
    print("   python automated_pipeline.py")
    print()
    print("4. Or run with specific subnets:")
    print("   python automated_pipeline.py --subnets 1 5 11")
    print()
    print("5. Check output files in the pipeline_output/ directory")
    print()

async def main():
    """Main demo function"""
    print_setup_instructions()
    
    # Ask user if they want to run the demo
    try:
        response = input("Do you want to run the pipeline demo? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            await test_pipeline_demo()
            await test_individual_components()
        else:
            print("Demo skipped. You can run it later with: python test_pipeline.py")
    except KeyboardInterrupt:
        print("\nDemo cancelled by user.")
    except EOFError:
        # Running in non-interactive environment
        print("Running automated demo...")
        await test_pipeline_demo()
        await test_individual_components()

if __name__ == "__main__":
    asyncio.run(main()) 