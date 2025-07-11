import { Menu, Transition } from '@headlessui/react';
import { useState, useEffect, Fragment } from 'react';
import { FiChevronDown } from 'react-icons/fi';

interface PresetOption { value: string; label: string; }
interface NumberWithPresetsInputProps {
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  presets: PresetOption[];
  format?: 'default' | 'year';
}

export const NumberWithPresetsInput = ({ value, onChange, placeholder, presets, format = 'default' }: NumberWithPresetsInputProps) => {
  const [displayValue, setDisplayValue] = useState('');

  useEffect(() => {
    if (value) {
      const num = parseInt(value, 10);
      setDisplayValue(isNaN(num) ? '' : format === 'year' ? num.toString() : num.toLocaleString('en-US'));
    } else {
      setDisplayValue('');
    }
  }, [value, format]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const numericString = e.target.value.replace(/[^0-9]/g, '');
    const finalString = format === 'year' ? numericString.slice(0, 4) : numericString;
    onChange(finalString);
  };

  return (
    <div className="relative w-full">
      <div className="relative w-full flex items-center cursor-default rounded-lg bg-white text-left shadow-md border-2 border-slate-200 focus-within:border-blue-600 transition-colors h-[50px]">
        <input
          type="text"
          inputMode="numeric"
          value={displayValue}
          onChange={handleChange}
          placeholder={placeholder}
          className="w-full h-full border-none py-3 pl-4 pr-10 text-sm bg-transparent text-gray-900 font-semibold focus:ring-0 focus:outline-none placeholder:text-gray-500"
          autoComplete="off"
        />
        <Menu as="div" className="absolute inset-y-0 right-0 flex items-center">
          <Menu.Button className="h-full px-2 text-gray-400 hover:text-gray-600">
            <FiChevronDown className="h-5 w-5" aria-hidden="true" />
          </Menu.Button>
          <Transition as={Fragment} enter="transition ease-out duration-100" enterFrom="transform opacity-0 scale-95" enterTo="transform opacity-100 scale-100" leave="transition ease-in duration-75" leaveFrom="transform opacity-100 scale-100" leaveTo="transform opacity-0 scale-95">
            <Menu.Items className="absolute top-full right-0 mt-1 w-40 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none z-10">
              <div className="px-1 py-1">
                {presets.map((preset) => (
                  <Menu.Item key={preset.value}>
                    {({ active }) => ( <button onClick={() => onChange(preset.value)} className={`${active ? 'bg-blue-600 text-white' : 'text-gray-900'} group flex w-full items-center rounded-md px-2 py-2 text-sm`}>{preset.label}</button>)}
                  </Menu.Item>
                ))}
              </div>
            </Menu.Items>
          </Transition>
        </Menu>
      </div>
    </div>
  );
};