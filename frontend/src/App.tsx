// FILE: frontend/src/App.tsx
// This is your file, modified to include the Toaster for notifications.

import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import { useEffect } from 'react';
import { Toaster } from 'react-hot-toast'; // <-- 1. IMPORT THE TOASTER

import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { HomePage } from './pages/HomePage';
import { InventoryPage } from './pages/InventoryPage';
import { CarDetailPage } from './pages/CarDetailPage';
import { SavedCarsPage } from './pages/SavedCarsPage';

const ScrollToTop = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
};

function App() {
  return (
    <HelmetProvider>
      <BrowserRouter>
        {/*
          --- 2. ADD THE TOASTER COMPONENT HERE ---
          This component listens for calls to `toast()` from anywhere in your app
          and renders the notifications. `position` and `toastOptions` are optional
          but good for styling.
        */}
        <Toaster position="bottom-center" toastOptions={{ duration: 3000 }} />

        <div className="flex flex-col min-h-screen">
          <ScrollToTop />
          <Header />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/inventory" element={<InventoryPage />} />
              <Route path="/car/:id" element={<CarDetailPage />} />
              <Route path="/saved" element={<SavedCarsPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </HelmetProvider>
  );
}
export default App;