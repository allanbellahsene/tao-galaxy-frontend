import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import openai
import os

logger = logging.getLogger(__name__)

class ScoringAgent:
    """
    AI-powered scoring agent that evaluates subnets based on research findings
    """
    
    def __init__(self, api_key: Optional[str] = None):
        # Initialize OpenAI client
        self.client = openai.AsyncOpenAI(
            api_key=api_key or os.getenv('OPENAI_API_KEY')
        )
        
        # Scoring categories and their criteria
        self.scoring_categories = {
            'team_strength': {
                'weight': 25,
                'description': 'Team quality, experience, and transparency',
                'criteria': [
                    'Team size and completeness',
                    'Leadership experience and credentials',
                    'Team transparency and public profiles',
                    'Track record of execution',
                    'Technical expertise alignment'
                ]
            },
            'product_viability': {
                'weight': 25,
                'description': 'Product development status and technical feasibility',
                'criteria': [
                    'Product development stage (concept to live)',
                    'Technical approach and innovation',
                    'Product differentiation and uniqueness',
                    'Scalability and technical architecture',
                    'User adoption evidence'
                ]
            },
            'market_opportunity': {
                'weight': 20,
                'description': 'Market size, demand, and competitive positioning',
                'criteria': [
                    'Target market size and growth potential',
                    'Market demand validation',
                    'Competitive landscape and positioning',
                    'Business model viability',
                    'Revenue potential and monetization'
                ]
            },
            'execution_progress': {
                'weight': 15,
                'description': 'Development activity and milestone achievement',
                'criteria': [
                    'Development activity and commits',
                    'Roadmap clarity and achievement',
                    'Community engagement and growth',
                    'Partnership development',
                    'Consistent progress demonstration'
                ]
            },
            'risk_management': {
                'weight': 15,
                'description': 'Risk assessment and mitigation strategies',
                'criteria': [
                    'Technical risk identification and mitigation',
                    'Market and competitive risks',
                    'Regulatory and compliance considerations',
                    'Team and operational risks',
                    'Financial sustainability'
                ]
            }
        }
        
        # Score interpretation guide
        self.score_guide = {
            5: "Excellent - Top tier subnet with strong fundamentals",
            4: "Good - Solid subnet with minor areas for improvement",
            3: "Average - Decent subnet with some concerns",
            2: "Below Average - Significant concerns but some potential",
            1: "Poor - Major red flags or insufficient information"
        }
    
    async def generate_scores(self, subnet_data: Dict, research_results: Dict) -> Dict:
        """
        Generate comprehensive scores for a subnet based on research results
        """
        logger.info(f"Starting scoring for subnet {subnet_data['netuid']}: {subnet_data['name']}")
        
        scoring_results = {
            'subnet_netuid': subnet_data['netuid'],
            'subnet_name': subnet_data['name'],
            'scoring_timestamp': datetime.now().isoformat(),
            'scoring_status': 'in_progress',
            'category_scores': {},
            'overall_score': 0.0,
            'risk_flags': [],
            'strengths': [],
            'weaknesses': [],
            'investment_recommendation': '',
            'confidence_level': 'unknown',
            'metadata': {
                'research_quality': research_results.get('analysis_metadata', {}).get('confidence_level', 'unknown'),
                'data_completeness': research_results.get('analysis_metadata', {}).get('data_completeness', 0)
            }
        }
        
        try:
            # Score each category
            for category, config in self.scoring_categories.items():
                logger.info(f"Scoring {category} for subnet {subnet_data['netuid']}")
                
                category_score = await self._score_category(
                    category,
                    config,
                    subnet_data,
                    research_results
                )
                
                scoring_results['category_scores'][category] = category_score
                
                # Brief pause between scoring calls
                await asyncio.sleep(0.3)
            
            # Calculate overall score and recommendations
            scoring_results = await self._finalize_scores(scoring_results, subnet_data, research_results)
            scoring_results['scoring_status'] = 'completed'
            
            logger.info(f"Scoring completed for subnet {subnet_data['netuid']} - Overall: {scoring_results['overall_score']}")
            
        except Exception as e:
            logger.error(f"Scoring failed for subnet {subnet_data['netuid']}: {e}")
            scoring_results['scoring_status'] = 'failed'
            scoring_results['error'] = str(e)
        
        return scoring_results
    
    async def _score_category(self, category: str, config: Dict, subnet_data: Dict, research_results: Dict) -> Dict:
        """
        Score a specific category using AI analysis
        """
        # Prepare scoring context
        context = self._prepare_scoring_context(category, subnet_data, research_results)
        
        # Create scoring prompt
        system_prompt = f"""You are an expert investment analyst specializing in blockchain and AI projects. You are scoring the "{category}" aspect of the Bittensor subnet "{subnet_data['name']}".

SCORING CRITERIA FOR {category.upper()}:
{config['description']}

Key evaluation criteria:
{chr(10).join([f"- {criterion}" for criterion in config['criteria']])}

SCORING SCALE:
5 = Excellent - Top tier performance, strong fundamentals
4 = Good - Solid performance with minor areas for improvement  
3 = Average - Decent performance with some concerns
2 = Below Average - Significant concerns but some potential
1 = Poor - Major red flags or insufficient information

INSTRUCTIONS:
1. Analyze the provided research data carefully
2. Evaluate against the specific criteria for this category
3. Assign a score from 1-5 based on the evidence
4. Provide 2-3 specific reasons for the score
5. Identify any red flags or notable strengths
6. Be objective and evidence-based

RESEARCH DATA:
{context}

Please provide:
1. Score (1-5)
2. Reasoning (3-5 bullet points)
3. Key strengths (if any)
4. Concerns/weaknesses (if any)
5. Confidence level (High/Medium/Low)"""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Please score the {category} category for {subnet_data['name']} based on the research data provided."}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_category_score(ai_response, category, config['weight'])
            
        except Exception as e:
            logger.error(f"AI scoring failed for category {category}: {e}")
            return {
                'category': category,
                'score': 1,
                'weight': config['weight'],
                'weighted_score': config['weight'] * 1,
                'reasoning': [f"Scoring failed: {str(e)}"],
                'strengths': [],
                'concerns': ['Unable to complete scoring due to technical error'],
                'confidence': 'Low',
                'status': 'error'
            }
    
    def _prepare_scoring_context(self, category: str, subnet_data: Dict, research_results: Dict) -> str:
        """
        Prepare relevant context for scoring a specific category
        """
        context_parts = []
        
        # Basic subnet info
        context_parts.append(f"SUBNET: {subnet_data['name']} (NetUID: {subnet_data['netuid']})")
        context_parts.append(f"DESCRIPTION: {subnet_data.get('description', 'No description')}")
        
        # Research answers relevant to this category
        if research_results.get('answers'):
            relevant_categories = self._get_relevant_research_categories(category)
            
            for research_category in relevant_categories:
                if research_category in research_results['answers']:
                    context_parts.append(f"\n{research_category.upper()} RESEARCH:")
                    
                    for question_key, answer_data in research_results['answers'][research_category].items():
                        if answer_data.get('research_status') == 'completed':
                            context_parts.append(f"- {answer_data['question']}")
                            context_parts.append(f"  Answer: {answer_data['answer']}")
                            context_parts.append(f"  Confidence: {answer_data['confidence']}")
        
        # Source quality information
        sources_summary = research_results.get('sources_analyzed', {})
        context_parts.append(f"\nSOURCE QUALITY:")
        context_parts.append(f"- Total sources: {sources_summary.get('total_sources', 0)}")
        context_parts.append(f"- Verified sources: {sources_summary.get('verified_sources', 0)}")
        context_parts.append(f"- Website scraped: {sources_summary.get('website_scraped', False)}")
        
        # Research metadata
        metadata = research_results.get('analysis_metadata', {})
        context_parts.append(f"- Research confidence: {metadata.get('confidence_level', 'unknown')}")
        context_parts.append(f"- Data completeness: {metadata.get('data_completeness', 0)}%")
        
        return "\n".join(context_parts)
    
    def _get_relevant_research_categories(self, scoring_category: str) -> List[str]:
        """
        Map scoring categories to relevant research categories
        """
        mapping = {
            'team_strength': ['team', 'basic_info'],
            'product_viability': ['product', 'basic_info', 'development'],
            'market_opportunity': ['business', 'basic_info'],
            'execution_progress': ['development', 'team'],
            'risk_management': ['risks', 'team', 'business']
        }
        
        return mapping.get(scoring_category, ['basic_info'])
    
    def _parse_category_score(self, ai_response: str, category: str, weight: int) -> Dict:
        """
        Parse AI response into structured category score
        """
        # Extract score using regex
        import re
        
        # Look for score patterns
        score_patterns = [
            r'Score:?\s*(\d)',
            r'score\s*is\s*(\d)',
            r'rating:?\s*(\d)',
            r'(\d)/5',
            r'(\d)\s*out\s*of\s*5'
        ]
        
        score = 3  # Default fallback
        for pattern in score_patterns:
            match = re.search(pattern, ai_response, re.IGNORECASE)
            if match:
                try:
                    score = int(match.group(1))
                    if 1 <= score <= 5:
                        break
                except ValueError:
                    continue
        
        # Extract reasoning (look for bullet points or numbered lists)
        reasoning = []
        lines = ai_response.split('\n')
        for line in lines:
            line = line.strip()
            if (line.startswith('-') or line.startswith('•') or 
                re.match(r'^\d+\.', line) or 'because' in line.lower()):
                reasoning.append(line.lstrip('-•0123456789. '))
        
        # Extract strengths and concerns
        strengths = []
        concerns = []
        
        current_section = None
        for line in lines:
            line = line.strip().lower()
            if 'strength' in line or 'positive' in line or 'advantage' in line:
                current_section = 'strengths'
            elif 'concern' in line or 'weakness' in line or 'risk' in line or 'negative' in line:
                current_section = 'concerns'
            elif current_section and (line.startswith('-') or line.startswith('•')):
                content = line.lstrip('-•').strip()
                if current_section == 'strengths':
                    strengths.append(content)
                elif current_section == 'concerns':
                    concerns.append(content)
        
        # Extract confidence
        confidence = 'Medium'  # Default
        if 'high confidence' in ai_response.lower():
            confidence = 'High'
        elif 'low confidence' in ai_response.lower() or 'uncertain' in ai_response.lower():
            confidence = 'Low'
        
        return {
            'category': category,
            'score': score,
            'weight': weight,
            'weighted_score': weight * score,
            'reasoning': reasoning[:5] if reasoning else [f"Limited information available for {category} assessment"],
            'strengths': strengths[:3],
            'concerns': concerns[:3],
            'confidence': confidence,
            'status': 'completed',
            'raw_response': ai_response
        }
    
    async def _finalize_scores(self, scoring_results: Dict, subnet_data: Dict, research_results: Dict) -> Dict:
        """
        Calculate final scores and generate overall recommendation
        """
        # Calculate weighted overall score
        total_weighted_score = 0
        total_weight = 0
        
        for category_data in scoring_results['category_scores'].values():
            if category_data.get('status') == 'completed':
                total_weighted_score += category_data['weighted_score']
                total_weight += category_data['weight']
        
        if total_weight > 0:
            scoring_results['overall_score'] = round(total_weighted_score / total_weight, 1)
        else:
            scoring_results['overall_score'] = 1.0
        
        # Collect strengths, weaknesses, and risk flags
        all_strengths = []
        all_concerns = []
        risk_flags = []
        
        for category_data in scoring_results['category_scores'].values():
            all_strengths.extend(category_data.get('strengths', []))
            all_concerns.extend(category_data.get('concerns', []))
            
            # Flag categories with scores <= 2 as risks
            if category_data.get('score', 3) <= 2:
                risk_flags.append(f"Low score in {category_data['category']}: {category_data['score']}/5")
        
        scoring_results['strengths'] = list(set(all_strengths))[:5]  # Top 5 unique strengths
        scoring_results['weaknesses'] = list(set(all_concerns))[:5]  # Top 5 unique concerns
        scoring_results['risk_flags'] = risk_flags
        
        # Generate investment recommendation
        overall_score = scoring_results['overall_score']
        
        if overall_score >= 4.0:
            recommendation = "Strong Buy - Excellent fundamentals across multiple areas"
        elif overall_score >= 3.5:
            recommendation = "Buy - Good investment potential with solid fundamentals"
        elif overall_score >= 2.5:
            recommendation = "Hold - Average performance, proceed with caution"
        elif overall_score >= 2.0:
            recommendation = "Weak Hold - Below average, significant concerns"
        else:
            recommendation = "Avoid - Major red flags or insufficient information"
        
        scoring_results['investment_recommendation'] = recommendation
        
        # Determine confidence level based on research quality
        research_confidence = research_results.get('analysis_metadata', {}).get('confidence_level', 'Low')
        data_completeness = research_results.get('analysis_metadata', {}).get('data_completeness', 0)
        
        if research_confidence == 'High' and data_completeness >= 70:
            confidence = 'High'
        elif research_confidence in ['High', 'Medium'] and data_completeness >= 50:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        scoring_results['confidence_level'] = confidence
        
        return scoring_results
    
    async def batch_scoring(self, subnets_with_research: List[Tuple[Dict, Dict]], max_concurrent: int = 2) -> List[Dict]:
        """
        Score multiple subnets with concurrency control
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def score_with_semaphore(subnet_data, research_results):
            async with semaphore:
                return await self.generate_scores(subnet_data, research_results)
        
        tasks = [score_with_semaphore(subnet, research) for subnet, research in subnets_with_research]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                subnet_data = subnets_with_research[i][0]
                logger.error(f"Scoring failed for subnet {subnet_data['netuid']}: {result}")
                final_results.append({
                    'subnet_netuid': subnet_data['netuid'],
                    'subnet_name': subnet_data['name'],
                    'scoring_status': 'failed',
                    'error': str(result),
                    'overall_score': 1.0
                })
            else:
                final_results.append(result)
        
        return final_results
    
    def generate_scoring_summary(self, all_scores: List[Dict]) -> Dict:
        """
        Generate summary statistics for all scored subnets
        """
        if not all_scores:
            return {'error': 'No scores to analyze'}
        
        # Filter successful scores
        successful_scores = [s for s in all_scores if s.get('scoring_status') == 'completed']
        
        if not successful_scores:
            return {'error': 'No successful scores to analyze'}
        
        # Calculate statistics
        overall_scores = [s['overall_score'] for s in successful_scores]
        
        summary = {
            'total_subnets_scored': len(successful_scores),
            'average_score': round(sum(overall_scores) / len(overall_scores), 2),
            'highest_score': max(overall_scores),
            'lowest_score': min(overall_scores),
            'score_distribution': {
                'excellent_4_5': len([s for s in overall_scores if s >= 4.0]),
                'good_3_4': len([s for s in overall_scores if 3.0 <= s < 4.0]),
                'average_2_3': len([s for s in overall_scores if 2.0 <= s < 3.0]),
                'poor_1_2': len([s for s in overall_scores if s < 2.0])
            },
            'top_subnets': sorted(successful_scores, key=lambda x: x['overall_score'], reverse=True)[:5],
            'high_risk_subnets': [s for s in successful_scores if len(s.get('risk_flags', [])) >= 2]
        }
        
        return summary

# Testing function
async def test_scoring_agent():
    """Test the scoring agent with sample data"""
    if not os.getenv('OPENAI_API_KEY'):
        print("OPENAI_API_KEY not set - skipping test")
        return
    
    agent = ScoringAgent()
    
    # Sample subnet and research data
    sample_subnet = {
        'netuid': 64,
        'name': 'Chutes',
        'description': 'AI-powered content curation subnet'
    }
    
    sample_research = {
        'research_status': 'completed',
        'answers': {
            'basic_info': {
                'mission_statement': {
                    'answer': 'Chutes aims to revolutionize content curation using AI',
                    'confidence': 'High',
                    'research_status': 'completed'
                }
            },
            'team': {
                'team_size': {
                    'answer': 'Team consists of 5 core members with AI/ML expertise',
                    'confidence': 'Medium',
                    'research_status': 'completed'
                }
            }
        },
        'analysis_metadata': {
            'confidence_level': 'Medium',
            'data_completeness': 75
        },
        'sources_analyzed': {
            'total_sources': 3,
            'verified_sources': 2,
            'website_scraped': True
        }
    }
    
    # Generate scores
    scores = await agent.generate_scores(sample_subnet, sample_research)
    
    print("=== SCORING AGENT TEST ===")
    print(f"Overall Score: {scores['overall_score']}/5")
    print(f"Recommendation: {scores['investment_recommendation']}")
    print(f"Confidence: {scores['confidence_level']}")
    
    if scores['category_scores']:
        print("\nCategory Scores:")
        for category, data in scores['category_scores'].items():
            print(f"  {category}: {data['score']}/5")

if __name__ == "__main__":
    asyncio.run(test_scoring_agent()) 