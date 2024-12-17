import { CircleDot } from 'lucide-react'

interface OpenOpportunityInsight {
  category: string;
  finding: string;
  severity: 'high' | 'medium' | 'low';
}

interface OpenOpportunityTableRow {
  Opportunity: string;
  Account: string;
  Stage: string;
  Score: string;
  Risk: string;
  Value: string;
  "Days Open": number;
  "Key Insights": string;
}

interface OpenOpportunityData {
  has_data: boolean;
  message?: string;
  total_opportunities?: number;
  total_value?: number;
  average_score?: number;
  summary_insights?: OpenOpportunityInsight[];
  opportunity_table?: {
    headers: string[];
    rows: OpenOpportunityTableRow[];
  };
}

interface OpenOpportunityAnalysisProps {
  data: OpenOpportunityData;
}

export default function OpenOpportunityAnalysis({ data }: OpenOpportunityAnalysisProps) {
  if (!data.has_data) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Open Opportunity Analysis</h3>
        <p className="text-gray-600">{data.message || "No data available for analysis"}</p>
      </div>
    )
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <div className="flex items-center gap-2 mb-4">
        <CircleDot className="h-6 w-6 text-blue-500" />
        <h3 className="text-xl font-semibold text-gray-800">Open Opportunity Analysis</h3>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-6">
        <div className="bg-blue-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Total Open Opportunities</p>
          <p className="text-lg font-semibold text-blue-600">{data.total_opportunities}</p>
        </div>
        <div className="bg-blue-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Total Potential Value</p>
          <p className="text-lg font-semibold text-blue-600">
            ${data.total_value?.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </p>
        </div>
        <div className="bg-blue-50 p-3 rounded-lg">
          <p className="text-xs text-gray-600 mb-1">Average Score</p>
          <p className="text-lg font-semibold text-blue-600">
            {data.average_score}%
          </p>
        </div>
      </div>

      {/* Summary Insights */}
      <div className="space-y-4 mb-6">
        {data.summary_insights?.map((insight, index) => (
          <div 
            key={index} 
            className={`p-4 rounded-lg ${
              insight.severity === 'high' 
                ? 'bg-blue-50 border border-blue-100' 
                : 'bg-sky-50 border border-sky-100'
            }`}
          >
            <div className="flex items-start gap-3">
              <div className="h-5 w-5 mt-0.5 flex-shrink-0 rounded-full bg-blue-100 flex items-center justify-center">
                <CircleDot className="h-3 w-3 text-blue-600" />
              </div>
              <div className="space-y-1 w-full">
                <p className="font-medium text-gray-900">{insight.category}</p>
                <p className="text-sm text-gray-600">{insight.finding}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Opportunities Table */}
      {data.opportunity_table && (
        <div className="overflow-x-auto rounded-lg border border-gray-100">
          <table className="w-full divide-y divide-gray-200">
            <thead>
              <tr className="bg-gradient-to-r from-blue-50 to-indigo-50">
                {data.opportunity_table.headers.map((header, index) => (
                  <th 
                    key={index}
                    className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.opportunity_table.rows.map((row, index) => (
                <tr key={index} className="hover:bg-blue-50 transition-colors">
                  <td className="px-4 py-3 text-sm text-gray-900">{row.Opportunity}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.Account}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.Stage}</td>
                  <td className="px-4 py-3 text-sm font-medium text-blue-600">{row.Score}</td>
                  <td className="px-4 py-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      row.Risk === 'Low' ? 'bg-green-100 text-green-800' :
                      row.Risk === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {row.Risk}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.Value}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row["Days Open"]}</td>
                  <td className="px-4 py-3 text-sm text-gray-600">{row["Key Insights"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
} 