'use client'; 

import { useState, useEffect } from 'react';
import useSWR from 'swr';
import { Calendar, Gauge, Droplets, Wrench, ShieldCheck, Car, User, Shield, Siren, AlertTriangle } from 'lucide-react';

const fetcher = (url: string) => fetch(url).then(res => {
    if (!res.ok) throw new Error('Car not found');
    return res.json();
});

export default function ListingDetailPage({ params }: { params: { id:string } }) {
    const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/listings/${params.id}`;
    const { data: car, error } = useSWR(apiUrl, fetcher);

    const [mainImage, setMainImage] = useState('');
    const [galleryImages, setGalleryImages] = useState<string[]>([]);

    useEffect(() => {
        if (car) {
            const imageBaseUrl = car['Image URL'].replace('_001.jpg', '');
            const timestamp = Date.now();
            const detailPolicy = `?impolicy=heightRate&rh=1200&cw=2000&ch=1200&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_04.png&wtmkg=SouthEast&wtmkw=1&wtmkh=1&t=${timestamp}`;

            const newGallery = Array.from({ length: 10 }, (_, i) => {
                const imageNumber = String(i + 1).padStart(3, '0');
                return `${imageBaseUrl}_${imageNumber}.jpg${detailPolicy}`;
            });

            setGalleryImages(newGallery);
            setMainImage(newGallery[0]);
        }
    }, [car]);

    if (error) return <main className="text-center p-20"><h1 className="text-xl">Vehicle not found.</h1></main>;
    if (!car) return <main className="text-center p-20"><h1 className="text-xl">Loading Vehicle Data...</h1></main>;

    const specItems = [
        { icon: <Calendar size={20}/>, label: 'Year', value: car.Year },
        { icon: <Gauge size={20}/>, label: 'Mileage', value: `${car['Mileage (km)'].toLocaleString()} km` },
        { icon: <Droplets size={20}/>, label: 'Fuel', value: car.Fuel },
        { icon: <Wrench size={20}/>, label: 'Transmission', value: car.Transmission },
        { icon: <ShieldCheck size={20}/>, label: 'Displacement', value: car['Displacement (cc)'] ? `${car['Displacement (cc)']} cc` : 'N/A' },
        { icon: <Car size={20}/>, label: 'Usage', value: car['Usage Type'] || 'N/A' },
        { icon: <User size={20}/>, label: 'Owner Changes', value: car['Owner Changes'] ?? 'N/A' },
        { icon: <Shield size={20}/>, label: 'Accidents', value: car['Accident Count'] ?? 'N/A' },
        { icon: <Siren size={20}/>, label: 'Tuning', value: car['Has Tuning'] ? 'Yes' : 'No' },
        { icon: <AlertTriangle size={20}/>, label: 'Open Recalls', value: car['Has Open Recall'] ? 'Yes' : 'No' },
    ];

    return (
        <div className="bg-light-gray min-h-screen py-12">
            <main className="container mx-auto p-4">
                <div className="bg-white p-6 md:p-8 rounded-2xl shadow-xl">
                    <div className="grid grid-cols-1 lg:grid-cols-10 gap-8">
                        
                        {/* Image Gallery Column */}
                        <div className="lg:col-span-6 flex flex-col gap-4">
                            <div className="w-full h-[350px] md:h-[500px] bg-gray-200 rounded-lg overflow-hidden">
                                {mainImage && <img src={mainImage} alt="Main vehicle view" className="w-full h-full object-cover"/>}
                            </div>
                            <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
                                {galleryImages.map((imgSrc, index) => (
                                    <div 
                                      key={index} 
                                      className={`h-16 bg-gray-200 rounded-md overflow-hidden cursor-pointer border-2 transition-all ${mainImage === imgSrc ? 'border-primary-teal scale-105' : 'border-transparent'}`} 
                                      onClick={() => setMainImage(imgSrc)}
                                    >
                                        <img src={imgSrc.replace('rh=1200&cw=2000&ch=1200', 'rh=240&cw=400&ch=240')} alt={`Thumbnail ${index + 1}`} className="w-full h-full object-cover" />
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Details Column */}
                        <div className="lg:col-span-4">
                            <h1 className="text-3xl md:text-4xl font-extrabold text-dark-text">{car.Brand} {car.Model}</h1>
                            <h2 className="text-xl md:text-2xl text-medium-text mb-4">{car.Badge}</h2>
                            <div className="bg-blue-50 text-blue-800 text-center py-4 px-6 rounded-lg my-4">
                                <span className="text-4xl font-bold">€{car['Price (EUR)'].toLocaleString()}</span>
                            </div>
                            
                            <div className="mt-6 border-t pt-6">
                                <h3 className="text-xl font-bold text-dark-text mb-4">Vehicle Specifications</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    {specItems.map(item => (
                                        <div key={item.label} className="flex items-center gap-3 p-2 bg-light-gray rounded-md">
                                            <div className="text-primary-teal">{item.icon}</div>
                                            <div>
                                                <p className="text-xs text-medium-text">{item.label}</p>
                                                <p className="font-bold text-dark-text">{String(item.value)}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}