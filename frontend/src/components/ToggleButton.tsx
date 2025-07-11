type ToggleButtonProps = {
  options: string[];
  value?: string;
  onChange: (value: string) => void;
};

export function ToggleButton({ options, value, onChange }: ToggleButtonProps) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {options.map((opt) => {
        const isActive = value === opt;
        return (
          <button
            key={opt}
            onClick={() => onChange(isActive ? '' : opt)} // Clicking an active button deselects it
            className={`w-full text-center px-3 py-2 rounded-md text-sm font-semibold border-2 transition-all duration-150 ${
              isActive
                ? 'bg-brand-blue/10 text-brand-blue border-brand-blue'
                : 'bg-gray-100 text-gray-700 border-gray-100 hover:border-gray-300'
            }`}
          >
            {opt}
          </button>
        );
      })}
    </div>
  );
}