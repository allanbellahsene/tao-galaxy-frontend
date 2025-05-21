import React, { useState } from 'react';
import { Menu, Zap, Compass, FileText, RssIcon, GraduationCap, Star, Settings, HelpCircle, ChevronDown } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import { useLocation, Link } from 'react-router-dom';

const Header: React.FC = () => {
  const { toggleSidebar } = useAppContext();
  const [showEducationMenu, setShowEducationMenu] = useState(false);
  const location = useLocation();

  const menuItems = [
    { icon: <Compass size={18} />, label: 'Subnet Explorer', path: '/app' },
    { icon: <FileText size={18} />, label: 'Reports', path: '/app/reports' },
    { icon: <RssIcon size={18} />, label: 'News', path: '/app/news' },
    {
      icon: <GraduationCap size={18} />,
      label: 'Education',
      hasSubmenu: true,
      submenu: [
        { label: 'Bittensor 101', path: '/app/education/bittensor' },
        { label: 'Subnets 101', path: '/app/education/subnets' },
        { label: 'Evaluate Subnets', path: '/app/education/evaluate' }
      ]
    },
    { icon: <Star size={18} />, label: 'Watchlist', path: '/app/watchlist' }
  ];

  return (
    <header className="sticky top-0 z-10 bg-slate-900/80 backdrop-blur-sm border-b border-slate-800">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <button 
                onClick={toggleSidebar}
                className="p-2 rounded-lg hover:bg-slate-800 transition-colors duration-200"
              >
                <Menu size={20} />
              </button>
              <Link to="/" className="flex items-center gap-2">
                <Zap className="text-indigo-500" size={24} />
                <h1 className="text-xl font-semibold tracking-tight">TAO Galaxy</h1>
              </Link>
            </div>

            <nav className="hidden md:flex items-center gap-2">
              {menuItems.map((item, index) => (
                <div key={index} className="relative">
                  {item.hasSubmenu ? (
                    <button
                      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg whitespace-nowrap transition-colors duration-200 hover:bg-slate-800/60 text-slate-300`}
                      onMouseEnter={() => setShowEducationMenu(true)}
                      onMouseLeave={() => setShowEducationMenu(false)}
                    >
                      {item.icon}
                      <span className="text-sm font-medium">{item.label}</span>
                      <ChevronDown size={14} className={`transition-transform duration-200 ${showEducationMenu ? 'rotate-180' : ''}`} />
                    </button>
                  ) : (
                    <Link
                      to={item.path}
                      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg whitespace-nowrap transition-colors duration-200 ${
                        location.pathname === item.path
                          ? 'bg-indigo-600/10 text-indigo-400'
                          : 'hover:bg-slate-800/60 text-slate-300'
                      }`}
                    >
                      {item.icon}
                      <span className="text-sm font-medium">{item.label}</span>
                    </Link>
                  )}
                  
                  {/* Education submenu */}
                  {item.hasSubmenu && showEducationMenu && (
                    <div 
                      className="absolute top-full left-0 mt-1 w-48 py-1 bg-slate-800 rounded-lg shadow-lg border border-slate-700/50"
                      onMouseEnter={() => setShowEducationMenu(true)}
                      onMouseLeave={() => setShowEducationMenu(false)}
                    >
                      {item.submenu.map((subItem, subIndex) => (
                        <Link
                          key={subIndex}
                          to={subItem.path}
                          className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-700/50 hover:text-white transition-colors duration-200"
                        >
                          {subItem.label}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </nav>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <button className="p-2 rounded-lg hover:bg-slate-800/60 text-slate-300 transition-colors duration-200">
                <Settings size={18} />
              </button>
              <button className="p-2 rounded-lg hover:bg-slate-800/60 text-slate-300 transition-colors duration-200">
                <HelpCircle size={18} />
              </button>
            </div>
            <button className="btn btn-primary hidden md:block">Connect Wallet</button>
            <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center">
              <span className="text-xs font-medium">GM</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;