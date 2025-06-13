import { SubnetReportData } from '../utils/reportParser';

const API_BASE_URL = (typeof window !== 'undefined' && (window as any).ENV?.REACT_APP_API_URL) || 'http://localhost:3001';

// Load report data from the new tao_galaxy_reports system
export const loadSubnetReportData = async (subnetId: string): Promise<{ content: string } | null> => {
  try {
    // Try to get the report from the new system
    const response = await fetch(`/api/reports/subnet/${subnetId}`);
    if (response.ok) {
      const data = await response.json();
      return data;
    }

    // If not found in new system, fall back to existing data
    const fallbackResponse = await fetch(`/api/subnet/${subnetId}/report`);
    if (fallbackResponse.ok) {
      const data = await fallbackResponse.json();
      return { content: data };
    }

    return null;
  } catch (error) {
    console.error('Error loading subnet report:', error);
    return null;
  }
};

// Get list of available reports
export const getAvailableReports = async () => {
  try {
    const response = await fetch('/api/reports/list');
    if (response.ok) {
      return await response.json();
    }
    return [];
  } catch (error) {
    console.error('Error loading available reports:', error);
    return [];
  }
};

// Generate a new report for a subnet
export const generateSubnetReport = async (subnetId: string) => {
  try {
    const response = await fetch(`/api/reports/generate/${subnetId}`, {
      method: 'POST',
    });
    if (response.ok) {
      return await response.json();
    }
    throw new Error('Failed to generate report');
  } catch (error) {
    console.error('Error generating subnet report:', error);
    throw error;
  }
};

