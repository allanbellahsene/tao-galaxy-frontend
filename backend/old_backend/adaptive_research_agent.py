import openai
import json
import logging
from typing import Dict, List, Optional, Tuple
import time
import asyncio
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ResearchQuery:
    question: str
    priority: int
    context: str
    data_sources: List[str]
    confidence_required: float

class AdaptiveResearchAgent:
    """
    Research agent that adapts its approach based on available data and context
    """
    
    def __init__(self, openai_api_key: str):
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.max_retries = 3
        self.timeout = 30
    
    async def conduct_adaptive_research(self, subnet_data: Dict, research_goals: List[str]) -> Dict:
        """
        Conduct research that adapts to available data quality and sources
        """
        try:
            # Step 1: Analyze available data quality
            data_analysis = self._analyze_data_completeness(subnet_data)
            
            # Step 2: Generate adaptive research queries
            research_queries = self._generate_adaptive_queries(subnet_data, research_goals, data_analysis)
            
            # Step 3: Execute research with multiple strategies
            research_results = await self._execute_adaptive_research(research_queries, subnet_data)
            
            # Step 4: Synthesize final analysis
            final_analysis = self._synthesize_comprehensive_analysis(research_results, subnet_data)
            
            return final_analysis
            
        except Exception as e:
            logger.error(f"Adaptive research failed: {e}")
            return self._create_error_response(str(e))
    
    def _analyze_data_completeness(self, subnet_data: Dict) -> Dict:
        """
        Analyze the completeness and quality of available data
        """
        analysis = {
            'data_sources': [],
            'completeness_score': 0.0,
            'missing_data_categories': [],
            'high_confidence_areas': [],
            'research_strategy': 'comprehensive'
        }
        
        # Check available data sources
        if 'website' in subnet_data.get('data_sources', []):
            analysis['data_sources'].append('website')
        if 'github' in subnet_data.get('data_sources', []):
            analysis['data_sources'].append('github')
        if 'social_media' in subnet_data.get('data_sources', []):
            analysis['data_sources'].append('social_media')
        
        # Analyze team information completeness
        team_info = subnet_data.get('team_information', {})
        if team_info.get('estimated_size', 0) > 0:
            analysis['high_confidence_areas'].append('team_size')
            analysis['completeness_score'] += 0.3
        else:
            analysis['missing_data_categories'].append('team_information')
        
        if team_info.get('team_members'):
            analysis['high_confidence_areas'].append('team_members')
            analysis['completeness_score'] += 0.2
        
        # Analyze company information completeness
        company_info = subnet_data.get('company_information', {})
        if company_info.get('mission'):
            analysis['high_confidence_areas'].append('mission')
            analysis['completeness_score'] += 0.2
        else:
            analysis['missing_data_categories'].append('mission_statement')
        
        if company_info.get('technology_focus'):
            analysis['high_confidence_areas'].append('technology')
            analysis['completeness_score'] += 0.15
        
        # Determine research strategy based on data quality
        if analysis['completeness_score'] > 0.7:
            analysis['research_strategy'] = 'verification_focused'
        elif analysis['completeness_score'] > 0.4:
            analysis['research_strategy'] = 'gap_filling'
        else:
            analysis['research_strategy'] = 'comprehensive_discovery'
        
        return analysis
    
    def _generate_adaptive_queries(self, subnet_data: Dict, research_goals: List[str], 
                                 data_analysis: Dict) -> List[ResearchQuery]:
        """
        Generate research queries that adapt to available data
        """
        queries = []
        strategy = data_analysis['research_strategy']
        missing_categories = data_analysis['missing_data_categories']
        
        # Base queries for all subnets
        base_queries = [
            ResearchQuery(
                question="What is the core mission and value proposition of this project?",
                priority=1,
                context="fundamental_understanding",
                data_sources=["website", "github", "social_media"],
                confidence_required=0.7
            ),
            ResearchQuery(
                question="Who are the key team members and what are their backgrounds?",
                priority=1,
                context="team_analysis",
                data_sources=["website", "github", "linkedin"],
                confidence_required=0.6
            )
        ]
        
        # Adaptive queries based on strategy
        if strategy == 'comprehensive_discovery':
            queries.extend([
                ResearchQuery(
                    question="What evidence exists of an active development team?",
                    priority=2,
                    context="team_validation",
                    data_sources=["github", "website", "social_media"],
                    confidence_required=0.5
                ),
                ResearchQuery(
                    question="What are the main products or services offered?",
                    priority=2,
                    context="product_discovery",
                    data_sources=["website", "github"],
                    confidence_required=0.6
                ),
                ResearchQuery(
                    question="What is the company's development and business model?",
                    priority=3,
                    context="business_model",
                    data_sources=["website", "social_media"],
                    confidence_required=0.5
                )
            ])
        
        elif strategy == 'gap_filling':
            # Focus on missing data categories
            if 'team_information' in missing_categories:
                queries.append(ResearchQuery(
                    question="Find any indirect evidence of team size and composition through job postings, credits, or mentions",
                    priority=1,
                    context="team_inference",
                    data_sources=["website", "github", "search"],
                    confidence_required=0.4
                ))
            
            if 'mission_statement' in missing_categories:
                queries.append(ResearchQuery(
                    question="Infer the company's mission from their products, code, and communications",
                    priority=2,
                    context="mission_inference",
                    data_sources=["github", "website", "social_media"],
                    confidence_required=0.5
                ))
        
        elif strategy == 'verification_focused':
            # Verify and enrich existing data
            queries.extend([
                ResearchQuery(
                    question="Verify and expand on the known team information with additional details",
                    priority=1,
                    context="team_verification",
                    data_sources=["linkedin", "github", "website"],
                    confidence_required=0.8
                ),
                ResearchQuery(
                    question="What recent developments or milestones has the company achieved?",
                    priority=2,
                    context="recent_progress",
                    data_sources=["github", "social_media", "website"],
                    confidence_required=0.7
                )
            ])
        
        # Add goal-specific queries
        for goal in research_goals:
            if "team" in goal.lower():
                queries.append(ResearchQuery(
                    question=f"Specifically address: {goal}",
                    priority=1,
                    context="custom_goal",
                    data_sources=["website", "github", "social_media"],
                    confidence_required=0.6
                ))
        
        # Combine with base queries
        all_queries = base_queries + queries
        
        return sorted(all_queries, key=lambda x: x.priority)
    
    async def _execute_adaptive_research(self, queries: List[ResearchQuery], 
                                       subnet_data: Dict) -> Dict:
        """
        Execute research queries with adaptive approaches
        """
        results = {
            'query_results': {},
            'research_metadata': {
                'queries_attempted': len(queries),
                'queries_successful': 0,
                'total_confidence': 0.0,
                'research_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        for query in queries:
            try:
                logger.info(f"Executing query: {query.question[:50]}...")
                
                # Try multiple research approaches for each query
                query_result = await self._multi_approach_query(query, subnet_data)
                
                results['query_results'][query.question] = query_result
                
                if query_result.get('confidence', 0) >= query.confidence_required:
                    results['research_metadata']['queries_successful'] += 1
                    results['research_metadata']['total_confidence'] += query_result['confidence']
                
                # Brief delay between queries
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"Query failed: {query.question[:30]}... - {e}")
                results['query_results'][query.question] = {
                    'answer': 'Query execution failed',
                    'confidence': 0.0,
                    'error': str(e)
                }
        
        # Calculate average confidence
        successful_queries = results['research_metadata']['queries_successful']
        if successful_queries > 0:
            results['research_metadata']['average_confidence'] = (
                results['research_metadata']['total_confidence'] / successful_queries
            )
        else:
            results['research_metadata']['average_confidence'] = 0.0
        
        return results
    
    async def _multi_approach_query(self, query: ResearchQuery, subnet_data: Dict) -> Dict:
        """
        Execute a single query using multiple research approaches
        """
        approaches = [
            self._direct_data_analysis,
            self._inferential_analysis,
            self._cross_reference_analysis
        ]
        
        best_result = {
            'answer': 'No reliable information found',
            'confidence': 0.0,
            'approach_used': 'none',
            'evidence': []
        }
        
        for approach in approaches:
            try:
                result = await approach(query, subnet_data)
                
                if result.get('confidence', 0) > best_result['confidence']:
                    best_result = result
                    
                    # If we meet the confidence requirement, use this result
                    if result['confidence'] >= query.confidence_required:
                        break
                        
            except Exception as e:
                logger.warning(f"Research approach failed: {e}")
                continue
        
        return best_result
    
    async def _direct_data_analysis(self, query: ResearchQuery, subnet_data: Dict) -> Dict:
        """
        Direct analysis of available structured data
        """
        try:
            # Prepare context from available data
            context_data = self._prepare_data_context(subnet_data, query.data_sources)
            
            if not context_data.strip():
                return {
                    'answer': 'No relevant data available for direct analysis',
                    'confidence': 0.0,
                    'approach_used': 'direct_data_analysis',
                    'evidence': []
                }
            
            # Use AI to analyze the structured data
            analysis_prompt = f"""
            Analyze the following data to answer this specific question: "{query.question}"
            
            Context: {query.context}
            Available data:
            {context_data}
            
            Provide a detailed answer based ONLY on the available data. If the data doesn't support 
            a confident answer, clearly state the limitations.
            
            Respond in JSON format with:
            - answer: Your detailed response
            - confidence: Float 0-1 indicating how confident you are
            - evidence: List of specific data points that support your answer
            - limitations: Any limitations or gaps in the available data
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert research analyst. Provide thorough, evidence-based analysis while being honest about data limitations."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            result['approach_used'] = 'direct_data_analysis'
            
            return result
            
        except Exception as e:
            logger.error(f"Direct analysis failed: {e}")
            return {
                'answer': f'Direct analysis failed: {str(e)}',
                'confidence': 0.0,
                'approach_used': 'direct_data_analysis',
                'evidence': []
            }
    
    async def _inferential_analysis(self, query: ResearchQuery, subnet_data: Dict) -> Dict:
        """
        Inferential analysis to find answers through logical deduction
        """
        try:
            # Look for indirect indicators and patterns
            indirect_data = self._gather_indirect_evidence(subnet_data, query)
            
            if not indirect_data:
                return {
                    'answer': 'No indirect evidence available for inference',
                    'confidence': 0.0,
                    'approach_used': 'inferential_analysis',
                    'evidence': []
                }
            
            inference_prompt = f"""
            Use logical inference to answer: "{query.question}"
            
            You have these indirect indicators and patterns:
            {json.dumps(indirect_data, indent=2)}
            
            Use your reasoning skills to infer answers based on these indicators. For example:
            - Job postings can indicate team size and growth
            - GitHub activity patterns can indicate team activity
            - Technical complexity can indicate team expertise
            - Contact information patterns can indicate company structure
            
            Respond in JSON format with:
            - answer: Your inferred conclusion
            - confidence: Float 0-1 (typically lower for inference)
            - reasoning: Your logical reasoning process
            - evidence: Indirect indicators used
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at logical inference and pattern recognition. Draw reasonable conclusions from indirect evidence."},
                    {"role": "user", "content": inference_prompt}
                ],
                temperature=0.2
            )
            
            result = json.loads(response.choices[0].message.content)
            result['approach_used'] = 'inferential_analysis'
            
            return result
            
        except Exception as e:
            logger.error(f"Inferential analysis failed: {e}")
            return {
                'answer': f'Inferential analysis failed: {str(e)}',
                'confidence': 0.0,
                'approach_used': 'inferential_analysis',
                'evidence': []
            }
    
    async def _cross_reference_analysis(self, query: ResearchQuery, subnet_data: Dict) -> Dict:
        """
        Cross-reference multiple data sources to validate and enrich answers
        """
        try:
            # Gather data from multiple sources
            cross_ref_data = {}
            
            for source in query.data_sources:
                if source in subnet_data.get('data_sources', []):
                    cross_ref_data[source] = self._extract_source_data(subnet_data, source, query)
            
            if len(cross_ref_data) < 2:
                return {
                    'answer': 'Insufficient sources for cross-reference analysis',
                    'confidence': 0.0,
                    'approach_used': 'cross_reference_analysis',
                    'evidence': []
                }
            
            cross_ref_prompt = f"""
            Cross-reference these multiple data sources to answer: "{query.question}"
            
            Sources available:
            {json.dumps(cross_ref_data, indent=2)}
            
            Look for:
            1. Consistent information across sources (high confidence)
            2. Complementary information that fills gaps
            3. Contradictions that need reconciliation
            4. Unique insights from each source
            
            Respond in JSON format with:
            - answer: Synthesized answer from all sources
            - confidence: Float 0-1 (higher when sources agree)
            - source_agreement: How well sources align
            - evidence: Supporting evidence from each source
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert at synthesizing information from multiple sources to create comprehensive, validated answers."},
                    {"role": "user", "content": cross_ref_prompt}
                ],
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            result['approach_used'] = 'cross_reference_analysis'
            
            return result
            
        except Exception as e:
            logger.error(f"Cross-reference analysis failed: {e}")
            return {
                'answer': f'Cross-reference analysis failed: {str(e)}',
                'confidence': 0.0,
                'approach_used': 'cross_reference_analysis',
                'evidence': []
            }
    
    def _synthesize_comprehensive_analysis(self, research_results: Dict, subnet_data: Dict) -> Dict:
        """
        Synthesize all research results into a comprehensive final analysis
        """
        try:
            # Prepare synthesis data
            synthesis_data = {
                'original_data': subnet_data,
                'research_results': research_results,
                'metadata': research_results.get('research_metadata', {})
            }
            
            synthesis_prompt = f"""
            Create a comprehensive analysis report by synthesizing all research findings.
            
            Data available:
            {json.dumps(synthesis_data, indent=2)[:8000]}  # Limit for API
            
            Create a structured analysis covering:
            
            1. EXECUTIVE SUMMARY
               - Key findings about the project/team
               - Overall confidence level
               - Data quality assessment
            
            2. TEAM ANALYSIS
               - Team size and composition
               - Leadership information
               - Development activity
               - Confidence level and evidence quality
            
            3. COMPANY ANALYSIS
               - Mission and vision
               - Products and services
               - Business model
               - Technology focus
            
            4. DATA QUALITY REPORT
               - Sources used and their reliability
               - Information gaps identified
               - Confidence levels by category
               - Recommendations for further research
            
            5. CONCLUSIONS
               - Final assessment
               - Key risks or concerns
               - Investment/partnership considerations
            
            Respond in JSON format with detailed structured analysis.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a senior business analyst creating comprehensive research reports. Be thorough, objective, and honest about limitations."},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.1
            )
            
            final_analysis = json.loads(response.choices[0].message.content)
            
            # Add metadata
            final_analysis['analysis_metadata'] = {
                'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'research_queries_executed': research_results['research_metadata']['queries_attempted'],
                'successful_queries': research_results['research_metadata']['queries_successful'],
                'average_confidence': research_results['research_metadata'].get('average_confidence', 0.0),
                'data_sources_used': subnet_data.get('data_sources', [])
            }
            
            return final_analysis
            
        except Exception as e:
            logger.error(f"Analysis synthesis failed: {e}")
            return self._create_error_response(f"Synthesis failed: {str(e)}")
    
    # Helper methods
    def _prepare_data_context(self, subnet_data: Dict, allowed_sources: List[str]) -> str:
        """Prepare context data from specified sources"""
        context_parts = []
        
        for source in allowed_sources:
            if source == 'website' and 'website' in subnet_data.get('data_sources', []):
                website_data = subnet_data.get('enhanced_team_info', {})
                if website_data:
                    context_parts.append(f"Website data: {json.dumps(website_data)}")
            
            elif source == 'github' and 'github' in subnet_data.get('data_sources', []):
                github_data = subnet_data.get('team_information', {})
                if github_data:
                    context_parts.append(f"GitHub data: {json.dumps(github_data)}")
        
        return "\n\n".join(context_parts)
    
    def _gather_indirect_evidence(self, subnet_data: Dict, query: ResearchQuery) -> Dict:
        """Gather indirect evidence for inferential analysis"""
        evidence = {}
        
        # Add implementation for gathering indirect evidence
        # This would look for patterns, job postings, activity indicators, etc.
        
        return evidence
    
    def _extract_source_data(self, subnet_data: Dict, source: str, query: ResearchQuery) -> Dict:
        """Extract relevant data from a specific source"""
        if source == 'website':
            return subnet_data.get('enhanced_team_info', {})
        elif source == 'github':
            return subnet_data.get('team_information', {})
        elif source == 'social_media':
            return subnet_data.get('social_media', {})
        return {}
    
    def _create_error_response(self, error: str) -> Dict:
        """Create standardized error response"""
        return {
            'error': error,
            'status': 'failed',
            'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_metadata': {
                'research_queries_executed': 0,
                'successful_queries': 0,
                'average_confidence': 0.0
            }
        } 