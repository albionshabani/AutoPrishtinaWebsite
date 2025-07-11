// FILE: frontend/src/components/SortByDropdown.tsx

import { Listbox, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import { FiCheck, FiChevronDown } from 'react-icons/fi';

interface SortOption {
  value: string;
  label: string;
}

interface SortByDropdownProps {
  options: SortOption[];
  value: string;
  onChange: (value: string) => void;
}

export const SortByDropdown = ({ options, value, onChange }: SortByDropdownProps) => {
  const selectedOption = options.find(opt => opt.value === value);

  return (
    <div className="relative w-full">
      <Listbox value={value} onChange={onChange}>
        <div className="relative">
          {/* This button is styled to look exactly like your filter inputs */}
          <Listbox.Button className="relative w-full flex items-center cursor-default rounded-lg bg-white text-left shadow-md border-2 border-slate-200 focus-within:border-blue-600 transition-colors h-[50px] px-4 py-3">
            <span className="block truncate text-sm font-semibold text-gray-900">
              {selectedOption?.label || 'Rendit Sipas...'}
            </span>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
              <FiChevronDown className="h-5 w-5 text-gray-400" aria-hidden="true" />
            </span>
          </Listbox.Button>
          <Transition as={Fragment} leave="transition ease-in duration-100" leaveFrom="opacity-100" leaveTo="opacity-0">
            <Listbox.Options className="absolute right-0 mt-1 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm z-30">
              {options.map((option) => (
                <Listbox.Option key={option.value} className={({ active }) => `relative cursor-default select-none py-2 pl-10 pr-4 ${active ? 'bg-blue-600 text-white' : 'text-gray-900'}`} value={option.value}>
                  {({ selected }) => (
                    <>
                      <span className={`block truncate ${selected ? 'font-bold' : 'font-normal'}`}>
                        {option.label}
                      </span>
                      {selected && <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-blue-600"><FiCheck className="h-5 w-5" aria-hidden="true" /></span>}
                    </>
                  )}
                </Listbox.Option>
              ))}
            </Listbox.Options>
          </Transition>
        </div>
      </Listbox>
    </div>
  );
};