// FILE: frontend/src/components/BrandShowcase.tsx

import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { fetchFilterOptions } from '../api';
import { getLogoUrl } from '../utils';
import { useState } from 'react';

// --- UI IMPROVEMENT: A small component to handle logo loading and fallbacks ---
const BrandLogo = ({ brand }: { brand: string }) => {
    const [logoError, setLogoError] = useState(false);
    const logoUrl = getLogoUrl(brand);

    if (logoError) {
        // If the logo fails, display the brand name text instead
        return <span className="text-center font-semibold text-slate-700">{brand}</span>;
    }

    return (
        <img 
            src={logoUrl} 
            alt={brand} 
            className="h-full w-full object-contain"
            // Set error state if the image fails to load
            onError={() => setLogoError(true)}
        />
    );
};


export const BrandShowcase = () => {
    const { data: filterOptions, isLoading, isError } = useQuery({
        queryKey: ['filterOptions'],
        queryFn: fetchFilterOptions,
        staleTime: Infinity,
    });

    if (isLoading || isError || !filterOptions?.brands) return null;
    
    // Define a curated list of top brands to ensure quality display
    const topBrands = ["Hyundai", "Kia", "Genesis", "Chevrolet (GM Daewoo)", "SsangYong", "Renault Samsung", "BMW", "Mercedes-Benz", "Audi", "Volkswagen", "Porsche", "Ford", "KG Mobility (SsangYong)"];
    const brandsToShow = filterOptions.brands.filter(b => topBrands.includes(b)).slice(0, 12);

    return (
        <motion.section 
            initial={{ opacity: 0, y: 50 }} 
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.2 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
        >
            <div className="text-center max-w-2xl mx-auto mb-12">
                <h2 className="text-3xl md:text-4xl font-extrabold text-slate-900 tracking-tight">Eksploroni Sipas Markës</h2>
                <p className="mt-4 text-lg text-slate-600">Zgjidhni prodhuesin tuaj të preferuar për të parë inventarin tonë.</p>
            </div>
            <div className="flex justify-center flex-wrap gap-4">
                {brandsToShow.map(brand => (
                    <Link
                        key={brand}
                        to={`/inventory?brand=${encodeURIComponent(brand)}`}
                        className="group p-4 bg-white rounded-xl border border-slate-200/80 shadow-lg shadow-slate-900/5 flex items-center justify-center 
                                   h-20 w-32 grayscale opacity-60 hover:grayscale-0 hover:opacity-100 hover:shadow-xl hover:border-slate-300 hover:scale-105 transition-all duration-300"
                    >
                        {/* --- UI IMPROVEMENT: Use the new BrandLogo component --- */}
                        <BrandLogo brand={brand} />
                    </Link>
                ))}
            </div>
        </motion.section>
    );
};