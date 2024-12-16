import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { X, ArrowUpDown, ChevronUp, ChevronDown } from 'lucide-react'

interface AgingOpportunity {
  "Account Name": string;
  "Opportunity Name": string;
  "Total ACV": number;
  "Created Date": string;
  "Days Open": number;
  "Stage": string;
}

interface AgingOpportunitiesTableProps {
  opportunities: AgingOpportunity[];
  onClose: () => void;
}

type SortField = keyof AgingOpportunity
type SortDirection = 'asc' | 'desc'

export default function AgingOpportunitiesTable({ opportunities, onClose }: AgingOpportunitiesTableProps) {
  const [sortField, setSortField] = useState<SortField>('Days Open')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const sortedOpportunities = [...opportunities].sort((a, b) => {
    const multiplier = sortDirection === 'asc' ? 1 : -1
    const aValue = a[sortField]
    const bValue = b[sortField]

    if (typeof aValue === 'number' && typeof bValue === 'number') {
      return (aValue - bValue) * multiplier
    }
    return String(aValue).localeCompare(String(bValue)) * multiplier
  })

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return <ArrowUpDown className="h-4 w-4 text-gray-400" />
    return sortDirection === 'asc' ? 
      <ChevronUp className="h-4 w-4 text-blue-500" /> : 
      <ChevronDown className="h-4 w-4 text-blue-500" />
  }

  const columns: { field: SortField; label: string; align?: string }[] = [
    { field: 'Account Name', label: 'Account' },
    { field: 'Opportunity Name', label: 'Opportunity' },
    { field: 'Total ACV', label: 'Value', align: 'right' },
    { field: 'Created Date', label: 'Date Created', align: 'right' },
    { field: 'Days Open', label: 'Days Open', align: 'right' }
  ]

  const formatCurrency = (value: number) => {
    return value.toLocaleString(undefined, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] m-4">
        <div className="p-6 flex justify-between items-center border-b">
          <h2 className="text-xl font-semibold">Aging Opportunities</h2>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="p-6 overflow-auto max-h-[calc(80vh-120px)]">
          <table className="w-full divide-y divide-gray-200">
            <thead>
              <tr className="bg-gradient-to-r from-blue-50 to-indigo-50">
                {columns.map(({ field, label, align }) => (
                  <th 
                    key={field}
                    className={`px-4 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider ${
                      align === 'right' ? 'text-right' : 'text-left'
                    }`}
                  >
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleSort(field)}
                      className={`flex items-center gap-1 hover:text-blue-600 transition-colors ${
                        sortField === field ? 'text-blue-600' : 'text-gray-500'
                      }`}
                    >
                      {label}
                      <SortIcon field={field} />
                    </Button>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sortedOpportunities.map((opp, index) => (
                <tr key={index} className="hover:bg-blue-50 transition-colors">
                  <td className="px-4 py-3 text-sm text-gray-900">{opp["Account Name"]}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{opp["Opportunity Name"]}</td>
                  <td className="px-4 py-3 text-sm text-right text-blue-600">
                    ${formatCurrency(opp["Total ACV"])}
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-900">
                    {formatDate(opp["Created Date"])}
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-900">
                    {opp["Days Open"].toFixed(0)} days
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
} 