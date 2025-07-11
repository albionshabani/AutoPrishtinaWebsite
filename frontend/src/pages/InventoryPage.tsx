// FILE: frontend/src/pages/InventoryPage.tsx
// FINAL, CORRECTED VERSION.
// Pagination is now fully functional while keeping your original, styled component.

import { useSearchParams } from 'react-router-dom';
import { useQuery, keepPreviousData } from '@tanstack/react-query';
import { useEffect, useState, useMemo } from 'react';
import { Helmet } from 'react-helmet-async';
import { fetchCars } from '../api';
import { CarCard } from '../components/CarCard';
import { GridCarCard } from '../components/GridCarCard';
import { useMediaQuery } from '../hooks/useMediaQuery';
import { FilterSidebar } from '../components/FilterSidebar';
import { CarCardSkeleton } from '../components/CarCardSkeleton';
import { SortByDropdown } from '../components/SortByDropdown';
import { Car } from '../types';
import { FiArrowUp, FiChevronLeft, FiChevronRight } from 'react-icons/fi';
import { AnimatePresence, motion } from 'framer-motion';
import { LuSlidersHorizontal } from "react-icons/lu";

// --- YOUR ORIGINAL PAGINATION COMPONENT (RESTORED & UNCHANGED) ---
const DOTS = '...';
const usePagination = ({ totalPages, currentPage, siblingCount = 1 }: { totalPages: number, currentPage: number, siblingCount?: number }) => { return useMemo(() => { const totalPageNumbers = siblingCount + 5; if (totalPageNumbers >= totalPages) { return Array.from({ length: totalPages }, (_, i) => i + 1); } const leftSiblingIndex = Math.max(currentPage - siblingCount, 1); const rightSiblingIndex = Math.min(currentPage + siblingCount, totalPages); const shouldShowLeftDots = leftSiblingIndex > 2; const shouldShowRightDots = rightSiblingIndex < totalPages - 2; const firstPageIndex = 1; const lastPageIndex = totalPages; if (!shouldShowLeftDots && shouldShowRightDots) { let leftItemCount = 3 + 2 * siblingCount; let leftRange = Array.from({ length: leftItemCount }, (_, i) => i + 1); return [...leftRange, DOTS, totalPages]; } if (shouldShowLeftDots && !shouldShowRightDots) { let rightItemCount = 3 + 2 * siblingCount; let rightRange = Array.from({ length: rightItemCount }, (_, i) => totalPages - rightItemCount + 1 + i); return [firstPageIndex, DOTS, ...rightRange]; } if (shouldShowLeftDots && shouldShowRightDots) { let middleRange = Array.from({ length: rightSiblingIndex - leftSiblingIndex + 1 }, (_, i) => leftSiblingIndex + i); return [firstPageIndex, DOTS, ...middleRange, DOTS, lastPageIndex]; } return []; }, [totalPages, currentPage, siblingCount]); };
const Pagination = ({ currentPage, totalPages, onPageChange }: { currentPage: number, totalPages: number, onPageChange: (page: number) => void }) => { 
    const paginationRange = usePagination({ currentPage, totalPages }); 
    if (currentPage === 0 || totalPages < 2) { return null; } 
    const onNext = () => onPageChange(currentPage + 1); 
    const onPrevious = () => onPageChange(currentPage - 1); 
    return ( 
        <nav className="flex justify-center sm:justify-end items-center gap-2 mt-8 py-4"> 
            <button onClick={onPrevious} disabled={currentPage === 1} className="flex items-center justify-center w-10 h-10 bg-surface rounded-md hover:bg-subtle disabled:opacity-50 disabled:cursor-not-allowed text-text-secondary border border-border-primary"><FiChevronLeft className="w-6 h-6" /></button> 
            {paginationRange.map((pageNumber, index) => { 
                if (pageNumber === DOTS) { return <span key={`${DOTS}-${index}`} className="px-2 py-2 text-text-secondary">...</span>; } 
                return (<button key={pageNumber} onClick={() => onPageChange(pageNumber as number)} className={`w-10 h-10 rounded-md font-semibold text-sm transition-colors ${ currentPage === pageNumber ? 'bg-blue-diagonal text-text-on-primary border-primary' : 'bg-surface text-text-primary hover:bg-subtle border border-border-primary' }`}>{pageNumber}</button>); 
            })} 
            <button onClick={onNext} disabled={currentPage === totalPages} className="flex items-center justify-center w-10 h-10 bg-blue-diagonal rounded-md hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed text-text-on-primary"><FiChevronRight className="w-6 h-6" /></button> 
        </nav> 
    ); 
};


