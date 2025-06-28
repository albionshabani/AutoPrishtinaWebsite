'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState, useCallback } from 'react';
import useSWR from 'swr';
import { SlidersHorizontal, Bookmark, History } from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => res.json());

function debounce(func: (...args: any[]) => void, delay: number) {
  let timeout: NodeJS.Timeout;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

export default function AdvancedFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [filters, setFilters] = useState(() => ({
    brand: searchParams.get('brand') ?? '',
    model: searchParams.get('model') ?? '',
    fuel: searchParams.get('fuel') ?? '',
    transmission: searchParams.get('transmission') ?? '',
    price_min: searchParams.get('price_min') ?? '',
    price_max: searchParams.get('price_max') ?? '',
    year_min: searchParams.get('year_min') ?? '',
    year_max: searchParams.get('year_max') ?? '',
    mileage_min: searchParams.get('mileage_min') ?? '',
    mileage_max: searchParams.get('mileage_max') ?? '',
  }));

  const handleFilterChange = (key: string, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const updateURL = useCallback(() => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.set(key, value);
    });

    const sort_by = searchParams.get('sort_by') ?? 'Price_EUR';
    const order = searchParams.get('order') ?? 'desc';
    params.set('sort_by', sort_by);
    params.set('order', order);
    params.set('page', '1');

    router.push(`/listings?${params.toString()}`, { scroll: false });
  }, [filters, router, searchParams]);

  const debouncedUpdateURL = useCallback(debounce(updateURL, 500), [updateURL]);

  useEffect(() => {
    debouncedUpdateURL();
  }, [filters, debouncedUpdateURL]);

  // Use full API URL from env for filter options fetch
  const apiHost = process.env.NEXT_PUBLIC_API_URL || '';
  const { data: options, error } = useSWR(`${apiHost}/api/filter-options`, fetcher);

  if (error) return <div className="p-4 text-center text-red-500">Failed to load filter options.</div>;
  if (!options) return <div className="p-4 text-center">Loading filters...</div>;

  const renderSelect = (name: string, label: string, opts: string[]) => (
    <div className="mb-4">
      <label htmlFor={name} className="block text-sm font-semibold text-gray-700 mb-1">{label}</label>
      <select
        id={name}
        name={name}
        value={filters[name as keyof typeof filters]}
        onChange={e => handleFilterChange(name, e.target.value)}
        className="mt-1 block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-base shadow-sm focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue sm:text-sm"
      >
        <option value="">All</option>
        {opts.map(opt => <option key={opt} value={opt}>{opt}</option>)}
      </select>
    </div>
  );

  const renderInput = (name: string, placeholder: string) => (
    <input
      type="number"
      id={name}
      name={name}
      value={filters[name as keyof typeof filters]}
      onChange={e => handleFilterChange(name, e.target.value)}
      placeholder={placeholder}
      className="block w-full rounded-md border border-gray-300 bg-white py-2 px-3 text-base shadow-sm focus:border-primary-blue focus:outline-none focus:ring-1 focus:ring-primary-blue sm:text-sm"
      min={0}
    />
  );

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-300 max-w-sm mx-auto">
      <div className="flex border-b border-gray-300 mb-5">
        <button className="flex-1 border-b-2 border-primary-blue py-3 font-semibold text-primary-blue flex items-center justify-center gap-2">
          <SlidersHorizontal size={18} /> Filter
        </button>
        <button className="flex-1 py-3 font-semibold text-gray-500 hover:text-primary-blue flex items-center justify-center gap-2">
          <Bookmark size={18} /> Saved
        </button>
        <button className="flex-1 py-3 font-semibold text-gray-500 hover:text-primary-blue flex items-center justify-center gap-2">
          <History size={18} /> History
        </button>
      </div>

      {renderSelect('brand', 'PRODHUESI', options.brands || [])}
      {renderSelect('model', 'MODELI', options.models || [])}

      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 mb-1">ÇMIMI</label>
        <div className="flex gap-3">
          {renderInput('price_min', 'Nga')}
          {renderInput('price_max', 'Deri')}
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 mb-1">VITI</label>
        <div className="flex gap-3">
          {renderInput('year_min', 'Nga')}
          {renderInput('year_max', 'Deri')}
        </div>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 mb-1">KILOMETRAT E KALUAR</label>
        <div className="flex gap-3">
          {renderInput('mileage_min', 'Nga')}
          {renderInput('mileage_max', 'Deri')}
        </div>
      </div>

      {renderSelect('fuel', 'KARBURANTI', options.fuels || [])}
      {renderSelect('transmission', 'MARSHI', options.transmissions || [])}
    </div>
  );
}
