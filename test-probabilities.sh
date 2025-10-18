#!/bin/bash

# Test script for the new data-driven outcome probabilities

echo "🎯 Testing Data-Driven Outcome Probabilities"
echo "============================================="
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend is not running. Start it with: cd backend && python main.py"
    exit 1
fi

echo "✅ Backend is running"
echo ""

echo "📊 Testing Outcome Probability Calculations"
echo "-------------------------------------------"
echo ""

# Test with a specific idea
echo "Analyzing: AI-powered developer tools"
echo ""

curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "AI-powered code completion and editing tool for software developers",
    "submission_type": "startup"
  }' | python3 -c "
import sys, json

data = json.load(sys.stdin)
probs = data.get('outcome_probabilities', {})

print('=' * 60)
print('OUTCOME PROBABILITIES (Data-Driven)')
print('=' * 60)
print()

# Next Round
next_round = probs.get('next_round', {})
print('📈 Next Round Funding')
print(f'   Probability: {next_round.get(\"mean\", 0):.1%}')
print(f'   Range: [{next_round.get(\"lower_ci\", 0):.1%} - {next_round.get(\"upper_ci\", 0):.1%}]')
print(f'   Explanation: {probs.get(\"next_round_explanation\", \"N/A\")}')
print()

# PMF
pmf = probs.get('pmf_proxy', {})
print('🎯 Product-Market Fit')
print(f'   Probability: {pmf.get(\"mean\", 0):.1%}')
print(f'   Range: [{pmf.get(\"lower_ci\", 0):.1%} - {pmf.get(\"upper_ci\", 0):.1%}]')
print(f'   Explanation: {probs.get(\"pmf_explanation\", \"N/A\")}')
print()

# Survival
survival = probs.get('survival_24m', {})
print('💪 24-Month Survival')
print(f'   Probability: {survival.get(\"mean\", 0):.1%}')
print(f'   Range: [{survival.get(\"lower_ci\", 0):.1%} - {survival.get(\"upper_ci\", 0):.1%}]')
print(f'   Explanation: {probs.get(\"survival_explanation\", \"N/A\")}')
print()

# Capital Efficiency
cap_eff = probs.get('capital_efficiency_percentile', 0)
print('💰 Capital Efficiency')
print(f'   Percentile: {cap_eff:.0f}th')
print(f'   Explanation: {probs.get(\"capital_efficiency_explanation\", \"N/A\")}')
print()

print('=' * 60)
print()

# Check for removed confidence_score
if 'confidence_score' in data:
    print('⚠️  WARNING: confidence_score still present (should be removed)')
else:
    print('✅ confidence_score successfully removed')

print()
print('=' * 60)
"

echo ""
echo ""
echo "✨ Test completed!"
echo ""
echo "📖 For details, see: OUTCOME_PROBABILITIES_UPGRADE.md"
echo "🔗 Frontend: http://localhost:3000"

