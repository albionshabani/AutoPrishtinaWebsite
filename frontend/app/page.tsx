import CarFilters from '@/components/carfilters'; // Corrected to lowercase
import { Truck, ShieldCheck, Headphones } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="bg-light-gray min-h-screen">
      <main className="container mx-auto px-4">
        <section className="text-center py-16 md:py-24">
          <h1 className="text-4xl md:text-6xl font-extrabold text-dark-text tracking-tight">
            Auto Prishtina Import
          </h1>
          <p className="text-lg md:text-xl text-medium-text mt-4 max-w-3xl mx-auto">
            Your trusted partner for certified pre-owned vehicles. Quality, transparency, and service you can rely on.
          </p>
        </section>
        <section className="bg-white p-8 rounded-xl shadow-lg max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-center text-dark-text mb-6">Find Your Next Car</h2>
            <CarFilters />
        </section>
        <section className="py-16 md:py-24">
            <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-dark-text">Why Auto Prishtina?</h2>
                <p className="text-medium-text mt-2">We deliver an exceptional car buying experience.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center p-6">
                    <Truck size={48} className="mx-auto text-primary-teal mb-4"/>
                    <h3 className="text-xl font-semibold text-dark-text">Fast & Reliable Import</h3>
                    <p className="text-medium-text mt-2">We handle the entire import process, delivering your car right to your doorstep.</p>
                </div>
                <div className="text-center p-6">
                    <ShieldCheck size={48} className="mx-auto text-primary-teal mb-4"/>
                    <h3 className="text-xl font-semibold text-dark-text">Certified Quality</h3>
                    <p className="text-medium-text mt-2">Every vehicle undergoes a rigorous inspection to ensure it meets our highest standards.</p>
                </div>
                <div className="text-center p-6">
                    <Headphones size={48} className="mx-auto text-primary-teal mb-4"/>
                    <h3 className="text-xl font-semibold text-dark-text">Dedicated Support</h3>
                    <p className="text-medium-text mt-2">Our team is here to help you every step of the way, from selection to ownership.</p>
                </div>
            </div>
        </section>
      </main>
    </div>
  );
}