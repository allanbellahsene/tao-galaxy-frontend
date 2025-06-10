import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class ResearchAgent:
    """
    AI-powered research agent that analyzes subnet data and sources to answer specific questions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        # Initialize OpenAI client
        self.client = openai.AsyncOpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY')
        )
        
        # Research questions to answer for each subnet
        self.research_questions = {
            # Basic Information
            'basic_info': {
                'mission_statement': "What is the subnet's mission statement or primary goal?",
                'problem_solving': "What specific problem does this subnet aim to solve?",
                'target_audience': "Who is the target audience or user base for this subnet?",
                'unique_value_proposition': "What makes this subnet unique compared to competitors?"
            },
            
            # Team & Leadership
            'team': {
                'team_size': "How many team members does this subnet have?",
                'team_experience': "What is the experience level and background of the team?",
                'leadership_quality': "Who are the key leaders and what are their credentials?",
                'team_transparency': "How transparent is the team about their identities and backgrounds?"
            },
            
            # Product & Technology
            'product': {
                'product_status': "What is the current status of their product/service (concept, MVP, beta, live)?",
                'technical_approach': "What technical approach or methodology do they use?",
                'product_differentiation': "How does their product differ from existing solutions?",
                'scalability': "How scalable is their technical solution?"
            },
            
            # Business Model
            'business': {
                'revenue_model': "What is their revenue model or monetization strategy?",
                'market_size': "What is the size of their target market?",
                'competitive_landscape': "Who are their main competitors?",
                'partnership_strategy': "Do they have notable partnerships or collaborations?"
            },
            
            # Development & Progress
            'development': {
                'development_activity': "How active is their development (based on GitHub, updates, etc.)?",
                'roadmap_clarity': "How clear and detailed is their development roadmap?",
                'milestone_achievement': "Have they achieved their stated milestones?",
                'community_engagement': "How engaged is their community?"
            },
            
            # Risk Assessment
            'risks': {
                'technical_risks': "What are the main technical risks or challenges?",
                'market_risks': "What market risks does the subnet face?",
                'regulatory_risks': "Are there any regulatory or compliance concerns?",
                'team_risks': "Are there any team-related risks (key person dependency, etc.)?"
            }
        }
    
    async def conduct_research(self, subnet_data: Dict) -> Dict:
        """
        Conduct comprehensive research on a subnet using AI analysis
        """
        logger.info(f"Starting research for subnet {subnet_data['netuid']}: {subnet_data['name']}")
        
        research_results = {
            'subnet_netuid': subnet_data['netuid'],
            'subnet_name': subnet_data['name'],
            'research_timestamp': datetime.now().isoformat(),
            'sources_analyzed': self._get_sources_summary(subnet_data),
            'research_status': 'in_progress',
            'answers': {},
            'analysis_metadata': {
                'sources_quality': self._assess_sources_quality(subnet_data),
                'data_completeness': 0.0,
                'confidence_level': 'unknown'
            }
        }
        
        try:
            # Prepare research context
            research_context = self._prepare_research_context(subnet_data)
            
            # Conduct research for each category
            for category, questions in self.research_questions.items():
                logger.info(f"Researching {category} for subnet {subnet_data['netuid']}")
                
                category_answers = await self._research_category(
                    category, 
                    questions, 
                    research_context,
                    subnet_data['name']
                )
                
                research_results['answers'][category] = category_answers
                
                # Brief pause between categories to avoid rate limits
                await asyncio.sleep(0.5)
            
            # Calculate overall completeness and confidence
            research_results['analysis_metadata'] = self._calculate_research_metadata(research_results)
            research_results['research_status'] = 'completed'
            
            logger.info(f"Research completed for subnet {subnet_data['netuid']}")
            
        except Exception as e:
            logger.error(f"Research failed for subnet {subnet_data['netuid']}: {e}")
            research_results['research_status'] = 'failed'
            research_results['error'] = str(e)
        
        return research_results
    
    def _prepare_research_context(self, subnet_data: Dict) -> str:
        """
        Prepare comprehensive context for AI research
        """
        context_parts = []
        
        # Basic subnet information
        context_parts.append(f"SUBNET: {subnet_data['name']} (NetUID: {subnet_data['netuid']})")
        context_parts.append(f"DESCRIPTION: {subnet_data.get('description', 'No description available')}")
        
        # Verified sources
        if 'sources' in subnet_data:
            context_parts.append("\nVERIFIED SOURCES:")
            for source_type, source_info in subnet_data['sources'].items():
                if isinstance(source_info, dict) and source_info.get('url'):
                    status = source_info.get('status', 'unknown')
                    context_parts.append(f"- {source_type.upper()}: {source_info['url']} (Status: {status})")
        
        # Website content
        if 'website_raw' in subnet_data and subnet_data['website_raw'].get('status') == 'success':
            website_data = subnet_data['website_raw']
            
            if website_data.get('title'):
                context_parts.append(f"\nWEBSITE TITLE: {website_data['title']}")
            
            if website_data.get('description'):
                context_parts.append(f"WEBSITE DESCRIPTION: {website_data['description']}")
            
            if website_data.get('mission'):
                context_parts.append(f"MISSION: {website_data['mission']}")
            
            if website_data.get('team_info', {}).get('team_description'):
                context_parts.append(f"TEAM INFO: {website_data['team_info']['team_description'][:500]}")
            
            if website_data.get('clean_text'):
                # Include relevant portions of clean text
                clean_text = website_data['clean_text'][:3000]  # Limit for context window
                context_parts.append(f"\nWEBSITE CONTENT SAMPLE:\n{clean_text}")
        
        return "\n".join(context_parts)
    
    async def _research_category(self, category: str, questions: Dict[str, str], context: str, subnet_name: str) -> Dict:
        """
        Research a specific category of questions using AI
        """
        category_answers = {}
        
        # Create system prompt for this category
        system_prompt = f"""You are a professional research analyst specializing in blockchain and AI projects. You are analyzing the Bittensor subnet "{subnet_name}" to answer specific research questions.

