export interface Position {
  x: number;
  y: number;
}

export interface MetricType {
  name: string;
  value: string;
  percentage: number;
}

export interface SubnetType {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive';
  marketCap: number;
  emissions: number;
  weeklyChange: number;
  validators: number;
  age: number;
  metrics: MetricType[];
  website?: string;
  github?: string;
  discord?: string;
  registrationDate?: string;
  daysSinceRegistration?: number;
  rank?: number;
  price?: number;
  priceChange1Day?: number;
  priceChange1Month?: number;
  taoVolume24hr?: number;
  timestamp?: string;
}

export interface CategoryType {
  id: string;
  name: string;
  description: string;
  marketCapTotal: number;
  subnets: SubnetType[];
}

export interface NewsType {
  id: string;
  title: string;
  summary: string;
  content: string;
  category: string;
  categoryName: string;
  source: string;
  sourceUrl: string;
  image?: string;
  timeAgo: string;
  commentsCount: number;
}