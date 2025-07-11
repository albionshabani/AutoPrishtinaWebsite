// FILE: frontend/src/pages/CarDetailPage.tsx
// THIS IS THE COMPLETE AND CORRECTED FILE.
// It makes the SimilarCarsSection background transparent and restores the arrow buttons to the header.

import { useState, useMemo, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { fetchCarById, fetchSimilarCars } from '../api';
import { Car } from '../types';
import { motion, AnimatePresence, Variants } from 'framer-motion';
import useEmblaCarousel from 'embla-carousel-react';
import { Helmet } from 'react-helmet-async';
import { getLogoUrl, normalizeFuelType, normalizeBrandName } from '../utils';
import { useSavedCars } from '../hooks/useSavedCars';
import { FlagBadges } from '../components/FlagBadges';
import { CarCard } from '../components/CarCard';

// Icons
import {
  FiLoader,
  FiAlertTriangle,
  FiChevronLeft,
  FiChevronRight,
  FiHelpCircle,
  FiChevronDown,
} from 'react-icons/fi';
import {
  TbRoad,
  TbCar,
  TbColorSwatch,
  TbEngine,
  TbFingerprint,
} from 'react-icons/tb';
import { BsFillFuelPumpFill, BsClockHistory, BsShieldCheck } from 'react-icons/bs';
import { GiGearStick } from 'react-icons/gi';
import { MdEventSeat, MdVerifiedUser } from 'react-icons/md';
import { IoIosHeart, IoIosHeartEmpty } from 'react-icons/io';
import toast from 'react-hot-toast';
import { FaCarCrash, FaUsers, FaWhatsapp } from 'react-icons/fa';

// --- HELPER COMPONENTS ---

const ImageCarousel = ({ car }: { car: Car }) => {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [mainRef, mainApi] = useEmblaCarousel({ loop: true });
  const [thumbRef, thumbApi] = useEmblaCarousel({ containScroll: 'keepSnaps', dragFree: true });
  const [imageUrls, setImageUrls] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const getFullImageUrl = (base?: string, index?: string) => {
    if (!base) return '/placeholder.jpg';
    return `${base}${index}.jpg?impolicy=heightRate&rh=1200&cw=2000&ch=1200&cg=Center&wtmk=http://ci.encar.com/wt_mark/w_mark_04.png&wtmkg=SouthEast&wtmkw=1&wtmkh=1`;
  };

  useEffect(() => {
    let isMounted = true;
    const findImages = async () => {
      setIsLoading(true);
      const base = car['Image URL'];
      if (!base) {
        if (isMounted) setIsLoading(false);
        return;
      }
      const checkUrl = (url: string) => new Promise<boolean>((resolve) => { const img = new window.Image(); img.onload = () => resolve(true); img.onerror = () => resolve(false); img.src = url; });
      const range1 = Array.from({ length: 10 }, (_, i) => i + 1);
      const range2 = Array.from({ length: 10 }, (_, i) => i + 15);
      const promises = [...range1, ...range2].map(async (num) => {
        const formattedIndex = String(num).padStart(3, '0');
        const url = getFullImageUrl(base, formattedIndex);
        const isValid = await checkUrl(url);
        if (isValid) return getFullImageUrl(base, formattedIndex);
        return null;
      });
      const results = await Promise.all(promises);
      if (isMounted) { setImageUrls(results.filter((url): url is string => url !== null)); setIsLoading(false); }
    };
    findImages();
    return () => { isMounted = false; };
  }, [car['Image URL']]);

  const onThumbClick = useCallback((index: number) => mainApi?.scrollTo(index), [mainApi]);
  const onSelect = useCallback(() => { if (!mainApi || !thumbApi) return; setSelectedIndex(mainApi.selectedScrollSnap()); thumbApi.scrollTo(mainApi.selectedScrollSnap()); }, [mainApi, thumbApi, setSelectedIndex]);

  useEffect(() => { if (mainApi) { onSelect(); mainApi.on('select', onSelect); mainApi.on('reInit', onSelect); } }, [mainApi, onSelect]);

  if (isLoading) return <div className="aspect-[4/3] w-full bg-slate-200 rounded-2xl animate-pulse"></div>;
  if (imageUrls.length === 0) return <div className="aspect-[4/3] w-full bg-slate-200 rounded-2xl flex items-center justify-center text-slate-500">No Images Available</div>;

  return (
    <div className="relative">
      <Link to={`/inventory?brand=${encodeURIComponent(car.Brand)}`} className="absolute top-4 left-4 z-10 flex items-center justify-center p-3 bg-gradient-to-br from-white/95 to-slate-100/80 backdrop-blur-md rounded-2xl border border-white/50 shadow-lg shadow-black/5 transition-all duration-300 hover:shadow-xl hover:scale-105"><img src={getLogoUrl(car.Brand)} alt={`${car.Brand} logo`} className="h-8 max-w-[120px] object-contain" /></Link>
      <div className="overflow-hidden rounded-2xl shadow-2xl shadow-slate-900/10" ref={mainRef}><div className="flex">{imageUrls.map((url, index) => (<div className="relative flex-grow-0 flex-shrink-0 w-full" key={index}><img src={url} alt={`View ${index + 1} of ${car.Year} ${car.Brand} ${car.Model}`} className="w-full h-auto object-cover bg-slate-200 aspect-[4/3]" /></div>))}</div></div>
      <button onClick={() => mainApi?.scrollPrev()} className="absolute top-1/2 left-4 -translate-y-1/2 bg-white/80 backdrop-blur-sm text-slate-800 p-2 rounded-full hover:bg-white shadow-lg transition-all"><FiChevronLeft size={24} /></button>
      <button onClick={() => mainApi?.scrollNext()} className="absolute top-1/2 right-4 -translate-y-1/2 bg-white/80 backdrop-blur-sm text-slate-800 p-2 rounded-full hover:bg-white shadow-lg transition-all"><FiChevronRight size={24} /></button>
      <div className="mt-4 overflow-hidden" ref={thumbRef}><div className="flex space-x-3 p-1">{imageUrls.map((url, index) => (<button key={index} onClick={() => onThumbClick(index)} className={`w-28 h-[70px] rounded-lg flex-shrink-0 transition-all duration-300 border-2 overflow-hidden ${index === selectedIndex ? 'border-primary' : 'border-transparent opacity-60 hover:opacity-100'}`}><img src={`${url.split('?')[0]}?impolicy=heightRate&rh=140&cw=224`} alt={`Thumbnail ${index + 1}`} className="w-full h-full object-cover" /></button>))}</div></div>
    </div>
  );
};

const CollapsibleSection = ({ title, children, count, defaultOpen = false }: { title: string; children: React.ReactNode; count?: number; defaultOpen?: boolean; }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  const contentVariants: Variants = { collapsed: { height: 0, opacity: 0, marginTop: 0 }, open: { height: 'auto', opacity: 1, marginTop: '1rem', transition: { duration: 0.3, ease: 'easeInOut' } } };
  return (
    <div className="bg-white rounded-2xl border border-border-secondary p-4 sm:p-6 shadow-xl shadow-slate-900/5">
      <button onClick={() => setIsOpen(!isOpen)} className="w-full flex justify-between items-center text-left" aria-expanded={isOpen}>
        <div className="flex items-center gap-3"><h3 className="text-lg sm:text-xl font-bold text-text-primary">{title}</h3>{count !== undefined && count > 0 && (<span className="bg-primary/10 text-primary font-semibold text-xs px-2.5 py-1 rounded-full">{count}</span>)}</div>
        <FiChevronDown className="text-text-secondary transition-transform duration-300" style={{ transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)' }}/>
      </button>
      <AnimatePresence initial={false}>{isOpen && (<motion.div key="content" initial="collapsed" animate="open" exit="collapsed" variants={contentVariants} style={{ overflow: 'hidden' }}>{children}</motion.div>)}</AnimatePresence>
    </div>
  );
};

const SpecItem = ({ label, value, icon: Icon }: { label: string; value: React.ReactNode; icon?: React.ElementType; }) => {
  if (value === null || value === undefined || value === '') return null;
  return (<div className="flex justify-between items-center py-3.5"><div className="flex items-center gap-2 text-text-secondary">{Icon && <Icon className="w-4 h-4 text-primary" />}<p>{label}</p></div><p className="font-semibold text-text-primary text-right">{value}</p></div>);
};

const AnimatedSection = ({ children, className = '' }: { children: React.ReactNode; className?: string; }) => (<motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, ease: 'easeOut' }} className={className}>{children}</motion.div>);

