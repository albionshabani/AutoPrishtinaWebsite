import { useState } from 'react';
import { NavLink, Link } from 'react-router-dom';
import { TbHeartFilled } from "react-icons/tb";
import { FiMenu, FiX } from "react-icons/fi";
import { AnimatePresence, motion } from 'framer-motion';

export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const logoPath = '/assets/logo.svg';

  const desktopNavLinkClasses = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-semibold leading-6 transition-all duration-200 
     ${isActive 
       ? 'bg-gradient-to-br from-[#0E3467] to-[#1C68CD] bg-clip-text text-transparent' 
       : 'text-text-secondary hover:bg-gradient-to-br hover:from-[#0E3467] hover:to-[#1C68CD] hover:bg-clip-text hover:text-transparent'}`;

  const mobileNavLinkClasses = ({ isActive }: { isActive: boolean }) =>
    `block w-full text-left py-3 px-4 text-lg font-semibold transition-colors rounded-md 
     ${isActive ? 'bg-blue-100 text-primary' : 'text-text-primary hover:bg-gray-100'}`;

  const closeMenu = () => setIsMenuOpen(false);

  return (
    <header className="bg-surface sticky top-0 z-40 shadow-sm border-b border-border-secondary">
      <nav className="container mx-auto flex items-center justify-between p-4" aria-label="Global">

        {/* Logo */}
        <div className="flex lg:flex-1">
          <Link to="/" className="-m-1.5 p-1.5" onClick={closeMenu}>
            <img className="h-8 w-auto" src={logoPath} alt="AutoPrishtina Logo" />
          </Link>
        </div>

        {/* Desktop Nav Links */}
        <div className="hidden lg:flex items-center gap-x-8 ml-auto">
          <NavLink to="/" className={desktopNavLinkClasses}>Ballina</NavLink>
          <NavLink to="/inventory" className={desktopNavLinkClasses}>Inventari</NavLink>
          <NavLink to="/saved" className={desktopNavLinkClasses} onClick={closeMenu}>
            <TbHeartFilled className="w-6 h-6" />
          </NavLink>
        </div>

        {/* Hamburger menu (Mobile only) */}
        <div className="lg:hidden">
          <button className="-mr-2 p-2" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            <span className="sr-only">Open main menu</span>
            {isMenuOpen
              ? <FiX className="h-6 w-6 text-text-primary" />
              : <FiMenu className="h-6 w-6 text-text-primary" />}
          </button>
        </div>
      </nav>

      {/* Mobile Dropdown Menu */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden border-t border-border-secondary"
          >
            <div className="container mx-auto p-4 space-y-2">
              <NavLink to="/" className={mobileNavLinkClasses} onClick={closeMenu}>
                Ballina
              </NavLink>
              <NavLink to="/inventory" className={mobileNavLinkClasses} onClick={closeMenu}>
                Inventari
              </NavLink>
              <NavLink to="/saved" className={mobileNavLinkClasses} onClick={closeMenu}>
                <span className="inline-flex items-center gap-x-2">
                  <TbHeartFilled className="w-5 h-5" /> Të preferuarat
                </span>
              </NavLink>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};
