// FILE: frontend/src/components/SaveButton.tsx
// A new, simple button using Framer Motion for a clean animation.

import React from 'react';
import { motion } from 'framer-motion';
import { IoHeartSharp, IoHeartOutline } from 'react-icons/io5';

interface SaveButtonProps {
  isSaved: boolean;
  onClick: (e: React.MouseEvent) => void;
}

export const SaveButton = ({ isSaved, onClick }: SaveButtonProps) => {
  return (
    <motion.button
      // The "enlarge and go back" animation on tap.
      whileTap={{ scale: 1.2, transition: { duration: 0.1 } }}
      onClick={onClick}
      className="absolute top-3 right-3 z-20 p-1.5"
      aria-label="Save car"
    >
      {isSaved ? (
        // The FINAL saved state: solid red icon.
        <IoHeartSharp className="w-6 h-6 text-red-500" />
      ) : (
        // The default state: an outline icon that turns red on hover.
        <IoHeartOutline className="w-6 h-6 text-slate-500 transition-colors group-hover:text-red-400" />
      )}
    </motion.button>
  );
};