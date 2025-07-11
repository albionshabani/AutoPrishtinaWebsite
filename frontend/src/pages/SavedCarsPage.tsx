import { useQuery } from '@tanstack/react-query';
import { Helmet } from 'react-helmet-async';
import { useSavedCars } from '../hooks/useSavedCars';
import { fetchCarsByIds } from '../api';
import { GridCarCard } from '../components/GridCarCard'; // We'll use the grid card for a nice gallery view

export const SavedCarsPage = () => {
  const [savedCarIds] = useSavedCars();

  const { data: savedCars, isLoading, isError } = useQuery({
    queryKey: ['savedCars', savedCarIds], // The query re-runs when savedCarIds changes
    queryFn: () => fetchCarsByIds(savedCarIds),
    enabled: savedCarIds.length > 0, // Only run the query if there are saved cars
  });

  return (
    <>
      <Helmet>
        <title>Veturat e Ruajtura - AutoPrishtina</title>
        <meta name="description" content="Shikoni listën tuaj të veturave të preferuara të ruajtura në AutoPrishtina." />
      </Helmet>
      <div className="bg-slate-50 min-h-screen">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-3xl font-extrabold text-slate-900 mb-6">Veturat e Mia të Ruajtura</h1>
          
          {isLoading ? (
            <p>Loading your saved cars...</p>
          ) : isError ? (
            <p className="text-red-500">Failed to load saved cars.</p>
          ) : !savedCars || savedCars.length === 0 ? (
            <div className="text-center py-16 px-6 bg-white rounded-lg shadow-sm">
                <h2 className="text-xl font-semibold text-slate-800">Nuk keni asnjë veturë të ruajtur.</h2>
                <p className="text-slate-500 mt-2">Kliko ikonën e zemrës tek një veturë për ta shtuar këtu.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {savedCars.map(car => (
                <GridCarCard key={car.ID} car={car} />
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};