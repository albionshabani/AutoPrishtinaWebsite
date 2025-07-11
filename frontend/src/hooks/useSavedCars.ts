import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'savedCars';

/**
 * A custom hook to manage saved car IDs in localStorage.
 * @returns A tuple: [array of saved car IDs, function to toggle a car's saved status]
 */
export const useSavedCars = (): [string[], (carId: string) => void] => {
  const [savedCarIds, setSavedCarIds] = useState<string[]>([]);

  // On initial load, read the saved cars from localStorage
  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) {
        setSavedCarIds(JSON.parse(saved));
      }
    } catch (error) {
      console.error("Failed to parse saved cars from localStorage", error);
    }
  }, []);

  // A memoized function to update localStorage whenever the state changes
  const updateStorage = (ids: string[]) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
    } catch (error) {
      console.error("Failed to save cars to localStorage", error);
    }
  };

  // The main function to add or remove a car ID
  const toggleSaveCar = useCallback((carId: string) => {
    setSavedCarIds(prevIds => {
      const isSaved = prevIds.includes(carId);
      let newIds: string[];

      if (isSaved) {
        // If it's already saved, remove it
        newIds = prevIds.filter(id => id !== carId);
      } else {
        // If it's not saved, add it
        newIds = [...prevIds, carId];
      }
      
      updateStorage(newIds); // Update localStorage with the new list
      return newIds;
    });
  }, []);

  return [savedCarIds, toggleSaveCar];
};