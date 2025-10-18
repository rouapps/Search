'use client'

import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts'
import type { RiskRadar } from '@/types'

interface RiskRadarChartProps {
  risk: RiskRadar
}

export default function RiskRadarChart({ risk }: RiskRadarChartProps) {
  const data = [
    { subject: 'Regulatory', value: risk.regulatory },
    { subject: 'Platform', value: risk.platform_dependency },
    { subject: 'Pricing', value: risk.pricing_pressure },
    { subject: 'Distribution', value: risk.distribution_risk },
  ]

  return (
    <ResponsiveContainer width="100%" height={200}>
      <RadarChart data={data}>
        <PolarGrid stroke="#e2e8f0" />
        <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 11 }} />
        <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 10 }} />
        <Radar name="Risk" dataKey="value" stroke="#1e293b" fill="#1e293b" fillOpacity={0.6} />
      </RadarChart>
    </ResponsiveContainer>
  )
}

