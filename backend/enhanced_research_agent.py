#!/usr/bin/env python3
"""
Enhanced AI Research Agent for Bittensor Subnet Analysis
Features:
- Configuration-driven questions and prompts
- Structured confidence scoring
- Human review flagging
- Red flag detection
- Enhanced context provision
"""

import asyncio
import json
import logging
import yaml
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import openai
import os
import re

logger = logging.getLogger(__name__)

class EnhancedResearchAgent:
    """
    Enhanced AI-powered research agent with confidence scoring and human review capabilities
    """
    
    def __init__(self, api_key: Optional[str] = None, config_path: str = "research_config.yaml"):
        # Initialize OpenAI client
        self.client = openai.AsyncOpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY')
        )
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Extract key components from config
        self.research_categories = self.config['research_categories']
        self.system_prompts = self.config['system_prompts']
        self.answer_format = self.config['answer_format']
        self.red_flags = self.config['red_flags']
        self.human_review_triggers = self.config['human_review_triggers']
        
        logger.info("Enhanced Research Agent initialized with configuration")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load research configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file {config_path} not found")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration file: {e}")
            raise
    
    async def conduct_comprehensive_research(self, subnet_data: Dict) -> Dict:
        """
        Conduct comprehensive research with enhanced confidence scoring and human review flagging
        """
        logger.info(f"Starting enhanced research for subnet {subnet_data['netuid']}: {subnet_data['name']}")
        
        research_results = {
            'subnet_netuid': subnet_data['netuid'],
            'subnet_name': subnet_data['name'],
            'research_timestamp': datetime.now().isoformat(),
            'research_status': 'in_progress',
            'sources_analyzed': self._get_sources_summary(subnet_data),
            'answers': {},
            'analysis_metadata': {
                'overall_confidence': 'unknown',
                'completeness_percentage': 0.0,
                'human_review_required': False,
                'red_flags_detected': [],
                'evidence_quality_distribution': {},
                'confidence_distribution': {}
            },
            'human_review_summary': {
                'triggers': [],
                'priority_items': [],
                'recommended_actions': []
            }
        }
        
        try:
            # Prepare enhanced research context
            research_context = self._prepare_enhanced_context(subnet_data)
            
            # Assess initial source quality
            source_quality = self._assess_enhanced_source_quality(subnet_data)
            research_results['analysis_metadata']['source_quality'] = source_quality
            
            # Conduct research for each category
            for category_key, category_config in self.research_categories.items():
                logger.info(f"Researching {category_config['name']} for subnet {subnet_data['netuid']}")
                
                category_answers = await self._research_category_enhanced(
                    category_key,
                    category_config,
                    research_context,
                    subnet_data
                )
                
                research_results['answers'][category_key] = category_answers
                
                # Brief pause between categories
                await asyncio.sleep(0.5)
            
            # Analyze results and determine human review requirements
            research_results = self._analyze_research_results(research_results)
            research_results['research_status'] = 'completed'
            
            logger.info(f"Enhanced research completed for subnet {subnet_data['netuid']} - "
                       f"Confidence: {research_results['analysis_metadata']['overall_confidence']}, "
                       f"Human Review: {research_results['analysis_metadata']['human_review_required']}")
            
        except Exception as e:
            logger.error(f"Enhanced research failed for subnet {subnet_data['netuid']}: {e}")
            research_results['research_status'] = 'failed'
            research_results['error'] = str(e)
            research_results['analysis_metadata']['human_review_required'] = True
            research_results['human_review_summary']['triggers'].append(f"Research failed: {str(e)}")
        
        return research_results
    
    def _prepare_enhanced_context(self, subnet_data: Dict) -> Dict:
        """
        Prepare comprehensive, structured context for AI research
        """
        context = {
            'basic_info': {
                'name': subnet_data['name'],
                'netuid': subnet_data['netuid'],
                'description': subnet_data.get('description', 'No description available')
            },
            'sources': {},
            'website_analysis': {},
            'github_analysis': {},
            'social_media': {},
            'additional_context': []
        }
        
        # Process verified sources
        if 'sources' in subnet_data:
            for source_type, source_info in subnet_data['sources'].items():
                if isinstance(source_info, dict) and source_info.get('url'):
                    context['sources'][source_type] = {
                        'url': source_info['url'],
                        'status': source_info.get('status', 'unknown'),
                        'accessibility': source_info.get('accessibility', 'unknown'),
                        'last_checked': source_info.get('last_checked', 'unknown')
                    }
        
        # Enhanced website content analysis
        if 'website_raw' in subnet_data and subnet_data['website_raw'].get('status') == 'success':
            website_data = subnet_data['website_raw']
            
            context['website_analysis'] = {
                'title': website_data.get('title', ''),
                'description': website_data.get('description', ''),
                'mission': website_data.get('mission', ''),
                'key_features': website_data.get('features', []),
                'team_information': website_data.get('team_info', {}),
                'technical_details': website_data.get('technical_info', {}),
                'business_model': website_data.get('business_info', {}),
                'content_sample': website_data.get('clean_text', '')[:4000] if website_data.get('clean_text') else '',
                'github_links': website_data.get('github_links', []),
                'social_links': website_data.get('social_links', []),
                'external_links': website_data.get('all_links', [])[:20]  # Limit for context
            }
        
        # GitHub analysis (if available)
        if 'github_analysis' in subnet_data:
            context['github_analysis'] = subnet_data['github_analysis']
        
        return context
    
    async def _research_category_enhanced(self, category_key: str, category_config: Dict, 
                                        context: Dict, subnet_data: Dict) -> Dict:
        """
        Research a category with enhanced prompting and structured responses
        """
        category_answers = {}
        
        # Create enhanced system prompt
        system_prompt = self._build_enhanced_system_prompt(category_config, subnet_data['name'])
        
        # Process each question in the category
        for question_key, question_config in category_config['questions'].items():
            logger.debug(f"Processing question: {question_key}")
            
            try:
                answer_data = await self._research_single_question(
                    question_key,
                    question_config,
                    category_config,
                    context,
                    system_prompt,
                    subnet_data['name']
                )
                
                category_answers[question_key] = answer_data
                
                # Brief pause between questions
                await asyncio.sleep(0.2)
                
            except Exception as e:
                logger.error(f"Failed to research question {question_key}: {e}")
                category_answers[question_key] = self._create_error_answer(question_config, str(e))
        
        return category_answers
    
    def _build_enhanced_system_prompt(self, category_config: Dict, subnet_name: str) -> str:
        """
        Build enhanced system prompt with specific guidance
        """
        base_prompt = self.system_prompts['base_analyst']
        research_prompt = self.system_prompts['research_specialist']
        
        category_prompt = f"""
CURRENT ANALYSIS FOCUS: {category_config['name']}
CATEGORY DESCRIPTION: {category_config['description']}

You are analyzing the Bittensor subnet "{subnet_name}" specifically for {category_config['name'].lower()}.

RESPONSE FORMAT REQUIREMENTS:
For each question, provide a structured response with:

1. **ANSWER**: Your analysis based strictly on available evidence
2. **CONFIDENCE LEVEL**: 
   - HIGH: Multiple verified sources with consistent information
   - MEDIUM: Single reliable source or minor inconsistencies
   - LOW: Limited evidence or significant uncertainty  
   - NO_DATA: No relevant information available
3. **EVIDENCE QUALITY**: Rate as EXCELLENT/GOOD/FAIR/POOR
4. **EVIDENCE SOURCES**: List specific sources used
5. **RED FLAGS**: Any concerning findings (if applicable)
6. **ADDITIONAL NOTES**: Important context or caveats

CRITICAL GUIDELINES:
- Be conservative in confidence assessments
- Flag ANY concerning information immediately
- Cite specific evidence when available
- Use "Information not available in sources" when appropriate
- Distinguish between facts and speculation
"""
        
        return f"{base_prompt}\n\n{research_prompt}\n\n{category_prompt}"
    
    async def _research_single_question(self, question_key: str, question_config: Dict,
                                      category_config: Dict, context: Dict, 
                                      system_prompt: str, subnet_name: str) -> Dict:
        """
        Research a single question with enhanced prompting
        """
        # Build detailed context for this specific question
        question_context = self._build_question_context(question_config, context)
        
        # Create specific user prompt
        user_prompt = f"""
QUESTION: {question_config['question']}

GUIDANCE: {question_config.get('guidance', 'Provide a thorough analysis based on available evidence.')}

EXPECTED EVIDENCE SOURCES: {', '.join(question_config.get('evidence_sources', ['any_available']))}

CONTEXT:
{question_context}

Please provide a structured analysis following the format requirements.
"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse the structured response
            parsed_answer = self._parse_structured_response(
                ai_response, 
                question_key, 
                question_config,
                context
            )
            
            return parsed_answer
            
        except Exception as e:
            logger.error(f"AI call failed for question {question_key}: {e}")
            return self._create_error_answer(question_config, str(e))
    
    def _build_question_context(self, question_config: Dict, context: Dict) -> str:
        """
        Build targeted context for a specific question
        """
        context_parts = []
        
        # Basic subnet info
        basic_info = context['basic_info']
        context_parts.append(f"SUBNET: {basic_info['name']} (NetUID: {basic_info['netuid']})")
        context_parts.append(f"DESCRIPTION: {basic_info['description']}")
        
        # Sources summary
        if context['sources']:
            context_parts.append("\nVERIFIED SOURCES:")
            for source_type, source_info in context['sources'].items():
                context_parts.append(f"- {source_type.upper()}: {source_info['url']} "
                                   f"(Status: {source_info['status']})")
        
        # Website analysis (most comprehensive)
        website = context.get('website_analysis', {})
        if website:
            if website.get('title'):
                context_parts.append(f"\nWEBSITE TITLE: {website['title']}")
            if website.get('description'):
                context_parts.append(f"WEBSITE DESCRIPTION: {website['description']}")
            if website.get('mission'):
                context_parts.append(f"STATED MISSION: {website['mission']}")
            
            # Include relevant sections based on expected evidence sources
            expected_sources = question_config.get('evidence_sources', [])
            
            if any(source in ['team_page', 'team_bios'] for source in expected_sources):
                team_info = website.get('team_information', {})
                if team_info:
                    context_parts.append(f"\nTEAM INFORMATION:")
                    for key, value in team_info.items():
                        if value:
                            context_parts.append(f"- {key}: {str(value)[:200]}")
            
            if any(source in ['technical_docs', 'github_code'] for source in expected_sources):
                tech_info = website.get('technical_details', {})
                if tech_info:
                    context_parts.append(f"\nTECHNICAL INFORMATION:")
                    for key, value in tech_info.items():
                        if value:
                            context_parts.append(f"- {key}: {str(value)[:200]}")
            
            # Include content sample for general analysis
            if website.get('content_sample'):
                context_parts.append(f"\nWEBSITE CONTENT SAMPLE:")
                context_parts.append(website['content_sample'][:2000])
        
        # GitHub analysis if available
        github = context.get('github_analysis', {})
        if github and any(source in ['github_activity', 'github_contributors'] 
                         for source in question_config.get('evidence_sources', [])):
            context_parts.append(f"\nGITHUB ANALYSIS:")
            for key, value in github.items():
                if value:
                    context_parts.append(f"- {key}: {str(value)[:200]}")
        
        return "\n".join(context_parts)
    
    def _parse_structured_response(self, ai_response: str, question_key: str, 
                                 question_config: Dict, context: Dict) -> Dict:
        """
        Parse AI response into structured format with confidence and evidence tracking
        """
        # Extract key components using regex patterns
        patterns = {
            'answer': r'\*\*ANSWER\*\*:?\s*(.*?)(?=\*\*[A-Z]|\Z)',
            'confidence': r'\*\*CONFIDENCE LEVEL\*\*:?\s*(HIGH|MEDIUM|LOW|NO_DATA)',
            'evidence_quality': r'\*\*EVIDENCE QUALITY\*\*:?\s*(EXCELLENT|GOOD|FAIR|POOR)',
            'evidence_sources': r'\*\*EVIDENCE SOURCES\*\*:?\s*(.*?)(?=\*\*[A-Z]|\Z)',
            'red_flags': r'\*\*RED FLAGS\*\*:?\s*(.*?)(?=\*\*[A-Z]|\Z)',
            'additional_notes': r'\*\*ADDITIONAL NOTES\*\*:?\s*(.*?)(?=\*\*[A-Z]|\Z)'
        }
        
        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, ai_response, re.DOTALL | re.IGNORECASE)
            if match:
                extracted[key] = match.group(1).strip()
            else:
                extracted[key] = ''
        
        # Clean and validate extracted data
        answer = extracted['answer'] or "No specific answer provided"
        confidence = extracted['confidence'].upper() if extracted['confidence'] else 'MEDIUM'
        if confidence not in ['HIGH', 'MEDIUM', 'LOW', 'NO_DATA']:
            confidence = 'MEDIUM'
        
        evidence_quality = extracted['evidence_quality'].upper() if extracted['evidence_quality'] else 'FAIR'
        if evidence_quality not in ['EXCELLENT', 'GOOD', 'FAIR', 'POOR']:
            evidence_quality = 'FAIR'
        
        # Process evidence sources
        evidence_sources = []
        if extracted['evidence_sources']:
            sources = extracted['evidence_sources'].replace(',', '\n').split('\n')
            evidence_sources = [s.strip() for s in sources if s.strip()]
        
        # Process red flags
        red_flags = []
        if extracted['red_flags'] and extracted['red_flags'].lower() not in ['none', 'no red flags', 'n/a']:
            flags = extracted['red_flags'].replace(',', '\n').split('\n')
            red_flags = [f.strip() for f in flags if f.strip()]
        
        # Determine human review requirement
        confidence_config = self.answer_format['confidence_levels']
        human_review_required = confidence_config.get(confidence.lower(), {}).get('human_review', False)
        
        # Additional human review triggers
        if red_flags:
            human_review_required = True
        if 'not available' in answer.lower() or 'no information' in answer.lower():
            human_review_required = True
        
        return {
            'question': question_config['question'],
            'question_key': question_key,
            'answer': answer,
            'confidence_level': confidence,
            'evidence_quality': evidence_quality,
            'evidence_sources': evidence_sources,
            'red_flags': red_flags,
            'additional_notes': extracted['additional_notes'],
            'human_review_required': human_review_required,
            'research_timestamp': datetime.now().isoformat(),
            'research_status': 'completed',
            'raw_ai_response': ai_response
        }
    
    def _create_error_answer(self, question_config: Dict, error_msg: str) -> Dict:
        """
        Create error answer structure
        """
        return {
            'question': question_config['question'],
            'answer': f"Research failed: {error_msg}",
            'confidence_level': 'NO_DATA',
            'evidence_quality': 'POOR',
            'evidence_sources': [],
            'red_flags': ['Research system error'],
            'additional_notes': 'Technical error during analysis',
            'human_review_required': True,
            'research_timestamp': datetime.now().isoformat(),
            'research_status': 'error'
        }
    
    def _analyze_research_results(self, research_results: Dict) -> Dict:
        """
        Analyze completed research and determine overall confidence and human review needs
        """
        all_answers = []
        for category_answers in research_results['answers'].values():
            all_answers.extend(category_answers.values())
        
        if not all_answers:
            research_results['analysis_metadata']['overall_confidence'] = 'NO_DATA'
            research_results['analysis_metadata']['human_review_required'] = True
            return research_results
        
        # Confidence distribution
        confidence_counts = {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'NO_DATA': 0}
        evidence_counts = {'EXCELLENT': 0, 'GOOD': 0, 'FAIR': 0, 'POOR': 0}
        all_red_flags = []
        human_review_triggers = []
        
        for answer in all_answers:
            confidence = answer.get('confidence_level', 'MEDIUM')
            evidence = answer.get('evidence_quality', 'FAIR')
            
            confidence_counts[confidence] += 1
            evidence_counts[evidence] += 1
            
            if answer.get('red_flags'):
                all_red_flags.extend(answer['red_flags'])
            
            if answer.get('human_review_required'):
                human_review_triggers.append(f"{answer['question_key']}: {confidence} confidence")
        
        total_answers = len(all_answers)
        
        # Calculate overall confidence
        high_pct = confidence_counts['HIGH'] / total_answers * 100
        medium_pct = confidence_counts['MEDIUM'] / total_answers * 100
        low_pct = (confidence_counts['LOW'] + confidence_counts['NO_DATA']) / total_answers * 100
        
        if high_pct >= 60:
            overall_confidence = 'HIGH'
        elif high_pct + medium_pct >= 70:
            overall_confidence = 'MEDIUM'
        else:
            overall_confidence = 'LOW'
        
        # Human review decision
        human_review_required = (
            low_pct > 30 or  # More than 30% low/no-data confidence
            len(all_red_flags) > 0 or  # Any red flags
            confidence_counts['HIGH'] == 0  # No high confidence answers
        )
        
        # Update metadata
        research_results['analysis_metadata'].update({
            'overall_confidence': overall_confidence,
            'completeness_percentage': round((total_answers / self._count_total_questions()) * 100, 1),
            'human_review_required': human_review_required,
            'red_flags_detected': list(set(all_red_flags)),
            'confidence_distribution': confidence_counts,
            'evidence_quality_distribution': evidence_counts
        })
        
        # Human review summary
        research_results['human_review_summary'] = {
            'triggers': human_review_triggers,
            'priority_items': all_red_flags,
            'recommended_actions': self._generate_review_recommendations(
                confidence_counts, evidence_counts, all_red_flags
            )
        }
        
        return research_results
    
    def _count_total_questions(self) -> int:
        """Count total questions across all categories"""
        return sum(len(cat['questions']) for cat in self.research_categories.values())
    
    def _generate_review_recommendations(self, confidence_counts: Dict, 
                                       evidence_counts: Dict, red_flags: List[str]) -> List[str]:
        """
        Generate specific recommendations for human reviewers
        """
        recommendations = []
        
        if confidence_counts['NO_DATA'] > 0:
            recommendations.append(f"Investigate {confidence_counts['NO_DATA']} questions with no data")
        
        if confidence_counts['LOW'] > 0:
            recommendations.append(f"Verify {confidence_counts['LOW']} low-confidence answers")
        
        if evidence_counts['POOR'] > 0:
            recommendations.append(f"Find better sources for {evidence_counts['POOR']} poorly-evidenced answers")
        
        if red_flags:
            recommendations.append(f"Address {len(red_flags)} red flags identified")
        
        if confidence_counts['HIGH'] == 0:
            recommendations.append("No high-confidence answers - consider additional research")
        
        return recommendations
    
    def _get_sources_summary(self, subnet_data: Dict) -> Dict:
        """Get summary of analyzed sources"""
        summary = {
            'total_sources': 0,
            'verified_sources': 0,
            'accessible_sources': 0,
            'website_scraped': False,
            'github_analyzed': False,
            'source_types': []
        }
        
        if 'sources' in subnet_data:
            sources = subnet_data['sources']
            summary['total_sources'] = len(sources)
            summary['verified_sources'] = len([s for s in sources.values() 
                                             if isinstance(s, dict) and s.get('status') in ['verified', 'both']])
            summary['accessible_sources'] = len([s for s in sources.values() 
                                               if isinstance(s, dict) and s.get('accessibility') == 'accessible'])
            summary['source_types'] = list(sources.keys())
        
        summary['website_scraped'] = (subnet_data.get('website_raw', {}).get('status') == 'success')
        summary['github_analyzed'] = ('github_analysis' in subnet_data)
        
        return summary
    
    def _assess_enhanced_source_quality(self, subnet_data: Dict) -> Dict:
        """Enhanced source quality assessment"""
        quality_score = 0
        max_score = 10
        
        quality_factors = {
            'verified_website': 3,
            'active_github': 2,
            'comprehensive_docs': 2,
            'social_presence': 1,
            'team_transparency': 2
        }
        
        # Check each factor
        scored_factors = {}
        
        # Verified website
        if subnet_data.get('website_raw', {}).get('status') == 'success':
            scored_factors['verified_website'] = quality_factors['verified_website']
            quality_score += quality_factors['verified_website']
        
        # Active GitHub
        github_sources = [s for s in subnet_data.get('sources', {}).values() 
                         if isinstance(s, dict) and 'github' in s.get('url', '').lower()]
        if github_sources:
            scored_factors['active_github'] = quality_factors['active_github']
            quality_score += quality_factors['active_github']
        
        # Other factors would be assessed based on available data...
        
        return {
            'overall_score': quality_score,
            'max_possible': max_score,
            'percentage': round((quality_score / max_score) * 100, 1),
            'rating': 'excellent' if quality_score >= 8 else 'good' if quality_score >= 6 else 'fair' if quality_score >= 4 else 'poor',
            'scored_factors': scored_factors
        }

# Testing function
async def test_enhanced_research_agent():
    """Test the enhanced research agent"""
    if not os.getenv('OPENAI_API_KEY'):
        print("OPENAI_API_KEY not set - skipping test")
        return
    
    # Create test agent
    agent = EnhancedResearchAgent()
    
    # Sample data
    sample_subnet = {
        'netuid': 64,
        'name': 'Test Subnet',
        'description': 'A test subnet for research agent validation',
        'sources': {
            'website': {
                'url': 'https://example.com',
                'status': 'verified',
                'accessibility': 'accessible'
            }
        },
        'website_raw': {
            'status': 'success',
            'title': 'Test Subnet - AI Innovation',
            'description': 'Revolutionary AI platform',
            'clean_text': 'We are building the future of AI with our innovative approach...'
        }
    }
    
    # Run research
    results = await agent.conduct_comprehensive_research(sample_subnet)
    
    print("=== ENHANCED RESEARCH AGENT TEST ===")
    print(f"Research Status: {results['research_status']}")
    print(f"Overall Confidence: {results['analysis_metadata']['overall_confidence']}")
    print(f"Human Review Required: {results['analysis_metadata']['human_review_required']}")
    print(f"Red Flags: {len(results['analysis_metadata']['red_flags_detected'])}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_research_agent()) 