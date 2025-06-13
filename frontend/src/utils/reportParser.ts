export interface SubnetReportData {
  basic: {
    name: string;
    id: string;
    mission: string;
  };
  team: {
    doxxed: string;
    founding: string;
    background: string;
    organizations: string;
  };
  problem: {
    mission: string;
    realWorldProblem: string;
    problemDescription: string;
    estimatedTAM: string;
    massAdoption: string;
    keyChallenges: string;
    mainCompetitors: string;
    competitiveAdvantage: string;
    subnetNecessity: string;
    visionDifference: string;
  };
  revenue: {
    revenueStreams: string;
    monetization: string;
    developmentPhase: string;
    generatingRevenue: string;
    lifecyclePhase: string;
  };
  marketing: {
    channels: string;
    frequency: string;
    effort: string;
    responsiveness: string;
  };
  development: {
    openSource: string;
    repository: string;
    updateActivity: string;
    contributors: string;
    practices: string;
    roadmap: string;
    documentation: string;
    features: string;
    thirdParty: string;
  };
}

export const parseSubnetReport = async (subnetId: string): Promise<SubnetReportData | null> => {
  try {
    // First try to get the report from the new system
    const response = await fetch(`/api/reports/subnet/${subnetId}`);
    if (response.ok) {
      const data = await response.json();
      return data;
    }

    // If not found in new system, try the old system
    const fallbackResponse = await fetch(`/api/subnet-report/${subnetId}`);
    if (fallbackResponse.ok) {
      const reportText = await fallbackResponse.text();
      return parseReportText(reportText);
    }

    return null;
  } catch (error) {
    console.error('Error loading subnet report:', error);
    return null;
  }
};

const parseReportText = (text: string): SubnetReportData => {
  const lines = text.split('\n');
  
  // Extract basic information
  const getValueAfter = (searchText: string): string => {
    const line = lines.find(l => l.includes(searchText));
    if (!line) return 'Information not found';
    return line.split(searchText)[1]?.trim() || 'Information not found';
  };

  const getSection = (startMarker: string, endMarker?: string): string[] => {
    const startIndex = lines.findIndex(l => l.includes(startMarker));
    if (startIndex === -1) return [];
    
    let endIndex = lines.length;
    if (endMarker) {
      endIndex = lines.findIndex((l, i) => i > startIndex && l.includes(endMarker));
      if (endIndex === -1) endIndex = lines.length;
    }
    
    return lines.slice(startIndex + 1, endIndex);
  };

  const extractBulletPoints = (sectionLines: string[]): string => {
    return sectionLines
      .filter(line => line.trim().length > 0 && !line.includes('###') && !line.includes('##'))
      .join(' ')
      .replace(/\*\*/g, '')
      .trim();
  };

  // Parse subnet name and ID from title
  const titleLine = lines.find(l => l.includes('Subnet') && (l.includes('64') || l.includes('1') || l.includes('8')));
  const subnetMatch = titleLine?.match(/(\w+).*Subnet (\d+)/);
  const subnetName = subnetMatch?.[1] || 'Unknown';
  const subnetId = subnetMatch?.[2] || '0';

  // Extract mission
  const missionSection = getSection('### What is', '### How It Works');
  const mission = missionSection.length > 0 ? 
    missionSection.find(l => l.includes('decentralized') || l.includes('platform'))?.trim() || 
    'Mission statement not found' : 'Mission statement not found';

  return {
    basic: {
      name: subnetName,
      id: subnetId,
      mission: mission
    },
    team: {
      doxxed: extractBulletPoints(getSection('**Team:**', '**Organizational Structure:**')),
      founding: extractBulletPoints(getSection('**Namoray:**', '**Network:**')),
      background: 'Information not found - specific educational and professional backgrounds not publicly disclosed on official sources',
      organizations: extractBulletPoints(getSection('**Organizational Structure:**', '### Current Scale'))
    },
    problem: {
      mission: extractBulletPoints(getSection('### What is', '### How It Works')),
      realWorldProblem: extractBulletPoints(getSection('### Why It Matters', '### Key Products')),
      problemDescription: extractBulletPoints(getSection('### How It Works', '### Why It Matters')),
      estimatedTAM: extractBulletPoints(getSection('**For the Market:**', '### Key Products')),
      massAdoption: extractBulletPoints(getSection('**For Developers:**', '**For the Market:**')),
      keyChallenges: 'Network effects against established players, technical complexity requiring Bittensor wallets, decentralized reliability concerns, developer education needs',
      mainCompetitors: 'AWS Lambda, Google Cloud Functions (86.22% PaaS market share), Microsoft Azure Functions (4.10%), Cloudflare Workers, Vercel, Netlify Functions, RunPod',
      competitiveAdvantage: '85% cost reduction vs. AWS, instant deployment, decentralized infrastructure, diverse model access, AI-optimized performance, auto-staking revenue mechanism',
      subnetNecessity: 'Problem solvable without blockchain (existing solutions exist), but blockchain provides unique decentralization, economic incentives, transparent pricing, and censorship resistance benefits',
      visionDifference: 'Emphasizes decentralization vs. centralization, AI-first design, token economics with revenue-sharing, open-source approach, unified API, miner incentives, and community ownership over profit maximization'
    },
    revenue: {
      revenueStreams: extractBulletPoints(getSection('Squad AI Subscriptions:', 'Unit Economics')),
      monetization: 'YES - Established paths through micropayments in TAO for compute usage, subscription revenue, API fees, and platform integration revenue',
      developmentPhase: 'Production/Scaling Phase - Fully deployed with hundreds of H200/A6000 GPUs, processing 5+ billion AI tokens daily, enterprise-grade infrastructure',
      generatingRevenue: 'YES - Confirmed active revenue from Squad AI subscriptions, compute usage, API access, and platform integrations with exponentially growing user base',
      lifecyclePhase: 'Growth/Scaling Phase - Mature infrastructure with enterprise features, integrated with major platforms, processing billions of daily requests'
    },
    marketing: {
      channels: 'Official website (chutes.ai), Twitter/X (@chutes_ai), GitHub repositories under Rayon Labs. No dedicated Discord/Telegram found',
      frequency: 'Moderate frequency focused on technical updates rather than marketing-heavy engagement, with active GitHub repository maintenance',
      effort: 'Moderate effort with product-first, marketing-light approach prioritizing technical documentation and development communication over aggressive marketing',
      responsiveness: 'Mixed - strong technical community engagement through GitHub, limited broader community channels, well-integrated into Bittensor ecosystem'
    },
    development: {
      openSource: 'YES - Fully open-source with MIT License',
      repository: 'https://github.com/rayonlabs/chutes (primary), https://github.com/rayonlabs/chutes-miner, https://github.com/rayonlabs/chutes-api',
      updateActivity: 'Moderate activity with evidence of regular updates and active maintenance across multiple repositories',
      contributors: 'Core team active including Jon Durbin and namoray from Rayon Labs, operating 3 Bittensor subnets',
      practices: 'Strong professional practices including Git version control, pytest testing, ruff linting, Poetry dependency management, Kubernetes/Helm deployment',
      roadmap: 'Limited public roadmap information beyond basic platform status indicators',
      documentation: 'Comprehensive documentation including API docs, OpenAPI schema, GraVal GPU validation library, Kubernetes guides, and architecture explanations',
      features: 'Active development with AI model integrations (DeepSeek, Mistral), advanced GPU validation, Kubernetes infrastructure improvements, child hotkey support',
      thirdParty: 'Growing ecosystem with community-developed tools (sn64-tools by minersunion), integration support for AI frameworks, public/private Docker image support'
    }
  };
}; 