import { PipelineHealth as PipelineHealthType } from '@/types/analysis'
import { Button } from "@/components/ui/button"

interface PipelineHealthProps {
  data: PipelineHealthType;
  onViewAgingOpportunities?: () => void;
}

export default function PipelineHealth({ data, onViewAgingOpportunities }: PipelineHealthProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Pipeline Health</h3>
      
      <div className="mb-6">
        <h4 className="text-lg font-medium mb-3">Stage Distribution</h4>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(data["Stage Distribution"]).map(([stage, stats]) => (
            <div key={stage} className="bg-gradient-to-r from-blue-50 to-indigo-50 p-3 rounded hover:from-blue-100 hover:to-indigo-100 transition-colors">
              <p className="text-sm text-gray-600">{stage}</p>
              <div className="flex justify-between items-baseline">
                <p className="text-lg font-semibold text-blue-600">
                  {(stats.percentage * 100).toFixed(1)}%
                </p>
                <p className="text-sm text-gray-600">
                  {stats.count} opportunities
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="flex justify-between items-center mb-3">
          <h4 className="text-lg font-medium">Aging Opportunities</h4>
          {onViewAgingOpportunities && (
            <Button
              variant="outline"
              size="sm"
              onClick={onViewAgingOpportunities}
              className="text-blue-600 hover:text-blue-700"
            >
              View Details
            </Button>
          )}
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-3 rounded hover:from-blue-100 hover:to-indigo-100 transition-colors">
            <p className="text-sm text-gray-600">Count</p>
            <p className="text-lg font-semibold text-blue-600">{data["Aging Opportunities"].Count}</p>
          </div>
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-3 rounded hover:from-blue-100 hover:to-indigo-100 transition-colors">
            <p className="text-sm text-gray-600">Total Value</p>
            <p className="text-lg font-semibold text-blue-600">${data["Aging Opportunities"]["Total Value"].toLocaleString()}</p>
          </div>
        </div>
      </div>
    </div>
  )
} 