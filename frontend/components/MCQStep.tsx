'use client'

import { useState } from 'react'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import type { MCQQuestion, MCQAnswer } from '@/types'

interface MCQStepProps {
  questions: MCQQuestion[]
  onComplete: (answers: MCQAnswer[]) => void
  onBack: () => void
  loading: boolean
}

export default function MCQStep({ questions, onComplete, onBack, loading }: MCQStepProps) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<MCQAnswer[]>([])
  const [selectedOption, setSelectedOption] = useState<string>('')

  const currentQuestion = questions[currentQuestionIndex]
  const isLastQuestion = currentQuestionIndex === questions.length - 1

  const handleNext = () => {
    if (!selectedOption) return

    const newAnswers = [
      ...answers,
      {
        question: currentQuestion.question,
        answer: selectedOption,
      },
    ]

    if (isLastQuestion) {
      onComplete(newAnswers)
    } else {
      setAnswers(newAnswers)
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setSelectedOption('')
    }
  }

  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
      setSelectedOption(answers[currentQuestionIndex - 1]?.answer || '')
      setAnswers(answers.slice(0, -1))
    } else {
      onBack()
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        {/* Progress Bar */}
        <div className="h-2 bg-slate-100">
          <div
            className="h-full bg-slate-900 transition-all duration-300"
            style={{
              width: `${((currentQuestionIndex + 1) / questions.length) * 100}%`,
            }}
          />
        </div>

        {/* Content */}
        <div className="p-8 md:p-12">
          <div className="mb-8">
            <p className="text-sm font-medium text-slate-500 mb-4">
              Question {currentQuestionIndex + 1} of {questions.length}
            </p>
            <h2 className="text-3xl font-serif font-bold text-slate-900 mb-3">
              {currentQuestion.question}
            </h2>
            <p className="text-slate-600">{currentQuestion.reason}</p>
          </div>

          {/* Options */}
          <div className="space-y-3 mb-8">
            {currentQuestion.options.map((option) => (
              <button
                key={option}
                onClick={() => setSelectedOption(option)}
                className={`w-full text-left px-6 py-4 rounded-xl border-2 transition-all transform hover:scale-[1.01] ${
                  selectedOption === option
                    ? 'border-slate-900 bg-slate-50 shadow-md'
                    : 'border-slate-200 hover:border-slate-300 bg-white'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all ${
                      selectedOption === option
                        ? 'border-slate-900 bg-slate-900'
                        : 'border-slate-300'
                    }`}
                  >
                    {selectedOption === option && (
                      <div className="w-2 h-2 rounded-full bg-white" />
                    )}
                  </div>
                  <span className="font-medium text-slate-900">{option}</span>
                </div>
              </button>
            ))}
          </div>

          {/* Navigation */}
          <div className="flex gap-4">
            <button
              onClick={handleBack}
              className="px-6 py-3 border-2 border-slate-200 rounded-xl font-medium text-slate-700 hover:bg-slate-50 transition-all flex items-center gap-2"
            >
              <ArrowLeft className="w-5 h-5" />
              Back
            </button>
            <button
              onClick={handleNext}
              disabled={!selectedOption || loading}
              className="flex-1 bg-slate-900 text-white px-6 py-3 rounded-xl font-medium hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-all"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  {isLastQuestion ? 'Analyze' : 'Next'}
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

