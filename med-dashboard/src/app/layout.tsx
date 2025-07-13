import './globals.css';

import type { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: 'Medical Research Trends Dashboard',
  description: 'Trend visualizations from PubMed abstracts',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0b1727] text-white min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 w-full overflow-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 w-full">
            {children}
          </div>
        </main>
        <Footer />
      </body>
    </html>
  );
}