INSTRUCTIONS:
1. Analyze the provided context carefully
2. Answer each question based ONLY on the available information
3. If information is not available, clearly state "Information not available"
4. Provide specific, factual answers with evidence from the context
5. Rate your confidence in each answer (High/Medium/Low)
6. Keep answers concise but comprehensive (50-200 words per question)

CONTEXT:
{context}

Please answer the following {category} questions about this subnet:"""
        
        # Prepare questions for the AI
        questions_text = "\n".join([f"{i+1}. {question}" for i, question in enumerate(questions.values())])
        
        user_prompt = f"{questions_text}\n\nPlease provide structured answers with confidence levels."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using cost-effective model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent, factual responses
                max_tokens=2000
            )
            
            # Parse the AI response
            ai_response = response.choices[0].message.content
            
            # Structure the answers
            question_keys = list(questions.keys())
            category_answers = self._parse_ai_response(ai_response, question_keys, questions)
            
        except Exception as e:
            logger.error(f"AI research failed for category {category}: {e}")
            # Fallback: create empty answers with error status
            for key in questions.keys():
                category_answers[key] = {
                    'question': questions[key],
                    'answer': f"Research failed: {str(e)}",
                    'confidence': 'Low',
                    'sources_used': [],
                    'research_status': 'error'
                }
        
        return category_answers
    
    def _parse_ai_response(self, ai_response: str, question_keys: List[str], questions: Dict[str, str]) -> Dict:
        """
        Parse AI response into structured format
        """
        structured_answers = {}
        
        # Split response by question numbers (1., 2., etc.)
        import re
        question_parts = re.split(r'\n\s*\d+\.', ai_response)
        
        # Remove empty first part if it exists
        if question_parts and not question_parts[0].strip():
            question_parts = question_parts[1:]
        
        for i, key in enumerate(question_keys):
            if i < len(question_parts):
                answer_text = question_parts[i].strip()
                
                # Extract confidence if mentioned
                confidence = 'Medium'  # Default
                if 'high confidence' in answer_text.lower() or 'confident' in answer_text.lower():
                    confidence = 'High'
                elif 'low confidence' in answer_text.lower() or 'uncertain' in answer_text.lower() or 'not available' in answer_text.lower():
                    confidence = 'Low'
                
                structured_answers[key] = {
                    'question': questions[key],
                    'answer': answer_text,
                    'confidence': confidence,
                    'sources_used': ['website_content', 'verified_sources'],
                    'research_status': 'completed'
                }
            else:
                # No answer provided for this question
                structured_answers[key] = {
                    'question': questions[key],
                    'answer': 'Information not available in provided sources',
                    'confidence': 'Low',
                    'sources_used': [],
                    'research_status': 'incomplete'
                }
        
        return structured_answers
    
    def _get_sources_summary(self, subnet_data: Dict) -> Dict:
        """Get summary of sources analyzed"""
        summary = {
            'total_sources': 0,
            'verified_sources': 0,
            'website_scraped': False,
            'source_types': []
        }
        
        if 'sources' in subnet_data:
            summary['total_sources'] = len(subnet_data['sources'])
            summary['verified_sources'] = len([s for s in subnet_data['sources'].values() 
                                             if isinstance(s, dict) and s.get('status') == 'both'])
            summary['source_types'] = list(subnet_data['sources'].keys())
        
        if 'website_raw' in subnet_data:
            summary['website_scraped'] = subnet_data['website_raw'].get('status') == 'success'
        
        return summary
    
    def _assess_sources_quality(self, subnet_data: Dict) -> str:
        """Assess the quality of available sources"""
        if not subnet_data.get('sources'):
            return 'poor'
        
        verified_count = len([s for s in subnet_data['sources'].values() 
                            if isinstance(s, dict) and s.get('status') == 'both'])
        total_count = len(subnet_data['sources'])
        
        website_available = (subnet_data.get('website_raw', {}).get('status') == 'success')
        
        if verified_count >= 3 and website_available:
            return 'excellent'
        elif verified_count >= 2 and website_available:
            return 'good'
        elif verified_count >= 1 or website_available:
            return 'fair'
        else:
            return 'poor'
    
    def _calculate_research_metadata(self, research_results: Dict) -> Dict:
        """Calculate metadata about the research quality"""
        total_questions = sum(len(category) for category in self.research_questions.values())
        answered_questions = 0
        high_confidence_answers = 0
        
        for category_answers in research_results['answers'].values():
            for answer_data in category_answers.values():
                if answer_data.get('research_status') == 'completed':
                    answered_questions += 1
                    if answer_data.get('confidence') == 'High':
                        high_confidence_answers += 1
        
        completeness = (answered_questions / total_questions * 100) if total_questions > 0 else 0
        
        # Determine overall confidence level
        if high_confidence_answers >= total_questions * 0.7:
            confidence_level = 'High'
        elif high_confidence_answers >= total_questions * 0.3:
            confidence_level = 'Medium'
        else:
            confidence_level = 'Low'
        
        return {
            'sources_quality': research_results['analysis_metadata']['sources_quality'],
            'data_completeness': round(completeness, 1),
            'confidence_level': confidence_level,
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'high_confidence_answers': high_confidence_answers
        }
    
    async def batch_research(self, subnets_data: List[Dict], max_concurrent: int = 3) -> List[Dict]:
        """
        Conduct research on multiple subnets with concurrency control
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def research_with_semaphore(subnet_data):
            async with semaphore:
                return await self.conduct_research(subnet_data)
        
        tasks = [research_with_semaphore(subnet) for subnet in subnets_data]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Research failed for subnet {subnets_data[i]['netuid']}: {result}")
                final_results.append({
                    'subnet_netuid': subnets_data[i]['netuid'],
                    'subnet_name': subnets_data[i]['name'],
                    'research_status': 'failed',
                    'error': str(result)
                })
            else:
                final_results.append(result)
        
        return final_results

