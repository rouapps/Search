'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import type { OutcomeProbabilities } from '@/types'

interface ProbabilityChartProps {
  probabilities: OutcomeProbabilities
}

export default function ProbabilityChart({ probabilities }: ProbabilityChartProps) {
  const data = [
    {
      name: 'Next Round',
      value: probabilities.next_round.mean * 100,
      lower: probabilities.next_round.lower_ci * 100,
      upper: probabilities.next_round.upper_ci * 100,
    },
    {
      name: 'PMF Proxy',
      value: probabilities.pmf_proxy.mean * 100,
      lower: probabilities.pmf_proxy.lower_ci * 100,
      upper: probabilities.pmf_proxy.upper_ci * 100,
    },
    {
      name: 'Survival',
      value: probabilities.survival_24m.mean * 100,
      lower: probabilities.survival_24m.lower_ci * 100,
      upper: probabilities.survival_24m.upper_ci * 100,
    },
  ]

  const colors = ['#1e293b', '#475569', '#64748b']

  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
        <XAxis dataKey="name" tick={{ fill: '#64748b', fontSize: 12 }} />
        <YAxis
          tick={{ fill: '#64748b', fontSize: 12 }}
          domain={[0, 100]}
          tickFormatter={(value) => `${value}%`}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: 'white',
            border: '1px solid #e2e8f0',
            borderRadius: '8px',
            fontSize: '12px',
          }}
          formatter={(value: number) => `${value.toFixed(1)}%`}
        />
        <Bar dataKey="value" radius={[8, 8, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

