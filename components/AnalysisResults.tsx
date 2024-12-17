import { useState } from 'react'
import { AnalysisResults as AnalysisResultsType } from '@/types/analysis'
import CoreMetrics from './analysis/CoreMetrics'
import PerformanceTable from './analysis/PerformanceTable'
import PipelineHealth from './analysis/PipelineHealth'
import DateFilter, { DateRange } from './analysis/DateFilter'
import dynamic from 'next/dynamic'
import AgingOpportunitiesTable from './analysis/AgingOpportunitiesTable'
import TrendAnalysis from './analysis/TrendAnalysis'
import LossAnalysis from './analysis/LossAnalysis'
import WinAnalysis from './analysis/WinAnalysis'
import OpenOpportunityAnalysis from './analysis/OpenOpportunityAnalysis'

// Dynamically import Plotly charts to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js').then(mod => mod.default), { ssr: false })

interface AnalysisResultsProps {
  results: AnalysisResultsType;
  onDateRangeChange?: (range: DateRange) => void;
}

export default function AnalysisResults({ results, onDateRangeChange }: AnalysisResultsProps) {
  const [dateRange, setDateRange] = useState<DateRange>('ytd')
  const [showAgingOpportunities, setShowAgingOpportunities] = useState(false)

  const handleDateChange = (range: DateRange) => {
    setDateRange(range)
    onDateRangeChange?.(range)
  }

  return (
    <div className="w-full max-w-7xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Analysis Results</h2>
        <DateFilter selected={dateRange} onChange={handleDateChange} />
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <CoreMetrics metrics={results["Advanced Analysis"]["Core Metrics"]} />
        <PipelineHealth 
          data={results["Advanced Analysis"]["Pipeline Health"]} 
          onViewAgingOpportunities={() => setShowAgingOpportunities(true)}
        />
      </div>

      <div className="space-y-6">
        <TrendAnalysis 
          winRateData={results.Visualizations["Win Rate Trend"]}
          volumeData={results.Visualizations["Volume Trend"]}
        />
        
        <PerformanceTable 
          data={results["Advanced Analysis"]["Segment Performance"]["Type Performance"]}
          title="Type Performance"
          nameField="Type"
          chart={
            <div className="w-full">
              <Plot
                data={JSON.parse(results.Visualizations["Win Rates by Type"].data).data}
                layout={JSON.parse(results.Visualizations["Win Rates by Type"].data).layout}
                config={results.Visualizations["Win Rates by Type"].config}
                className="w-full h-[300px]"
              />
            </div>
          }
        />

        <PerformanceTable 
          data={results["Advanced Analysis"]["Segment Performance"]["Practice Area Performance"]}
          title="Practice Area Performance"
          nameField="Practice Area"
        />

        <PerformanceTable 
          data={results["Advanced Analysis"]["Segment Performance"]["Account Performance"]}
          title="Account Performance"
          nameField="Account Name"
        />
        
        <div>
          <h2 className="text-xl font-semibold mb-4">Analysis by Stage</h2>
          <div className="grid grid-cols-1 gap-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <WinAnalysis 
                data={results["Advanced Analysis"]["Win Analysis"]}
              />
              <LossAnalysis 
                data={results["Advanced Analysis"]["Loss Analysis"]}
              />
            </div>
            <OpenOpportunityAnalysis 
              data={results["Advanced Analysis"]["Score Open Opportunities"]}
            />
          </div>
        </div>
      </div>

      {showAgingOpportunities && (
        <AgingOpportunitiesTable
          opportunities={results["Advanced Analysis"]["Pipeline Health"]["Aging Opportunities"]["Details"]}
          onClose={() => setShowAgingOpportunities(false)}
        />
      )}
    </div>
  )
}