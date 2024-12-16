export default function Loading() {
  return (
    <div className="flex flex-col items-center">
      <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      <p className="mt-4 text-xl">Analyzing your report...</p>
    </div>
  )
}

