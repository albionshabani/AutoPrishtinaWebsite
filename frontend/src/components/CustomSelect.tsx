// FILE: frontend/src/components/CustomSelect.tsx

import { Listbox, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import { FiCheck, FiChevronDown } from 'react-icons/fi';

interface Option { value: string; label: string; }
interface CustomSelectProps {
  value: string;
  onChange: (value: string) => void;
  options: Option[];
  placeholder: string;
  getIcon?: (value: string) => string;
  disabled?: boolean;
}

export const CustomSelect = ({ value, onChange, options, placeholder, getIcon, disabled = false }: CustomSelectProps) => {
  const selectedOption = options.find(opt => opt.value === value);

  return (
    <div className="w-full">
      <Listbox value={value} onChange={onChange} disabled={disabled}>
        <div className="relative">
          <Listbox.Button className="relative w-full flex items-center cursor-default rounded-lg bg-white text-left shadow-md border-2 border-slate-200 focus-within:border-blue-600 transition-colors h-[50px] px-4 py-3 disabled:bg-slate-100 disabled:opacity-70">
            {/* Icon */}
            {getIcon && selectedOption && selectedOption.value !== 'any' && (
              <img src={getIcon(selectedOption.value)} alt={selectedOption.label} className="h-5 w-5 object-contain mr-3" />
            )}
            
            {/* Label */}
            <span className={`block truncate ${!selectedOption || selectedOption.value === 'any' ? 'text-gray-500' : 'text-gray-900 font-semibold'}`}>
              {selectedOption?.label || placeholder}
            </span>
            
            {/* Chevron */}
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
              <FiChevronDown className="h-5 w-5 text-gray-400" aria-hidden="true" />
            </span>
          </Listbox.Button>
          
          <Transition as={Fragment} leave="transition ease-in duration-100" leaveFrom="opacity-100" leaveTo="opacity-0">
            <Listbox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm z-30">
              {options.map((option) => (
                <Listbox.Option key={option.value} className={({ active }) => `relative cursor-default select-none py-2 pl-10 pr-4 ${active ? 'bg-blue-600 text-white' : 'text-gray-900'}`} value={option.value}>
                  {({ selected }) => (
                    <>
                      <span className={`flex items-center gap-3 truncate ${selected ? 'font-bold' : 'font-normal'}`}>
                        {getIcon && option.value !== 'any' && <img src={getIcon(option.value)} alt={option.label} className="h-5 w-5 object-contain flex-shrink-0" />}
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