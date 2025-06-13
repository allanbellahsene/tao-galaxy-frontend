import React, { useState, useEffect } from 'react';
import { ArrowLeft, Globe, Download, GitBranch, Building, DollarSign, Target, Users, Code, CheckCircle, ExternalLink, TrendingUp, AlertTriangle, Shield, BarChart3, FileText, Clock, Star, ChevronDown, ChevronRight, ChevronUp } from 'lucide-react';
import { SubnetReportData } from '../../utils/reportParser';
import { loadSubnetReportData } from '../../api/subnetReport';

interface SubnetReportProps {
  subnetId?: string;
  onBack?: () => void;
}

interface ParsedReportData {
  title: string;
  rating: string;
  executiveSummary: {
    investmentRating: string;
    allocation: string;
    timeline: string;
    thesis: string;
    strengths: string[];
    risks: string[];
  };
  mission: string;
  vision: string;
  team: {
    status: string;
    founders: string[];
    background: string;
    organizations: string;
  };
  market: {
    problem: string;
    solution: string;
    tam: string;
    competitors: string[];
    advantage: string;
    marketSize: string;
    marketTiming: string;
    competitivePosition: string;
    moatAssessment: string;
    massAdoption: string;
  };
  product: {
    phase: string;
    revenue: string;
    features: string[];
  };
  financial: {
    potential: string;
    sustainability: string;
    timeline: string;
  };
  metrics: {
    development: number;
    team: number;
    market: number;
    innovation: number;
  };
  risks: {
    technical: string;
    market: string;
    team: string;
    regulatory: string;
    competition: string;
  };
}

