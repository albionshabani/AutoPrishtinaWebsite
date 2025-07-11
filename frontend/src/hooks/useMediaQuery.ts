// FILE: frontend/src/hooks/useMediaQuery.ts
// A simple hook to detect screen size for responsive component rendering.

import { useState, useEffect } from 'react';

export const useMediaQuery = (query: string): boolean => {
  const [matches, setMatches] = useState<boolean>(false);

  useEffect(() => {
    // Make sure window is defined (for server-side rendering safety)
    if (typeof window === 'undefined') {
      return;
    }

    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => {
      setMatches(media.matches);
    };

    media.addEventListener('change', listener);
    
    // Cleanup function to remove the listener when the component unmounts
    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
};