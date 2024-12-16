import { ChangeEvent } from 'react'
import { Button } from "@/components/ui/button"

interface FileUploadProps {
  onFileUpload: (file: File) => void
  onAnalyze: () => void
  file: File | null
}

export default function FileUpload({ onFileUpload, onAnalyze, file }: FileUploadProps) {
  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (files && files.length > 0) {
      onFileUpload(files[0])
    }
  }

  return (
    <div className="flex flex-col items-center gap-4">
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
      />
      {file && (
        <div className="text-sm text-gray-500">
          Selected file: {file.name}
        </div>
      )}
      <Button onClick={onAnalyze} disabled={!file}>
        Analyze Report
      </Button>
    </div>
  )
}

