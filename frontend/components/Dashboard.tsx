'use client'

import {
  TrendingUp,
  Zap,
  RefreshCw,
  ExternalLink,
  CheckCircle2,
  XCircle,
  MinusCircle,
  Image as ImageIcon,
} from 'lucide-react'
import type { AnalysisResult } from '@/types'
import { formatPercentage } from '@/lib/utils'

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
          {/* Market Landscape */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
            <div className="flex items-center gap-3 mb-6">
              <TrendingUp className="w-6 h-6 text-slate-900" />
              <h2 className="text-2xl font-serif font-bold text-slate-900">
                Market Landscape
              </h2>
            </div>
            
            <div className="prose prose-slate max-w-none">
              <div className="text-slate-700 whitespace-pre-line">
                {result.market_analysis.landscape}
              </div>
            </div>
          </div>

          {/* Comparable Companies */}
          <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
            <h2 className="text-2xl font-serif font-bold text-slate-900 mb-6">
              Similar Startups
            </h2>
            <div className="space-y-4">
              {result.comparables.slice(0, 10).map((comp, idx) => (
                <div
                  key={idx}
                  className={`p-5 border-2 rounded-xl ${getOutcomeColor(comp.outcome_label)} transition-all hover:shadow-md`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      {getOutcomeIcon(comp.outcome_label)}
                      <a 
                        href={comp.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-3 hover:opacity-80 transition-opacity"
                      >
                        {comp.logo_url && (
                          <img 
                            src={comp.logo_url}
                            alt={`${comp.name} logo`}
                            className="w-8 h-8 object-contain rounded"
                            onError={(e) => {
                              // Fallback if logo doesn't load
                              e.currentTarget.style.display = 'none';
                            }}
                          />
                        )}
                        <h3 className="font-serif font-bold text-slate-900 text-lg hover:text-blue-600">
                          {comp.name}
                        </h3>
                      </a>
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
                  <p className="text-sm text-slate-600 mb-3">{comp.funding_snippet}</p>
                  {comp.citations.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-slate-200">
                      {comp.citations.slice(0, 2).map((citation, citIdx) => (
                        <a
                          key={citIdx}
                          href={citation.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 hover:underline transition-colors"
                          title={citation.title}
                        >
                          <ExternalLink className="w-3 h-3" />
                          {citation.title.substring(0, 40)}{citation.title.length > 40 ? '...' : ''}
                        </a>
                      ))}
                    </div>
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
            <div className="space-y-6">
              {result.execution_levers.map((lever, idx) => (
                <div key={idx} className="p-6 bg-slate-50 rounded-xl border border-slate-200">
                  {/* Header with category and impact */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      {lever.category && (
                        <div className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-1">
                          {lever.category}
                        </div>
                      )}
                      <h3 className="font-semibold text-lg text-slate-900">{lever.title}</h3>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ml-3 ${
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
                  
                  {/* Description */}
                  <p className="text-sm text-slate-700 mb-4">{lever.description}</p>
                  
                  {/* Visual demonstration if available */}
                  {lever.media_url && (
                    <div className="mt-4 rounded-lg overflow-hidden border border-slate-300">
                      {lever.media_url.includes('youtube.com') || lever.media_url.includes('youtu.be') || lever.media_url.includes('vimeo.com') ? (
                        <div className="aspect-video bg-slate-100 flex items-center justify-center">
                          <Video className="w-12 h-12 text-slate-400" />
                          <p className="ml-2 text-sm text-slate-600">Video demonstration available</p>
                        </div>
                      ) : (
                        <img 
                          src={lever.media_url} 
                          alt={lever.media_description || 'Visual demonstration'}
                          className="w-full h-auto"
                          onError={(e) => {
                            e.currentTarget.style.display = 'none';
                          }}
                        />
                      )}
                      {lever.media_description && (
                        <div className="p-3 bg-slate-100 border-t border-slate-200">
                          <p className="text-xs text-slate-600">{lever.media_description}</p>
                        </div>
                      )}
                    </div>
                  )}
                  
                  {/* Source company if available */}
                  {lever.source_company && (
                    <div className="mt-3 flex items-center gap-2 text-xs text-slate-500">
                      <ExternalLink className="w-3 h-3" />
                      <span>Example from: <span className="font-medium text-slate-700">{lever.source_company}</span></span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - 1/3 width */}
        <div className="space-y-6">
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
        </div>
      </div>


      {/* Market Visual Content Section - Full Width */}
      {result.market_visual_content && result.market_visual_content.visual_content.length > 0 && (
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
          <div className="flex items-center gap-3 mb-6">
            <ImageIcon className="w-6 h-6 text-slate-900" />
            <h2 className="text-2xl font-serif font-bold text-slate-900">
              Market Insights & Visualizations
            </h2>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {result.market_visual_content.visual_content.map((item, idx) => (
              <div key={idx} className="border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow">
                <div className="aspect-video w-full bg-slate-100 flex items-center justify-center">
                  <img 
                    src={item.url} 
                    alt={item.description}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                </div>
                <div className="p-4">
                  <p className="text-sm text-slate-700">{item.description}</p>
                </div>
              </div>
            ))}
          </div>

          {result.market_visual_content.market_insights.length > 0 && (
            <div className="mt-6 p-4 bg-slate-50 rounded-xl">
              <h3 className="font-semibold text-slate-900 mb-2">Key Insights</h3>
              <ul className="space-y-1">
                {result.market_visual_content.market_insights.map((insight, idx) => (
                  <li key={idx} className="text-sm text-slate-700 flex items-start">
                    <span className="mr-2">•</span>
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

