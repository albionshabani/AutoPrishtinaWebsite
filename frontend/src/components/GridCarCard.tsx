// FILE: frontend/src/components/GridCarCard.tsx
// FINAL VERSION WITH FULL-WIDTH MOBILE IMAGE.
// The image now spans the full width on mobile views.

import { Link } from 'react-router-dom';
import { Car } from '../types';
import { useSavedCars } from '../hooks/useSavedCars';
import { normalizeFuelType } from '../utils';
import { FlagBadges } from './FlagBadges';
import { SaveButton } from './SaveButton';
import toast from 'react-hot-toast';
import { useMemo, useState, useEffect } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import { LazyLoadImage } from 'react-lazy-load-image-component';
import 'react-lazy-load-image-component/src/effects/blur.css';

import { FiCamera } from 'react-icons/fi';
import { TbRoad } from 'react-icons/tb';
import { FiCalendar } from 'react-icons/fi';
import { LuDroplets } from "react-icons/lu";
import { FaBolt } from "react-icons/fa6";
import { GiBoltDrop } from "react-icons/gi";
import { TbManualGearbox } from "react-icons/tb";

/**
 * Renders a single car specification item with an icon and value.
 */
const SpecItem = ({
  icon: Icon,
  value,
  iconClassName,
}: {
  icon: React.ElementType;
  value?: string | number | null;
  iconClassName?: string;
}) => (
  <div className="flex items-center gap-2 text-text-secondary">
    <Icon className={`w-5 h-5 flex-shrink-0 ${iconClassName || 'text-primary'}`} />
    <span className="font-medium text-sm whitespace-nowrap">{value || '-'}</span>
  </div>
);

/**
 * Image slider for car images, with lazy loading and image count.
 */
const CardImageSlider = ({ car }: { car: Car }) => {
  const [emblaRef] = useEmblaCarousel({ loop: true, align: 'start' });
  const [imageCount, setImageCount] = useState<number | null>(null);

  // Helper to build image URLs
  const getImageUrl = (base?: string, index?: string) => {
    if (!base) return '/placeholder.jpg';
    const queryParams =
      '?impolicy=heightRate&rh=600&cw=800&ch=600&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_04.png&wtmkg=SouthEast&wtmkw=1&wtmkh=1';
    return `${base}${index}.jpg${queryParams}`;
  };

  // Prepares the slider image URLs
  const sliderImageUrls = useMemo(() => {
    const primaryUrl = car?.['Image URL'] || '';
    return ['001', '002', '007', '006'].map(index => getImageUrl(primaryUrl, index));
  }, [car]);

  // Counts how many images are available for the car
  useEffect(() => {
        let isMounted = true;
        const countImages = async () => {
            const primaryUrl = car?.['Image URL'];
            if (!primaryUrl || !isMounted) {
                if (isMounted) setImageCount(0);
                return;
            }
            
            const range1 = Array.from({ length: 10 }, (_, i) => i + 1);
            const range2 = Array.from({ length: 10 }, (_, i) => i + 15);
            const imageNumbersToCheck = [...range1, ...range2];

            const promises = imageNumbersToCheck.map(num => {
                return new Promise<number>(resolve => {
                    const img = new Image();
                    const imgUrl = getImageUrl(primaryUrl, String(num).padStart(3, '0'));
                    img.onload = () => resolve(1);
                    img.onerror = () => resolve(0);
                    img.src = imgUrl;
                });
            });

            const results = await Promise.all(promises);
            if (isMounted) {
                const total = results.reduce((sum, count) => sum + count, 0);
                setImageCount(total > 0 ? total : 1);
            }
        };

        countImages();
        return () => { isMounted = false; };
    }, [car]);

  return (
    // On small screens (sm:), the rounded corners are applied to the slider itself.
    <div className="relative overflow-hidden group/slider sm:rounded-t-2xl" ref={emblaRef}>
      <div className="flex">
        {sliderImageUrls.map((url, index) => (
          <div className="flex-none w-full relative" key={index}>
            <LazyLoadImage
              effect="blur"
              src={url}
              alt={`${car.Brand} ${car.Model} view ${index + 1}`}
              wrapperClassName="w-full h-full"
              className="w-full h-auto object-cover aspect-[4/3] bg-subtle"
            />
          </div>
        ))}
      </div>
      <div className="absolute bottom-3 right-3 z-10 px-2 py-1 bg-black/50 backdrop-blur-sm rounded-md text-white text-xs font-semibold flex items-center gap-1.5">
        <FiCamera className="w-3 h-3" />
        <span>{imageCount ?? '...'}</span>
      </div>
    </div>
  );
};

