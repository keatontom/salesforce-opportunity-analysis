import { ChangeEvent } from 'react'
import { Button } from "@/components/ui/button"
import { Download, Upload, Info } from 'lucide-react'

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
    <div className="fixed inset-0 min-h-screen w-full flex flex-col items-center justify-between py-12 bg-gradient-to-br from-white from-5% via-blue-200 via-50% to-blue-500">
      <div className="flex-1 flex flex-col items-center justify-center w-full">
        <div className="bg-white/90 backdrop-blur-sm p-6 rounded-2xl shadow-2xl max-w-xl w-full mx-4">
          <div className="flex flex-col items-center">
            <h1 className="text-3xl font-bold text-blue-700 mb-8">
              Salesforce Opportunity Analysis
            </h1>
            
            <div className="flex flex-col items-center justify-center w-full flex-1 mb-6">
              <div className="relative w-full">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="w-full cursor-pointer opacity-0 absolute inset-0 z-10 h-[52px]"
                />
                <div className="w-full bg-blue-50 hover:bg-blue-100 rounded-xl py-3 flex items-center justify-center gap-3 transition-colors duration-200 text-lg font-semibold">
                  <Upload className="w-5 h-5 text-blue-500" />
                  <span className="text-blue-500">
                    {file ? 'Change CSV File' : 'Choose CSV File'}
                  </span>
                </div>
              </div>
              {file && (
                <div className="text-sm text-blue-500 mt-3 flex items-center gap-2">
                  <span className="font-medium">Selected:</span> {file.name}
                </div>
              )}
            </div>

            <div className="w-full space-y-3">
              <Button 
                onClick={onAnalyze} 
                disabled={!file}
                className="bg-blue-400 hover:bg-blue-500 text-white w-full py-3 text-lg font-semibold rounded-xl"
              >
                Analyze Report
              </Button>
              {file && (
                <p className="text-xs text-blue-500 text-center">
                  <Info className="w-3 h-3 inline-block mr-1" />
                  Analysis may take up to 30 seconds for large reports
                </p>
              )}
            </div>
          </div>
        </div>

        <div className="mt-8">
          <Button
            variant="link"
            onClick={handleDownloadSample}
            className="text-white font-semibold text-lg flex items-center gap-3 hover:text-blue-100 transition-colors"
          >
            <Download className="w-6 h-6" />
            Download Sample Report
          </Button>
        </div>
      </div>

      <div className="text-xs text-blue-900/70 flex items-center gap-1.5 bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
        <Info className="w-3.5 h-3.5" />
        <span>Required columns: Account Name, Opportunity Name, Stage, Close Date, Created Date, Type, Total ACV, Primary Campaign Source, Closed Lost Reason, Law Firm Practice Area, NumofLawyers</span>
      </div>
    </div>
  )
}

