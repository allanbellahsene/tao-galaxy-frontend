import React from 'react';
import { ExternalLink, MessageSquare } from 'lucide-react';
import { NewsType } from '../../types';
import { getCategoryColor } from '../../utils/colors';

interface NewsTableProps {
  news: NewsType[];
}

const NewsTable: React.FC<NewsTableProps> = ({ news }) => {
  return (
    <div className="card overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700/50">
              <th className="text-left p-4 font-medium text-sm text-slate-300">Title</th>
              <th className="text-left p-4 font-medium text-sm text-slate-300">Category</th>
              <th className="text-left p-4 font-medium text-sm text-slate-300">Source</th>
              <th className="text-left p-4 font-medium text-sm text-slate-300">Time</th>
              <th className="text-right p-4 font-medium text-sm text-slate-300">Comments</th>
            </tr>
          </thead>
          <tbody>
            {news.map((item) => {
              const categoryColor = getCategoryColor(item.category);
              return (
                <tr 
                  key={item.id}
                  className="border-b border-slate-700/50 hover:bg-slate-700/20 transition-colors duration-200"
                >
                  <td className="p-4">
                    <a 
                      href={item.sourceUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 text-sm hover:text-indigo-400 transition-colors duration-200"
                    >
                      {item.title}
                      <ExternalLink size={14} className="opacity-50" />
                    </a>
                    {item.summary && (
                      <p className="text-xs text-slate-400 mt-1">{item.summary}</p>
                    )}
                  </td>
                  <td className="p-4">
                    <span
                      className="text-xs font-medium px-2 py-1 rounded-full"
                      style={{ backgroundColor: `${categoryColor}20`, color: categoryColor }}
                    >
                      {item.categoryName}
                    </span>
                  </td>
                  <td className="p-4">
                    <span className="text-sm text-slate-300">{item.source}</span>
                  </td>
                  <td className="p-4">
                    <span className="text-sm text-slate-400">{item.timeAgo}</span>
                  </td>
                  <td className="p-4 text-right">
                    <div className="flex items-center justify-end gap-1.5 text-sm text-slate-400">
                      <MessageSquare size={14} />
                      <span>{item.commentsCount}</span>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default NewsTable;