# Testing function
async def test_research_agent():
    """Test the research agent with sample data"""
    # Note: Requires OPENAI_API_KEY environment variable
    if not os.getenv('OPENAI_API_KEY'):
        print("OPENAI_API_KEY not set - skipping test")
        return
    
    agent = ResearchAgent()
    
    # Sample subnet data
    sample_subnet = {
        'netuid': 64,
        'name': 'Chutes',
        'description': 'AI-powered content curation subnet',
        'sources': {
            'website': {
                'url': 'https://chutes.ai',
                'status': 'both'
            },
            'github': {
                'url': 'https://github.com/chutes-ai',
                'status': 'both'
            }
        },
        'website_raw': {
            'status': 'success',
            'title': 'Chutes - AI Content Curation',
            'description': 'Revolutionary AI-powered content curation platform',
            'clean_text': 'Chutes is building the future of content curation using advanced AI...'
        }
    }
    
    # Conduct research
    results = await agent.conduct_research(sample_subnet)
    
    print("=== RESEARCH AGENT TEST ===")
    print(f"Research Status: {results['research_status']}")
    print(f"Data Completeness: {results['analysis_metadata']['data_completeness']}%")
    print(f"Confidence Level: {results['analysis_metadata']['confidence_level']}")
    
    # Print sample answers
    if 'basic_info' in results['answers']:
        print("\nSample Basic Info Answers:")
        for key, answer in results['answers']['basic_info'].items():
            print(f"  {key}: {answer['answer'][:100]}...")

if __name__ == "__main__":
    asyncio.run(test_research_agent()) 