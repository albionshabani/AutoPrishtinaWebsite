'use client';

import Link from 'next/link';
import Image from 'next/image';
import { Calendar, Gauge, Droplets, Wrench, Camera, Heart } from 'lucide-react';

type Car = {
  ID: string;
  'Image URL'?: string;
  Brand?: string;
  Model?: string;
  Badge?: string;
  Year?: string;
  'Mileage (km)'?: number;
  Fuel?: string;
  Transmission?: string;
  'Price (EUR)'?: number;
};

type CarCardProps = {
  car: Car;
};

export default function CarCard({ car }: CarCardProps) {
  const timestamp = Date.now();
  const thumbnailPolicy = `?impolicy=heightRate&rh=600&cw=800&ch=600&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_04.png&wtmkg=SouthEast&wtmkw=1&wtmkh=1&t=${timestamp}`;
  const thumbnailUrl = car['Image URL'] ? car['Image URL'] + thumbnailPolicy : '/placeholder-image.png';

  const features = ['Digital Cockpit', 'Apple CarPlay', 'Android Auto'];

  return (
    <Link
      href={`/car/${car.ID}`}
      className="block max-w-xs mx-auto rounded-lg border border-gray-300 bg-white shadow hover:shadow-lg transition-transform duration-300 hover:-translate-y-1"
      aria-label={`View details for ${car.Brand ?? ''} ${car.Model ?? ''}`}
    >
      <div className="relative h-48 w-full">
        <Image
          src={thumbnailUrl}
          alt={`${car.Brand ?? ''} ${car.Model ?? ''}`}
          fill
          sizes="(max-width: 640px) 100vw, 400px"
          className="object-cover rounded-t-lg"
          unoptimized
          priority
        />
        <div className="absolute top-2 right-2 bg-white bg-opacity-70 rounded-full p-1 shadow hover:bg-red-500 hover:text-white cursor-pointer transition-colors">
          <Heart size={18} />
        </div>
        <div className="absolute bottom-2 right-2 bg-black bg-opacity-60 rounded-md px-2 py-0.5 flex items-center text-white text-xs font-semibold shadow-md">
          <Camera size={14} className="mr-1" />
          24
        </div>
      </div>

      <div className="p-4 flex flex-col h-full">
        <h2
          className="text-lg font-semibold text-gray-900 truncate"
          title={`${car.Brand ?? ''} ${car.Model ?? ''}`}
        >
          {car.Brand ?? 'Unknown Brand'} {car.Model ?? 'Unknown Model'}
        </h2>
        <p className="text-sm text-gray-500 truncate mb-2">{car.Badge ?? ''}</p>

        <div className="grid grid-cols-2 gap-4 text-gray-600 text-sm mb-3">
          <div className="flex items-center gap-1">
            <Calendar size={16} />
            <span>{car.Year ?? 'N/A'}</span>
          </div>
          <div className="flex items-center gap-1">
            <Gauge size={16} />
            <span>{car['Mileage (km)'] !== undefined ? car['Mileage (km)'].toLocaleString() : 'N/A'} km</span>
          </div>
          <div className="flex items-center gap-1">
            <Droplets size={16} />
            <span>{car.Fuel ?? 'N/A'}</span>
          </div>
          <div className="flex items-center gap-1">
            <Wrench size={16} />
            <span>{car.Transmission ?? 'N/A'}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {features.slice(0, 3).map((feature) => (
            <span
              key={feature}
              className="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded-full select-none"
            >
              {feature}
            </span>
          ))}
        </div>

        <div className="mt-auto border-t border-gray-200 pt-3 text-right">
          <p className="text-xl font-bold text-gray-900">
            €{car['Price (EUR)'] !== undefined ? car['Price (EUR)'].toLocaleString() : 'N/A'}
          </p>
          <p className="text-xs text-gray-500">Dogana e përfshirë në çmim</p>
        </div>
      </div>
    </Link>
  );
}
