import { AlertTriangle, TrendingDown } from 'lucide-react'

interface LossInsight {
  category: string;
  finding: string;
  severity: 'high' | 'medium' | 'low';
}

interface LossAnalysisData {
  has_data: boolean;
  message?: string;
  total_lost?: number;
  total_value_lost?: number;
  avg_value_lost?: number;
  avg_cycle_length?: number;
  insights?: LossInsight[];
}

interface LossAnalysisProps {
  data: LossAnalysisData;
}

export default function LossAnalysis({ data }: LossAnalysisProps) {
  if (!data.has_data) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Loss Analysis</h3>
        <p className="text-gray-600">{data.message || "No data available for analysis"}</p>
      </div>
    )
  }

  const formatBulletPoints = (text: string) => {
    return text.split('\n').map((line, index) => {
      if (!line.trim()) return null;
      const isMainPoint = !line.startsWith('  •');
      return (
        <div key={index} className={`${isMainPoint ? '' : 'ml-4'} ${line.trim().startsWith('•') ? 'mb-1' : 'mb-2'}`}>
          {line.trim()}
        </div>
      );
    }).filter(Boolean);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <div className="flex items-center gap-2 mb-4">
        <TrendingDown className="h-6 w-6 text-red-500" />
        <h3 className="text-xl font-semibold text-gray-800">Loss Analysis</h3>
      </div>

      <div className="grid grid-cols-4 gap-3 mb-6">
        <div className="bg-red-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Total Lost Opportunities</p>
          <p className="text-lg font-semibold text-red-600">{data.total_lost}</p>
        </div>
        <div className="bg-red-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Total Value Lost</p>
          <p className="text-lg font-semibold text-red-600">
            ${data.total_value_lost?.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </p>
        </div>
        <div className="bg-red-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Average Value</p>
          <p className="text-lg font-semibold text-red-600">
            ${data.avg_value_lost?.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </p>
        </div>
        <div className="bg-red-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Avg. Sales Cycle</p>
          <p className="text-lg font-semibold text-red-600">
            {Math.round(data.avg_cycle_length || 0)} days
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {data.insights?.map((insight, index) => (
          <div 
            key={index} 
            className={`p-4 rounded-lg ${
              insight.severity === 'high' 
                ? 'bg-red-50 border border-red-100' 
                : 'bg-orange-50 border border-orange-100'
            }`}
          >
            <div className="flex items-start gap-3">
              <AlertTriangle className={`h-5 w-5 mt-0.5 flex-shrink-0 ${
                insight.severity === 'high' ? 'text-red-500' : 'text-orange-500'
              }`} />
              <div className="space-y-1 w-full">
                <p className="font-medium text-gray-900">{insight.category}</p>
                <div className="text-sm text-gray-600">
                  {formatBulletPoints(insight.finding)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
} 