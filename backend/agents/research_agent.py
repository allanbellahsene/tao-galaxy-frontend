import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from pathlib import Path
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class TaoGalaxyResearchAgent:
    """
    TAO Galaxy Research Agent - Execution Engine
    
    Loads instructions and context from markdown files and executes research workflow.
    All detailed instructions are maintained in context_data/global/research_agent_instructions.md
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Fix the path - go up to root directory, then to context_data/global
        self.context_dir = Path(__file__).parent.parent.parent / "context_data" / "global"
        
        # Load instructions and context at initialization
        self.instructions = self._load_instructions()
        self.global_context = self._load_global_context()
    
    def _load_instructions(self) -> str:
        """Load research agent instructions from markdown file"""
        instructions_path = self.context_dir / "research_agent_instructions.md"
        if not instructions_path.exists():
            raise FileNotFoundError(f"Instructions file not found: {instructions_path}")
        
        with open(instructions_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_global_context(self) -> Dict[str, str]:
        """Load the unified global context document"""
        context_file = "tao_galaxy_core_context.md"
        file_path = self.context_dir / context_file

        context = {}
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                context[context_file] = f.read()
        else:
            logger.warning(f"Context file not found: {context_file}")
        
        return context
    
    async def research_subnet(self, subnet_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute research for a single subnet following the instructions
        
        Args:
            subnet_data: Dict containing subnet name, id, website, github, etc.
            
        Returns:
            Dict with research results in the format specified in instructions
        """
        
        # Build the research prompt using loaded instructions and context
        research_prompt = self._build_research_prompt(subnet_data)
        
        try:
            response = await self._execute_research_with_ai(research_prompt)
            result = self._parse_research_response(response, subnet_data)
            
            logger.info(f"Research completed for subnet {subnet_data.get('name', 'Unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Research failed for subnet {subnet_data.get('name', 'Unknown')}: {e}")
            return self._create_error_result(subnet_data, str(e))
    
    def _build_research_prompt(self, subnet_data: Dict[str, Any]) -> str:
        """Build the complete research prompt using loaded instructions and context"""
        
        # Extract subnet info
        subnet_name = subnet_data.get('name', 'Unknown')
        subnet_id = subnet_data.get('netuid', 'Unknown')
        website = subnet_data.get('website', '')
        github = subnet_data.get('github', '')
        twitter = subnet_data.get('twitter', '')
        discord = subnet_data.get('discord', '')
        description = subnet_data.get('description', '')
        
        prompt = f"""You are the TAO Galaxy Research Agent conducting deep research on Bittensor subnets. Use your advanced reasoning capabilities to thoroughly research and analyze the provided subnet information.

## RESEARCH TASK

I need you to conduct comprehensive research on the "{subnet_name}" subnet (ID: {subnet_id}) in the Bittensor ecosystem. You should use all available information sources and your reasoning capabilities to provide detailed, accurate answers.

## RESEARCH INSTRUCTIONS

{self.instructions}

## BACKGROUND CONTEXT

Here is essential background about the Bittensor ecosystem and TAO Galaxy strategy:

"""
        
        # Add global context documents with more context
        for filename, content in self.global_context.items():
            prompt += f"\n### {filename}:\n{content[:3000]}...\n"  # More context for o1
        
        prompt += f"""

## SUBNET TO RESEARCH

**Name:** {subnet_name}
**Subnet ID:** {subnet_id}
**Description:** {description}
**Official Website:** {website}
**GitHub Repository:** {github}
**Twitter/X:** {twitter}
**Discord:** {discord}

## RESEARCH METHODOLOGY

Please conduct thorough research using the following approach:

1. **Deep Analysis**: Use your reasoning capabilities to analyze the provided links and information
2. **Cross-Reference**: Compare information across different sources for consistency
3. **Inferential Reasoning**: Draw reasonable conclusions from available evidence
4. **Comprehensive Coverage**: Address ALL research questions systematically

## SPECIFIC RESEARCH TARGETS

Based on the provided links, please investigate:
- {website} - Official website content and announcements
- {github} - Code repository, documentation, activity levels, contributors
- {twitter} - Social media presence, updates, community engagement
- {discord} - Community discussions and team activity (if accessible)

## OUTPUT REQUIREMENTS

For each of the 10 research questions, provide a detailed JSON response with:
- Comprehensive answers based on your research
- High confidence scores when you find solid evidence
- Specific sources and citations
- Only use "Data not available" when absolutely no relevant information exists

Please conduct this research thoroughly and provide detailed findings for each question category. Use your advanced reasoning to make informed conclusions based on available evidence.

IMPORTANT: This is for investment and strategic analysis purposes, so accuracy and completeness are critical.
"""
        
        return prompt
    
    async def _execute_research_with_ai(self, prompt: str) -> str:
        """Execute research using OpenAI's deep research model"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using OpenAI's deep research model for thorough analysis
                messages=[
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                # Note: o1 models don't support system messages or temperature settings
                max_completion_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _parse_research_response(self, response: str, subnet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        
        return {
            "subnet_id": subnet_data.get('netuid'),
            "subnet_name": subnet_data.get('name'),
            "research_date": datetime.now().isoformat(),
            "research_results": response,  # For now, store raw response
            "metadata": {
                "instructions_version": "v1",
                "global_context_files": list(self.global_context.keys()),
                "source_priority_followed": True
            }
        }
    
    def _create_error_result(self, subnet_data: Dict[str, Any], error_msg: str) -> Dict[str, Any]:
        """Create error result structure"""
        return {
            "subnet_id": subnet_data.get('netuid'),
            "subnet_name": subnet_data.get('name'),
            "research_date": datetime.now().isoformat(),
            "error": error_msg,
            "research_results": None
        }
    
    async def research_multiple_subnets(self, subnets_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Research multiple subnets with rate limiting"""
        results = []
        
        for i, subnet_data in enumerate(subnets_data):
            logger.info(f"Researching subnet {i+1}/{len(subnets_data)}: {subnet_data.get('name', 'Unknown')}")
            
            result = await self.research_subnet(subnet_data)
            results.append(result)
            
            # Rate limiting - adjust as needed
            if i < len(subnets_data) - 1:
                await asyncio.sleep(2)  # 2 second delay between requests
        
        return results

# Usage example
async def main():
    """Example usage"""
    agent = TaoGalaxyResearchAgent()
    
    # Example subnet data
    subnet_data = {
        "name": "My Subnet",
        "netuid": 1,
        "website": "https://example.com",
        "github": "https://github.com/example/repo"
    }
    
    result = await agent.research_subnet(subnet_data)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 