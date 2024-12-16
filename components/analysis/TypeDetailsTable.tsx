import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { X, ArrowUpDown, ChevronUp, ChevronDown } from 'lucide-react'
import { TypeOpportunity } from '@/types/analysis'

interface TypeDetailsTableProps {
  opportunities: TypeOpportunity[];
  onClose: () => void;
  type: string;
}

type SortField = keyof TypeOpportunity
type SortDirection = 'asc' | 'desc'

export default function TypeDetailsTable({ opportunities, onClose, type }: TypeDetailsTableProps) {
  const [sortField, setSortField] = useState<SortField>('Total ACV')
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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[80vh] m-4">
        <div className="p-6 flex justify-between items-center border-b">
          <h2 className="text-xl font-semibold">{type} Opportunities</h2>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="h-4 w-4" />
          </Button>
        </div>
        <div className="p-6 overflow-auto max-h-[calc(80vh-120px)]">
          <table className="w-full divide-y divide-gray-200">
            <thead>
              <tr className="bg-gradient-to-r from-blue-50 to-indigo-50">
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleSort('Account Name')}
                    className="flex items-center gap-1"
                  >
                    Account
                    <SortIcon field="Account Name" />
                  </Button>
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleSort('Opportunity Name')}
                    className="flex items-center gap-1"
                  >
                    Opportunity
                    <SortIcon field="Opportunity Name" />
                  </Button>
                </th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleSort('Total ACV')}
                    className="flex items-center gap-1 ml-auto"
                  >
                    Value
                    <SortIcon field="Total ACV" />
                  </Button>
                </th>
                <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleSort('Created Date')}
                    className="flex items-center gap-1 ml-auto"
                  >
                    Created Date
                    <SortIcon field="Created Date" />
                  </Button>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sortedOpportunities.map((opp, index) => (
                <tr key={index} className="hover:bg-blue-50 transition-colors">
                  <td className="px-4 py-3 text-sm text-gray-900">{opp["Account Name"]}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{opp["Opportunity Name"]}</td>
                  <td className="px-4 py-3 text-sm text-right text-blue-600">
                    ${opp["Total ACV"].toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2
                    })}
                  </td>
                  <td className="px-4 py-3 text-sm text-right text-gray-900">
                    {formatDate(opp["Created Date"])}
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