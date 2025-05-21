import React from 'react';
import { TrendingUp, TrendingDown, ArrowRight, Calendar, Radio } from 'lucide-react';

const DailyRecap: React.FC = () => {
  const recaps = [
    {
      date: 'Today, March 14',
      headlines: [
        {
          title: 'TAOHash achieves 25% performance improvement',
          subnets: ['SN15', 'SN12'],
          summary: 'Latest update reduces latency and increases throughput significantly.',
          tags: ['Infrastructure', 'Development']
        },
        {
          title: 'New governance proposal for GenAI emissions',
          subnets: ['SN1', 'SN2', 'SN3'],
          summary: 'Community discusses increasing TAO emissions for high-performing subnets.',
          tags: ['Governance', 'GenAI']
        }
      ],
      stats: {
        taoPrice: 2.45,
        taoChange: 5.2,
        tvl: 892,
        tvlChange: 2.1,
        validators: 3245,
        validatorChange: 52
      }
    },
    {
      date: 'March 13',
      headlines: [
        {
          title: 'PTN subnet launches advanced trading features',
          subnets: ['SN16'],
          summary: 'New trading capabilities and improved liquidity mechanisms introduced.',
          tags: ['DeFi', 'Launch']
        },
        {
          title: 'Templar subnet enhances training capabilities',
          subnets: ['SN6'],
          summary: 'Major improvements in model training infrastructure and efficiency.',
          tags: ['Training', 'Development']
        }
      ],
      stats: {
        taoPrice: 2.33,
        taoChange: -1.2,
        tvl: 874,
        tvlChange: -0.8,
        validators: 3193,
        validatorChange: 28
      }
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <h3 className="text-xl font-semibold">Daily Recaps</h3>
          <span className="text-xs bg-slate-700/50 px-2 py-1 rounded-full">Powered by TAO AI</span>
        </div>
        <div className="flex gap-1">
          <button className="p-2 rounded-lg hover:bg-slate-700/50 transition-colors">
            <ArrowRight size={16} className="rotate-180" />
          </button>
          <button className="p-2 rounded-lg hover:bg-slate-700/50 transition-colors">
            <ArrowRight size={16} />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {recaps.map((recap, index) => (
          <div key={index} className="card bg-slate-800/90">
            <div className="p-4 border-b border-slate-700/50">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <Radio size={16} className="text-indigo-400" />
                  <span className="text-sm font-medium">{recap.date}</span>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div className="space-y-1">
                  <span className="text-slate-400">TAO Price</span>
                  <div className={`flex items-center gap-1 ${
                    recap.stats.taoChange >= 0 ? 'text-emerald-400' : 'text-red-400'
                  }`}>
                    {recap.stats.taoChange >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                    <span className="font-medium">${recap.stats.taoPrice}</span>
                    <span>({recap.stats.taoChange}%)</span>
                  </div>
                </div>
                <div className="space-y-1">
                  <span className="text-slate-400">TVL</span>
                  <div className={`flex items-center gap-1 ${
                    recap.stats.tvlChange >= 0 ? 'text-emerald-400' : 'text-red-400'
                  }`}>
                    {recap.stats.tvlChange >= 0 ? <TrendingUp size={12} /> : <TrendingDown size={12} />}
                    <span className="font-medium">${recap.stats.tvl}M</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="p-4 space-y-4">
              {recap.headlines.map((headline, hIndex) => (
                <div key={hIndex} className="space-y-2">
                  <div className="flex flex-wrap gap-1">
                    {headline.subnets.map((subnet, sIndex) => (
                      <span 
                        key={sIndex}
                        className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400"
                      >
                        {subnet}
                      </span>
                    ))}
                  </div>
                  <h4 className="text-sm font-medium leading-snug hover:text-indigo-400 transition-colors cursor-pointer">
                    {headline.title}
                  </h4>
                  <p className="text-xs text-slate-400 line-clamp-2">{headline.summary}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DailyRecap;