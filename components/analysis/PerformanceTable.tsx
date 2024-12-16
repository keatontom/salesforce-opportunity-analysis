import { useState } from 'react'
import { PerformanceRecord, TypePerformanceRecord } from '@/types/analysis'
import { Button } from "@/components/ui/button"
import { ChevronDown, ChevronUp, ArrowUpDown } from 'lucide-react'
import TypeDetailsTable from '@/components/analysis/TypeDetailsTable'

type SortField = 'Total Volume' | 'Avg Deal Size' | 'Win Rate'
type SortDirection = 'asc' | 'desc'

interface PerformanceTableProps<T extends PerformanceRecord> {
  data: T[];
  title: string;
  nameField: keyof T;
  chart?: React.ReactNode;
  isTypeTable?: boolean;
}

const isRenderable = (value: unknown): value is string | number => 
  typeof value === 'string' || typeof value === 'number';

export default function PerformanceTable<T extends PerformanceRecord>({ 
  data, 
  title, 
  nameField, 
  chart,
  isTypeTable = false
}: PerformanceTableProps<T>) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [sortField, setSortField] = useState<SortField>('Total Volume')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')
  const [selectedType, setSelectedType] = useState<string | null>(null)

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const sortedData = [...data].sort((a, b) => {
    const multiplier = sortDirection === 'asc' ? 1 : -1
    return (a[sortField] - b[sortField]) * multiplier
  })

  const displayData = isExpanded ? sortedData : sortedData.slice(0, 5)

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return <ArrowUpDown className="h-4 w-4 text-gray-400" />
    return sortDirection === 'asc' ? 
      <ChevronUp className="h-4 w-4 text-blue-500" /> : 
      <ChevronDown className="h-4 w-4 text-blue-500" />
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-semibold text-gray-800">{title}</h3>
        {data.length > 5 && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="flex items-center gap-1 text-gray-600 hover:text-blue-600 transition-colors"
          >
            {isExpanded ? (
              <>Show Less <ChevronUp className="h-4 w-4" /></>
            ) : (
              <>Show All ({data.length}) <ChevronDown className="h-4 w-4" /></>
            )}
          </Button>
        )}
      </div>

      <div className={`grid ${chart ? 'lg:grid-cols-2' : ''} gap-6`}>
        <div className="overflow-x-auto rounded-lg border border-gray-100">
          <table className="w-full divide-y divide-gray-200">
            <thead>
              <tr className="bg-gradient-to-r from-blue-50 to-indigo-50">
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-[30%]">
                  Name
                </th>
                {[
                  { field: 'Total Volume', label: 'Volume', width: '30%' },
                  { field: 'Avg Deal Size', label: 'Avg Size', width: '25%' },
                  { field: 'Win Rate', label: 'Win Rate', width: '15%' }
                ].map(({ field, label, width }) => (
                  <th 
                    key={field} 
                    className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    style={{ width }}
                  >
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleSort(field as SortField)}
                      className={`flex items-center gap-1 hover:text-blue-600 transition-colors ${
                        sortField === field ? 'text-blue-600' : 'text-gray-500'
                      }`}
                    >
                      {label}
                      <SortIcon field={field as SortField} />
                    </Button>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {displayData.map((record, index) => (
                <tr 
                  key={index}
                  className="hover:bg-blue-50 transition-colors"
                >
                  <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                    {isRenderable(record[nameField]) ? record[nameField] : String(record[nameField])}
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right">
                          <span className="text-blue-600 font-medium">
                      ${record["Total Volume"].toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                      })}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right">
                    <span className="text-indigo-600 font-medium">
                      ${record["Avg Deal Size"].toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2
                      })}
                    </span>
                  </td>
                  <td className="px-4 py-3 whitespace-nowrap text-sm text-right">
                    <span className={`font-medium ${
                      record["Win Rate"] > 70 ? 'text-green-600' :
                      record["Win Rate"] > 40 ? 'text-blue-600' : 
                      'text-gray-600'
                    }`}>
                      {record["Win Rate"].toFixed(2)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {chart && (
          <div className="h-full flex items-center justify-center">
            {chart}
          </div>
        )}
      </div>

      {selectedType && isTypeTable && (
        <TypeDetailsTable
          opportunities={(data as unknown as TypePerformanceRecord[]).find(r => r.Type === selectedType)?.opportunities || []}
          type={selectedType}
          onClose={() => setSelectedType(null)}
        />
      )}
    </div>
  )
} 