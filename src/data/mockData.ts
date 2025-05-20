import { CategoryType } from '../types';

// Calculate total market cap for a category
const calculateCategoryTotal = (subnets: any[]) => {
  return subnets.reduce((total, subnet) => total + subnet.marketCap, 0);
};

// Group subnets by category
const genAISubnets = [
  {
    id: 'subnet-1',
    name: 'Apex',
    description: 'Advanced GenAI subnet for text and code generation',
    status: 'active',
    marketCap: 48000,
    emissions: 2.66,
    weeklyChange: 5.2,
    validators: 248,
    age: 124,
    metrics: [
      { name: 'TPS', value: '850', percentage: 85 },
      { name: 'Uptime', value: '99.8%', percentage: 99 },
      { name: 'Response', value: '120ms', percentage: 92 }
    ]
  },
  {
    id: 'subnet-2',
    name: 'Omron',
    description: 'Specialized GenAI subnet for medical applications',
    status: 'active',
    marketCap: 13000,
    emissions: 0.63,
    weeklyChange: 3.1,
    validators: 186,
    age: 87,
    metrics: [
      { name: 'TPS', value: '620', percentage: 62 },
      { name: 'Uptime', value: '99.5%', percentage: 95 },
      { name: 'Response', value: '350ms', percentage: 75 }
    ]
  },
  {
    id: 'subnet-3',
    name: 'Targon',
    description: 'High-performance GenAI subnet for enterprise solutions',
    status: 'active',
    marketCap: 122000,
    emissions: 6.29,
    weeklyChange: 8.7,
    validators: 214,
    age: 68,
    metrics: [
      { name: 'TPS', value: '710', percentage: 71 },
      { name: 'Uptime', value: '99.9%', percentage: 97 },
      { name: 'Response', value: '180ms', percentage: 88 }
    ]
  },
  {
    id: 'subnet-4',
    name: 'Three Gen',
    description: 'Innovative GenAI solutions for creative industries',
    status: 'active',
    marketCap: 41000,
    emissions: 2.12,
    weeklyChange: 4.5,
    validators: 192,
    age: 95,
    metrics: [
      { name: 'TPS', value: '680', percentage: 68 },
      { name: 'Uptime', value: '99.7%', percentage: 96 },
      { name: 'Response', value: '150ms', percentage: 90 }
    ]
  },
  {
    id: 'subnet-5',
    name: 'Nineteen',
    description: 'Next-generation AI models and applications',
    status: 'active',
    marketCap: 55000,
    emissions: 2.94,
    weeklyChange: 6.2,
    validators: 205,
    age: 82,
    metrics: [
      { name: 'TPS', value: '750', percentage: 75 },
      { name: 'Uptime', value: '99.8%', percentage: 98 },
      { name: 'Response', value: '130ms', percentage: 91 }
    ]
  }
];

const trainingSubnets = [
  {
    id: 'subnet-6',
    name: 'Templar',
    description: 'Advanced training infrastructure for large-scale models',
    status: 'active',
    marketCap: 90000,
    emissions: 4.85,
    weeklyChange: 7.3,
    validators: 235,
    age: 156,
    metrics: [
      { name: 'TPS', value: '820', percentage: 82 },
      { name: 'Uptime', value: '99.9%', percentage: 99 },
      { name: 'Response', value: '110ms', percentage: 94 }
    ]
  },
  {
    id: 'subnet-7',
    name: 'Pre-training',
    description: 'Specialized subnet for model pre-training tasks',
    status: 'active',
    marketCap: 25000,
    emissions: 1.28,
    weeklyChange: 3.8,
    validators: 168,
    age: 112,
    metrics: [
      { name: 'TPS', value: '580', percentage: 58 },
      { name: 'Uptime', value: '99.6%', percentage: 96 },
      { name: 'Response', value: '220ms', percentage: 82 }
    ]
  }
];

