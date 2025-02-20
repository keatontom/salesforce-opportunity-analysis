import { ChangeEvent } from 'react'
import { Button } from "@/components/ui/button"
import { Download } from 'lucide-react'

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

  const handleDownloadSample = async () => {
    try {
      const response = await fetch('/Opportunity_Report_SAMPLE.csv')
      if (!response.ok) throw new Error('Failed to download file')
      
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = 'Opportunity_Report_SAMPLE.csv'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error downloading file:', error)
      alert('Failed to download the sample file. Please try again.')
    }
  }

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="flex flex-col items-center gap-2">
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
        />
        <Button
          variant="outline"
          onClick={handleDownloadSample}
          className="text-sm"
        >
          <Download className="w-4 h-4" />
          Download Sample CSV
        </Button>
      </div>
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

