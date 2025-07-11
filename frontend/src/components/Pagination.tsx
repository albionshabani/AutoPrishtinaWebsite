// FILE: frontend/src/components/Pagination.tsx
// A new component for handling page navigation.

import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const Pagination = ({ currentPage, totalPages, onPageChange }: PaginationProps) => {
  if (totalPages <= 1) return null;

  return (
    <div className="flex items-center justify-center gap-4 mt-8">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-md bg-surface border border-border-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors hover:bg-subtle"
        aria-label="Previous Page"
      >
        <FiChevronLeft className="w-5 h-5" />
      </button>

      <span className="font-semibold text-text-primary">
        Page {currentPage} of {totalPages}
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded-md bg-surface border border-border-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors hover:bg-subtle"
        aria-label="Next Page"
      >
        <FiChevronRight className="w-5 h-5" />
      </button>
    </div>
  );
};