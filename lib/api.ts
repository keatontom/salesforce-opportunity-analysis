import { AnalysisResults } from '@/types/analysis'

export type { AnalysisResults }

export async function analyzeFile(file: File): Promise<AnalysisResults> {
  const formData = new FormData()
  formData.append('file', file)
  const response = await fetch(`https://salesforce-opportunity-analysis.fly.dev/api/analyze`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Analysis failed')
  }

  return response.json()
}
