'use client'

import { useState } from 'react'
import { ArrowRight, Lightbulb, Building2 } from 'lucide-react'
import MCQStep from '@/components/MCQStep'
import Dashboard from '@/components/Dashboard'
import { generateMCQs, analyzeIdea } from '@/lib/api'
import type { MCQQuestion, MCQAnswer, AnalysisResult } from '@/types'

export default function Home() {
  const [step, setStep] = useState<'input' | 'mcq' | 'results'>('input')
  const [submissionType, setSubmissionType] = useState<'idea' | 'startup'>('idea')
  const [ideaText, setIdeaText] = useState('')
  const [mcqQuestions, setMcqQuestions] = useState<MCQQuestion[]>([])
  const [mcqAnswers, setMcqAnswers] = useState<MCQAnswer[]>([])
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmitIdea = async () => {
    if (!ideaText.trim()) return

    setLoading(true)
    setError(null)

    try {
      if (submissionType === 'idea') {
        // Generate MCQs
        const response = await generateMCQs(ideaText, submissionType)
        setMcqQuestions(response.questions)
        setStep('mcq')
      } else {
        // Skip MCQs for startup name/domain
        const result = await analyzeIdea(ideaText, [], submissionType)
        setAnalysisResult(result)
        setStep('results')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleMCQComplete = async (answers: MCQAnswer[]) => {
    setMcqAnswers(answers)
    setLoading(true)
    setError(null)

    try {
      const result = await analyzeIdea(ideaText, answers, submissionType)
      setAnalysisResult(result)
      setStep('results')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setStep('input')
    setIdeaText('')
    setMcqQuestions([])
    setMcqAnswers([])
    setAnalysisResult(null)
    setError(null)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-serif font-bold text-slate-900">
              IdeaCompass
            </h1>
            <p className="text-sm text-slate-600">
              Live market intelligence for founders & investors
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {step === 'input' && (
          <div className="max-w-3xl mx-auto">
            {/* Hero Section */}
            <div className="text-center mb-12 space-y-4">
              <h2 className="text-5xl font-serif font-bold text-slate-900 leading-tight">
                Share your idea
              </h2>
              <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
                Get probabilistic outcome estimates, comparable companies, and risk analysis—all grounded in live web evidence with citations
              </p>
            </div>

            {/* Input Card */}
            <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
              {/* Tab Selection */}
              <div className="flex border-b border-slate-200">
                <button
                  onClick={() => setSubmissionType('idea')}
                  className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 font-medium transition-all ${
                    submissionType === 'idea'
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-50 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <Lightbulb className="w-5 h-5" />
                  I have an idea
                </button>
                <button
                  onClick={() => setSubmissionType('startup')}
                  className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 font-medium transition-all ${
                    submissionType === 'startup'
                      ? 'bg-slate-900 text-white'
                      : 'bg-slate-50 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <Building2 className="w-5 h-5" />
                  I have a startup
                </button>
              </div>

              {/* Input Area */}
              <div className="p-8">
                <div className="space-y-4">
                  <label className="block">
                    <span className="text-sm font-medium text-slate-700 mb-2 block">
                      {submissionType === 'idea'
                        ? 'Describe your business idea (≤25 words ideal)'
                        : 'Enter your company name or domain'}
                    </span>
                    <textarea
                      value={ideaText}
                      onChange={(e) => setIdeaText(e.target.value)}
                      placeholder={
                        submissionType === 'idea'
                          ? 'e.g., AI agent that reconciles invoices and cards for SMBs and files expenses automatically'
                          : 'e.g., company.com or Company Name'
                      }
                      className="w-full px-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent resize-none font-serif text-lg"
                      rows={4}
                    />
                  </label>

                  {error && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                      {error}
                    </div>
                  )}

                  <button
                    onClick={handleSubmitIdea}
                    disabled={!ideaText.trim() || loading}
                    className="w-full bg-slate-900 text-white px-6 py-4 rounded-xl font-medium hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg transition-all transform hover:scale-[1.02] active:scale-[0.98]"
                  >
                    {loading ? (
                      <>
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Processing...
                      </>
                    ) : (
                      <>
                        Analyze
                        <ArrowRight className="w-5 h-5" />
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {step === 'mcq' && (
          <MCQStep
            questions={mcqQuestions}
            onComplete={handleMCQComplete}
            onBack={handleReset}
            loading={loading}
          />
        )}

        {step === 'results' && analysisResult && (
          <Dashboard result={analysisResult} onReset={handleReset} />
        )}
      </div>
    </main>
  )
}

