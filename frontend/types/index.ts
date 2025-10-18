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
  logo_url?: string  // Company logo from Clearbit
  similarity_score: number
  tags: {
    [key: string]: string
  }
  traction_snippet: string
  funding_snippet: string
  outcome_label: 'win' | 'ok' | 'fail'
  citations: Citation[]
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
  category?: string | null  // Flexible category from AI
  media_url?: string | null  // Visual demonstration if available
  media_description?: string | null
  source_company?: string | null
  citations: Citation[]
}

export interface MarketVisualContent {
  visual_content: Array<{
    url: string
    type: string
    description: string
  }>
  market_insights: string[]
  media_results_count: number
}

export interface AnalysisResult {
  id: string
  idea_summary: string
  tags: string[]
  mcq_answers?: MCQAnswer[]
  comparables: Comparable[]
  market_analysis: MarketAnalysis
  market_visual_content?: MarketVisualContent
  execution_levers: ExecutionLever[]
  pivot_suggestions: PivotSuggestion[]
  created_at: string
}