// ** CORRECTED SimilarCarsSection **
const SimilarCarsSection = ({ currentCarId }: { currentCarId: string }) => {
    const { data: similarCars, isLoading, isError } = useQuery<Car[]>({ queryKey: ['similarCars', currentCarId], queryFn: () => fetchSimilarCars(currentCarId), });
    const [emblaRef, emblaApi] = useEmblaCarousel({
        align: 'center',
        containScroll: 'trimSnaps',
    });
    
    if (isLoading || isError || !similarCars || similarCars.length === 0) return null;

    return (
        <AnimatedSection>
            {/* The wrapper div is now transparent, without bg-white, border, or shadow */}
            <div>
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-lg sm:text-xl font-bold text-text-primary">Vetura të ngjashme</h3>
                    {/* Arrow buttons are restored to the header */}
                    <div className="flex gap-2">
                        <button onClick={() => emblaApi?.scrollPrev()} className="bg-slate-100 hover:bg-slate-200 p-2 rounded-full text-slate-600 transition-colors" aria-label="Previous similar car"><FiChevronLeft size={20} /></button>
                        <button onClick={() => emblaApi?.scrollNext()} className="bg-slate-100 hover:bg-slate-200 p-2 rounded-full text-slate-600 transition-colors" aria-label="Next similar car"><FiChevronRight size={20} /></button>
                    </div>
                </div>
                <div className="overflow-hidden" ref={emblaRef}>
                    <div className="flex -ml-4">
                        {similarCars.map((car) => (
                            <div key={car.ID} className="flex-grow-0 flex-shrink-0 w-full sm:w-[90%] md:w-[80%] lg:w-full pl-4">
                                <CarCard car={car} />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </AnimatedSection>
    );
};

// --- MAIN DETAIL PAGE COMPONENT ---

export function CarDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: car, isLoading, isError } = useQuery<Car, Error>({ queryKey: ['car', id], queryFn: () => fetchCarById(id!), enabled: !!id });
  const [savedCarIds, toggleSaveCar] = useSavedCars();
  
  useEffect(() => { window.scrollTo(0, 0); }, [id]);
  
  const isSaved = useMemo(() => car ? savedCarIds.includes(car.ID) : false, [car, savedCarIds]);
  const optionsList = useMemo(() => car?.Options ? car.Options.split(',').map((opt) => opt.trim()).filter(Boolean) : [], [car?.Options]);

  if (isLoading) return <div className="flex justify-center items-center h-screen bg-surface"><FiLoader className="animate-spin text-primary h-16 w-16" /></div>;
  if (isError) return <div className="container mx-auto mt-10 text-center p-8 bg-red-50 rounded-lg"><FiAlertTriangle className="text-red-500 h-12 w-12 mx-auto mb-4" /><h2 className="text-2xl font-bold text-red-800">Error Fetching Data</h2><Link to="/" className="text-blue-600 mt-4 inline-block">Go to Homepage</Link></div>;
  if (!car) return <div className="container mx-auto mt-10 text-center p-8"><h2 className="text-2xl font-bold text-text-primary">Car Not Found</h2><p className="text-text-secondary mt-2">The car you are looking for does not exist or may have been removed.</p><Link to="/inventory" className="mt-6 inline-block bg-primary text-white font-bold py-2 px-6 rounded-lg hover:opacity-90 transition-opacity">Back to Inventory</Link></div>;

  const handleSaveClick = (e: React.MouseEvent) => {
    e.preventDefault(); e.stopPropagation();
    const carName = `${normalizeBrandName(car.Brand)} ${car.Model || ''}`.trim();
    if (!isSaved) { toast.success(`${carName} u ruajt!`, { id: 'save-notification' }); } else { toast(`${carName} u hoq.`, { id: 'save-notification' }); }
    toggleSaveCar(car.ID);
  };
  
  const handleReservation = () => {
    const carDetails = `${car.Year} ${car.Brand} ${car.Model} ${car.Badge || ''}`.trim();
    const message = `Përshëndetje, jam i interesuar të rezervoj veturën: ${carDetails} (ID: ${car.ID}).`;
    const whatsappUrl = `https://wa.me/38346777779?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };
  
  const pageTitle = `${car.Year} ${normalizeBrandName(car.Brand)} ${car.Model} ${car.Badge || ''} | AutoPrishtina`;
  const description = `Shitet ${normalizeBrandName(car.Brand)} ${car.Model} i vitit ${car.Year} me ${car['Mileage (km)']?.toLocaleString('de-DE')} km. Çmimi: ${car['Price (EUR)']?.toLocaleString('de-DE')} €.`;
  const optionTranslations: Record<string, string> = { 'Airbag (driver seat)': 'Airbag (shofer)', 'Airbag (passenger seat)': 'Airbag (pasagjer)', 'Bluetooth': 'Bluetooth', 'Navigation': 'Navigim', 'Parking Sensor (front)': 'Sensor parkimi (para)', 'Parking Sensor (rear)': 'Sensor parkimi (mbrapa)', 'Heated Seats': 'Sedilje me ngrohje', 'Leather Seats': 'Sedilje lëkure', 'Sunroof': 'Tavan xhami', 'Keyless Entry': 'Hyrje pa çelës', 'Backup Camera': 'Kamera e pasme', 'LED Headlights': 'Drita LED', 'Cruise Control': 'Tempomat', 'Adaptive Cruise Control': 'Tempomat adaptiv', 'Lane Departure Warning': 'Asistent korsie' };
  const translatedOption = (option: string) => optionTranslations[option] || option;

  return (
    <>
      <Helmet>
        <title>{pageTitle}</title>
        <meta name="description" content={description} />
      </Helmet>
      <div className="bg-background font-sans antialiased text-text-primary">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={{ hidden: { opacity: 0 }, visible: { opacity: 1 } }}
          className="w-full pb-28 lg:pb-12"
        >
          <div className="container mx-auto px-4 lg:px-8 pt-8 space-y-8 lg:space-y-10">
            <AnimatedSection>
              <p className="text-sm font-semibold text-primary">{normalizeBrandName(car.Brand)}</p>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-text-primary tracking-tighter mt-1">{car.Model}</h1>
              <div className="flex flex-wrap gap-2 items-center mt-3">{car.Badge && (<p className="inline-block bg-surface border border-border-secondary font-semibold px-3 py-1 rounded-full text-sm">{car.Badge}</p>)}{car.Year && (<p className="inline-block bg-surface border border-border-secondary font-semibold px-3 py-1 rounded-full text-sm">{car.Year}</p>)}</div>
            </AnimatedSection>
            <AnimatedSection><FlagBadges flags={car.flags} context="detail" /></AnimatedSection>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12 items-start">
              <AnimatedSection className="lg:col-span-2"><ImageCarousel car={car} /></AnimatedSection>
              <aside className="lg:col-span-1 lg:sticky top-20 w-full hidden lg:block">
                <AnimatedSection>
                  <div className="bg-white rounded-2xl border border-border-secondary shadow-lg p-6 space-y-4">
                    <div><p className="text-sm font-medium text-text-secondary">Çmimi final i automjetit</p><p className="text-5xl font-extrabold text-text-primary my-1 tracking-tighter">{car['Price (EUR)']?.toLocaleString('de-DE')} €</p><p className="text-xs text-text-secondary">Përfshirë transportin, pa doganë.</p></div>
                    <div className="grid grid-cols-1 gap-3 pt-2">
                      <button onClick={handleReservation} className="w-full bg-blue-diagonal text-text-on-primary font-bold py-3.5 rounded-xl hover:opacity-90 shadow-lg shadow-blue-500/30 transition-all text-lg flex items-center justify-center gap-2"><FaWhatsapp /> Rezervo Veturën</button>
                      <button onClick={handleSaveClick} className={`w-full flex items-center justify-center gap-2 font-bold py-3 rounded-xl transition-all ${isSaved ? 'bg-red-100 text-red-600' : 'bg-slate-100 hover:bg-slate-200 text-slate-700'}`}>{isSaved ? <IoIosHeart className="animate-wiggle" /> : <IoIosHeartEmpty />} {isSaved ? 'E Ruajtur' : 'Ruaj Veturën'}</button>
                    </div>
                    <div className="text-center pt-2"><a href="#" className="text-sm font-medium text-text-secondary hover:text-primary inline-flex items-center gap-1.5"><FiHelpCircle /><span>Keni pyetje? Na kontaktoni.</span></a></div>
                  </div>
                </AnimatedSection>
              </aside>
            </div>
            <AnimatedSection><div className="bg-white rounded-2xl border border-border-secondary p-4 sm:p-6 shadow-xl shadow-slate-900/5"><h3 className="text-lg sm:text-xl font-bold text-text-primary border-b border-border-secondary pb-4 mb-2">Specifikat e automjetit</h3><div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-0"><div><SpecItem icon={TbRoad} label="Kilometrat" value={`${car['Mileage (km)']?.toLocaleString('de-DE')} km`} /><SpecItem icon={BsFillFuelPumpFill} label="Karburanti" value={normalizeFuelType(car['Fuel'] || '').displayName} /><SpecItem icon={MdEventSeat} label="Viti" value={car.Year} /><SpecItem icon={GiGearStick} label="Marshi" value={car.Transmission} /></div><div><SpecItem icon={TbFingerprint} label="VIN" value={car.VIN} /><SpecItem icon={TbCar} label="Tipi i Karrocerisë" value={car['Body Type']} /><SpecItem icon={TbColorSwatch} label="Ngjyra" value={car.Color} /><SpecItem icon={TbEngine} label="Kubikazha (cc)" value={car['Displacement (cc)']} /></div></div></div></AnimatedSection>
            <AnimatedSection><CollapsibleSection title="Historiku i Vetures" defaultOpen={true}><div className="divide-y divide-border-secondary"><div className="grid grid-cols-1 md:grid-cols-2 gap-x-8"><SpecItem icon={FaCarCrash} label="Aksidente" value={car['Accident Count'] ?? 'N/A'} /><SpecItem icon={FaUsers} label="Ndryshime pronari" value={car['Owner Changes'] ?? 'N/A'} /><SpecItem icon={BsShieldCheck} label="Dëmtim total" value={car['Total Loss Count'] ?? 'N/A'} /><SpecItem icon={BsClockHistory} label="Histori vjedhje" value={car['Theft History Count'] ?? 'N/A'} /><SpecItem icon={MdVerifiedUser} label="Regjistrimi i parë" value={car['First Registration Date'] ?? 'N/A'} /></div>{car['Accident History'] && (<div className="pt-4 mt-4"><h4 className="font-semibold text-text-secondary mb-1 flex items-center gap-2"><FaCarCrash/>Detajet e Aksidenteve</h4><p className="text-sm text-text-primary whitespace-pre-wrap pl-6">{car['Accident History']}</p></div>)}{car['Owner Change History'] && (<div className="pt-4 mt-4"><h4 className="font-semibold text-text-secondary mb-1 flex items-center gap-2"><FaUsers/>Historiku i Pronarëve</h4><p className="text-sm text-text-primary whitespace-pre-wrap pl-6">{car['Owner Change History']}</p></div>)}</div></CollapsibleSection></AnimatedSection>
            {optionsList.length > 0 && (<AnimatedSection><CollapsibleSection title="Pajisjet dhe Opsionet" count={optionsList.length}><div className="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-4">{optionsList.map((option) => (<span key={option} className="bg-slate-100 text-slate-700 text-xs font-medium px-3 py-1.5 rounded-lg text-center">{translatedOption(option)}</span>))}</div></CollapsibleSection></AnimatedSection>)}
            <SimilarCarsSection currentCarId={car.ID} />
          </div>
        </motion.div>
      </div>
      <div className="fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-md border-t border-gray-200 px-4 py-3 flex items-center justify-between gap-4 shadow-[0_-2px_10px_rgba(0,0,0,0.05)] lg:hidden">
        <div className="flex flex-col leading-tight"><span className="text-[11px] text-gray-500 uppercase tracking-wide">Çmimi</span><span className="text-lg font-semibold text-gray-900">{car['Price (EUR)']?.toLocaleString('de-DE')} €</span></div>
        <button onClick={handleSaveClick} className={`p-2 rounded-md transition-all border ${isSaved ? 'bg-red-50 text-red-600 border-red-200' : 'bg-gray-100 text-gray-700 border-gray-300'}`} aria-label="Ruaje veturën">{isSaved ? <IoIosHeart size={22} /> : <IoIosHeartEmpty size={22} />}</button>
        <button onClick={handleReservation} className="flex-1 bg-blue-diagonal transition-colors text-white font-medium py-3 rounded-md text-sm text-center flex items-center justify-center gap-2"><FaWhatsapp /> Rezervo Veturën</button>
      </div>
    </>
  );
}