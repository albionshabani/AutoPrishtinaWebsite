'use client';

import CarCard from '@/components/carcard';
import AdvancedFilters from '@/components/advancedfilters';
import PaginationControls from '@/components/paginationcontrols';
import { ListFilter } from 'lucide-react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

async function fetchListings(params: Record<string, string>) {
  const query = new URLSearchParams(params);
  const apiHost = process.env.NEXT_PUBLIC_API_URL || '';
  const res = await fetch(`${apiHost}/api/listings?${query.toString()}`, { cache: 'no-store' });
  if (!res.ok) {
    throw new Error('Failed to fetch listings');
  }
  return res.json();
}

export default function ListingsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [listings, setListings] = useState<any[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const brand = searchParams.get('brand') || undefined;
  const sort_by = searchParams.get('sort_by') || 'Price_EUR';
  const order = searchParams.get('order') || 'desc';
  const page = searchParams.get('page') || '1';
  const per_page = searchParams.get('per_page') || '20';

  const params = {
    ...(brand ? { brand } : {}),
    sort_by,
    order,
    page,
    per_page,
  };

  useEffect(() => {
    setLoading(true);
    setError('');
    fetchListings(params)
      .then((data) => {
        setListings(data.listings);
        setTotalCount(data.totalCount);
        setTotalPages(data.totalPages);
      })
      .catch(() => setError('Could not load vehicle listings.'))
      .finally(() => setLoading(false));
  }, [brand, sort_by, order, page, per_page]);

  function handlePageChange(newPage: number) {
    const newParams = new URLSearchParams(searchParams.toString());
    newParams.set('page', newPage.toString());
    router.push(`/listings?${newParams.toString()}`, { scroll: false });
  }

  if (error) {
    return (
      <main className="container mx-auto p-4 sm:p-6">
        <h1 className="text-2xl font-bold mb-4">An Error Occurred</h1>
        <p>{error}</p>
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <main className="container mx-auto px-4 sm:px-6">
        <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-8">
          {/* Sidebar filters */}
          <aside className="sticky top-20 self-start bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <AdvancedFilters />
          </aside>

          {/* Listings grid */}
          <section>
            <div className="flex justify-between items-center mb-6 p-4 bg-white rounded-lg shadow-sm">
              <h1 className="text-xl font-bold text-gray-900">
                Veturat e verifikuara{' '}
                <span className="text-gray-600 font-normal">({totalCount.toLocaleString()} rezultate)</span>
              </h1>
              <div className="flex items-center gap-2 border border-gray-300 rounded-md px-3 py-1.5">
                <ListFilter size={16} className="text-gray-600" />
                <span className="text-sm font-medium text-gray-900">Më të rejat</span>
              </div>
            </div>

            {loading ? (
              <p className="text-center text-lg py-20">Loading vehicles...</p>
            ) : listings.length === 0 ? (
              <div className="text-center py-16 bg-white rounded-lg shadow-sm">
                <h2 className="text-2xl font-semibold">No vehicles found</h2>
                <p className="text-gray-600 mt-2">Try adjusting your filters to find your perfect car.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {listings.map((car) => (
                  <CarCard key={car.ID} car={car} />
                ))}
              </div>
            )}

            <div className="mt-12 flex justify-center">
              <PaginationControls totalPages={totalPages} onPageChange={handlePageChange} />
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