const SubnetReport: React.FC<SubnetReportProps> = ({ subnetId = '64', onBack }) => {
  const [reportContent, setReportContent] = useState<string | null>(null);
  const [parsedData, setParsedData] = useState<ParsedReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedSections, setExpandedSections] = useState({
    executive: true,
    mission: false,
    team: false,
    market: false,
    product: false,
    financial: false,
    metrics: false,
    risks: false
  });

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);
      setReportContent(null);
      setParsedData(null);
      
      console.log('Loading data for subnet:', subnetId);
      
      try {
        let data = await loadSubnetReportData(subnetId);
        
        console.log('Received data for subnet', subnetId, ':', data?.content?.substring(0, 200));
        
        // If no data found for the requested subnet, try SN1 as fallback (but only if not already SN1)
        if (!data?.content && subnetId !== '1') {
          console.log('No data found for subnet', subnetId, 'falling back to SN1');
          data = await loadSubnetReportData('1');
        }
        
        if (data?.content) {
          setReportContent(data.content);
          const parsed = parseHTMLReport(data.content);
          console.log('Parsed title:', parsed.title);
          setParsedData(parsed);
        } else {
          setError(`No report available for subnet ${subnetId}`);
        }
      } catch (err) {
        setError(`Error loading subnet report: ${err instanceof Error ? err.message : 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [subnetId]);

  const parseHTMLReport = (html: string): ParsedReportData => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    
    // Extract title directly from HTML content
    const title = doc.querySelector('h1')?.textContent?.trim() || 'Unknown Subnet';
    
    // Extract rating
    const rating = doc.querySelector('.rating-badge')?.textContent?.trim() || 'N/A';
    
    // Extract executive summary
    const allocation = doc.querySelector('.allocation')?.textContent || '';
    const timeline = doc.querySelector('.timeline')?.textContent || '';
    const thesis = doc.querySelector('.thesis p')?.textContent || '';
    
    const strengthsList = Array.from(doc.querySelectorAll('.strengths li')).map(li => li.textContent || '');
    const risksList = Array.from(doc.querySelectorAll('.risks li')).map(li => li.textContent || '');
    
    // Extract mission and vision
    const mission = doc.querySelector('.mission p')?.textContent || '';
    const vision = doc.querySelector('.vision p')?.textContent || '';
    
    // Extract team info
    const teamStatus = doc.querySelector('.status-badge')?.textContent || '';
    const founders = Array.from(doc.querySelectorAll('.team-list li')).map(li => li.textContent || '');
    const teamBackground = doc.querySelector('.team-card:nth-child(3) p')?.textContent || '';
    const organizations = doc.querySelector('.team-card:nth-child(4) p')?.textContent || '';
    
    // Extract market info - Fixed selectors for TAM and Advantage
    const problem = doc.querySelector('.problem-content h4:first-child + p')?.textContent || '';
    const solution = doc.querySelector('.problem-content h4:nth-child(3) + p')?.textContent || '';
    
    // More specific TAM selector - target the h4 with "Estimated TAM" text
    const tamElement = Array.from(doc.querySelectorAll('.problem-content h4')).find(h4 => 
      h4.textContent?.includes('Estimated TAM')
    );
    const tam = tamElement?.nextElementSibling?.textContent || '';
    
    // Extract market opportunity metrics
    const marketSize = doc.querySelector('.opportunity-metrics .metric:nth-child(1) p')?.textContent || '';
    const marketTiming = doc.querySelector('.opportunity-metrics .metric:nth-child(2) p')?.textContent || '';
    const competitivePosition = doc.querySelector('.opportunity-metrics .metric:nth-child(3) p')?.textContent || '';
    const moatAssessment = doc.querySelector('.opportunity-metrics .metric:nth-child(4) p')?.textContent || '';
    
    const competitors = Array.from(doc.querySelectorAll('.competition-content ul li')).map(li => li.textContent || '');
    
    // More specific Competitive Advantage selector - target the h4 with "Competitive Advantage" text
    const advantageElement = Array.from(doc.querySelectorAll('.competition-content h4')).find(h4 => 
      h4.textContent?.includes('Competitive Advantage')
    );
    const advantage = advantageElement?.nextElementSibling?.textContent || '';
    
    const massAdoption = doc.querySelector('.competition-content h4:last-child + p')?.textContent || '';
    
    // Extract product info
    const phase = doc.querySelector('.status-item:first-child p')?.textContent || '';
    const revenue = doc.querySelector('.revenue-info h4 + p')?.textContent || '';
    const features = Array.from(doc.querySelectorAll('.feature-list li')).map(li => li.textContent || '');
    
    // Extract financial info
    const potential = doc.querySelector('.financial-metrics .metric:first-child p')?.textContent || '';
    const sustainability = doc.querySelector('.business-metrics .metric:first-child p')?.textContent || '';
    const financialTimeline = doc.querySelector('.timeline-info .timeline')?.textContent || '';
    
    // Extract metrics (parse percentages)
    const development = parseInt(doc.querySelector('.metric-card:nth-child(1) .percentile-value')?.textContent || '0');
    const team = parseInt(doc.querySelector('.metric-card:nth-child(2) .percentile-value')?.textContent || '0');
    const market = parseInt(doc.querySelector('.metric-card:nth-child(3) .percentile-value')?.textContent || '0');
    const innovation = parseInt(doc.querySelector('.metric-card:nth-child(4) .percentile-value')?.textContent || '0');
    
    // Extract risks
    const technical = doc.querySelector('.risk-card:nth-child(1) p')?.textContent || '';
    const marketRisk = doc.querySelector('.risk-card:nth-child(2) p')?.textContent || '';
    const teamRisk = doc.querySelector('.risk-card:nth-child(3) p')?.textContent || '';
    const regulatory = doc.querySelector('.risk-card:nth-child(4) p')?.textContent || '';
    const competition = doc.querySelector('.risk-card:nth-child(5) p')?.textContent || '';

    return {
      title,
      rating,
      executiveSummary: {
        investmentRating: rating,
        allocation,
        timeline,
        thesis,
        strengths: strengthsList,
        risks: risksList
      },
      mission,
      vision,
      team: {
        status: teamStatus,
        founders,
        background: teamBackground,
        organizations
      },
      market: {
        problem,
        solution,
        tam,
        competitors,
        advantage,
        marketSize,
        marketTiming,
        competitivePosition,
        moatAssessment,
        massAdoption
      },
      product: {
        phase,
        revenue,
        features
      },
      financial: {
        potential,
        sustainability,
        timeline: financialTimeline
      },
      metrics: {
        development,
        team,
        market,
        innovation
      },
      risks: {
        technical,
        market: marketRisk,
        team: teamRisk,
        regulatory,
        competition
      }
    };
  };

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const getRatingColor = (rating: string) => {
    switch (rating.toLowerCase()) {
      case 'buy': return 'bg-emerald-500';
      case 'hold': return 'bg-amber-500';
      case 'sell': return 'bg-red-500';
      default: return 'bg-slate-500';
    }
  };

  const getRiskColor = (risk: string) => {
    if (risk.toLowerCase().includes('low')) return 'bg-emerald-500/20 border-emerald-500/30 text-emerald-400';
    if (risk.toLowerCase().includes('medium')) return 'bg-amber-500/20 border-amber-500/30 text-amber-400';
    if (risk.toLowerCase().includes('high')) return 'bg-red-500/20 border-red-500/30 text-red-400';
    return 'bg-slate-500/20 border-slate-500/30 text-slate-400';
  };

  const MetricBar = ({ label, value, color = 'indigo' }: { label: string; value: number; color?: string }) => (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-slate-300">{label}</span>
        <span className="text-sm text-slate-400">{value}%</span>
      </div>
      <div className="w-full bg-slate-800 rounded-full h-2">
        <div 
          className={`bg-${color}-500 h-2 rounded-full transition-all duration-500`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );

  const SectionCard = ({ 
    icon, 
    title, 
    children, 
    sectionKey, 
    className = "" 
  }: {
    icon: React.ReactNode;
    title: string;
    children: React.ReactNode;
    sectionKey: keyof typeof expandedSections;
    className?: string;
  }) => (
    <div className={`bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden ${className}`}>
      <div 
        className="flex items-center justify-between p-6 cursor-pointer hover:bg-slate-800/50 transition-colors"
        onClick={() => toggleSection(sectionKey)}
      >
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white">
            {icon}
          </div>
          <h2 className="text-xl font-semibold text-white">{title}</h2>
        </div>
        {expandedSections[sectionKey] ? 
          <ChevronUp size={20} className="text-slate-400" /> : 
          <ChevronDown size={20} className="text-slate-400" />
        }
      </div>
      {expandedSections[sectionKey] && (
        <div className="px-6 pb-6">
          {children}
        </div>
      )}
    </div>
  );

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
          <div className="text-white text-lg">Loading Subnet {subnetId} Report...</div>
          <div className="text-slate-400 text-sm mt-2">Parsing institutional research data</div>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !parsedData) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center">
        <div className="text-center max-w-md">
          <AlertTriangle size={48} className="text-red-400 mx-auto mb-4" />
          <div className="text-white text-xl mb-2">Report Not Available</div>
          <div className="text-slate-400 mb-6">{error || `No report data found for subnet ${subnetId}`}</div>
          <button 
            onClick={onBack}
            className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors"
          >
            Back to Overview
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900">
      {/* Header */}
      <div className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button 
                onClick={onBack}
                className="text-slate-400 hover:text-slate-300 transition-colors"
              >
                <ArrowLeft size={20} />
              </button>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                  <span className="text-white font-bold text-lg">SN</span>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white">{parsedData.title}</h1>
                  <p className="text-sm text-slate-400">Institutional Investment Analysis</p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <div className={`px-4 py-2 rounded-full text-white font-semibold ${getRatingColor(parsedData.rating)}`}>
                {parsedData.rating}
              </div>
              <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 transition-colors text-white">
                <Download size={16} />
                <span className="text-sm font-medium">Export PDF</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        
        {/* Executive Summary */}
        <SectionCard 
          icon={<BarChart3 size={20} />} 
          title="Executive Summary" 
          sectionKey="executive"
        >
          <div className="grid lg:grid-cols-3 gap-6">
            {/* Investment Rating */}
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <div className="flex items-center gap-3 mb-4">
                <TrendingUp size={20} className="text-emerald-400" />
                <h3 className="text-lg font-semibold text-white">Investment Rating</h3>
              </div>
              <div className={`inline-block px-4 py-2 rounded-full text-white font-semibold mb-4 ${getRatingColor(parsedData.executiveSummary.investmentRating)}`}>
                {parsedData.executiveSummary.investmentRating}
              </div>
              {parsedData.executiveSummary.allocation && (
                <p className="text-slate-300 text-sm mb-3">{parsedData.executiveSummary.allocation}</p>
              )}
              {parsedData.executiveSummary.timeline && (
                <p className="text-slate-400 text-sm">{parsedData.executiveSummary.timeline}</p>
              )}
            </div>

            {/* Investment Thesis */}
            <div className="lg:col-span-2 bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <div className="flex items-center gap-3 mb-4">
                <Target size={20} className="text-blue-400" />
                <h3 className="text-lg font-semibold text-white">Investment Thesis</h3>
              </div>
              <p className="text-slate-300 leading-relaxed">{parsedData.executiveSummary.thesis}</p>
            </div>
          </div>

          {/* Key Points */}
          <div className="grid md:grid-cols-2 gap-6 mt-6">
            {/* Strengths */}
            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <CheckCircle size={20} className="text-emerald-400" />
                <h3 className="text-lg font-semibold text-emerald-400">Key Strengths</h3>
              </div>
              <ul className="space-y-2">
                {parsedData.executiveSummary.strengths.map((strength, index) => (
                  <li key={index} className="text-slate-300 text-sm flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 flex-shrink-0" />
                    {strength}
                  </li>
                ))}
              </ul>
            </div>

            {/* Risks */}
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <AlertTriangle size={20} className="text-red-400" />
                <h3 className="text-lg font-semibold text-red-400">Key Risks</h3>
              </div>
              <ul className="space-y-2">
                {parsedData.executiveSummary.risks.map((risk, index) => (
                  <li key={index} className="text-slate-300 text-sm flex items-start gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-red-400 mt-2 flex-shrink-0" />
                    {risk}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </SectionCard>

        {/* Mission & Vision */}
        <SectionCard 
          icon={<Target size={20} />} 
          title="Mission & Vision" 
          sectionKey="mission"
        >
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Mission</h3>
              <p className="text-slate-300 leading-relaxed">{parsedData.mission}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Vision</h3>
              <p className="text-slate-300 leading-relaxed">{parsedData.vision}</p>
            </div>
          </div>
        </SectionCard>

        {/* Team & Governance */}
        <SectionCard 
          icon={<Users size={20} />} 
          title="Team & Governance" 
          sectionKey="team"
        >
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Team Status</h3>
              <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${
                parsedData.team.status.toLowerCase().includes('anonymous') 
                  ? 'bg-amber-500/20 border-amber-500/30 text-amber-400'
                  : 'bg-emerald-500/20 border-emerald-500/30 text-emerald-400'
              }`}>
                {parsedData.team.status}
              </div>
            </div>

            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Founding Team</h3>
              <ul className="space-y-1">
                {parsedData.team.founders.map((founder, index) => (
                  <li key={index} className="text-slate-300 text-sm">{founder}</li>
                ))}
              </ul>
            </div>

            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Background</h3>
              <p className="text-slate-300 text-sm">{parsedData.team.background}</p>
            </div>

            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Organizations</h3>
              <p className="text-slate-300 text-sm">{parsedData.team.organizations}</p>
            </div>
          </div>
        </SectionCard>

        {/* Market Analysis */}
        <SectionCard 
          icon={<Building size={20} />} 
          title="Market Analysis" 
          sectionKey="market"
        >
          <div className="space-y-6">
            {/* Problem, Solution, TAM */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-3">Problem</h3>
                <p className="text-slate-300 text-sm">{parsedData.market.problem}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-3">Solution</h3>
                <p className="text-slate-300 text-sm">{parsedData.market.solution}</p>
              </div>
              <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-3">TAM</h3>
                <p className="text-slate-300 text-sm">{parsedData.market.tam}</p>
              </div>
            </div>

            {/* Market Opportunity Metrics */}
            <div className="bg-slate-800/30 rounded-lg p-6 border border-slate-700">
              <h3 className="text-xl font-semibold text-white mb-6">Market Opportunity</h3>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-600">
                  <h4 className="text-sm font-semibold text-emerald-400 mb-2">Market Size</h4>
                  <p className="text-slate-300 text-sm">{parsedData.market.marketSize}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-600">
                  <h4 className="text-sm font-semibold text-blue-400 mb-2">Market Timing</h4>
                  <p className="text-slate-300 text-sm">{parsedData.market.marketTiming}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-600">
                  <h4 className="text-sm font-semibold text-purple-400 mb-2">Competitive Position</h4>
                  <p className="text-slate-300 text-sm">{parsedData.market.competitivePosition}</p>
                </div>
                <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-600">
                  <h4 className="text-sm font-semibold text-amber-400 mb-2">Moat Assessment</h4>
                  <p className="text-slate-300 text-sm">{parsedData.market.moatAssessment}</p>
                </div>
              </div>
            </div>

            {/* Competition and Advantage */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-3">Main Competitors</h3>
                <ul className="space-y-1">
                  {parsedData.market.competitors.slice(0, 7).map((competitor, index) => (
                    <li key={index} className="text-slate-300 text-sm flex items-center gap-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                      {competitor}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="space-y-4">
                <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                  <h3 className="text-lg font-semibold text-white mb-3">Competitive Advantage</h3>
                  <p className="text-slate-300 text-sm">{parsedData.market.advantage}</p>
                </div>
                {parsedData.market.massAdoption && (
                  <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
                    <h3 className="text-lg font-semibold text-white mb-3">Path to Mass Adoption</h3>
                    <p className="text-slate-300 text-sm">{parsedData.market.massAdoption}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </SectionCard>

        {/* Product & Development */}
        <SectionCard 
          icon={<Building size={20} />} 
          title="Product & Development" 
          sectionKey="product"
        >
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Development Phase</h3>
              <p className="text-slate-300 text-sm">{parsedData.product.phase}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Revenue Status</h3>
              <p className="text-slate-300 text-sm">{parsedData.product.revenue}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Recent Features</h3>
              <ul className="space-y-1">
                {parsedData.product.features.slice(0, 3).map((feature, index) => (
                  <li key={index} className="text-slate-300 text-sm flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </SectionCard>

        {/* Financial Analysis */}
        <SectionCard 
          icon={<DollarSign size={20} />} 
          title="Financial Analysis" 
          sectionKey="financial"
        >
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Revenue Potential</h3>
              <p className="text-slate-300 text-sm">{parsedData.financial.potential}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Sustainability</h3>
              <p className="text-slate-300 text-sm">{parsedData.financial.sustainability}</p>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <h3 className="text-lg font-semibold text-white mb-3">Investment Timeline</h3>
              <p className="text-slate-300 text-sm">{parsedData.financial.timeline}</p>
            </div>
          </div>
        </SectionCard>

        {/* Comparative Metrics */}
        <SectionCard 
          icon={<BarChart3 size={20} />} 
          title="Comparative Metrics" 
          sectionKey="metrics"
        >
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <MetricBar label="Development" value={parsedData.metrics.development} color="emerald" />
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <MetricBar label="Team Quality" value={parsedData.metrics.team} color="blue" />
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <MetricBar label="Market Opportunity" value={parsedData.metrics.market} color="purple" />
            </div>
            <div className="bg-slate-800/50 rounded-lg p-6 border border-slate-700">
              <MetricBar label="Innovation" value={parsedData.metrics.innovation} color="indigo" />
            </div>
          </div>
        </SectionCard>

        {/* Risk Assessment */}
        <SectionCard 
          icon={<Shield size={20} />} 
          title="Risk Assessment" 
          sectionKey="risks"
        >
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className={`rounded-lg p-6 border ${getRiskColor(parsedData.risks.technical)}`}>
              <h3 className="text-lg font-semibold mb-3">Technical Risk</h3>
              <p className="text-sm">{parsedData.risks.technical}</p>
            </div>
            <div className={`rounded-lg p-6 border ${getRiskColor(parsedData.risks.market)}`}>
              <h3 className="text-lg font-semibold mb-3">Market Risk</h3>
              <p className="text-sm">{parsedData.risks.market}</p>
            </div>
            <div className={`rounded-lg p-6 border ${getRiskColor(parsedData.risks.team)}`}>
              <h3 className="text-lg font-semibold mb-3">Team Risk</h3>
              <p className="text-sm">{parsedData.risks.team}</p>
            </div>
            <div className={`rounded-lg p-6 border ${getRiskColor(parsedData.risks.regulatory)}`}>
              <h3 className="text-lg font-semibold mb-3">Regulatory Risk</h3>
              <p className="text-sm">{parsedData.risks.regulatory}</p>
            </div>
            <div className={`rounded-lg p-6 border ${getRiskColor(parsedData.risks.competition)}`}>
              <h3 className="text-lg font-semibold mb-3">Competition Risk</h3>
              <p className="text-sm">{parsedData.risks.competition}</p>
            </div>
          </div>
        </SectionCard>

      </div>

      {/* Footer */}
      <div className="border-t border-slate-800 bg-slate-950/50 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between text-slate-400 text-sm">
            <div className="flex items-center gap-2">
              <Clock size={16} />
              <span>Generated on {new Date().toLocaleDateString()}</span>
            </div>
            <span>TAO Galaxy Institutional Research</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubnetReport;