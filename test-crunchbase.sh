#!/bin/bash

# Test script for Real Crunchbase Data Integration

echo "💰 Testing Real Crunchbase Data Integration"
echo "==========================================="
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend is not running. Start it with: cd backend && python main.py"
    exit 1
fi

echo "✅ Backend is running"
echo ""

echo "🔍 Analyzing: AI-powered code completion tools"
echo "This will fetch REAL Crunchbase data..."
echo ""

# Analyze an AI code editor idea (should have lots of Crunchbase data)
curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "AI-powered code completion and editing tool for software developers",
    "submission_type": "startup",
    "mcq_answers": [
      {"question": "Target buyer?", "answer": "Developer"},
      {"question": "Go-to-market?", "answer": "Self-serve PLG"}
    ]
  }' | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    probs = data.get('outcome_probabilities', {})
    
    print('=' * 70)
    print('CRUNCHBASE-DRIVEN PROBABILITY ANALYSIS')
    print('=' * 70)
    print()
    
    # Next Round - should mention Crunchbase data
    next_round = probs.get('next_round', {})
    next_explanation = probs.get('next_round_explanation', '')
    
    print('📈 NEXT ROUND FUNDING')
    print(f'   Probability: {next_round.get(\"mean\", 0):.1%}')
    print(f'   Range: [{next_round.get(\"lower_ci\", 0):.1%} - {next_round.get(\"upper_ci\", 0):.1%}]')
    print()
    print('   📊 Explanation (look for Crunchbase data):')
    print(f'   {next_explanation}')
    print()
    
    # Check if Crunchbase data is mentioned
    if 'crunchbase' in next_explanation.lower():
        print('   ✅ Crunchbase data is being used!')
    else:
        print('   ⚠️  WARNING: Crunchbase data not mentioned in explanation')
    
    # Look for actual numbers (e.g., \"28 of 87\")
    import re
    numbers = re.findall(r'(\d+)\s+of\s+(\d+)', next_explanation)
    if numbers:
        funded, total = numbers[0]
        print(f'   ✅ Real data found: {funded} funded out of {total} startups')
        success_rate = int(funded) / int(total) if int(total) > 0 else 0
        print(f'   ✅ Success rate: {success_rate:.1%}')
    else:
        print('   ⚠️  WARNING: Could not find specific startup counts')
    
    print()
    print('-' * 70)
    print()
    
    # PMF
    pmf = probs.get('pmf_proxy', {})
    print('🎯 PRODUCT-MARKET FIT')
    print(f'   Probability: {pmf.get(\"mean\", 0):.1%}')
    print(f'   Explanation: {probs.get(\"pmf_explanation\", \"N/A\")}')
    print()
    
    # Capital Efficiency - should mention average funding from Crunchbase
    cap_eff = probs.get('capital_efficiency_percentile', 0)
    cap_explanation = probs.get('capital_efficiency_explanation', '')
    
    print('💰 CAPITAL EFFICIENCY')
    print(f'   Percentile: {cap_eff:.0f}th')
    print(f'   Explanation: {cap_explanation}')
    print()
    
    # Check for funding amounts
    funding_amounts = re.findall(r'\$(\d+(?:\.\d+)?[MB])', cap_explanation)
    if funding_amounts:
        print(f'   ✅ Average funding from Crunchbase: {funding_amounts[0]}')
    else:
        print('   ⚠️  WARNING: No funding amount data found')
    
    print()
    print('=' * 70)
    print()
    
    # Summary
    print('📋 VERIFICATION CHECKLIST')
    print()
    
    checks = [
        ('Crunchbase mentioned', 'crunchbase' in next_explanation.lower()),
        ('Specific company counts', bool(numbers)),
        ('Funding amounts', bool(funding_amounts)),
        ('Real data vs estimates', 'based on' in next_explanation.lower())
    ]
    
    for check_name, passed in checks:
        status = '✅' if passed else '❌'
        print(f'{status} {check_name}')
    
    print()
    all_passed = all(passed for _, passed in checks)
    if all_passed:
        print('🎉 All checks passed! Using real Crunchbase data.')
    else:
        print('⚠️  Some checks failed. Review integration.')
    
    print()
    print('=' * 70)
    
except Exception as e:
    print(f'❌ Error parsing response: {e}')
    import traceback
    traceback.print_exc()
"

echo ""
echo ""
echo "✨ Test completed!"
echo ""
echo "📖 For details, see: CRUNCHBASE_INTEGRATION.md"
echo "🔗 Frontend: http://localhost:3000"
echo ""
echo "💡 TIP: Check backend logs for lines like:"
echo "   'Fetching real Crunchbase data for: ...'"
echo "   'Crunchbase data: 87 companies, 32% success rate'"

