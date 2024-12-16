interface InsightsProps {
  insights: string[];
}

export default function Insights({ insights }: InsightsProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">Actionable Insights</h3>
      <ul className="space-y-3">
        {insights.map((insight, index) => (
          <li key={index} className="bg-gray-50 p-4 rounded">{insight}</li>
        ))}
      </ul>
    </div>
  )
} 