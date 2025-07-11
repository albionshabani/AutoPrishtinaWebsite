// FILE: frontend/src/components/SearchForm.tsx
// This is your working file, with the layout updated to a responsive 3x2 grid.

import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { CustomSelect } from './CustomSelect';
import { fetchFilterOptions, fetchCarCount } from '../api';
import { getLogoUrl, normalizeBrandName } from '../utils';
import { PrimaryButton } from './PrimaryButton'; // Assuming you have this component
import { FiSearch } from 'react-icons/fi';


export function SearchForm() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({
    brand: 'any',
    model: 'any',
    yearFrom: 'any',
    priceTo: 'any',
    mileageTo: 'any'
  });

  const { data: optionsData, isLoading: isLoadingOptions } = useQuery({
    queryKey: ['filterOptions'],
    queryFn: fetchFilterOptions,
    staleTime: Infinity,
  });
  
  const queryParams = useMemo(() => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => { if (value !== 'any') params.append(key, value); });
    return params.toString();
  }, [filters]);

  const { data: carCount, isLoading: isLoadingCount } = useQuery({
    queryKey: ['carCount', queryParams],
    queryFn: () => fetchCarCount(queryParams),
  });

  const brandOptions = useMemo(() => {
    if (!optionsData?.brands) return [{ value: 'any', label: 'Marka' }];
    
    // 1. Normalize all raw brand names using the function from utils.ts
    const normalized = optionsData.brands.map(b => normalizeBrandName(b));
    
    // 2. Create a Set to get unique values, filter out junk, then sort alphabetically
    const uniqueCleanBrands = [...new Set(normalized)]
      .filter(b => b !== '...')
      .sort((a, b) => a.localeCompare(b));
      
    // 3. Map to the final format for the dropdown
    const finalOptions = uniqueCleanBrands.map(b => ({ value: b, label: b }));

    // 4. Return the final array with the "any" option at the start
    return [{ value: 'any', label: 'Marka' }, ...finalOptions];
  }, [optionsData]);

  const modelOptions = useMemo(() => { if (!optionsData || filters.brand === 'any') return [{ value: 'any', label: 'Modeli' }]; return [ { value: 'any', label: 'Çfarëdo Modeli' }, ...optionsData.models.filter(m => m.brand === filters.brand).map(m => ({ value: m.model, label: m.model })) ]; }, [optionsData, filters.brand]);
  const yearOptions = useMemo(() => ([ { value: 'any', label: 'Viti prej' }, ...(optionsData?.years.map(y => ({ value: y, label: y })) ?? []) ]), [optionsData]);
  const priceOptions = [ { value: 'any', label: 'Çmimi deri' }, { value: '5000', label: 'deri në €5,000' }, { value: '10000', label: 'deri në €10,000' }, { value: '20000', label: 'deri në €20,000' }, { value: '30000', label: 'deri në €30,000' }, { value: '40000', label: 'deri në €40,000' }, { value: '50000', label: 'deri në €50,000' }, { value: '100000', label: 'deri në €100,000' }, { value: '200000', label: 'deri në €200,000' } ];
  const mileageOptions = [ { value: 'any', label: 'Kilometra deri' }, { value: '30000', label: 'deri në 30,000 km' }, { value: '50000', label: 'deri në 50,000 km' }, { value: '100000', label: 'deri në 100,000 km' }, { value: '150000', label: 'deri në 150,000 km' }, { value: '200000', label: 'deri në 200,000 km' }, { value: '300000', label: 'deri në 300,000 km' }, { value: '400000', label: 'deri në 400,000 km' } ];

  const handleFilterChange = (filterName: keyof typeof filters, value: string) => { setFilters(prev => ({ ...prev, [filterName]: value, ...(filterName === 'brand' && { model: 'any' }) })); };

  const handleSearch = () => { navigate(`/inventory?${queryParams}`); };
  
  const buttonText = (isLoadingOptions || isLoadingCount) ? 'Kërko...' : `${(carCount ?? 0).toLocaleString()} Oferta`;

  return (
    <div className="w-full max-w-5xl p-6 bg-white backdrop-blur-lg rounded-2xl shadow-xl shadow-slate-1000/5 border border-white/10">
      
      {/* --- THIS IS THE 3x2 GRID LAYOUT YOU WANTED --- */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        
        {/* Row 1 */}
        <CustomSelect placeholder="Marka" options={brandOptions} value={filters.brand} onChange={(val) => handleFilterChange('brand', val)} getIcon={getLogoUrl} />
        <CustomSelect placeholder="Modeli" options={modelOptions} value={filters.model} onChange={(val) => handleFilterChange('model', val)} disabled={filters.brand === 'any'} />
        <CustomSelect placeholder="Cmimi deri" options={priceOptions} value={filters.priceTo} onChange={(val) => handleFilterChange('priceTo', val)} />
        
        {/* Row 2 */}
        <CustomSelect placeholder="Regjistrimi prej" options={yearOptions} value={filters.yearFrom} onChange={(val) => handleFilterChange('yearFrom', val)} />
        <CustomSelect placeholder="Kilometrazhi deri" options={mileageOptions} value={filters.mileageTo} onChange={(val) => handleFilterChange('mileageTo', val)} />
        
        {/* The button now correctly sits in the last cell of the grid */}
        <PrimaryButton onClick={handleSearch} icon={FiSearch} className="h-[50px]">
          {buttonText}
        </PrimaryButton>
      </div>
      
      <div className="text-center mt-4">
          <button onClick={() => navigate('/inventory')} className="text-blue-500 font-semibold text-gray-300 hover:text-blue-600 transition-colors">
              Kërkim i detajuar
          </button>
      </div>
    </div>
  );
};