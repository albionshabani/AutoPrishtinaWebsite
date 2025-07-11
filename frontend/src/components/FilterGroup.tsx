import React from 'react';

export function FilterGroup({ title, children }: { title: string, children: React.ReactNode }) {
  return (
    <div className="py-6 border-b border-gray-200">
      <h3 className="text-sm font-semibold uppercase tracking-wider text-gray-800">{title}</h3>
      <div className="mt-4">{children}</div>
    </div>
  );
}