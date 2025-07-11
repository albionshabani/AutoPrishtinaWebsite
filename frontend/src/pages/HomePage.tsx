// FILE: frontend/src/pages/HomePage.tsx
// FINAL, MOBILE-RESPONSIVE VERSION.
// Spacing has been adjusted to look great on all screen sizes.

import { motion } from 'framer-motion';
import { Hero } from '../components/Hero';
import { FeaturedCars } from "../components/FeaturedCars";
import { BrandShowcase } from '../components/BrandShowcase';
import { HowItWorks } from '../components/HowItWorks';

export function HomePage() {
  const pageVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.2 } }
  };

  const AnimatedSection = ({ children }: { children: React.ReactNode }) => (
    <motion.section
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.1 }}
      transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }} // A smoother easing function
    >
      {children}
    </motion.section>
  );

  return (
    <div className="bg-slate-50 font-sans">
      <Hero />
      
      <motion.div 
        variants={pageVariants} 
        initial="hidden" 
        animate="visible" 
        // --- THIS IS THE RESPONSIVE FIX ---
        // 1. Vertical spacing is reduced on mobile (`space-y-16`) and increases on desktop (`lg:space-y-32`).
        // 2. A negative top margin (`-mt-16`) pulls the content up to sit nicely below the Hero's search bar on mobile.
        // 3. This is overridden on desktop (`lg:mt-32`) to create the intended large gap.
        className="container w-full mx-auto p-4 space-y-16 lg:space-y-32 -mt-16 lg:mt-32 mt-24"
      >
        <div className="relative z-10 ">
          <FeaturedCars />
        </div>
        
        <AnimatedSection>
          <HowItWorks />
        </AnimatedSection>
        
        <AnimatedSection>
            <BrandShowcase />
        </AnimatedSection>

      </motion.div>
    </div>
  );
}