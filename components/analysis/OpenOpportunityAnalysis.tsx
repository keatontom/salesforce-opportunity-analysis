import { CircleDot, ChevronDown, ChevronUp, ArrowUpDown, Info } from 'lucide-react'
import { useState } from 'react'
import { Button } from '../ui/button'

interface OpenOpportunityInsight {
  category: string;
  finding: string;
  severity: 'high' | 'medium' | 'low';
}

interface OpenOpportunityTableRow {
  Opportunity: string;
  Score: string;
  Risk: string;
  Value: string;
  "Days Open": number;
  "Key Insights": string;
}

interface OpenOpportunityData {
  has_data: boolean;
  message?: string;
  total_open?: number;
  total_opportunities?: number;
  total_value?: number;
  total_pipeline_value?: number;
  avg_value?: number;
  average_value?: number;
  average_score?: number;
  avg_cycle_length?: number;
  insights?: OpenOpportunityInsight[];
  opportunity_table?: {
    headers: string[];
    rows: OpenOpportunityTableRow[];
  };
}

interface OpenOpportunityAnalysisProps {
  data: OpenOpportunityData;
}

type SortableColumns = 'Score' | 'Value' | 'Days Open';

type SortConfig = {
  key: SortableColumns | null;
  direction: 'asc' | 'desc';
};

function InsightsCell({ insights }: { insights: string }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const criteriaCount = insights.split('\n').length - 1; // Subtract 1 for the final score line

  const formatInsights = (insights: string) => {
    return insights.split('\n').map((insight, index) => {
      const formattedInsight = insight.replace(/(\d+\.\d+%)/g, '<span class="font-bold">$1</span>');
      return (
        <div 
          key={index} 
          className="mb-2"
          dangerouslySetInnerHTML={{ __html: formattedInsight }}
        />
      );
    });
  };

  return (
    <div>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-1 text-blue-600 hover:text-blue-800"
      >
        {isExpanded ? (
          <>Hide Details <ChevronUp className="h-4 w-4" /></>
        ) : (
          <>Based on {criteriaCount} criteria <ChevronDown className="h-4 w-4" /></>
        )}
      </Button>
      {isExpanded && (
        <div className="mt-2">
          {formatInsights(insights)}
        </div>
      )}
    </div>
  );
}

const formatBulletPoints = (text: string) => {
  return text.split('\n').map((point, index) => (
    <div key={index} className="flex items-start gap-2">
      <span className="text-blue-500 mt-1.5">•</span>
      <span>{point}</span>
    </div>
  ));
};

