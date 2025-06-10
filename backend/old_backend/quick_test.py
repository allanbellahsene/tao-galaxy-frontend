#!/usr/bin/env python3

import asyncio
import json
import os
import sys
from enhanced_website_scraper import EnhancedWebsiteScraper
from flexible_pipeline import FlexibleSubnetAnalysisPipeline

async def quick_test_website_scraper():
    """Quick test of the enhanced website scraper with Apex"""
    print("🔍 Quick Test: Enhanced Website Scraper")
    print("-" * 40)
    
    try:
        scraper = EnhancedWebsiteScraper()
        result = scraper.scrape_subnet_website('https://www.macrocosmos.ai', 'Apex')
        
        print(f"Status: {result.get('status')}")
        if result.get('status') == 'success':
            print(f"AI Analysis Available: {'ai_analysis' in result}")
            print(f"Enhanced Team Info: {'enhanced_team_info' in result}")
            
            team_info = result.get('enhanced_team_info', {})
            print(f"Team Members Found: {team_info.get('team_members_found', 0)}")
            print(f"Has Team Section: {team_info.get('has_team_section', False)}")
            
            # Save result for inspection
            with open('quick_test_scraper_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("✅ Result saved to quick_test_scraper_result.json")
        else:
            print(f"❌ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

async def quick_test_apex_analysis():
    """Quick test of the full pipeline with Apex"""
    print("\n🎯 Quick Test: Apex Full Analysis")
    print("-" * 40)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return
    
    try:
        pipeline = FlexibleSubnetAnalysisPipeline(api_key)
        
        apex_subnet = {
            'name': 'Apex',
            'netuid': 1,
            'description': 'Decentralized AI development platform',
            'sources': {
                'website': 'https://www.macrocosmos.ai',
                'github': 'https://github.com/macrocosm-os/prompting'
            }
        }
        
        print("Starting analysis...")
        result = await pipeline.analyze_subnet_comprehensive(apex_subnet)
        
        print(f"Status: {result.get('status', 'unknown')}")
        
        if result.get('status') != 'failed':
            team_analysis = result.get('team_analysis', {})
            team_size = team_analysis.get('comprehensive_findings', {}).get('estimated_size', 0)
            sources_used = result.get('data_collection_summary', {}).get('sources_used', [])
            confidence = result.get('analysis_metadata', {}).get('analysis_confidence', 0)
            
            print(f"Team Size Found: {team_size}")
            print(f"Data Sources: {sources_used}")
            print(f"Overall Confidence: {confidence:.2f}")
            
            # Save detailed result
            with open('quick_test_apex_result.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("✅ Detailed result saved to quick_test_apex_result.json")
            
            # Check if we solved the original issue
            if team_size > 0:
                print("🎉 SUCCESS: Found team information!")
            else:
                print("⚠️ PARTIAL: No team size detected")
        else:
            print(f"❌ Analysis failed: {result.get('error')}")
        
        await pipeline.close()
        
    except Exception as e:
        print(f"❌ Exception: {e}")

async def main():
    """Run quick tests"""
    print("🚀 Enhanced Scraping System - Quick Tests")
    print("=" * 50)
    
    # Test 1: Website scraper only
    await quick_test_website_scraper()
    
    # Test 2: Full pipeline
    await quick_test_apex_analysis()
    
    print("\n✅ Quick tests completed!")
    print("For full testing, run: python test_enhanced_system.py")

if __name__ == "__main__":
    asyncio.run(main()) 