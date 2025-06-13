import React, { useState, useEffect } from 'react';
import { FileText, Filter, Download, ArrowUpRight, Loader2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { getAvailableReports } from '../../api/subnetReport';

interface Report {
  id: string;
  title: string;
  description: string;
  type: string;
  date: string;
  category: string;
  pages: number;
  premium: boolean;
}

const ReportsView: React.FC = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadReports = async () => {
      try {
        setLoading(true);
        const data = await getAvailableReports();
        setReports(data);
      } catch (err) {
        setError('Failed to load reports');
        console.error('Error loading reports:', err);
      } finally {
        setLoading(false);
      }
    };

    loadReports();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-64px)] p-6 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-indigo-500" />
          <p className="text-slate-400">Loading reports...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-[calc(100vh-64px)] p-6 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-64px)] p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-semibold mb-2">Subnet Reports</h2>
            <p className="text-slate-400">Institutional grade analysis and insights for Bittensor subnets</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition-colors duration-200">
              <Filter size={16} />
              <span className="text-sm">Filters</span>
            </button>
            <button className="btn btn-primary">
              Subscribe to Premium
            </button>
          </div>
        </div>

        {/* Reports Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map(report => (
            <Link 
              key={report.id} 
              to={`/app/subnet/${report.id}`}
              className="card group hover:border-indigo-500/50 transition-all duration-200"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <FileText size={20} className="text-indigo-400" />
                    <span className="text-sm text-slate-400">{report.type}</span>
                  </div>
                  {report.premium && (
                    <span className="px-2 py-1 text-xs font-medium bg-indigo-500/10 text-indigo-400 rounded-full">
                      Premium
                    </span>
                  )}
                </div>

                <h3 className="text-lg font-medium mb-2 group-hover:text-indigo-400 transition-colors duration-200">
                  {report.title}
                </h3>

                <p className="text-sm text-slate-400 mb-4">
                  {report.description}
                </p>

                <div className="flex items-center justify-between text-sm text-slate-400">
                  <span>{report.date}</span>
                  <span>{report.pages} pages</span>
                </div>
              </div>

              <div className="border-t border-slate-700/50 p-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium px-3 py-1 rounded-full bg-slate-700/50">
                    {report.category}
                  </span>
                  <div className="flex items-center gap-2">
                    <button className="p-2 rounded-lg hover:bg-slate-700/50 transition-colors duration-200">
                      <Download size={16} />
                    </button>
                    <button className="p-2 rounded-lg hover:bg-slate-700/50 transition-colors duration-200">
                      <ArrowUpRight size={16} />
                    </button>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ReportsView;