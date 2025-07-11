// FILE: frontend/src/components/FilterSidebar.tsx
// This is the complete, final version that is aware of mobile/desktop layouts.

import { useQuery } from "@tanstack/react-query";
import { useEffect, useState, useMemo } from "react";
import { fetchCarCount, fetchFilterOptions } from "../api";
import { useDebounce } from "../hooks/useDebounce"; 
import { getLogoUrl } from '../utils';
import { TextWithSuggestionsInput } from './TextWithSuggestionsInput';
import { NumberWithPresetsInput } from './NumberWithPresetsInput';
import { FilterGroup } from "./FilterGroup";
import { CheckboxFilter } from "./CheckboxFilter";
import { PrimaryButton } from "./PrimaryButton";
import { FiLoader, FiX } from "react-icons/fi";
import { LuSlidersHorizontal } from "react-icons/lu";
import { FaSearch } from "react-icons/fa";

type FilterValues = Record<string, string>;

// ADDED new props for mobile responsiveness
type FilterSidebarProps = { 
  initialFilters: FilterValues; 
  onApplyFilters: (newFilters: FilterValues) => void;
  isMobile?: boolean; // Prop to know if we are in the mobile modal view
  onClose?: () => void; // Prop to close the mobile modal
};

export function FilterSidebar({ initialFilters, onApplyFilters, isMobile, onClose }: FilterSidebarProps) {
  const [localFilters, setLocalFilters] = useState<FilterValues>(initialFilters);
  const debouncedFilters = useDebounce(localFilters, 400);

  const { data: carCount, isLoading: isCountLoading } = useQuery({
    queryKey: ['carCount', debouncedFilters],
    queryFn: () => {
        const params = new URLSearchParams(debouncedFilters).toString();
        return fetchCarCount(params);
    },
    placeholderData: 0,
    staleTime: 500, // Added a short stale time for responsiveness
  });

  useEffect(() => { setLocalFilters(initialFilters); }, [initialFilters]);

  const { data: optionsData } = useQuery({ queryKey: ['filterOptions'], queryFn: fetchFilterOptions, staleTime: Infinity });

  // Your existing handlers and options logic is perfect and unchanged.
  const handleFilterChange = (key: string, value: string | boolean) => {
    setLocalFilters(prev => {
      const newFilters = { ...prev };
      if (value) { newFilters[key] = String(value); } else { delete newFilters[key]; }
      if (key === 'brand') { delete newFilters['model']; }
      return newFilters;
    });
  };
  const generateOptions = (items: string[] | undefined) => items?.map(i => ({ value: i, label: i })) ?? [];
  const brandOptions = useMemo(() => generateOptions(optionsData?.brands), [optionsData]);
  const modelOptions = useMemo(() => {
    if (!optionsData || !localFilters.brand) return [];
    return optionsData.models.filter(m => m.brand === localFilters.brand).map(m => ({ value: m.model, label: m.model }));
  }, [optionsData, localFilters.brand]);
  const transmissionOptions = [{ value: 'Automatic', label: 'Automatic' }, { value: 'Manual', label: 'Manual' }];
  const fuelOptions = useMemo(() => generateOptions(optionsData?.fuels), [optionsData]);
  const yearOptions = useMemo(() => generateOptions(optionsData?.years), [optionsData]);
  const generateNumericPresets = (max: number, step: number, start = step) => Array.from({ length: Math.floor(max / step) }, (_, i) => start + i * step).map(v => ({ value: String(v), label: v.toLocaleString() }));
  const smartPricePresets = [...generateNumericPresets(20000, 5000, 5000), ...generateNumericPresets(100000, 10000, 30000)];
  const mileagePresets = generateNumericPresets(500000, 50000);
  const handleClearFilters = () => { setLocalFilters({}); onApplyFilters({}); };

  return (
    // If mobile, it's a column layout with padding. If desktop, it uses your existing styles.
    <div className={`bg-surface h-full flex flex-col ${isMobile ? 'p-6' : 'p-5 rounded-2xl shadow-xl border border-border-secondary'}`}>
      
      {/* --- THIS IS THE NEW RESPONSIVE HEADER --- */}
      <div className="flex justify-between items-center border-b border-border-secondary pb-4">
        <h2 className="text-xl font-bold text-text-primary flex items-center gap-2">
            <LuSlidersHorizontal /> Filtro
        </h2>
        {/* The X button to close the modal, only shown in mobile view */}
        {isMobile && onClose && (
            <button onClick={onClose} className="p-1 -mr-1 text-text-secondary hover:text-text-primary">
                <FiX size={24} />
            </button>
        )}
        {/* The "Pastro" button, only shown if filters are active */}
        {Object.keys(localFilters).length > 0 && !isMobile && (
          <button onClick={handleClearFilters} className="text-sm font-semibold text-text-secondary hover:text-primary">Pastro</button>
        )}
      </div>

      {/* --- Main content area now scrolls independently on mobile --- */}
      <div className="flex-grow overflow-y-auto py-4 -mx-2 px-2 space-y-1">
        <FilterGroup title="Prodhuesi dhe Modeli"><div className="space-y-3"><TextWithSuggestionsInput placeholder="Marka" options={brandOptions} value={localFilters.brand || ''} onChange={(val) => handleFilterChange('brand', val)} getIcon={getLogoUrl} /><TextWithSuggestionsInput placeholder="Modeli" options={modelOptions} value={localFilters.model || ''} onChange={(val) => handleFilterChange('model', val)} disabled={!localFilters.brand} /></div></FilterGroup>
        <FilterGroup title="Çmimi (€)"><div className="grid grid-cols-2 gap-3"><NumberWithPresetsInput placeholder="Nga" presets={smartPricePresets} value={localFilters.priceFrom || ''} onChange={(val) => handleFilterChange('priceFrom', val)} /><NumberWithPresetsInput placeholder="Deri" presets={smartPricePresets} value={localFilters.priceTo || ''} onChange={(val) => handleFilterChange('priceTo', val)} /></div></FilterGroup>
        <FilterGroup title="Viti i Prodhimit"><div className="grid grid-cols-2 gap-3"><NumberWithPresetsInput placeholder="Nga" presets={yearOptions} value={localFilters.yearFrom || ''} onChange={(val) => handleFilterChange('yearFrom', val)} format="year" /><NumberWithPresetsInput placeholder="Deri" presets={yearOptions} value={localFilters.yearTo || ''} onChange={(val) => handleFilterChange('yearTo', val)} format="year" /></div></FilterGroup>
        <FilterGroup title="Kilometrat e Kaluar"><div className="grid grid-cols-2 gap-3"><NumberWithPresetsInput placeholder="Nga" presets={mileagePresets} value={localFilters.mileageFrom || ''} onChange={(val) => handleFilterChange('mileageFrom', val)} /><NumberWithPresetsInput placeholder="Deri" presets={mileagePresets} value={localFilters.mileageTo || ''} onChange={(val) => handleFilterChange('mileageTo', val)} /></div></FilterGroup>
        <FilterGroup title="Marshi"><TextWithSuggestionsInput placeholder="Marshi" options={transmissionOptions} value={localFilters.transmission || ''} onChange={(val) => handleFilterChange('transmission', val)} /></FilterGroup>
        <FilterGroup title="Karburanti"><TextWithSuggestionsInput placeholder="Karburanti" options={fuelOptions} value={localFilters.fuel || ''} onChange={(val) => handleFilterChange('fuel', val)} /></FilterGroup>
        <FilterGroup title="Specifika"><CheckboxFilter label="Vetura pa aksidente" checked={localFilters.hasAccidents === 'false'} onChange={(c) => handleFilterChange('hasAccidents', c ? 'false' : '')}/><CheckboxFilter label="Pronar i vetëm" checked={localFilters.singleOwner === 'true'} onChange={(c) => handleFilterChange('singleOwner', c ? 'true' : '')}/><CheckboxFilter label="Me rikthim në fabrikë" checked={localFilters.hasRecall === 'true'} onChange={(c) => handleFilterChange('hasRecall', c ? 'true' : '')}/></FilterGroup>
      </div>

      {/* --- Footer with the main action button --- */}
      <div className="mt-auto pt-6 border-t border-border-secondary">
        <PrimaryButton onClick={() => onApplyFilters(localFilters)} icon={FaSearch}>
          {isCountLoading ? ( 
            <FiLoader className="animate-spin" /> 
          ) : ( 
            <span>{carCount?.toLocaleString() || 0} Rezultate</span> 
          )}
        </PrimaryButton>
      </div>
    </div>
  );
};