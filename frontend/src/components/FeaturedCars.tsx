import { useQuery } from '@tanstack/react-query';
import useEmblaCarousel from 'embla-carousel-react';
import { fetchFeaturedCars } from '../api';
import { Car } from '../types';
import { GridCarCard } from './GridCarCard'; // Using the NEW GridCarCard
import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

export const FeaturedCars = () => {
  const { data: featuredCars, isLoading, isError } = useQuery<Car[]>({
    queryKey: ['featuredCars'],
    queryFn: fetchFeaturedCars,
    staleTime: 1000 * 60 * 5,
  });

  const [emblaRef, emblaApi] = useEmblaCarousel({
    align: 'start',
    loop: true,
  });

  if (isLoading || isError || !featuredCars || featuredCars.length === 0) {
    // Return a simple loading state or null to avoid layout shifts
    return null;
  }

  return (
    <div className="bg-white rounded-2xl p-6 lg:p-8 shadow-xl shadow-slate-900/5 border border-slate-100 -mt-20">
      <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-slate-900">
          Oferta Speciale
          </h2>
          <div className="flex gap-2">
              <button onClick={() => emblaApi?.scrollPrev()} className="bg-slate-100 hover:bg-slate-200 p-2 rounded-full text-slate-600 transition-colors"><FiChevronLeft size={20} /></button>
              <button onClick={() => emblaApi?.scrollNext()} className="bg-slate-100 hover:bg-slate-200 p-2 rounded-full text-slate-600 transition-colors"><FiChevronRight size={20} /></button>
          </div>
      </div>

      {/* THE FIX: The refined gradient mask applied to the container */}
          <div className="overflow-hidden -ml-6" ref={emblaRef}>
              <div className="flex">
                  {featuredCars.map(car => (
                      <div key={car.ID} className="flex-shrink-0 w-11/12 sm:w-1/2 md:w-1/3 lg:w-1/4 pl-6 py-4">
                          <GridCarCard car={car} />
                      </div>
                  ))}
              </div>
          </div>
      </div>
  );
};