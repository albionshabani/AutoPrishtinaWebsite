import React, { ForwardedRef } from 'react';

type SelectInputProps = {
  options: { value: string; label: string }[];
  containerClassName?: string;
  disabled?: boolean;
  onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  value?: string;
};

export const SelectInput = React.forwardRef(
  ({ options, containerClassName = '', disabled = false, onChange, value }: SelectInputProps, ref: ForwardedRef<HTMLSelectElement>) => {
    return (
      <div className={`relative ${containerClassName}`}>
        <select
          ref={ref}
          disabled={disabled}
          onChange={onChange}
          value={value}
          // --- FIX IS HERE ---
          // The background color is now applied directly to the select element.
          className="block w-full px-3 py-2 text-md text-white bg-black/20 rounded-md border border-gray-600/50 appearance-none focus:outline-none focus:ring-1 focus:ring-brand-blue focus:border-brand-blue disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {options.map(option => (
            <option key={option.value} value={option.value} className="text-black bg-white">
              {option.label}
            </option>
          ))}
        </select>
      </div>
    );
  }
);