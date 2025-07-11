import { FiCheck } from 'react-icons/fi';

type CheckboxFilterProps = {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
};

export function CheckboxFilter({ label, checked, onChange }: CheckboxFilterProps) {
  return (
    <label className="flex items-center cursor-pointer select-none">
      <div className={`w-5 h-5 border-2 rounded-md flex items-center justify-center transition-all duration-150 ${
        checked ? 'bg-brand-blue border-brand-blue' : 'border-gray-300 bg-gray-100'
      }`}>
        {checked && <FiCheck className="w-4 h-4 text-white" />}
      </div>
      <input type="checkbox" className="absolute opacity-0 w-0 h-0" checked={checked} onChange={e => onChange(e.target.checked)} />
      <span className={`ml-3 font-semibold ${checked ? 'text-brand-blue' : 'text-gray-700'}`}>{label}</span>
    </label>
  );
}