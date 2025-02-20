export default function Loading() {
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-32 h-32">
        {/* Outer ring - slower rotation */}
        <div className="absolute inset-0 rounded-full border-4 border-blue-100 opacity-20"></div>
        <div className="absolute inset-0 rounded-full border-4 border-blue-500 border-t-transparent animate-spin-slow"></div>
        
        {/* Inner ring - faster rotation */}
        <div className="absolute inset-4 rounded-full border-4 border-blue-100 opacity-20"></div>
        <div className="absolute inset-4 rounded-full border-4 border-blue-400 border-t-transparent animate-spin"></div>
        
        {/* Center dot */}
        <div className="absolute inset-[42%] rounded-full bg-blue-500"></div>
      </div>
      
      <div className="mt-8 text-center">
        <p className="text-xl font-semibold text-blue-700">
          Analyzing your report...
        </p>
      </div>
    </div>
  )
}