const modelDevSubnets = [
  {
    id: 'subnet-8',
    name: 'OpenKaito',
    description: 'Open-source model development platform',
    status: 'active',
    marketCap: 58000,
    emissions: 3.26,
    weeklyChange: 5.9,
    validators: 198,
    age: 134,
    metrics: [
      { name: 'TPS', value: '690', percentage: 69 },
      { name: 'Uptime', value: '99.7%', percentage: 97 },
      { name: 'Response', value: '160ms', percentage: 89 }
    ]
  },
  {
    id: 'subnet-9',
    name: 'Dippy Roleplay',
    description: 'Specialized model development for interactive AI',
    status: 'active',
    marketCap: 12000,
    emissions: 0.58,
    weeklyChange: 2.8,
    validators: 145,
    age: 78,
    metrics: [
      { name: 'TPS', value: '520', percentage: 52 },
      { name: 'Uptime', value: '99.4%', percentage: 94 },
      { name: 'Response', value: '280ms', percentage: 78 }
    ]
  }
];

const predictionsSubnets = [
  {
    id: 'subnet-10',
    name: 'Infinite Games',
    description: 'AI-powered prediction markets and gaming',
    status: 'active',
    marketCap: 8000,
    emissions: 0.45,
    weeklyChange: 2.1,
    validators: 132,
    age: 65,
    metrics: [
      { name: 'TPS', value: '480', percentage: 48 },
      { name: 'Uptime', value: '99.3%', percentage: 93 },
      { name: 'Response', value: '320ms', percentage: 74 }
    ]
  },
  {
    id: 'subnet-11',
    name: 'Zeus',
    description: 'Advanced prediction models for financial markets',
    status: 'active',
    marketCap: 9000,
    emissions: 0.57,
    weeklyChange: 2.4,
    validators: 138,
    age: 72,
    metrics: [
      { name: 'TPS', value: '510', percentage: 51 },
      { name: 'Uptime', value: '99.5%', percentage: 95 },
      { name: 'Response', value: '290ms', percentage: 76 }
    ]
  }
];

const infraSubnets = [
  {
    id: 'subnet-12',
    name: 'SubVortex',
    description: 'Core infrastructure services for the network',
    status: 'active',
    marketCap: 5000,
    emissions: 0.27,
    weeklyChange: 1.5,
    validators: 118,
    age: 45,
    metrics: [
      { name: 'TPS', value: '420', percentage: 42 },
      { name: 'Uptime', value: '99.2%', percentage: 92 },
      { name: 'Response', value: '380ms', percentage: 70 }
    ]
  },
  {
    id: 'subnet-13',
    name: 'Horde',
    description: 'Distributed computing and storage infrastructure',
    status: 'active',
    marketCap: 17000,
    emissions: 0.99,
    weeklyChange: 3.2,
    validators: 156,
    age: 89,
    metrics: [
      { name: 'TPS', value: '550', percentage: 55 },
      { name: 'Uptime', value: '99.6%', percentage: 96 },
      { name: 'Response', value: '240ms', percentage: 81 }
    ]
  },
  {
    id: 'subnet-14',
    name: 'Data Universe',
    description: 'Data management and analytics infrastructure',
    status: 'active',
    marketCap: 34000,
    emissions: 1.77,
    weeklyChange: 4.8,
    validators: 182,
    age: 112,
    metrics: [
      { name: 'TPS', value: '640', percentage: 64 },
      { name: 'Uptime', value: '99.7%', percentage: 97 },
      { name: 'Response', value: '190ms', percentage: 86 }
    ]
  },
  {
    id: 'subnet-15',
    name: 'TAOHash',
    description: 'High-performance computing infrastructure',
    status: 'active',
    marketCap: 124000,
    emissions: 6.90,
    weeklyChange: 8.9,
    validators: 245,
    age: 167,
    metrics: [
      { name: 'TPS', value: '890', percentage: 89 },
      { name: 'Uptime', value: '99.9%', percentage: 99 },
      { name: 'Response', value: '100ms', percentage: 95 }
    ]
  }
];

