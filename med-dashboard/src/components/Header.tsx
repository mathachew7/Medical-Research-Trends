'use client';

export default function Header() {
  return (
    <header className="w-full px-4 sm:px-0 py-4 bg-gray-900 border-b border-gray-800 shadow-sm">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[2fr_1fr] items-center">
        {/* Title */}
        <h1 className="text-xl font-semibold tracking-wide text-white">
          Medical Research Trends Dashboard
        </h1>

        {/* Download Button */}
        <div className="flex justify-start lg:justify-end mt-3 lg:mt-0">
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 text-sm rounded-md shadow"
            onClick={() => {
              // download logic here
              console.log('Download clicked');
            }}
          >
            Download CSV
          </button>
        </div>
      </div>
    </header>
  );
}
