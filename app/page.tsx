'use client'

import { useState } from 'react'
import FileUpload from '@/components/FileUpload'
import Loading from '@/components/Loading'
import AnalysisResults from '@/components/AnalysisResults'
import { analyzeFile, AnalysisResults as AnalysisResultsType } from '../lib/api'
import { DateRange } from '@/components/analysis/DateFilter'

export default function Home() {
  const [file, setFile] = useState<File | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResults, setAnalysisResults] = useState<AnalysisResultsType | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [dateRange, setDateRange] = useState<DateRange>('ytd')

  const handleFileUpload = (uploadedFile: File) => {
    setFile(uploadedFile)
  }

  const handleAnalyze = async () => {
    if (!file) return

    setIsAnalyzing(true)
    setError(null)

    try {
      const data = await analyzeFile(file, dateRange)
      setAnalysisResults(data)
    } catch (error) {
      console.error("Error during analysis:", error)
      setError(error instanceof Error ? error.message : 'Failed to analyze file')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleDateRangeChange = async (newRange: DateRange) => {
    setDateRange(newRange)
    if (file && analysisResults) {
      setIsAnalyzing(true)
      setError(null)
      try {
        const data = await analyzeFile(file, newRange)
        setAnalysisResults(data)
      } catch (error) {
        console.error("Error during analysis:", error)
        setError(error instanceof Error ? error.message : 'Failed to analyze file')
      } finally {
        setIsAnalyzing(false)
      }
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">Salesforce Opportunity Report Analyzer</h1>
      {!isAnalyzing && !analysisResults && (
        <FileUpload onFileUpload={handleFileUpload} onAnalyze={handleAnalyze} file={file} />
      )}
      {isAnalyzing && <Loading />}
      {analysisResults && (
        <AnalysisResults 
          results={analysisResults} 
          onDateRangeChange={handleDateRangeChange}
        />
      )}
      {error && <p className="text-red-500">{error}</p>}
    </main>
  )
}

