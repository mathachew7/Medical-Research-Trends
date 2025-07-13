import StatCard from '@/components/Dashboard/StatCard';
import TrendLineChart from '@/components/Dashboard/TrendLineChart';
import DonutChart from '@/components/Dashboard/DonutChart';
import ForecastChart from '@/components/Dashboard/ForecastChart';
import TopKeywords from '@/components/Dashboard/TopKeywords';
import KeywordCoOccurrence from '@/components/Dashboard/KeywordCoOccurrence';
import RecentAbstracts from '@/components/Dashboard/RecentAbstracts';

export default function HomePage() {
  return (
    <section className="max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6 auto-rows-min">
      
      {/* ROW 1: StatCards left, DonutChart right */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard />
      </div>

      <div className="row-span-2">
        <DonutChart />
      </div>

      {/* ROW 2 & 3: TrendLineChart full height on left, ForecastChart on right */}
      <div className="row-span-3">
        <TrendLineChart />
      </div>

      <div className="row-span-2">
        <ForecastChart />
      </div>

      {/* ROW 4: Bottom 3 keyword blocks */}

     <div className="col-span-full grid grid-cols-1 md:grid-cols-3 gap-6 max-h-[350px] mb-6">
  <div className="flex flex-col h-full">
    <TopKeywords />
  </div>
  <div className="flex flex-col h-full">
    <KeywordCoOccurrence />
  </div>
  <div className="flex flex-col h-full">
    <RecentAbstracts />
  </div>
</div>





      
    </section>
  );
}
