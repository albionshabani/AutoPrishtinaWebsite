export function CarCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden flex flex-col md:flex-row mb-6 border border-gray-200">
      {/* Skeleton for the image */}
      <div className="md:w-1/3 h-52 md:h-auto bg-gray-200 animate-pulse flex-shrink-0"></div>

      {/* Skeleton for the text content */}
      <div className="p-6 flex-grow flex flex-col w-full">
        <div className="flex-grow">
          <div className="h-7 w-3/4 bg-gray-200 rounded animate-pulse"></div>
          <div className="h-5 w-1/2 bg-gray-200 rounded animate-pulse mt-2"></div>
        </div>
        <div className="flex flex-col md:flex-row items-end mt-4">
          <div className="grid grid-cols-3 gap-4 text-center flex-grow w-full">
            <div className="h-10 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-10 bg-gray-200 rounded animate-pulse"></div>
            <div className="h-10 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div className="mt-4 md:mt-0 md:ml-6 w-1/3">
            <div className="h-10 bg-gray-200 rounded animate-pulse"></div>
          </div>
        </div>
      </div>
    </div>
  );
}