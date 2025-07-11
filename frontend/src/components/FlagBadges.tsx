// FILE: frontend/src/components/FlagBadges.tsx

import { CarFlags } from '../types';
import {
  Tag,
  ShieldCheck,
  Gauge,
  UserCheck,
  SearchCheck,
  Settings,
  Leaf
} from 'lucide-react';

const FLAG_CONFIG = {
  isGreatPrice: {
    label: 'Çmim i Shkëlqyer',
    icon: Tag,
    color: 'text-green-800 bg-green-100',
  },
  isWellMaintained: {
    label: 'I Mirëmbajtur',
    icon: ShieldCheck,
    color: 'text-emerald-800 bg-emerald-100',
  },
  isLowMileage: {
    label: 'Kilometra të Pakta',
    icon: Gauge,
    color: 'text-sky-800 bg-sky-100',
  },
  isFirstOwner: {
    label: 'Pronar i Parë',
    icon: UserCheck,
    color: 'text-blue-800 bg-blue-100',
  },
  isRareFind: {
    label: 'Gjetje e Rrallë',
    icon: SearchCheck,
    color: 'text-yellow-800 bg-yellow-100',
  },
  isFullyLoaded: {
    label: 'Full Opsione',
    icon: Settings,
    color: 'text-indigo-800 bg-indigo-100',
  },
  isFuelEfficient: {
    label: 'Efikas',
    icon: Leaf,
    color: 'text-lime-800 bg-lime-100',
  },
};


interface FlagBadgesProps {
  flags?: Partial<CarFlags>;
  context: 'card' | 'detail';
  size?: 'normal' | 'small';
  className?: string;
}

export const FlagBadges = ({
  flags,
  size = 'normal',
  className = '',
}: FlagBadgesProps) => {
  if (!flags) return null;

  const activeFlags = (Object.entries(flags) as [keyof CarFlags, boolean][])
    .filter(([key, value]) => value && FLAG_CONFIG[key])
    .map(([key]) => FLAG_CONFIG[key]);

  if (activeFlags.length === 0) return null;

  const sizeStyles = size === 'small'
    ? {
        badge: 'text-xs px-2 py-1 gap-1',
        icon: 'w-3 h-3',
      }
    : {
        badge: 'text-sm px-3 py-1.5 gap-1.5',
        icon: 'w-4 h-4',
      };

  return (
    <div className={`flex flex-wrap gap-1.5 ${className}`}>
      {activeFlags.map(({ label, icon: Icon, color }) => (
        <div
          key={label}
          className={`inline-flex items-center font-medium rounded-full ${color} ${sizeStyles.badge}`}
        >
          <Icon className={`${sizeStyles.icon}`} />
          <span>{label}</span>
        </div>
      ))}
    </div>
  );
};
