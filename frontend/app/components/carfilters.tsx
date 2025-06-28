'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

const brands = [
  'All',
  'Hyundai',
  'Kia',
  'Genesis',
  'KG Mobility (Ssangyong)',
  'Renault Korea (Samsung)',
  'Chevrolet (GM Korea)'
];

const sortOptions = [
  { name: 'Price (High to Low)', value: 'Price_EUR,desc' },
  { name: 'Price (Low to High)', value: 'Price_EUR,asc' },
  { name: 'Mileage (Low to High)', value: 'Mileage_km,asc' },
  { name: 'Year (Newest First)', value: 'Year,desc' },
];

function debounce(func: (...args: any[]) => void, delay: number) {
  let timeout: NodeJS.Timeout;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}

export default function CarFilters() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [brand, setBrand] = useState(() => searchParams.get('brand') || 'All');
  const [sort, setSort] = useState(() => searchParams.get('sort_by') && searchParams.get('order') 
    ? `${searchParams.get('sort_by')},${searchParams.get('order')}` 
    : 'Price_EUR,desc'
  );

  const updateURL = useCallback(() => {
    const params = new URLSearchParams();

    if (brand && brand !== 'All') {
      params.set('brand', brand);
    }

    if (sort) {
      const [sortBy, order] = sort.split(',');
      params.set('sort_by', sortBy);
      params.set('order', order);
    }

    // Reset to page 1 on filter change
    params.set('page', '1');

    router.push(`/listings?${params.toString()}`, { scroll: false });
  }, [brand, sort, router]);

  const debouncedUpdateURL = useCallback(debounce(updateURL, 300), [updateURL]);

  useEffect(() => {
    debouncedUpdateURL();
  }, [brand, sort, debouncedUpdateURL]);

  return (
    <div className="p-4 bg-white rounded-lg shadow-md flex flex-wrap gap-x-6 gap-y-4 items-end justify-center border border-gray-300">
      <div>
        <label htmlFor="brand" className="block text-sm font-medium text-gray-700">Prodhuesi</label>
        <select
          id="brand"
          value={brand}
          onChange={e => setBrand(e.target.value)}
          className="mt-1 p-2 border border-gray-300 rounded-md shadow-sm text-lg w-48"
        >
          {brands.map(b => (
            <option key={b} value={b}>{b}</option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="sort" className="block text-sm font-medium text-gray-700">Rendit sipas</label>
        <select
          id="sort"
          value={sort}
          onChange={e => setSort(e.target.value)}
          className="mt-1 p-2 border border-gray-300 rounded-md shadow-sm text-lg w-60"
        >
          {sortOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.name}</option>
          ))}
        </select>
      </div>

      <button
        onClick={updateURL}
        className="bg-primary-blue hover:bg-blue-600 text-white font-bold py-2 px-8 text-lg rounded-md"
      >
        Kërko
      </button>
    </div>
  );
}