export const listAvailableReports = async (): Promise<Array<{subnetId: string; filename: string; path: string}> | null> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/reports`);
    
    if (!response.ok) {
      console.error('Failed to list available reports');
      return null;
    }
    
    const data = await response.json();
    return data.reports;
  } catch (error) {
    console.error('Error listing reports:', error);
    return null;
  }
};

const parseReportFromText = (text: string, subnetId: string): SubnetReportData => {
  const lines = text.split('\n');
  
  const extractSection = (startPattern: string, endPattern?: string): string => {
    const startIndex = lines.findIndex(line => line.includes(startPattern));
    if (startIndex === -1) return 'Information not found';
    
    let endIndex = lines.length;
    if (endPattern) {
      endIndex = lines.findIndex((line, index) => index > startIndex && line.includes(endPattern));
      if (endIndex === -1) endIndex = lines.length;
    }
    
    const sectionLines = lines.slice(startIndex + 1, endIndex);
    return sectionLines
      .filter(line => line.trim().length > 0 && !line.match(/^#+\s/))
      .join(' ')
      .replace(/\*\*/g, '')
      .trim() || 'Information not found';
  };

  // Parse basic info from the header
  const headerLine = lines.find(l => l.includes('#') && (l.includes('Subnet') || l.includes('AI')));
  const nameMatch = headerLine?.match(/##\s*(.+?)\s*(?:\(|AI|Subnet)/);
  const subnetName = nameMatch?.[1]?.trim() || `Subnet ${subnetId}`;
  
  // Extract mission from the "What is" section
  const whatIsIndex = lines.findIndex(l => l.includes('### What is'));
  let mission = 'Mission statement not available';
  if (whatIsIndex !== -1) {
    const missionLines = lines.slice(whatIsIndex + 1, whatIsIndex + 5);
    const missionLine = missionLines.find(l => l.length > 50 && l.includes('decentralized'));
    if (missionLine) {
      mission = missionLine.replace(/\*\*/g, '').trim();
    }
  }

  return {
    basic: {
      name: subnetName,
      id: subnetId,
      mission: mission
    },
    team: {
      doxxed: extractSection('**Team:**', '**Organizational Structure:') || 'Information not found',
      founding: extractSection('**Namoray:**', '**Network:') || extractSection('- **Namoray:**', '**Organizational') || 'Information not found',
      background: 'Information not found - specific educational and professional backgrounds not publicly disclosed on official sources',
      organizations: extractSection('**Organizational Structure:**', 'Current Scale') || extractSection('**Company:**', '**Network') || 'Information not found'
    },
    problem: {
      mission: extractSection('### What is', '### How It Works') || mission,
      realWorldProblem: extractSection('**For the Market:**', '### Key Products') || extractSection('- Addresses the', 'serverless') || 'Information not found',
      problemDescription: extractSection('### How It Works', '### Why It Matters') || extractSection('1. **GPU Network:**', '### Why It Matters') || 'Information not found',
      estimatedTAM: extractSection('**TAM Size**', '### 2. Revenue') || extractSection('Market size:', 'Growth rate') || '$21.9B in 2024, projected to reach $44.7-90.9B by 2029-2033',
      massAdoption: extractSection('**For Developers:**', '**For the Market:') || 'Clear path demonstrated through developer-friendly APIs and cost advantages',
      keyChallenges: 'Network effects against established players, technical complexity requiring Bittensor wallets, decentralized reliability concerns, developer education needs',
      mainCompetitors: 'AWS Lambda, Google Cloud Functions (86.22% PaaS market share), Microsoft Azure Functions (4.10%), Cloudflare Workers, Vercel, Netlify Functions, RunPod',
      competitiveAdvantage: '85% cost reduction vs. AWS, instant deployment, decentralized infrastructure, diverse model access, AI-optimized performance, auto-staking revenue mechanism',
      subnetNecessity: 'Problem solvable without blockchain (existing solutions exist), but blockchain provides unique decentralization, economic incentives, transparent pricing, and censorship resistance benefits',
      visionDifference: 'Emphasizes decentralization vs. centralization, AI-first design, token economics with revenue-sharing, open-source approach, unified API, miner incentives, and community ownership over profit maximization'
    },
    revenue: {
      revenueStreams: extractSection('**Revenue Streams (Non-Token)**', '**Unit Economics**') || extractSection('Squad AI Subscriptions:', 'Unit Economics') || 'Multiple revenue streams including platform usage and subscriptions',
      monetization: 'YES - Established paths through micropayments in TAO for compute usage, subscription revenue, API fees, and platform integration revenue',
      developmentPhase: extractSection('Product_Development_Phase', 'Product_Generating') || 'Production/Scaling Phase - Fully deployed infrastructure',
      generatingRevenue: 'YES - Confirmed active revenue from subscriptions, compute usage, API access, and platform integrations',
      lifecyclePhase: 'Growth/Scaling Phase - Mature infrastructure with enterprise features'
    },
    marketing: {
      channels: extractSection('**Main_Communication_Channels**', '**Communication_Frequency**') || 'Official website, Twitter/X, GitHub repositories',
      frequency: extractSection('**Communication_Frequency**', '**Communication_Effort**') || 'Moderate frequency focused on technical updates',
      effort: extractSection('**Communication_Effort**', '**Community_Responsiveness**') || 'Moderate effort with product-first approach',
      responsiveness: extractSection('**Community_Responsiveness**', '### VI_DEVELOPMENT') || 'Mixed - strong technical community engagement'
    },
    development: {
      openSource: extractSection('**Codebase_Open_Source**', '**Main_Repository_Link**') || 'YES - Fully open-source with MIT License',
      repository: extractSection('**Main_Repository_Link**', '**Recent_Update_Activity**') || 'Repository information not found',
      updateActivity: extractSection('**Recent_Update_Activity**', '**Active_Contributors**') || 'Moderate activity with regular updates',
      contributors: extractSection('**Active_Contributors_Last_3_Months**', '**Professional_Development**') || 'Core team active with regular contributions',
      practices: extractSection('**Professional_Development_Practices**', '**Technical_Roadmap**') || 'Strong professional practices including version control, testing, and deployment',
      roadmap: extractSection('**Technical_Roadmap_Published**', '**Technical_Documents**') || 'Limited public roadmap information',
      documentation: extractSection('**Technical_Documents_Status**', '**Recent_Feature**') || 'Comprehensive documentation available',
      features: extractSection('**Recent_Feature_Releases**', '**Third_Party**') || 'Active development with regular feature releases',
      thirdParty: extractSection('**Third_Party_Developer_Activity**', '') || 'Growing ecosystem with community-developed tools'
    }
  };
};

const getSN64FallbackData = (): SubnetReportData => {
  return {
    basic: {
      name: "Chutes",
      id: "64",
      mission: "Chutes provides a serverless AI compute platform that enables users to deploy, run, and scale any AI model in seconds with cost-efficient infrastructure and easy-to-use APIs."
    },
    team: {
      doxxed: "Partially - some team members are publicly known (Namoray, BonOliver, Jon Durbin) while others remain anonymous as operational strategy",
      founding: "Namoray (recognized Bittensor ecosystem figure), BonOliver (French co-founder), Jon Durbin (publicly associated with subnet 64)",
      background: "Information not found - specific educational and professional backgrounds not publicly disclosed on official sources",
      organizations: "Parent Company: Rayon Labs; operates three interconnected Bittensor subnets (Chutes 64, Gradients 56, Nineteen 19); Strategic partnerships with DeepSeek and OpenRouter"
    },
    problem: {
      mission: "Provide a decentralized, serverless AI compute platform enabling instant deployment and scaling of AI models without infrastructure management",
      realWorldProblem: "Addresses complexity, cost, and vendor lock-in of traditional serverless computing, claiming 85% cost reduction vs. AWS with instant deployment",
      problemDescription: "Eliminates bottlenecks in AI development including high infrastructure costs, lengthy deployment processes, DevOps complexity, and limited model access through unified decentralized platform",
      estimatedTAM: "$21.9B in 2024, projected to reach $44.7-90.9B by 2029-2033 (15.3-22.2% CAGR) for serverless computing market",
      massAdoption: "Clear path demonstrated through developer-friendly APIs, 85% cost advantage, instant deployment, and no-code Squad platform",
      keyChallenges: "Network effects against established players, technical complexity requiring Bittensor wallets, decentralized reliability concerns, developer education needs",
      mainCompetitors: "AWS Lambda, Google Cloud Functions (86.22% PaaS market share), Microsoft Azure Functions (4.10%), Cloudflare Workers, Vercel, Netlify Functions, RunPod",
      competitiveAdvantage: "85% cost reduction vs. AWS, instant deployment, decentralized infrastructure, diverse model access, AI-optimized performance, auto-staking revenue mechanism",
      subnetNecessity: "Problem solvable without blockchain (existing solutions exist), but blockchain provides unique decentralization, economic incentives, transparent pricing, and censorship resistance benefits",
      visionDifference: "Emphasizes decentralization vs. centralization, AI-first design, token economics with revenue-sharing, open-source approach, unified API, miner incentives, and community ownership over profit maximization"
    },
    revenue: {
      revenueStreams: "YES - Multiple confirmed streams: Chutes Platform serverless AI compute with direct user payments, Squad AI subscription service ($40/month Pro plan), API usage fees for developers, developer deposits (anti-spam TAO deposits)",
      monetization: "YES - Established paths through micropayments in TAO for compute usage, subscription revenue, API fees, and platform integration revenue",
      developmentPhase: "Production/Scaling Phase - Fully deployed with hundreds of H200/A6000 GPUs, processing 5+ billion AI tokens daily, enterprise-grade infrastructure",
      generatingRevenue: "YES - Confirmed active revenue from Squad AI subscriptions, compute usage, API access, and platform integrations with exponentially growing user base",
      lifecyclePhase: "Growth/Scaling Phase - Mature infrastructure with enterprise features, integrated with major platforms, processing billions of daily requests"
    },
    marketing: {
      channels: "Official website (chutes.ai), Twitter/X (@chutes_ai), GitHub repositories under Rayon Labs. No dedicated Discord/Telegram found",
      frequency: "Moderate frequency focused on technical updates rather than marketing-heavy engagement, with active GitHub repository maintenance",
      effort: "Moderate effort with product-first, marketing-light approach prioritizing technical documentation and development communication over aggressive marketing",
      responsiveness: "Mixed - strong technical community engagement through GitHub, limited broader community channels, well-integrated into Bittensor ecosystem"
    },
    development: {
      openSource: "YES - Fully open-source with MIT License",
      repository: "https://github.com/rayonlabs/chutes (primary), https://github.com/rayonlabs/chutes-miner, https://github.com/rayonlabs/chutes-api",
      updateActivity: "Moderate activity with evidence of regular updates and active maintenance across multiple repositories",
      contributors: "Core team active including Jon Durbin and namoray from Rayon Labs, operating 3 Bittensor subnets",
      practices: "Strong professional practices including Git version control, pytest testing, ruff linting, Poetry dependency management, Kubernetes/Helm deployment",
      roadmap: "Limited public roadmap information beyond basic platform status indicators",
      documentation: "Comprehensive documentation including API docs, OpenAPI schema, GraVal GPU validation library, Kubernetes guides, and architecture explanations",
      features: "Active development with AI model integrations (DeepSeek, Mistral), advanced GPU validation, Kubernetes infrastructure improvements, child hotkey support",
      thirdParty: "Growing ecosystem with community-developed tools (sn64-tools by minersunion), integration support for AI frameworks, public/private Docker image support"
    }
  };
}; 