export interface CoreMetrics {
  "Total Volume": number;
  "Average Deal Size": number;
  "Win Rate": number;
  "Average Time to Close": number;
  "Number of Opportunities": number;
}

export interface PerformanceRecord {
  [key: string]: string | number | TypeOpportunity[];
  "Total Volume": number;
  "Avg Deal Size": number;
  "Win Rate": number;
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

export interface Visualization {
  data: string;
  config: {
    displayModeBar: boolean;
    staticPlot: boolean;
    responsive: boolean;
  };
}

export interface AnalysisResults {
  "Advanced Analysis": {
    "Core Metrics": CoreMetrics;
    "Segment Performance": {
      "Account Performance": PerformanceRecord[];
      "Type Performance": PerformanceRecord[];
      "Practice Area Performance": PerformanceRecord[];
    };
    "Pipeline Health": PipelineHealth;
    "Loss Analysis": {
      has_data: boolean;
      message?: string;
      total_lost?: number;
      total_value_lost?: number;
      avg_cycle_length?: number;
      insights?: Array<{
        category: string;
        finding: string;
        severity: 'high' | 'medium' | 'low';
      }>;
    };
    "Win Analysis": {
      has_data: boolean;
      message?: string;
      total_won?: number;
      total_value_won?: number;
      avg_cycle_length?: number;
      insights?: Array<{
        category: string;
        finding: string;
        severity: 'high' | 'medium' | 'low';
      }>;
    };
  };
  "Visualizations": {
    "Win Rates by Type": Visualization;
    "Win Rate Trend": Visualization;
    "Volume Trend": Visualization;
  };
}

export type DateRange = 'all' | 'q1' | 'q2' | 'q3' | 'q4' | 'ytd' | 'last_year'; 

export interface TypeOpportunity {
  "Account Name": string;
  "Opportunity Name": string;
  "Total ACV": number;
  "Created Date": string;
  "Type": string;
}