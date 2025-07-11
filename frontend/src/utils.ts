// FILE: frontend/src/utils.ts
// This is the final, corrected version with robust normalization logic.

/**
 * Takes a raw brand name and returns its clean, global equivalent.
 */
export const normalizeBrandName = (brand?: string | null): string => {
  if (!brand) return '...';
  const lowerCaseBrand = brand.toLowerCase();
  
  const junkTerms = ['other', 'award', 'sub', 'photon'];
  if (junkTerms.some(term => lowerCaseBrand.includes(term))) {
    return '...';
  }

  const mapping: { [key: string]: string } = {
    'chevrolet (gm daewoo)': 'Chevrolet',
    'renault korea (samsung)': 'Renault',
    'kg mobility (ssangyong)': 'SsangYong',
    'benz': 'Mercedes-Benz',
    'citroen/ds': 'Citroën',
    'dongfeng sokon': 'Dongfeng',
    'mg rover': 'MG',
    'rolls royce': 'Rolls-Royce',
    'mitsuoka' : 'Mitsuoka',
    'mini': 'MINI',
    'ford': 'Ford',
    'jeep': 'Jeep'
  };
  if (mapping[lowerCaseBrand]) return mapping[lowerCaseBrand];
  
  return brand.charAt(0).toUpperCase() + brand.slice(1);
};

/**
 * Takes a brand name and returns the path to its logo.
 */
export const getLogoUrl = (brandName?: string | null): string => {
  if (!brandName) return '';
  const normalized = normalizeBrandName(brandName);
  if (normalized === '...') return '';
  const formattedName = normalized.toLowerCase().replace(/\s/g, '-').replace(/&/g, 'co').replace(/\./g, '');
  return `/logos/${formattedName}.webp`;
};

/**
 * Formats a number into a standardized EUR currency string.
 * @param price The price as a number.
 * @returns A formatted string like "23,019 €" or "N/A".
 */
export const formatPrice = (price?: number): string => {
    if (price === undefined || price === null || isNaN(price)) {
        return 'N/A';
    }
    return `${new Intl.NumberFormat('de-DE').format(price)} €`;
};

/**
 * Formats a number into a standardized kilometer string.
 * @param mileage The mileage as a number.
 * @returns A formatted string like "91,400 km" or "N/A".
 */
export const formatMileage = (mileage?: number): string => {
    if (mileage === undefined || mileage === null || isNaN(mileage)) {
        return 'N/A';
    }
    return `${new Intl.NumberFormat('de-DE').format(mileage)} km`;
};

/**
 * Parses a comma-separated string of image URLs and cleans them up.
 * @param imageUrlString A string containing one or more URLs.
 * @returns An array of valid, trimmed image URLs.
 */
export const getCleanImageUrls = (imageUrlString?: string): string[] => {
    if (!imageUrlString) {
        return [];
    }
    return imageUrlString
        .split(',')
        .map(url => url.trim())
        .filter(url => url.length > 0 && (url.startsWith('http') || url.startsWith('https')));
};

/**
 * Formats a date string into MM/YYYY format for consistency.
 * Falls back to showing just the year if the date is invalid or missing.
 * @param dateString The full date string (e.g., '2021-08-15')
 * @param fallbackYear The year to show if formatting fails (e.g., '2021')
 * @returns Formatted date like '08/2021' or just the fallback year.
 */
export const formatRegistrationDate = (dateString?: string, fallbackYear?: string): string => {
  if (!dateString) {
    return fallbackYear || 'N/A';
  }
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return fallbackYear || dateString;
    }
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${year}`;
  } catch (error) {
    return fallbackYear || dateString;
  }
};

/**
 * Normalizes the messy fuel data from the database into a clean, usable format.
 * This is the single source of truth for interpreting fuel types.
 * @param fuel The raw fuel string from the database (e.g., "Gasoline+Electricity", "Dizel").
 * @returns An object with a clean 'category' for logic and a 'displayName' for the UI.
 */
export const normalizeFuelType = (fuel?: string): { category: 'electric' | 'hybrid' | 'other', displayName: string } => {
  if (!fuel) {
    return { category: 'other', displayName: 'N/A' };
  }

  const lowerFuel = fuel.toLowerCase();

  // 1. Check for hybrids: any combination with "+electricity" or "+electric".
  if (lowerFuel.includes('+electricity') || lowerFuel.includes('+electric')) {
    return { category: 'hybrid', displayName: 'Hybrid' };
  }

  // 2. Check for pure electric.
  if (lowerFuel === 'electric' || lowerFuel === 'elektrik') {
    return { category: 'electric', displayName: 'Electric' };
  }
  
  // 3. Handle common fuel types and standardize their names.
  if (lowerFuel.includes('diesel') || lowerFuel.includes('dizel')) {
    return { category: 'other', displayName: 'Diesel' };
  }

  if (lowerFuel.includes('gasoline') || lowerFuel.includes('benzinë')) {
    if (lowerFuel.includes('+lpg') || lowerFuel.includes('+cng')) {
       return { category: 'other', displayName: 'Gasoline + Gas' };
    }
    return { category: 'other', displayName: 'Gasoline' };
  }

  if (lowerFuel.includes('lpg')) {
    return { category: 'other', displayName: 'LPG' };
  }

  // 4. Fallback for any other cases (e.g., "Hydrogen").
  const capitalizedDisplayName = fuel.charAt(0).toUpperCase() + fuel.slice(1);
  return { category: 'other', displayName: capitalizedDisplayName };
};