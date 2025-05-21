import React, { useState, useRef, useEffect } from 'react';
import { Check, ChevronDown } from 'lucide-react';

interface FilterOption {
  id: string;
  name: string;
  category?: string;
}

interface FilterDropdownProps {
  label: string;
  options: FilterOption[];
  selectedValues: string[];
  onChange: (values: string[]) => void;
  grouped?: boolean;
}

const FilterDropdown: React.FC<FilterDropdownProps> = ({
  label,
  options,
  selectedValues,
  onChange,
  grouped = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [dropdownStyle, setDropdownStyle] = useState({
    top: 0,
    left: 0,
    width: 0,
  });

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (isOpen && buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      const scrollY = window.scrollY;
      
      setDropdownStyle({
        top: rect.bottom + scrollY,
        left: rect.left,
        width: rect.width,
      });
    }
  }, [isOpen]);

  const toggleOption = (optionId: string) => {
    const newValues = selectedValues.includes(optionId)
      ? selectedValues.filter(id => id !== optionId)
      : [...selectedValues, optionId];
    onChange(newValues);
  };

  const selectAll = () => {
    onChange(options.map(option => option.id));
  };

  const clearAll = () => {
    onChange([]);
  };

  // Group options by category if grouped is true
  const groupedOptions = grouped
    ? options.reduce((acc, option) => {
        const category = option.category || 'Other';
        if (!acc[category]) {
          acc[category] = [];
        }
        acc[category].push(option);
        return acc;
      }, {} as Record<string, FilterOption[]>)
    : { '': options };

  return (
    <div className="relative" ref={dropdownRef}>
      <label className="block text-xs text-slate-400 mb-1.5">{label}</label>
      <button
        ref={buttonRef}
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-slate-700/50 rounded-lg py-1.5 px-3 text-sm border border-slate-600/50 hover:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/25 transition-colors duration-200 text-left flex items-center justify-between"
      >
        <span className="truncate">
          {selectedValues.length === 0
            ? `Select ${label}`
            : selectedValues.length === 1
            ? options.find(opt => opt.id === selectedValues[0])?.name
            : `${selectedValues.length} selected`}
        </span>
        <ChevronDown 
          size={16} 
          className={`transition-transform duration-200 ml-2 ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      {isOpen && (
        <div 
          className="absolute z-50 bg-slate-800 rounded-lg border border-slate-700 shadow-lg"
          style={{
            top: 'calc(100% + 4px)',
            left: 0,
            width: '100%',
            maxHeight: '400px',
            overflowY: 'auto'
          }}
        >
          <div className="sticky top-0 p-2 border-b border-slate-700 bg-slate-800 z-[51]">
            <div className="flex items-center justify-between gap-2">
              <button
                onClick={selectAll}
                className="text-xs px-2 py-1 rounded hover:bg-slate-700 transition-colors"
              >
                Select All
              </button>
              <button
                onClick={clearAll}
                className="text-xs px-2 py-1 rounded hover:bg-slate-700 transition-colors"
              >
                Clear
              </button>
            </div>
          </div>

          <div className="relative">
            {Object.entries(groupedOptions).map(([category, categoryOptions]) => (
              <div key={category}>
                {grouped && category && (
                  <div className="sticky top-[41px] px-3 py-1.5 text-xs font-medium text-slate-400 bg-slate-800 border-b border-slate-700 z-[51]">
                    {category}
                  </div>
                )}
                {categoryOptions.map(option => (
                  <label
                    key={option.id}
                    className="flex items-center gap-2 px-3 py-2 hover:bg-slate-700/50 cursor-pointer"
                  >
                    <div className="relative flex items-center">
                      <input
                        type="checkbox"
                        checked={selectedValues.includes(option.id)}
                        onChange={() => toggleOption(option.id)}
                        className="hidden"
                      />
                      <div
                        className={`w-4 h-4 rounded border ${
                          selectedValues.includes(option.id)
                            ? 'bg-indigo-500 border-indigo-500'
                            : 'border-slate-600'
                        } transition-colors duration-200`}
                      >
                        {selectedValues.includes(option.id) && (
                          <Check size={12} className="text-white" />
                        )}
                      </div>
                    </div>
                    <span className="text-sm">{option.name}</span>
                  </label>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterDropdown;