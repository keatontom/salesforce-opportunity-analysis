import dynamic from 'next/dynamic'
import { Visualization } from '@/types/analysis'
const Plot = dynamic(() => import('react-plotly.js').then(mod => mod.default), { ssr: false })

interface TrendAnalysisProps {
  winRateData: Visualization;
  volumeData: Visualization;
}

export default function TrendAnalysis({ winRateData, volumeData }: TrendAnalysisProps) {
  if (!winRateData || !volumeData) return null;
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Trend Analysis</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <Plot
            data={JSON.parse(winRateData.data).data}
            layout={JSON.parse(winRateData.data).layout}
            config={winRateData.config}
            className="w-full"
          />
        </div>
        <div>
          <Plot
            data={JSON.parse(volumeData.data).data}
            layout={JSON.parse(volumeData.data).layout}
            config={volumeData.config}
            className="w-full"
          />
        </div>
      </div>
    </div>
  )
} 