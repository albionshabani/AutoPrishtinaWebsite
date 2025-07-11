// This is a minimal version to ensure it doesn't crash. 
// We will replace its usage with GridCarCard, but this makes it safe.
import { Link } from 'react-router-dom';
import { Car } from '../types';

export const SimilarCarCard = ({ car }: { car: Car }) => {
  const imageUrl = car['Image URL']?.split(',')[0].trim();

  return (
    <Link to={`/car/${car.ID}`} className="block group">
      <div className="overflow-hidden rounded-lg">
        <img src={imageUrl} alt={`${car.Brand} ${car.Model}`} className="w-full h-40 object-cover transform group-hover:scale-105 transition-transform duration-300" />
      </div>
      <div className="mt-2">
        <h3 className="font-bold text-slate-800">{car.Brand} {car.Model}</h3>
        <p className="text-slate-600">{car.Year} · {car['Price (EUR)']?.toLocaleString('de-DE')} €</p>
      </div>
    </Link>
  );
};