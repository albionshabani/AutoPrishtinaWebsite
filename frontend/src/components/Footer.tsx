// FILE: frontend/src/components/Footer.tsx

import { Link } from 'react-router-dom';
import { FaFacebook, FaInstagram, FaTiktok, FaWhatsapp } from 'react-icons/fa';

export const Footer = () => {
  const logoPath = '/assets/logo.svg';

  return (
    // Using `bg-surface` and `border-secondary`
    <footer className="bg-surface text-text-primary border-t border-border-secondary">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-1">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <img src={logoPath} alt="AutoPrishtina Logo" className="h-8" />
            </Link>
            <p className="text-sm text-text-secondary">
              Besueshmëri në Çdo Hap!
            </p>
          </div>
          <div>
            <h3 className="font-bold text-text-primary mb-4">Linqe të Shpejta</h3>
            <ul className="space-y-2 text-sm">
              <li><Link to="/" className="text-text-secondary hover:text-primary transition-colors">Ballina</Link></li>
              <li><Link to="/inventory" className="text-text-secondary hover:text-primary transition-colors">Inventari</Link></li>
              <li><Link to="/saved" className="text-text-secondary hover:text-primary transition-colors">Të Ruajtura</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-text-primary mb-4">Kontakti</h3>
            <ul className="space-y-2 text-sm">
              <li className="text-text-secondary">Shpend Malaj, Prishtinë, Kosovë</li>
              <li><a href="mailto:info@autoprishtina.com" className="text-text-secondary hover:text-primary transition-colors">info@autoprishtina.com</a></li>
              <li className="text-text-secondary">+383-46-777-779</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-text-primary mb-4">Na Ndiqni</h3>
            <div className="flex space-x-4">
              <a href="https://www.facebook.com/people/Auto-Prishtina-Import/61567116036913/" aria-label="Facebook" className="text-text-secondary hover:text-primary transition-colors"><FaFacebook size={20} /></a>
              <a href="https://www.instagram.com/autoprishtina.import/?hl=en" aria-label="Instagram" className="text-text-secondary hover:text-primary transition-colors"><FaInstagram size={20} /></a>
              <a href="https://www.tiktok.com/@autoprishtina.import" aria-label="TikTok" className="text-text-secondary hover:text-primary transition-colors"><FaTiktok size={20} /></a>
              <a href="#" aria-label="WhatsApp" className="text-text-secondary hover:text-primary transition-colors"><FaWhatsapp size={20} /></a>
            </div>
          </div>
        </div>
        <div className="mt-12 pt-8 border-t border-border-secondary text-center text-sm text-text-secondary">
          <p>© {new Date().getFullYear()} AutoPrishtina. Të gjitha të drejtat e rezervuara.</p>
        </div>
      </div>
    </footer>
  );
};