/**
 * Main card component for displaying car info in a grid.
 */
export function GridCarCard({ car }: { car: Car }) {
  const { category, displayName } = normalizeFuelType(car.Fuel || '');
  const [savedCarIds, toggleSaveCar] = useSavedCars();
  const isSaved = savedCarIds.includes(car.ID);

  const handleSaveClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isSaved) {
      toast.success(`${car.Brand} ${car.Model} u ruajt!`, { id: 'save-notification' });
    } else {
      toast(`${car.Brand} ${car.Model} u hoq.`, { id: 'save-notification' });
    }
    toggleSaveCar(car.ID);
  };

  return (
    // The main container is now a simple div on mobile and becomes the card on larger screens.
    // The `sm:rounded-2xl`, `sm:border`, and `sm:shadow-md` classes apply the card styling only on `sm` and up.
    <div className="group relative bg-surface sm:rounded-2xl flex flex-col sm:border sm:border-border-secondary h-full sm:shadow-md transition-shadow duration-300 ease-in-out overflow-hidden hover:sm:shadow-xl">
      <div className="absolute top-3 right-3 z-20 bg-black/20 backdrop-blur-sm rounded-full">
        <SaveButton isSaved={isSaved} onClick={handleSaveClick} />
      </div>

      {/* 
        This wrapper now handles the full-width effect.
        - `sm:w-auto` resets the width for larger screens.
        - `-mx-4` with padding `px-4` on the parent would create a full-bleed effect if the parent had padding.
        - Assuming the parent grid has `gap-6`, we don't need negative margins if the card background is transparent on mobile.
      */}
      <Link to={`/car/${car.ID}`} className="block">
        <CardImageSlider car={car} />
      </Link>

      {/* The padding `p-4` is now on this content wrapper, so the image above is not affected. */}
      <div className="p-4 flex-grow flex flex-col w-full">
        <Link to={`/car/${car.ID}`} className="block">
          <h2 className="text-lg font-bold text-text-primary leading-tight truncate">
            {car.Brand} {car.Model}
          </h2>
          <p className="text-text-secondary text-sm truncate">{car.Badge || 'Standard Trim'}</p>
        </Link>

        <div className="mt-2 min-h-[28px]">
          <FlagBadges flags={car.flags} context="card" />
        </div>

        <div className="grid grid-cols-2 gap-x-4 gap-y-2 mt-3">
          <SpecItem icon={TbRoad} value={car['Mileage (km)']?.toLocaleString() + ' km'} />
          <SpecItem icon={FiCalendar} value={car.Year} />
          {category === 'electric' ? (
            <SpecItem icon={FaBolt} value={displayName} iconClassName="text-yellow-400" />
          ) : category === 'hybrid' ? (
            <SpecItem icon={GiBoltDrop} value={displayName} iconClassName="text-teal-600" />
          ) : (
            <SpecItem icon={LuDroplets} value={displayName} />
          )}
          <SpecItem icon={TbManualGearbox} value={car.Transmission} />
        </div>

        <div className="flex-grow" />

        <div className="flex items-baseline justify-between pt-2 border-t border-border-secondary mt-4">
            <p className="text-[0.625rem] text-text-secondary">
                Qmimi përfshin transportin deri në Durrës
            </p>
            <p className="text-lg font-bold text-text-primary">
                {car['Price (EUR)']?.toLocaleString()}
                <span className="text-primary font-semibold"> €</span>
            </p>
        </div>
      </div>
    </div>
  );
}