const sortOptions = [
    { value: 'any', label: 'Renditja Standarde' },
    { value: 'bestDeals-desc', label: 'Renditja më e mirë' },
    { value: 'year-desc', label: 'Viti (Më të rejat)' },
    { value: 'year-asc', label: 'Viti (Më të vjetrat)' },
    { value: 'price-asc', label: 'Çmimi (Më i liri)' },
    { value: 'price-desc', label: 'Çmimi (Më i shtrenjti)' },
    { value: 'mileage-asc', label: 'Kilometrat (Më pak)' },
    { value: 'mileage-desc', label: 'Kilometrat (Më shumë)' },
];
const getDealScore = (car: Car): number => { let score = 0; if (!car.flags) return 0; if (car.flags.isGreatPrice) score += 5; if (car.flags.isWellMaintained) score += 4; if (car.flags.isLowMileage) score += 3; if (car.flags.isRareFind) score += 2; if (car.flags.isFirstOwner) score += 2; if (car.flags.isFullyLoaded) score += 1; return score; };

export function InventoryPage() {
  const isDesktop = useMediaQuery('(min-width: 1024px)');
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const [showScrollButton, setShowScrollButton] = useState(false);

  const currentPage = Number(searchParams.get('page') || '1');
  const sortBy = searchParams.get('sortBy');
  const order = searchParams.get('order');
  const currentSort = sortBy && order ? `${sortBy}-${order}` : 'any';
  
  const currentFilters = useMemo(() => Object.fromEntries(searchParams), [searchParams]);

  // --- **THIS IS THE DEFINITIVE FIX** ---
  // The queryFn now correctly calls `fetchCars` with the structure it expects:
  // an object containing both the query string and the current page number.
  const { data, isLoading, isError, isPlaceholderData } = useQuery({ 
    queryKey: ['cars', searchParams.toString()], 
    queryFn: () => fetchCars({ 
      queryParams: searchParams.toString(),
      pageParam: currentPage 
    }), 
    placeholderData: keepPreviousData,
  });
  
  const seo = useMemo(() => { const brand = searchParams.get('brand'); const model = searchParams.get('model'); let title = 'Inventari i Veturave - AutoPrishtina'; let description = 'Shfletoni inventarin tonë të veturave të përdorura premium.'; if (brand && model) { title = `Vetura ${brand} ${model} në shitje - AutoPrishtina`; description = `Gjeni vetura të përdorura ${brand} ${model}.`; } else if (brand) { title = `Vetura ${brand} në shitje - AutoPrishtina`; description = `Shikoni të gjitha veturat e markës ${brand}.`; } return { title, description }; }, [searchParams]);

  const handleApplyFilters = (newFilters: Record<string, any>) => { 
    const params = new URLSearchParams(searchParams);
    for (const key in newFilters) {
        const value = newFilters[key];
        if (value && value.length > 0) {
            if (Array.isArray(value)) {
                params.delete(key);
                value.forEach(v => params.append(key, v));
            } else {
                params.set(key, String(value));
            }
        } else {
            params.delete(key);
        }
    }
    params.set('page', '1');
    setSearchParams(params); 
    setIsFilterOpen(false); 
  };
  
  const handleSortChange = (value: string) => { 
    const params = new URLSearchParams(searchParams); 
    if (value === 'any') { 
      params.delete('sortBy'); 
      params.delete('order'); 
    } else { 
      const [sortBy, order] = value.split('-'); 
      params.set('sortBy', sortBy); 
      params.set('order', order); 
    } 
    params.set('page', '1'); 
    setSearchParams(params); 
  };

  const handlePageChange = (newPage: number) => { 
    const params = new URLSearchParams(searchParams); 
    params.set('page', String(newPage)); 
    setSearchParams(params); 
    window.scrollTo({ top: 0, behavior: 'smooth' }); 
  };

  useEffect(() => { const handleScroll = () => { setShowScrollButton(window.scrollY > 400); }; window.addEventListener('scroll', handleScroll); return () => window.removeEventListener('scroll', handleScroll); }, []);
  const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' });
  const sortedCars = useMemo(() => { if (!data?.cars) return []; if (currentSort === 'bestDeals-desc') { return [...data.cars].sort((a, b) => getDealScore(b) - getDealScore(a)); } return data.cars; }, [data?.cars, currentSort]);

  return (
    <>
      <Helmet> <title>{seo.title}</title> <meta name="description" content={seo.description} /> <link rel="canonical" href={window.location.href} /> </Helmet>
       <AnimatePresence>
        {isFilterOpen && !isDesktop && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setIsFilterOpen(false)} className="fixed inset-0 bg-black/60 z-50 lg:hidden" >
            <motion.div initial={{ x: '-100%' }} animate={{ x: 0 }} exit={{ x: '-100%' }} transition={{ type: 'spring', stiffness: 300, damping: 30 }} onClick={(e) => e.stopPropagation()} className="absolute inset-y-0 left-0 w-full max-w-sm bg-background" >
                <FilterSidebar isMobile={true} onClose={() => setIsFilterOpen(false)} initialFilters={currentFilters} onApplyFilters={handleApplyFilters} />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      <div className="container mx-auto px-4 lg:px-8 mt-4 lg:mt-8">
        <div className="flex flex-col lg:flex-row gap-8 items-start">
          <aside className="hidden lg:block lg:w-1/4 w-full h-full self-start top-24">
            <FilterSidebar isMobile={false} initialFilters={currentFilters} onApplyFilters={handleApplyFilters} />
          </aside>
          <main className="flex-grow w-full">
            <div className="mb-4 bg-white rounded-xl shadow-sm lg:shadow-none flex justify-between items-center gap-4">
              <div className="p-4">
                <div className="flex-1">
                 <h1 className="text-xl lg:text-2xl font-bold text-slate-900">Veturat e verifikuara</h1>
                 <p className="text-sm text-slate-500 mt-1">{data && `${data.totalItems.toLocaleString()} rezultate`}</p>
                </div>
              </div>
              <div className="lg:hidden h-[84px]">
                <button onClick={() => setIsFilterOpen(true)} className="flex items-center justify-center w-20 h-full bg-blue-diagonal text-white rounded-r-xl shadow-lg shadow-blue-500/30 hover:shadow-xl hover:-translate-y-px transition-all">
                    <LuSlidersHorizontal size={18} />
                </button>
              </div>
              <div className="hidden lg:block w-full max-w-[240px]">
                 <SortByDropdown options={sortOptions} value={currentSort} onChange={handleSortChange} />
              </div>
            </div>
            <div className="lg:hidden mb-4">
                 <SortByDropdown options={sortOptions} value={currentSort} onChange={handleSortChange} />
            </div>
            {isLoading ? ( <div className="space-y-6">{Array.from({ length: 9 }).map((_, i) => <CarCardSkeleton key={i} />)}</div> ) 
             : isError ? ( <div className="text-center p-12 text-red-500">Gabim në server.</div> ) 
             : (
              <div style={{ opacity: isPlaceholderData ? 0.7 : 1, transition: 'opacity 0.2s linear' }}>
                <div className={ isDesktop ? 'space-y-6' : 'grid grid-cols-1 sm:grid-cols-2 gap-6' }>
                  {sortedCars && sortedCars.length > 0 ? (
                    sortedCars.map(car => (
                      isDesktop ? <CarCard key={car.ID} car={car} /> : <GridCarCard key={car.ID} car={car} />
                    ))
                  ) : ( <div className="sm:col-span-2 text-center p-12 bg-surface rounded-lg shadow-md"><h2 className="text-2xl font-semibold">Nuk u gjet asnjë rezultat</h2></div> )}
                </div>
                {/* Using your original, styled Pagination component */}
                {data && data.totalPages > 1 && <Pagination currentPage={currentPage} totalPages={data.totalPages} onPageChange={handlePageChange}/>}
              </div>
            )}
          </main>
        </div>
      </div>
      <button onClick={scrollToTop} className={`fixed bottom-8 right-8 bg-blue-diagonal text-text-on-primary w-12 h-12 rounded-md flex items-center justify-center shadow-lg hover:opacity-90 transition-all z-50 ${showScrollButton ? 'opacity-100' : 'opacity-0'}`}> <FiArrowUp className="w-6 h-6" /> </button>
    </>
  );
};