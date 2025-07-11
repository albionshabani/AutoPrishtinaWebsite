// FILE: frontend/src/components/CarCard.tsx
// FINAL, CORRECTED VERSION: Image container is now full-width on mobile
// and two-up on desktop, as requested.

import { Link } from 'react-router-dom';
import { Car } from '../types';
import { LazyLoadImage } from 'react-lazy-load-image-component';
import 'react-lazy-load-image-component/src/effects/blur.css';
import { useSavedCars } from '../hooks/useSavedCars';
import { normalizeFuelType } from '../utils';
import { FlagBadges } from './FlagBadges';
import { SaveButton } from './SaveButton';
import toast from 'react-hot-toast';

// Your existing icons
import { TbRoad } from 'react-icons/tb';
import { FiCalendar } from 'react-icons/fi';
import { LuDroplets } from "react-icons/lu";
import { FaBolt } from "react-icons/fa6";
import { GiBoltDrop } from "react-icons/gi";
import { TbManualGearbox } from "react-icons/tb";

type CarCardProps = { car: Car };

const SpecItem = ({ icon: Icon, value, iconClassName }: { icon: React.ElementType; value?: string | number | null; iconClassName?: string; }) => ( <div className="flex items-center gap-2 text-slate-600"> <Icon className={`w-4 h-4 flex-shrink-0 ${iconClassName || 'text-blue-600'}`} /> <span className="font-medium text-sm whitespace-nowrap">{value || '-'}</span> </div> );

export function CarCard({ car }: CarCardProps) {
  const primaryImageUrl = car['Image URL'];
  
  const getImageUrl = (base?: string, index?: string) => {
      if (!base) {
          return '/placeholder.jpg';
      }
      const queryParams = `?impolicy=heightRate&rh=600&cw=800&ch=600&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_04.png&wtmkg=SouthEast&wtmkw=1&wtmkh=1`;
      return `${base}${index}.jpg${queryParams}`;
  }

  const firstImageUrl = getImageUrl(primaryImageUrl, '001');
  const interiorImageUrl = getImageUrl(primaryImageUrl, '007');
  const { category, displayName } = normalizeFuelType(car.Fuel || '');
  const [savedCarIds, toggleSaveCar] = useSavedCars();
  const isSaved = savedCarIds.includes(car.ID);

  const handleSaveClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const carName = `${car?.Brand || 'Makina'} ${car?.Model || ''}`.trim();

    if (!isSaved) {
      toast.success(`${carName} u ruajt!`, { id: 'save-notification' });
    } else {
      toast(`${carName} u hoq.`, { id: 'save-notification' });
    }

    if(car?.ID) {
      toggleSaveCar(car.ID);
    }
  };

  return (
    <Link to={`/car/${car.ID}`} className="group relative bg-white rounded-2xl flex flex-col sm:flex-row border border-slate-200/60 h-auto sm:h-44 shadow-md transition-shadow duration-300 ease-in-out hover:shadow-[0_8px_30px_rgb(0,0,0,0.08),_0_3px_8px_rgb(59,130,246,0.2)]">
      
      {/* --- THIS IS THE CORRECTED IMAGE CONTAINER --- */}
      <div className="relative w-full sm:w-2/5 flex items-center justify-center flex-shrink-0 h-44 sm:h-full gap-0.5">
        
        {/* Primary Image: Full width on mobile, half width on desktop */}
        <div className="relative w-full sm:w-1/2 h-full overflow-hidden rounded-t-2xl sm:rounded-l-lg sm:rounded-tr-none">
            <LazyLoadImage effect="blur" src={firstImageUrl} alt={`${car.Brand} ${car.Model}`} wrapperClassName="w-full h-full" className="absolute inset-0 w-full h-full object-cover" />
        </div>
        
        {/* Secondary (Interior) Image: Hidden on mobile, half width on desktop */}
        <div className="relative w-1/2 h-full overflow-hidden sm:rounded-r-lg sm:rounded-tr-none hidden sm:block">
            <LazyLoadImage effect="blur" src={interiorImageUrl} alt={`${car.Brand} ${car.Model} interior`} wrapperClassName="w-full h-full" className="absolute inset-0 w-full h-full object-cover" />
        </div>
      </div>

      {/* Details Div */}
      <div className="relative p-4 flex-grow flex flex-col w-full sm:w-3/5">
        
        <SaveButton isSaved={isSaved} onClick={handleSaveClick} />

        <div>
          <h2 className="text-lg font-bold text-slate-900 leading-tight truncate">{car.Brand} {car.Model}</h2>
          <p className="text-slate-500 text-sm truncate">{car.Badge || 'Standard Trim'}</p>
        </div>
        
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2">
            <SpecItem icon={TbRoad} value={car['Mileage (km)']?.toLocaleString() + ' km'} />
            <SpecItem icon={FiCalendar} value={car.Year} />
            {category === 'electric' ? <SpecItem icon={FaBolt} value={displayName} iconClassName="text-yellow-400" /> : category === 'hybrid' ? <SpecItem icon={GiBoltDrop} value={displayName} iconClassName="text-teal-600" /> : <SpecItem icon={LuDroplets} value={displayName} />}
            <SpecItem icon={TbManualGearbox} value={car.Transmission} />
        </div>
        
        <div className="flex-grow" />

        <div className="flex items-end justify-between pt-2 gap-4">
          <div className="flex-grow">
             <FlagBadges flags={car.flags} context="card" size="small" />
          </div>
          <div className="flex-shrink-0">
             <p className="text-xl font-bold text-slate-900 transition-colors group-hover:text-blue-600">
                {car['Price (EUR)']?.toLocaleString('de-DE')}
                <span className="text-blue-600"> €</span>
            </p>
          </div>
        </div>
      </div>
    </Link>
  );
}