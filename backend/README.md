# Automated Bittensor Subnet Analysis Pipeline

A comprehensive automated system for collecting, verifying, and analyzing fundamental data across all Bittensor subnets. This pipeline provides objective metrics and AI-powered insights for investors and subnet owners.

## 🎯 Overview

This pipeline automates the complete research process for Bittensor subnets:

1. **Ingest Taostats Data** - Fetches metadata and source URLs from the Taostats API
2. **Verify & Complete Sources** - Crawls subnet websites to discover and verify all relevant links
3. **Normalize & Store** - Creates unified source objects with verification status flags
4. **Deep Research & Scoring** - Uses AI agents to extract structured answers and generate 1-5 scores
5. **Dashboard & Insights** - Surfaces objective and subjective data in a clean, interactive format

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMATED PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: TaoStats Ingestion                                   │
│  ├── TaoStatsAPI: Fetch all subnet metadata                    │
│  └── Output: phase_1_taostats_data.json                        │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: Source Verification                                  │
│  ├── SubnetWebsiteScraper: Crawl subnet websites               │
│  ├── SourceVerifier: Compare & flag sources                    │
│  └── Output: phase_2_verified_sources.json                     │
├─────────────────────────────────────────────────────────────────┤
│  Phase 3: Data Normalization                                   │
│  ├── Create unified source objects                             │
│  ├── Add verification metadata                                 │
│  └── Output: phase_3_normalized_data.json                      │
├─────────────────────────────────────────────────────────────────┤
│  Phase 4: AI Research & Scoring                                │
│  ├── ResearchAgent: Extract structured answers                 │
│  ├── ScoringAgent: Generate 1-5 scores per category            │
│  └── Output: phase_4_research_scores.json                      │
├─────────────────────────────────────────────────────────────────┤
│  Phase 5: Final Dataset Generation                             │
│  ├── Create dashboard-ready format                             │
│  ├── Calculate health metrics                                  │
│  └── Output: final_subnet_analysis.json                        │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (recommended for AI research & scoring)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key (optional but recommended):**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. **Run the test demo:**
   ```bash
   python test_pipeline.py
   ```

### Basic Usage

**Run the full pipeline for all subnets:**
```bash
python automated_pipeline.py
```

**Run for specific subnets:**
```bash
python automated_pipeline.py --subnets 1 5 11 19 27 64
```

**Specify custom output directory:**
```bash
python automated_pipeline.py --output-dir custom_results
```

## 📊 Source Verification System

The pipeline automatically compares sources from Taostats with those discovered on subnet websites, flagging each source as:

- **`both`** - Present in both Taostats and website (verified)
- **`taostats_only`** - Only in Taostats (potentially outdated)
- **`website_only`** - Only on website (missing from Taostats)

### Source Health Score

Each subnet gets a **Source Health Score** calculated as:
```
Health Score = (Verified Sources / Total Sources) × 100
```

## 🤖 AI Research System

### Research Categories

The AI Research Agent analyzes each subnet across 6 categories with 24 total questions:

1. **Basic Information** (4 questions)
   - Mission statement and goals
   - Problem being solved
   - Target audience
   - Unique value proposition

2. **Team & Leadership** (4 questions)
   - Team size and experience
   - Leadership credentials
   - Team transparency
   - Track record

3. **Product & Technology** (4 questions)
   - Product development status
   - Technical approach
   - Product differentiation
   - Scalability

4. **Business Model** (4 questions)
   - Revenue model
   - Market size
   - Competitive landscape
   - Partnerships

5. **Development & Progress** (4 questions)
   - Development activity
   - Roadmap clarity
   - Milestone achievement
   - Community engagement

6. **Risk Assessment** (4 questions)
   - Technical risks
   - Market risks
   - Regulatory risks
   - Team risks

### Research Quality Indicators

- **Data Completeness**: Percentage of questions answered
- **Confidence Level**: High/Medium/Low based on source quality
- **Source Quality**: Excellent/Good/Fair/Poor based on verified sources

## 📈 Scoring System

### Scoring Categories & Weights

The AI Scoring Agent evaluates subnets across 5 weighted categories:

1. **Team Strength** (25% weight)
   - Team quality, experience, transparency
   
2. **Product Viability** (25% weight)
   - Development status, technical feasibility
   
3. **Market Opportunity** (20% weight)
   - Market size, demand, competitive positioning
   
4. **Execution Progress** (15% weight)
   - Development activity, milestone achievement
   
5. **Risk Management** (15% weight)
   - Risk identification and mitigation

### Score Interpretation

- **5** - Excellent: Top tier subnet with strong fundamentals
- **4** - Good: Solid subnet with minor areas for improvement
- **3** - Average: Decent subnet with some concerns
- **2** - Below Average: Significant concerns but some potential
- **1** - Poor: Major red flags or insufficient information

### Investment Recommendations

Based on overall scores:
- **≥4.0**: Strong Buy - Excellent fundamentals
- **≥3.5**: Buy - Good investment potential
- **≥2.5**: Hold - Average performance, proceed with caution
- **≥2.0**: Weak Hold - Below average, significant concerns
- **<2.0**: Avoid - Major red flags

## 📁 Output Files

