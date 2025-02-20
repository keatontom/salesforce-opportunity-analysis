import { useState } from 'react'
import { AnalysisResults as AnalysisResultsType } from '@/types/analysis'
import CoreMetrics from './analysis/CoreMetrics'
import PipelineHealth from './analysis/PipelineHealth'
import AgingOpportunitiesTable from './analysis/AgingOpportunitiesTable'
import TrendAnalysis from './analysis/TrendAnalysis'
import LossAnalysis from './analysis/LossAnalysis'
import WinAnalysis from './analysis/WinAnalysis'
import OpenOpportunityAnalysis from './analysis/OpenOpportunityAnalysis'
import PerformanceAnalysis from './analysis/PerformanceAnalysis'

interface AnalysisResultsProps {
  results: AnalysisResultsType;
}

export default function AnalysisResults({ results }: AnalysisResultsProps) {
  const [showAgingOpportunities, setShowAgingOpportunities] = useState(false)

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Analysis Results</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <CoreMetrics metrics={results["Advanced Analysis"]["Core Metrics"]} />
        <PipelineHealth 
          data={results["Advanced Analysis"]["Pipeline Health"]} 
          onViewAgingOpportunities={() => setShowAgingOpportunities(true)}
        />
      </div>

      <TrendAnalysis 
        winRateData={results.Visualizations["Win Rate Trend"]}
        volumeData={results.Visualizations["Volume Trend"]}
      />
      
      <section>
        <h2 className="text-xl font-semibold mb-4">Analysis by Stage</h2>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <WinAnalysis data={results["Advanced Analysis"]["Win Analysis"]} />
            <LossAnalysis data={results["Advanced Analysis"]["Loss Analysis"]} />
          </div>
          <OpenOpportunityAnalysis 
            data={results["Advanced Analysis"]["Score Open Opportunities"]}
          />
        </div>
      </section>

      <PerformanceAnalysis 
        segmentPerformance={results["Advanced Analysis"]["Segment Performance"]}
        visualizations={results.Visualizations}
      />

      {showAgingOpportunities && (
        <AgingOpportunitiesTable
          opportunities={results["Advanced Analysis"]["Pipeline Health"]["Aging Opportunities"]["Details"]}
          onClose={() => setShowAgingOpportunities(false)}
        />
      )}
    </div>
  )
}