export default function OpenOpportunityAnalysis({ data }: OpenOpportunityAnalysisProps) {
  const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: 'asc' });
  const [isExpanded, setIsExpanded] = useState(false);

  const totalOpportunities = data.total_opportunities || data.total_open || 0;
  const totalValue = data.total_pipeline_value || data.total_value || 0;
  const avgValue = totalOpportunities > 0 ? totalValue / totalOpportunities : 0;
  
  // Calculate average time open from the opportunity table
  const avgTimeOpen = data.opportunity_table?.rows.reduce((sum, row) => sum + row["Days Open"], 0) || 0;
  const avgDaysOpen = data.opportunity_table?.rows.length 
    ? Math.round(avgTimeOpen / data.opportunity_table.rows.length) 
    : 0;

  const sortedRows = data.opportunity_table?.rows.slice().sort((a, b) => {
    if (!sortConfig.key) return 0;
    
    const aValue = a[sortConfig.key];
    const bValue = b[sortConfig.key];

    // Handle numeric values (Score, Days Open)
    if (sortConfig.key === 'Score') {
      const aNum = parseFloat(aValue.toString().replace('%', ''));
      const bNum = parseFloat(bValue.toString().replace('%', ''));
      return sortConfig.direction === 'asc' ? aNum - bNum : bNum - aNum;
    }
    
    if (sortConfig.key === 'Days Open') {
      const aNum = Number(aValue);
      const bNum = Number(bValue);
      return sortConfig.direction === 'asc' ? aNum - bNum : bNum - aNum;
    }

    // Handle Value column
    if (sortConfig.key === 'Value') {
      const aNum = parseFloat(aValue.toString().replace(/[$,]/g, ''));
      const bNum = parseFloat(bValue.toString().replace(/[$,]/g, ''));
      return sortConfig.direction === 'asc' ? aNum - bNum : bNum - aNum;
    }

    return 0;
  });

  const displayedRows = isExpanded ? sortedRows : sortedRows?.slice(0, 5);
  const hasMoreRows = sortedRows && sortedRows.length > 5;

  const handleSort = (key: string) => {
    // Only allow sorting for specific columns
    if (key !== 'Score' && key !== 'Value' && key !== 'Days Open') return;
    
    setSortConfig((currentSort) => ({
      key: key as SortableColumns,
      direction: 
        currentSort.key === key && currentSort.direction === 'asc'
          ? 'desc'
          : 'asc',
    }));
  };

  if (!data.has_data) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100">
        <h3 className="text-xl font-semibold mb-4 text-gray-800">Open Opportunity Analysis</h3>
        <p className="text-gray-600">{data.message || "No data available for analysis"}</p>
      </div>
    )
  }

  return (
    <div className="bg-sky-50 p-6 rounded-lg shadow-md border border-sky-200 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <div className="flex items-center gap-2 mb-4">
        <CircleDot className="h-6 w-6 text-sky-600" />
        <h3 className="text-xl font-semibold text-sky-800">Open Opportunity Analysis</h3>
      </div>

      <div className="grid grid-cols-4 gap-3 mb-6">
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <p className="text-xs text-sky-700 mb-1 font-medium">Total Open Opportunities</p>
          <p className="text-lg font-semibold text-sky-600">{totalOpportunities}</p>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <p className="text-xs text-sky-700 mb-1 font-medium">Total Pipeline Value</p>
          <p className="text-lg font-semibold text-sky-600">
            ${totalValue.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </p>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <p className="text-xs text-sky-700 mb-1 font-medium">Average Value</p>
          <p className="text-lg font-semibold text-sky-600">
            ${avgValue.toLocaleString(undefined, {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2
            })}
          </p>
        </div>
        <div className="bg-white p-3 rounded-lg shadow-sm">
          <p className="text-xs text-sky-700 mb-1 font-medium">Average Time Open</p>
          <p className="text-lg font-semibold text-sky-600">
            {avgDaysOpen} days
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {data.insights?.map((insight, index) => (
          <div 
            key={index} 
            className={`p-4 rounded-lg bg-white shadow-sm`}
          >
            <div className="flex items-start gap-3">
              <Info className={`h-5 w-5 mt-0.5 flex-shrink-0 text-sky-600`} />
              <div className="space-y-1 w-full">
                <p className="font-medium text-sky-700">{insight.category}</p>
                <div className="text-sm text-sky-600">
                  {formatBulletPoints(insight.finding)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Opportunities Table */}
      {data.opportunity_table && (
        <div>
          <div className="overflow-x-auto rounded-lg bg-white shadow-sm">
            <table className="w-full divide-y divide-gray-200">
              <thead>
                <tr className="bg-gradient-to-r from-sky-50 to-sky-100">
                  {data.opportunity_table.headers.map((header, index) => {
                    let alignment = "text-left";
                    if (header === "Score" || header === "Value" || header === "Days Open") {
                      alignment = "text-right";
                    } else if (header === "Risk") {
                      alignment = "text-center";
                    }
                    
                    const isSortable = header === "Score" || header === "Value" || header === "Days Open";
                    
                    return (
                      <th 
                        key={index}
                        className={`px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider ${alignment} ${isSortable ? 'cursor-pointer hover:bg-sky-100' : ''}`}
                        onClick={() => isSortable && handleSort(header)}
                      >
                        <div className="flex items-center gap-1 justify-between">
                          <span>{header}</span>
                          {isSortable && (
                            <div className="flex flex-col">
                              {sortConfig.key === header ? (
                                sortConfig.direction === 'asc' ? (
                                  <ChevronUp className="h-3 w-3" />
                                ) : (
                                  <ChevronDown className="h-3 w-3" />
                                )
                              ) : (
                                <ArrowUpDown className="h-3 w-3" />
                              )}
                            </div>
                          )}
                        </div>
                      </th>
                    );
                  })}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {displayedRows?.map((row, index) => (
                  <tr key={index} className="hover:bg-sky-50 transition-colors">
                    <td className="px-4 py-3 text-sm text-gray-900">{row.Opportunity}</td>
                    <td className="px-4 py-3 text-sm font-medium text-sky-600 text-right">{row.Score}</td>
                    <td className="px-4 py-3 text-sm text-center">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        row.Risk === 'Low' ? 'bg-green-100 text-green-800' :
                        row.Risk === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {row.Risk}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 text-right">{row.Value}</td>
                    <td className="px-4 py-3 text-sm text-gray-900 text-right">{row["Days Open"]}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      <InsightsCell insights={row["Key Insights"]} />
                    </td>
                  </tr>
                ))}
                {hasMoreRows && !isExpanded && (
                  <tr>
                    <td colSpan={6} className="px-4 py-2 text-center">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setIsExpanded(true)}
                        className="text-sky-600 hover:text-sky-800"
                      >
                        <div className="flex items-center gap-1">
                          <span>Show More</span>
                          <ChevronDown className="h-4 w-4" />
                        </div>
                      </Button>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          {isExpanded && hasMoreRows && (
            <div className="mt-4 text-center">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsExpanded(false)}
                className="text-sky-600 hover:text-sky-800"
              >
                <div className="flex items-center gap-1">
                  <span>Show Less</span>
                  <ChevronUp className="h-4 w-4" />
                </div>
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  )
} 