The pipeline generates structured output files for each phase:

### Phase 1: Taostats Data
```json
{
  "netuid": 64,
  "name": "Chutes",
  "description": "AI-powered content curation",
  "sources": {
    "github": "https://github.com/chutes-ai",
    "website": "https://chutes.ai",
    "discord": "https://discord.gg/chutes"
  }
}
```

### Phase 2: Verified Sources
```json
{
  "sources": {
    "github": {
      "url": "https://github.com/chutes-ai",
      "status": "both",
      "taostats_url": "https://github.com/chutes-ai",
      "website_urls": ["https://github.com/chutes-ai"],
      "match_confidence": 1.0
    }
  },
  "source_verification_summary": {
    "total_sources": 3,
    "both_sources": 2,
    "taostats_only": 1,
    "website_only": 0,
    "health_score": 66.7
  }
}
```

### Phase 4: Research & Scores
```json
{
  "research_results": {
    "answers": {
      "basic_info": {
        "mission_statement": {
          "question": "What is the subnet's mission statement?",
          "answer": "Chutes aims to revolutionize content curation...",
          "confidence": "High",
          "research_status": "completed"
        }
      }
    }
  },
  "scores": {
    "overall_score": 4.2,
    "category_scores": {
      "team_strength": {"score": 4, "weight": 25},
      "product_viability": {"score": 4, "weight": 25}
    },
    "investment_recommendation": "Buy - Good investment potential"
  }
}
```

### Final Dataset (Dashboard-Ready)
```json
{
  "netuid": 64,
  "name": "Chutes",
  "overall_score": 4.2,
  "investment_recommendation": "Buy",
  "source_health": {"health_score": 85.0},
  "primary_links": {
    "website": "https://chutes.ai",
    "github": "https://github.com/chutes-ai"
  },
  "risk_flags": [],
  "last_updated": "2024-01-15T10:30:00Z"
}
```

## ⚙️ Configuration

Copy `env_example.txt` to `.env` and customize:

```bash
# Required for AI features
OPENAI_API_KEY=your_openai_api_key_here

# Pipeline performance tuning
MAX_CONCURRENT_RESEARCH=3
MAX_CONCURRENT_SCORING=2
RATE_LIMIT_DELAY=1.0

# Output configuration
OUTPUT_DIR=pipeline_output
LOG_LEVEL=INFO
```

## 🔧 API Components

### TaoStatsAPI
```python
from subnets_basic_info import TaoStatsAPI

api = TaoStatsAPI()
subnets = api.get_all_subnets()
specific_subnet = api.get_subnet_by_id(64)
```

### SubnetWebsiteScraper
```python
from subnet_website_scraper import SubnetWebsiteScraper

scraper = SubnetWebsiteScraper()
website_data = scraper.scrape_subnet_website("https://chutes.ai", "Chutes")
```

### SourceVerifier
```python
from source_verifier import SourceVerifier

verifier = SourceVerifier()
verified_sources = verifier.verify_and_merge_sources(
    taostats_sources=taostats_data,
    website_data=scraped_data
)
```

### ResearchAgent
```python
from research_agent import ResearchAgent

agent = ResearchAgent()
research_results = await agent.conduct_research(subnet_data)
```

### ScoringAgent
```python
from scoring_agent import ScoringAgent

scorer = ScoringAgent()
scores = await scorer.generate_scores(subnet_data, research_results)
```

## 🚦 Error Handling

The pipeline includes comprehensive error handling:

- **Graceful degradation**: Components can fail without stopping the entire pipeline
- **Rate limiting**: Built-in delays to respect API limits
- **Retry logic**: Automatic retries for transient failures
- **Detailed logging**: Comprehensive logs for debugging
- **Status tracking**: Each subnet's processing status is tracked

## 📈 Performance

### Benchmarks
- **Full pipeline** (all subnets): ~2-4 hours depending on API rate limits
- **Website scraping**: ~1-2 seconds per subnet
- **AI research**: ~30-60 seconds per subnet (with GPT-4o-mini)
- **AI scoring**: ~15-30 seconds per subnet

### Optimization
- Concurrent processing with configurable limits
- Efficient caching and data persistence
- Minimal API calls through smart batching
- Progressive data saving (no data loss on interruption)

## 🔍 Monitoring

Monitor pipeline execution through:

1. **Console output**: Real-time progress updates
2. **Log files**: Detailed execution logs (`pipeline.log`)
3. **State tracking**: Pipeline state saved in results
4. **Output files**: Progressive data saving at each phase

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the output logs for error details
2. Verify your OpenAI API key is set correctly
3. Ensure all dependencies are installed
4. Run the test suite: `python test_pipeline.py`

## 🗺️ Roadmap

- [ ] **Enhanced scraping**: Support for more complex websites
- [ ] **Additional AI models**: Support for Anthropic Claude, local models
- [ ] **Real-time monitoring**: Web dashboard for pipeline status
- [ ] **Advanced scoring**: Machine learning-based scoring models
- [ ] **API endpoints**: REST API for on-demand analysis
- [ ] **Scheduled runs**: Automatic daily/weekly pipeline execution
- [ ] **Alert system**: Notifications for significant score changes 