const defiSubnets = [
  {
    id: 'subnet-16',
    name: 'PTN',
    description: 'Premier DeFi platform for advanced trading',
    status: 'active',
    marketCap: 130000,
    emissions: 6.83,
    weeklyChange: 9.2,
    validators: 256,
    age: 178,
    metrics: [
      { name: 'TVL', value: '$62M', percentage: 92 },
      { name: 'Uptime', value: '100%', percentage: 100 },
      { name: 'Response', value: '90ms', percentage: 96 }
    ]
  },
  {
    id: 'subnet-17',
    name: 'Sturdy',
    description: 'Stable DeFi infrastructure and services',
    status: 'active',
    marketCap: 25000,
    emissions: 1.14,
    weeklyChange: 3.7,
    validators: 172,
    age: 98,
    metrics: [
      { name: 'TVL', value: '$28M', percentage: 68 },
      { name: 'Uptime', value: '99.8%', percentage: 98 },
      { name: 'Response', value: '170ms', percentage: 88 }
    ]
  }
];

const aiToolSubnets = [
  {
    id: 'subnet-18',
    name: 'De_Val',
    description: 'AI development tools and utilities',
    status: 'active',
    marketCap: 8000,
    emissions: 0.43,
    weeklyChange: 2.2,
    validators: 134,
    age: 67,
    metrics: [
      { name: 'TPS', value: '490', percentage: 49 },
      { name: 'Uptime', value: '99.4%', percentage: 94 },
      { name: 'Response', value: '310ms', percentage: 75 }
    ]
  },
  {
    id: 'subnet-19',
    name: 'BitAds',
    description: 'AI-powered advertising platform',
    status: 'active',
    marketCap: 3000,
    emissions: 0.19,
    weeklyChange: 1.2,
    validators: 112,
    age: 42,
    metrics: [
      { name: 'TPS', value: '380', percentage: 38 },
      { name: 'Uptime', value: '99.1%', percentage: 91 },
      { name: 'Response', value: '420ms', percentage: 66 }
    ]
  },
  {
    id: 'subnet-20',
    name: 'BitAgent',
    description: 'AI agent development and deployment platform',
    status: 'active',
    marketCap: 6000,
    emissions: 0.36,
    weeklyChange: 1.8,
    validators: 126,
    age: 56,
    metrics: [
      { name: 'TPS', value: '450', percentage: 45 },
      { name: 'Uptime', value: '99.3%', percentage: 93 },
      { name: 'Response', value: '350ms', percentage: 72 }
    ]
  }
];

export const mockCategories: CategoryType[] = [
  {
    id: 'genai',
    name: 'GenAI',
    description: 'Generative AI subnets focused on text, image, and multimodal generation',
    marketCapTotal: calculateCategoryTotal(genAISubnets),
    subnets: genAISubnets
  },
  {
    id: 'training',
    name: 'Training',
    description: 'Subnets dedicated to AI model training and optimization',
    marketCapTotal: calculateCategoryTotal(trainingSubnets),
    subnets: trainingSubnets
  },
  {
    id: 'modeldev',
    name: 'Model Dev',
    description: 'Platforms for AI model development and testing',
    marketCapTotal: calculateCategoryTotal(modelDevSubnets),
    subnets: modelDevSubnets
  },
  {
    id: 'predictions',
    name: 'Predictions',
    description: 'AI-powered prediction and forecasting platforms',
    marketCapTotal: calculateCategoryTotal(predictionsSubnets),
    subnets: predictionsSubnets
  },
  {
    id: 'infra',
    name: 'Infrastructure',
    description: 'Core infrastructure and services supporting the ecosystem',
    marketCapTotal: calculateCategoryTotal(infraSubnets),
    subnets: infraSubnets
  },
  {
    id: 'defi',
    name: 'DeFi',
    description: 'Decentralized Finance subnets offering financial services',
    marketCapTotal: calculateCategoryTotal(defiSubnets),
    subnets: defiSubnets
  },
  {
    id: 'aitool',
    name: 'AI Tools',
    description: 'Specialized tools and utilities for AI development',
    marketCapTotal: calculateCategoryTotal(aiToolSubnets),
    subnets: aiToolSubnets
  }
];