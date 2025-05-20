import React from 'react';
import { ExternalLink, MessageSquare, ArrowUpRight } from 'lucide-react';
import { NewsType } from '../../types';
import { getCategoryColor } from '../../utils/colors';

interface NewsCardProps {
  news: NewsType;
}

const NewsCard: React.FC<NewsCardProps> = ({ news }) => {
  const categoryColor = getCategoryColor(news.category);

  return (
    <div className="card group hover:border-slate-600 transition-colors duration-200">
      {/* Image */}
      {news.image && (
        <div className="relative h-48 rounded-t-xl overflow-hidden">
          <img
            src={news.image}
            alt={news.title}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-900 to-transparent opacity-60"></div>
        </div>
      )}

      {/* Content */}
      <div className="p-4">
        <div className="flex items-center gap-2 mb-3">
          <span
            className="text-xs font-medium px-2 py-1 rounded-full"
            style={{ backgroundColor: `${categoryColor}20`, color: categoryColor }}
          >
            {news.categoryName}
          </span>
          <span className="text-xs text-slate-400">{news.timeAgo}</span>
        </div>

        <h3 className="text-lg font-medium mb-2 group-hover:text-indigo-400 transition-colors duration-200">
          {news.title}
        </h3>

        <p className="text-sm text-slate-300 mb-4 line-clamp-2">
          {news.summary}
        </p>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <a
              href={news.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 text-sm text-slate-400 hover:text-slate-300 transition-colors"
            >
              <ExternalLink size={14} />
              <span>{news.source}</span>
            </a>
            {news.commentsCount > 0 && (
              <div className="flex items-center gap-1.5 text-sm text-slate-400">
                <MessageSquare size={14} />
                <span>{news.commentsCount}</span>
              </div>
            )}
          </div>
          <button className="p-2 rounded-lg hover:bg-slate-700/50 transition-colors duration-200">
            <ArrowUpRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default NewsCard;