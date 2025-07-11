import React from 'react';

type RangeOption = { value: string; label: string };

type RangeDropdownGroupProps = {
  fromOptions: RangeOption[];
  toOptions: RangeOption[];
  fromValue?: string;
  toValue?: string;
  onFromChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  onToChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
};

export function RangeDropdownGroup({ fromOptions, toOptions, fromValue, toValue, onFromChange, onToChange }: RangeDropdownGroupProps) {
  return (
    <div className="flex items-center border-2 border-gray-200 rounded-md bg-gray-50 focus-within:border-brand-blue focus-within:ring-1 focus-within:ring-brand-blue transition-all">
      {/* "From" Dropdown */}
      <select 
        value={fromValue || ''} 
        onChange={onFromChange}
        className="w-1/2 bg-transparent text-sm font-semibold text-gray-800 p-2.5 appearance-none focus:outline-none"
      >
        <option value="">Nga</option>
        {fromOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
      </select>

      {/* Separator */}
      <div className="w-px h-6 bg-gray-300"></div>

      {/* "To" Dropdown */}
      <select 
        value={toValue || ''} 
        onChange={onToChange}
        className="w-1/2 bg-transparent text-sm font-semibold text-gray-800 p-2.5 appearance-none focus:outline-none"
      >
        <option value="">Deri</option>
        {toOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
      </select>
    </div>
  );
}