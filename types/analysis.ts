export interface CoreMetrics {
  "Total Volume": number;
  "Average Deal Size": number;
  "Win Rate": number;
  "Average Time to Close": number;
  "Number of Opportunities": number;
}

export interface PerformanceRecord {
  "Total Volume": number;
  "Avg Deal Size": number;
  "Win Rate": number;
  [key: string]: any;
}

export interface TypePerformanceRecord extends PerformanceRecord {
  Type: string;
  opportunities: TypeOpportunity[];
}

interface StageDistribution {
  percentage: number;
  count: number;
}

export interface PipelineHealth {
  "Stage Distribution": Record<string, StageDistribution>;
  "Lost Reasons": Record<string, number>;
  "Aging Opportunities": {
    Count: number;
    "Total Value": number;
    Details: Array<{
      "Account Name": string;
      "Opportunity Name": string;
      "Total ACV": number;
      "Created Date": string;
      "Days Open": number;
      "Stage": string;
    }>;
  };
}

export interface OpenOpportunityTableRow {
  Opportunity: string;
  Score: string;
  Risk: string;
  Value: string;
  "Days Open": number;
  "Key Insights": string;
}

export interface OpenOpportunityAnalysis {
  has_data: boolean;
  message?: string;
  total_opportunities?: number;
  total_value?: number;
  average_score?: number;
  summary_insights?: Array<{
    category: string;
    finding: string;
    severity: 'high' | 'medium' | 'low';
  }>;
  opportunity_table?: {
    headers: string[];
    rows: OpenOpportunityTableRow[];
  };
  scoring_factors?: Record<string, number>;
}

export interface Visualization {
  data: string;
  config: {
    displayModeBar: boolean;
    staticPlot: boolean;
    responsive: boolean;
  };
}

export interface Visualizations {
  "Win Rate Trend": Visualization;
  "Volume Trend": Visualization;
  "Win Rates by Type": Visualization;
}

export interface SegmentPerformance {
  "Type Performance": TypePerformanceRecord[];
  "Practice Area Performance": PerformanceRecord[];
  "Account Performance": PerformanceRecord[];
}

export interface StageAnalysis {
  has_data: boolean;
  message?: string;
  total_value?: number;
  avg_value?: number;
  avg_cycle_length?: number;
  insights?: Array<{
    category: string;
    finding: string;
    severity: 'high' | 'medium' | 'low';
  }>;
}

export interface WinAnalysis extends StageAnalysis {
  total_won?: number;
  total_value_won?: number;
  avg_value_won?: number;
}

export interface LossAnalysis extends StageAnalysis {
  total_lost?: number;
  total_value_lost?: number;
  avg_value_lost?: number;
}

export interface OpenOpportunityData {
  has_data: boolean;
  message?: string;
  total_open?: number;
  total_opportunities?: number;
  total_value?: number;
  total_pipeline_value?: number;
  avg_value?: number;
  average_value?: number;
  average_score?: number;
  avg_cycle_length?: number;
  insights?: Array<{
    category: string;
    finding: string;
    severity: 'high' | 'medium' | 'low';
  }>;
  opportunity_table?: {
    headers: string[];
    rows: OpenOpportunityTableRow[];
  };
}

export interface AnalysisResults {
  "Advanced Analysis": {
    "Core Metrics": CoreMetrics;
    "Pipeline Health": PipelineHealth;
    "Win Analysis": WinAnalysis;
    "Loss Analysis": LossAnalysis;
    "Score Open Opportunities": OpenOpportunityData;
    "Segment Performance": SegmentPerformance;
  };
  "Visualizations": Visualizations;
}

export interface TypeOpportunity {
  "Account Name": string;
  "Opportunity Name": string;
  "Total ACV": number;
  "Created Date": string;
  "Type": string;
}