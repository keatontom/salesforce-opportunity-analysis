import dynamic from 'next/dynamic'
import PerformanceTable from './PerformanceTable'
import { SegmentPerformance, Visualizations } from '@/types/analysis'

const Plot = dynamic(() => import('react-plotly.js').then(mod => mod.default), { ssr: false })

interface PerformanceAnalysisProps {
  segmentPerformance: SegmentPerformance;
  visualizations: Visualizations;
}

export default function PerformanceAnalysis({ segmentPerformance, visualizations }: PerformanceAnalysisProps) {
  return (
    <section>
      <h2 className="text-xl font-semibold mb-4">Performance Analysis</h2>
      <div className="space-y-6">
        <PerformanceTable 
          data={segmentPerformance["Type Performance"]}
          title="Type Performance"
          nameField="Type"
          chart={
            <div className="w-full">
              <Plot
                data={JSON.parse(visualizations["Win Rates by Type"].data).data}
                layout={JSON.parse(visualizations["Win Rates by Type"].data).layout}
                config={visualizations["Win Rates by Type"].config}
                className="w-full h-[300px]"
              />
            </div>
          }
        />

        <PerformanceTable 
          data={segmentPerformance["Practice Area Performance"]}
          title="Practice Area Performance"
          nameField="Practice Area"
        />

        <PerformanceTable 
          data={segmentPerformance["Account Performance"]}
          title="Account Performance"
          nameField="Account Name"
        />
      </div>
    </section>
  )
} 