// FILE: frontend/src/components/PrimaryButton.tsx

import React from 'react';

interface PrimaryButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  icon?: React.ElementType;
}

export const PrimaryButton = ({ children, icon: Icon, className, ...props }: PrimaryButtonProps) => {
  return (
    <button
      className={`
        w-full flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-bold text-text-on-primary
        bg-blue-diagonal  // Gradient using your theme's primary color
        shadow-lg shadow-primary/30  // Soft, colored shadow for a modern "cool" look
        transition-all duration-300 ease-in-out
        hover:shadow-xl hover:shadow-primary/40  // Shadow gets bigger on hover
        hover:-translate-y-px  // Slight lift on hover
        focus:outline-none focus:ring-4 focus:ring-primary/50
        disabled:opacity-60 disabled:cursor-not-allowed
        ${className}
      `}
      {...props}
    >
      {Icon && <Icon className="w-5 h-5" />}
      <span>{children}</span>
    </button>
  );
};