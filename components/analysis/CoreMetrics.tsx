import { CoreMetrics as CoreMetricsType } from '@/types/analysis'

interface CoreMetricsProps {
  metrics: CoreMetricsType;
  title?: string;
}

export default function CoreMetrics({ metrics, title = "Core Metrics" }: CoreMetricsProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 transition-all duration-200 hover:shadow-lg hover:scale-[1.01]">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">{title}</h3>
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(metrics).map(([key, value]: [string, number]) => (
          <div key={key} className="bg-gradient-to-r from-blue-50 to-indigo-50 p-4 rounded hover:from-blue-100 hover:to-indigo-100 transition-colors">
            <h4 className="text-sm text-gray-600">{key}</h4>
            <p className="text-lg font-semibold text-blue-600">
              {key.includes('Rate') 
                ? `${value.toFixed(2)}%`
                : key.includes('Volume') || key.includes('Size')
                  ? `$${value.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2
                    })}`
                  : key.includes('Time to Close')
                    ? `${Math.round(value)} days`
                    : key.includes('Opportunities')
                      ? value.toLocaleString()
                      : value.toFixed(2)}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
} 