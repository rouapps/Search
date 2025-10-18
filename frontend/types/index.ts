export interface MCQQuestion {
  question: string
  options: string[]
  reason: string
}

export interface MCQAnswer {
  question: string
  answer: string
}

export interface Citation {
  title: string
  url: string
  snippet: string
  date?: string
}

export interface Comparable {
  name: string
  url: string
  similarity_score: number
  tags: {
    [key: string]: string
  }
  traction_snippet: string
  funding_snippet: string
  outcome_label: 'win' | 'ok' | 'fail'
  citations: Citation[]
}

export interface OutcomeProbabilities {
  next_round: {
    mean: number
    lower_ci: number
    upper_ci: number
  }
  pmf_proxy: {
    mean: number
    lower_ci: number
    upper_ci: number
  }
  survival_24m: {
    mean: number
    lower_ci: number
    upper_ci: number
  }
  capital_efficiency_percentile: number
}

export interface RiskRadar {
  regulatory: number
  platform_dependency: number
  pricing_pressure: number
  distribution_risk: number
  explanations: {
    [key: string]: string
  }
}

export interface PivotSuggestion {
  title: string
  rationale: string
  expected_uplift: number
  effort_score: number
  citations: Citation[]
}

export interface MarketAnalysis {
  crowding_index: number
  tam_sam_rationale: string
  funding_velocity: string
  notable_moats: string
  citations: Citation[]
}

export interface ExecutionLever {
  title: string
  description: string
  impact: 'high' | 'medium' | 'low'
  citations: Citation[]
}

export interface AnalysisResult {
  id: string
  idea_summary: string
  tags: string[]
  mcq_answers?: MCQAnswer[]
  comparables: Comparable[]
  outcome_probabilities: OutcomeProbabilities
  market_analysis: MarketAnalysis
  risk_radar: RiskRadar
  execution_levers: ExecutionLever[]
  pivot_suggestions: PivotSuggestion[]
  confidence_score: number
  evidence_summary: {
    total_sources: number
    high_quality_sources: number
    recent_sources: number
    source_types: {
      [key: string]: number
    }
  }
  created_at: string
}

