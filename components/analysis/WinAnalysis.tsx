import { TrendingUp } from 'lucide-react'

interface WinInsight {
  category: string;
  finding: string;
  severity: 'high' | 'medium' | 'low';
}

interface WinAnalysisData {
  has_data: boolean;
  message?: string;
  total_won?: number;
  total_value_won?: number;
  avg_cycle_length?: number;
  insights?: WinInsight[];
}

interface WinAnalysisProps {
  data: WinAnalysisData;
}

export default function WinAnalysis({ data }: WinAnalysisProps) {
  if (!data.has_data) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Win Analysis</h3>
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
        <TrendingUp className="h-6 w-6 text-green-500" />
        <h3 className="text-xl font-semibold text-gray-800">Win Analysis</h3>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Won Opportunities</p>
          <p className="text-xl font-semibold text-green-600">{data.total_won}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Value Won</p>
          <p className="text-xl font-semibold text-green-600">
            ${data.total_value_won?.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Avg. Sales Cycle</p>
          <p className="text-xl font-semibold text-green-600">
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
                ? 'bg-green-50 border border-green-100' 
                : 'bg-emerald-50 border border-emerald-100'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className="h-5 w-5 mt-0.5 flex-shrink-0 rounded-full bg-green-100 flex items-center justify-center">
                <TrendingUp className="h-3 w-3 text-green-600" />
              </div>
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