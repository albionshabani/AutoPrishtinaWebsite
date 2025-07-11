import axios from 'axios';
import { Car } from './types';

export interface PaginatedCarsResponse {
  cars: Car[];
  totalPages: number;
  currentPage: number;
  totalItems: number;
}

export interface FilterOptions {
  brands: string[];
  models: { brand: string; model: string }[];
  years: string[];
  transmissions: string[];
  fuels: string[];
}

// All functions are now wrapped in try/catch for more robust error handling.
export async function fetchFilterOptions(): Promise<FilterOptions> {
  try {
    const response = await axios.get<FilterOptions>('/api/filter-options');
    return response.data;
  } catch (error) {
    console.error("Error fetching filter options:", error);
    throw error;
  }
}

export async function fetchCarCount(queryParams: string): Promise<number> {
  try {
    const response = await axios.get<{ count: number }>(`/api/cars/count?${queryParams}`);
    return response.data.count;
  } catch (error) {
    console.error("Error fetching car count:", error);
    throw error;
  }
}

export async function fetchCars({ queryParams, pageParam = 1 }: { queryParams: string; pageParam?: number; }): Promise<PaginatedCarsResponse> {
  try {
    const params = new URLSearchParams(queryParams);
    params.set('page', String(pageParam));
    const response = await axios.get<PaginatedCarsResponse>(`/api/cars?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching paginated cars:", error);
    throw error;
  }
}

export async function fetchCarById(id: string): Promise<Car> {
  try {
    const response = await axios.get<Car>(`/api/car/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching car by ID (${id}):`, error);
    throw error;
  }
}

export async function fetchSimilarCars(carId: string): Promise<Car[]> {
  try {
    const response = await axios.get<Car[]>(`/api/car/${carId}/similar`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching similar cars for ID (${carId}):`, error);
    throw error;
  }
}

export async function fetchFeaturedCars(): Promise<Car[]> {
  try {
    const response = await axios.get<Car[]>('/api/cars/featured');
    return response.data;
  } catch (error) {
    console.error("Error fetching featured cars:", error);
    throw error;
  }
}

// --- THIS FUNCTION WAS MISSING, CAUSING THE CRASH ---
/**
 * Fetches a specific list of cars by their IDs.
 * Uses a POST request to send the array of IDs.
 * @param ids An array of car ID strings.
 * @returns A promise that resolves to an array of Car objects.
 */
export async function fetchCarsByIds(ids: string[]): Promise<Car[]> {
  // If there are no IDs, don't make an API call.
  if (ids.length === 0) {
    return [];
  }
  try {
    const response = await axios.post<Car[]>(`/api/cars/by-ids`, { ids });
    return response.data;
  } catch (error) {
    console.error("Error fetching cars by IDs:", error);
    throw error;
  }
}