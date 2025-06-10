#!/usr/bin/env python3
"""
Test script for the enhanced subnet analysis pipeline with AI research improvements
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

from enhanced_automated_pipeline import EnhancedAutomatedSubnetPipeline
from human_review_dashboard import HumanReviewDashboard

async def test_enhanced_pipeline_demo():
    """
    Run a demo of the enhanced pipeline with confidence scoring and human review
    """
    print("="*70)
    print("ENHANCED BITTENSOR SUBNET ANALYSIS PIPELINE - DEMO")
    print("="*70)
    
    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY environment variable not set!")
        print("   The enhanced pipeline will run but AI research and scoring will be limited.")
        print("   To enable full functionality, set your OpenAI API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    print("🚀 Starting enhanced pipeline demo...")
    print("📁 Output directory: enhanced_demo_output/")
    print()
    
    # Test with a few specific subnets
    test_subnets = [1, 5, 11, 19, 27]  # Mix of different subnet types
    
    print(f"🎯 Testing with subnets: {test_subnets}")
    print()
    
    try:
        # Initialize enhanced pipeline
        pipeline = EnhancedAutomatedSubnetPipeline(
            output_dir="enhanced_demo_output",
            config_path="research_config.yaml"
        )
        
        # Run the enhanced pipeline
        result = await pipeline.run_enhanced_pipeline(
            target_netuids=test_subnets,
            enable_human_review=True
        )
        
        print("✅ Enhanced pipeline completed!")
        print()
        print("="*70)
        print("ENHANCED EXECUTION SUMMARY")
        print("="*70)
        
        if result['status'] == 'success':
            summary = result['summary']['execution_summary']
            quality = result['summary']['quality_metrics']
            
            print(f"📊 Total subnets processed: {summary['total_subnets_processed']}")
            print(f"🔬 Research-ready subnets: {summary['research_ready_subnets']}")
            print(f"🤖 Successfully researched: {summary['successfully_researched']}")
            print(f"🎯 High confidence results: {summary['high_confidence_results']}")
            print(f"👥 Human review required: {summary['human_review_required']}")
            print(f"📈 Success rate: {summary['success_rate']}")
            print(f"❌ Pipeline errors: {summary['pipeline_errors']}")
            print()
            
            # Show confidence distribution
            print("📋 Confidence Distribution:")
            for level, count in quality['confidence_distribution'].items():
                print(f"   {level}: {count}")
            print()
            
            # Show scoring distribution
            print("📊 Scoring Distribution:")
            for category, count in quality['scoring_distribution'].items():
                print(f"   {category}: {count}")
            print()
            
            # Show top subnets
            print("🏆 Top Performing Subnets:")
            for subnet in result['summary']['top_subnets'][:5]:
                confidence = subnet['confidence']
                score = subnet['overall_score']
                print(f"   #{subnet['netuid']} {subnet['name']}: {score:.1f}/5 ({confidence} confidence)")
            print()
            
            # Show recommendations
            if result['summary']['recommendations']:
                print("💡 Recommendations:")
                for rec in result['summary']['recommendations']:
                    print(f"   • {rec}")
                print()
            
            # Show completed phases
            completed_phases = result['pipeline_state']['completed_phases']
            print("📋 Completed phases:")
            for phase in completed_phases:
                print(f"   ✓ {phase}")
            print()
            
            # Show human review summary if available
            if summary['human_review_required'] > 0:
                print("👥 Human Review Summary:")
                print(f"   • {summary['human_review_required']} subnets need human review")
                print("   • Check enhanced_demo_output/human_review/ for review worksheets")
                print("   • Use: python human_review_dashboard.py --action worksheet --subnet-id <ID>")
                print()
            
            print("🎉 Enhanced demo completed successfully!")
            print("👀 Check the enhanced_demo_output/ directory for detailed results")
            print()
            print("📂 Key output files:")
            print("   • final_enhanced_analysis.json - Complete analysis results")
            print("   • phase_4_research_results.json - AI research outputs with confidence")
            print("   • phase_6_review_summary.json - Human review requirements")
            print("   • human_review/ - Human review worksheets and summaries")
            
        else:
            print("❌ Enhanced pipeline failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            if result.get('pipeline_state', {}).get('errors'):
                print("Detailed errors:")
                for error in result['pipeline_state']['errors']:
                    print(f"   - {error}")
    
    except Exception as e:
        print(f"❌ Enhanced demo failed with exception: {e}")
        import traceback
        traceback.print_exc()

async def test_human_review_workflow():
    """
    Test the human review workflow specifically
    """
    print("\n" + "="*70)
    print("HUMAN REVIEW WORKFLOW TEST")
    print("="*70)
    
    # Create sample research results that would trigger human review
    sample_research_results = [
        {
            'subnet_netuid': 999,
            'subnet_name': 'Test Subnet',
            'research_status': 'completed',
            'analysis_metadata': {
                'overall_confidence': 'LOW',
                'human_review_required': True,
                'red_flags_detected': ['Anonymous team'],
                'completeness_percentage': 45.0
            },
            'answers': {
                'team': {
                    'team_transparency': {
                        'question': 'How transparent is the team about their identities?',
                        'answer': 'Team members are anonymous with no verifiable backgrounds',
                        'confidence_level': 'LOW',
                        'evidence_quality': 'POOR',
                        'evidence_sources': ['website_content'],
                        'red_flags': ['Anonymous team with no verifiable identities'],
                        'human_review_required': True,
                        'question_key': 'team_transparency'
                    }
                }
            }
        }
    ]
    
    try:
        # Initialize review dashboard
        dashboard = HumanReviewDashboard("test_human_review")
        
        # Process the sample results
        review_summary = dashboard.process_research_results(sample_research_results)
        
        print(f"📊 Review summary generated:")
        print(f"   • Total items for review: {review_summary['total_items_for_review']}")
        print(f"   • High priority items: {review_summary['high_priority_items']}")
        print(f"   • Subnets requiring review: {review_summary['subnets_requiring_review']}")
        print()
        
        # Generate a sample worksheet
        if review_summary['review_queue']:
            subnet_id = review_summary['review_queue'][0]['subnet_netuid']
            worksheet = dashboard.generate_review_worksheet(subnet_id)
            
            print(f"📝 Sample worksheet generated for subnet {subnet_id}")
            print(f"   • Estimated review time: {worksheet['subnet_info']['estimated_time']} minutes")
            print(f"   • Priority: {worksheet['subnet_info']['priority']}")
            print(f"   • Review items: {len(worksheet['review_items'])}")
            print()
            
            print("📋 Review instructions:")
            for instruction in worksheet['review_instructions'][:3]:
                print(f"   • {instruction}")
            print()
        
        print("✅ Human review workflow test completed!")
        
    except Exception as e:
        print(f"❌ Human review test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_individual_enhanced_components():
    """
    Test individual enhanced components
    """
    print("\n" + "="*70)
    print("ENHANCED COMPONENT TESTS")
    print("="*70)
    
    # Test 1: Enhanced Research Agent
    print("🧪 Testing Enhanced Research Agent...")
    try:
        from enhanced_research_agent import EnhancedResearchAgent
        agent = EnhancedResearchAgent()
        print("   ✅ Enhanced Research Agent initialized successfully")
        print("   📋 Configuration loaded with enhanced prompts and scoring")
    except Exception as e:
        print(f"   ❌ Enhanced Research Agent test failed: {e}")
    
    # Test 2: Configuration Loading
    print("\n🧪 Testing Research Configuration...")
    try:
        import yaml
        with open('research_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        categories = list(config['research_categories'].keys())
        total_questions = sum(len(cat['questions']) for cat in config['research_categories'].values())
        
        print(f"   ✅ Configuration loaded successfully")
        print(f"   📊 Categories: {len(categories)} ({', '.join(categories)})")
        print(f"   📝 Total questions: {total_questions}")
        print(f"   🎯 Confidence levels defined: {len(config['answer_format']['confidence_levels'])}")
        print(f"   🚨 Red flag categories: {len(config['red_flags'])}")
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
    
    # Test 3: Human Review Dashboard
    print("\n🧪 Testing Human Review Dashboard...")
    try:
        from human_review_dashboard import HumanReviewDashboard
        dashboard = HumanReviewDashboard()
        print("   ✅ Human Review Dashboard initialized successfully")
        print("   📂 Review output directory created")
    except Exception as e:
        print(f"   ❌ Human Review Dashboard test failed: {e}")
    
    print("\n✅ Enhanced component tests completed!")

def print_enhanced_setup_instructions():
    """
    Print setup instructions for the enhanced pipeline
    """
    print("\n" + "="*70)
    print("ENHANCED PIPELINE SETUP INSTRUCTIONS")
    print("="*70)
    print()
    print("1. Install enhanced dependencies:")
    print("   pip install -r requirements.txt")
    print("   # New: PyYAML for configuration management")
    print()
    print("2. Set up OpenAI API key (required for enhanced AI features):")
    print("   export OPENAI_API_KEY='your-api-key-here'")
    print()
    print("3. Configuration Management:")
    print("   • research_config.yaml - Configure questions, prompts, and criteria")
    print("   • Customize confidence thresholds and human review triggers")
    print("   • Add domain-specific red flags and evaluation criteria")
    print()
    print("4. Run the enhanced pipeline:")
    print("   python enhanced_automated_pipeline.py")
    print("   python enhanced_automated_pipeline.py --subnets 1 5 11")
    print("   python enhanced_automated_pipeline.py --disable-human-review")
    print()
    print("5. Human Review Workflow:")
    print("   # Process research results for review")
    print("   python human_review_dashboard.py --action process --input-file results.json")
    print("   # Generate review worksheet")
    print("   python human_review_dashboard.py --action worksheet --subnet-id 1")
    print("   # Generate review report")
    print("   python human_review_dashboard.py --action report")
    print()
    print("6. Key Enhanced Features:")
    print("   ✓ Structured confidence scoring (HIGH/MEDIUM/LOW/NO_DATA)")
    print("   ✓ Automated human review flagging")
    print("   ✓ Red flag detection and escalation")
    print("   ✓ Evidence quality assessment")
    print("   ✓ Configurable research questions and prompts")
    print("   ✓ Review workflow management")
    print("   ✓ Performance analytics and reporting")
    print()

async def main():
    """Main demo function"""
    print_enhanced_setup_instructions()
    
    # Ask user if they want to run the demo
    try:
        response = input("Do you want to run the enhanced pipeline demo? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            await test_enhanced_pipeline_demo()
            await test_human_review_workflow()
            await test_individual_enhanced_components()
        else:
            print("Demo skipped. You can run it later with: python test_enhanced_pipeline.py")
    except KeyboardInterrupt:
        print("\nDemo cancelled by user.")
    except EOFError:
        # Running in non-interactive environment
        print("Running automated enhanced demo...")
        await test_enhanced_pipeline_demo()
        await test_human_review_workflow()
        await test_individual_enhanced_components()

if __name__ == "__main__":
    asyncio.run(main()) 