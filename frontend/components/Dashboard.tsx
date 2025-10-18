'use client'

import {
  Target,
  TrendingUp,
  AlertTriangle,
  Zap,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  XCircle,
  MinusCircle,
} from 'lucide-react'
import type { AnalysisResult } from '@/types'
import { formatConfidenceInterval, formatPercentage } from '@/lib/utils'
import ProbabilityChart from './ProbabilityChart'
import RiskRadarChart from './RiskRadarChart'

interface DashboardProps {
  result: AnalysisResult
  onReset: () => void
}

export default function Dashboard({ result, onReset }: DashboardProps) {
  const getOutcomeIcon = (label: string) => {
    switch (label) {
      case 'win':
        return <CheckCircle2 className="w-5 h-5 text-green-600" />
      case 'fail':
        return <XCircle className="w-5 h-5 text-red-600" />
      default:
        return <MinusCircle className="w-5 h-5 text-yellow-600" />
    }
  }

  const getOutcomeColor = (label: string) => {
    switch (label) {
      case 'win':
        return 'bg-green-50 border-green-200'
      case 'fail':
        return 'bg-red-50 border-red-200'
      default:
        return 'bg-yellow-50 border-yellow-200'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            <h1 className="text-3xl font-serif font-bold text-slate-900 mb-3">
              {result.idea_summary}
            </h1>
            <div className="flex flex-wrap gap-2 mb-4">
              {result.tags.map((tag) => (
                <span
                  key={tag}
                  className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-medium"
                >
                  {tag}
                </span>
              ))}
            </div>
            {result.mcq_answers && result.mcq_answers.length > 0 && (
              <div className="space-y-2">
                {result.mcq_answers.map((answer, idx) => (
                  <div key={idx} className="text-sm">
                    <span className="text-slate-600">{answer.question}</span>
                    <span className="ml-2 font-medium text-slate-900">{answer.answer}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
          <div className="ml-6 text-right">
            <div className="text-sm text-slate-600 mb-1">Evidence Confidence</div>
            <div className="text-4xl font-serif font-bold text-slate-900">
              {result.confidence_score}
              <span className="text-xl text-slate-600">/100</span>
            </div>
          </div>
        </div>
        <button
          onClick={onReset}
          className="px-6 py-2 border-2 border-slate-200 rounded-xl font-medium text-slate-700 hover:bg-slate-50 transition-all flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Analyze Another Idea
        </button>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Left Column - 2/3 width */}
        <div className="lg:col-span-2 space-y-6">
          {/* Outcome Probabilities */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <Target className="w-6 h-6 text-slate-900" />
              <h2 className="text-2xl font-serif font-bold text-slate-900">
                Outcome Probabilities (12–24 months)
              </h2>
            </div>
            <ProbabilityChart probabilities={result.outcome_probabilities} />
            <div className="mt-6 grid md:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="text-sm text-slate-600 mb-1">Next Round</div>
                <div className="text-xl font-serif font-bold text-slate-900">
                  {formatConfidenceInterval(
                    result.outcome_probabilities.next_round.mean,
                    result.outcome_probabilities.next_round.lower_ci,
                    result.outcome_probabilities.next_round.upper_ci
                  )}
                </div>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="text-sm text-slate-600 mb-1">PMF Proxy</div>
                <div className="text-xl font-serif font-bold text-slate-900">
                  {formatConfidenceInterval(
                    result.outcome_probabilities.pmf_proxy.mean,
                    result.outcome_probabilities.pmf_proxy.lower_ci,
                    result.outcome_probabilities.pmf_proxy.upper_ci
                  )}
                </div>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="text-sm text-slate-600 mb-1">24m Survival</div>
                <div className="text-xl font-serif font-bold text-slate-900">
                  {formatConfidenceInterval(
                    result.outcome_probabilities.survival_24m.mean,
                    result.outcome_probabilities.survival_24m.lower_ci,
                    result.outcome_probabilities.survival_24m.upper_ci
                  )}
                </div>
              </div>
              <div className="p-4 bg-slate-50 rounded-xl">
                <div className="text-sm text-slate-600 mb-1">Capital Efficiency</div>
                <div className="text-xl font-serif font-bold text-slate-900">
                  {result.outcome_probabilities.capital_efficiency_percentile.toFixed(0)}th percentile
                </div>
              </div>
            </div>
          </div>

          {/* Comparable Companies */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
            <h2 className="text-2xl font-serif font-bold text-slate-900 mb-6">
              Similar Startups
            </h2>
            <div className="space-y-4">
              {result.comparables.slice(0, 5).map((comp, idx) => (
                <div
                  key={idx}
                  className={`p-5 border-2 rounded-xl ${getOutcomeColor(comp.outcome_label)}`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      {getOutcomeIcon(comp.outcome_label)}
                      <h3 className="font-serif font-bold text-slate-900 text-lg">
                        {comp.name}
                      </h3>
                    </div>
                    <div className="text-sm font-medium text-slate-600">
                      {comp.similarity_score.toFixed(0)}% match
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {Object.entries(comp.tags).map(([key, value]) => (
                      <span
                        key={key}
                        className="px-2 py-1 bg-white rounded-md text-xs font-medium text-slate-700"
                      >
                        {value}
                      </span>
                    ))}
                  </div>
                  <p className="text-sm text-slate-700 mb-2">{comp.traction_snippet}</p>
                  <p className="text-sm text-slate-600">{comp.funding_snippet}</p>
                  {comp.citations.length > 0 && (
                    <a
                      href={comp.citations[0].url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-3 inline-flex items-center gap-1 text-sm text-slate-600 hover:text-slate-900 transition-colors"
                    >
                      <ExternalLink className="w-4 h-4" />
                      Source
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Execution Levers */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <Zap className="w-6 h-6 text-slate-900" />
              <h2 className="text-2xl font-serif font-bold text-slate-900">
                Execution Levers
              </h2>
            </div>
            <div className="space-y-4">
              {result.execution_levers.map((lever, idx) => (
                <div key={idx} className="p-5 bg-slate-50 rounded-xl">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-slate-900">{lever.title}</h3>
                    <span
                      className={`px-2 py-1 rounded-md text-xs font-medium ${
                        lever.impact === 'high'
                          ? 'bg-green-100 text-green-700'
                          : lever.impact === 'medium'
                          ? 'bg-yellow-100 text-yellow-700'
                          : 'bg-slate-100 text-slate-700'
                      }`}
                    >
                      {lever.impact} impact
                    </span>
                  </div>
                  <p className="text-sm text-slate-700">{lever.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - 1/3 width */}
        <div className="space-y-6">
          {/* Market & Competition */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-slate-900" />
              <h2 className="text-xl font-serif font-bold text-slate-900">
                Market & Competition
              </h2>
            </div>
            <div className="space-y-4">
              <div>
                <div className="text-sm text-slate-600 mb-2">Crowding Index</div>
                <div className="flex items-center gap-3">
                  <div className="flex-1 h-3 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500"
                      style={{ width: `${result.market_analysis.crowding_index}%` }}
                    />
                  </div>
                  <span className="text-lg font-serif font-bold text-slate-900">
                    {result.market_analysis.crowding_index.toFixed(0)}
                  </span>
                </div>
              </div>
              <div>
                <div className="text-sm text-slate-600 mb-1">TAM/SAM</div>
                <p className="text-sm text-slate-900">{result.market_analysis.tam_sam_rationale}</p>
              </div>
              <div>
                <div className="text-sm text-slate-600 mb-1">Funding Velocity</div>
                <p className="text-sm text-slate-900">{result.market_analysis.funding_velocity}</p>
              </div>
              <div>
                <div className="text-sm text-slate-600 mb-1">Notable Moats</div>
                <p className="text-sm text-slate-900">{result.market_analysis.notable_moats}</p>
              </div>
            </div>
          </div>

          {/* Risk Radar */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="w-5 h-5 text-slate-900" />
              <h2 className="text-xl font-serif font-bold text-slate-900">Risk Radar</h2>
            </div>
            <RiskRadarChart risk={result.risk_radar} />
            <div className="mt-4 space-y-3">
              {Object.entries(result.risk_radar.explanations).map(([key, value]) => (
                <div key={key} className="text-sm">
                  <span className="font-medium text-slate-900 capitalize">
                    {key.replace('_', ' ')}:
                  </span>{' '}
                  <span className="text-slate-700">{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Pivot Navigator */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6">
            <h2 className="text-xl font-serif font-bold text-slate-900 mb-4">
              Pivot Navigator
            </h2>
            <div className="space-y-4">
              {result.pivot_suggestions.map((pivot, idx) => (
                <div key={idx} className="p-4 bg-blue-50 border border-blue-200 rounded-xl">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-slate-900 text-sm">{pivot.title}</h3>
                    <span className="text-xs font-medium text-green-600">
                      +{formatPercentage(pivot.expected_uplift, 1)}
                    </span>
                  </div>
                  <p className="text-xs text-slate-700 mb-2">{pivot.rationale}</p>
                  <div className="text-xs text-slate-600">
                    Effort: {pivot.effort_score.toFixed(1)}/10
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Evidence Summary */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6">
            <h2 className="text-xl font-serif font-bold text-slate-900 mb-4">
              Evidence Summary
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">Total Sources</span>
                <span className="font-semibold text-slate-900">
                  {result.evidence_summary.total_sources}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">High Quality</span>
                <span className="font-semibold text-slate-900">
                  {result.evidence_summary.high_quality_sources}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-slate-600">Recent (≤12mo)</span>
                <span className="font-semibold text-slate-900">
                  {result.evidence_summary.recent_sources}
                </span>
              </div>
              <div className="pt-3 border-t border-slate-200">
                <div className="text-sm text-slate-600 mb-2">Source Types</div>
                {Object.entries(result.evidence_summary.source_types).map(([type, count]) => (
                  <div key={type} className="flex justify-between items-center text-xs mb-1">
                    <span className="text-slate-600 capitalize">{type}</span>
                    <span className="text-slate-900">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

