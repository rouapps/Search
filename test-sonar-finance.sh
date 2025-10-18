#!/bin/bash

# Test script for Sonar Finance and Media Classifier features
# Tests the new dynamic market intelligence capabilities

echo "🧪 Testing Sonar Finance & Media Classifier Integration"
echo "========================================================"
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend is not running. Start it with: cd backend && python main.py"
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Test 1: Health check with API configuration
echo "📊 Test 1: Health Check"
echo "----------------------"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Media Classifier
echo "🖼️  Test 2: Media Classifier"
echo "----------------------------"
echo "Analyzing Cursor.sh logo..."
curl -s -X POST http://localhost:8000/api/classify-media \
  -H "Content-Type: application/json" \
  -d '{
    "media_url": "https://logo.clearbit.com/cursor.sh",
    "context": "AI code editor for developers"
  }' | python3 -m json.tool
echo ""
echo ""

# Test 3: Full Analysis with Sonar Finance
echo "💰 Test 3: Full Analysis with Sonar Finance"
echo "-------------------------------------------"
echo "Analyzing: AI-powered code completion tool"
echo ""
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
data = json.load(sys.stdin)
market = data.get('market_analysis', {})

print('Market Analysis (Sonar Finance):')
print('=' * 50)
print(f'Crowding Index: {market.get(\"crowding_index\", \"N/A\")}')
print(f'TAM/SAM: {market.get(\"tam_sam_rationale\", \"N/A\")}')
print(f'Funding Velocity: {market.get(\"funding_velocity\", \"N/A\")}')
print(f'Notable Moats: {market.get(\"notable_moats\", \"N/A\")}')
print(f'Citations: {len(market.get(\"citations\", []))} sources')
"
echo ""
echo ""

# Test 4: Analysis with Media URLs
echo "🎨 Test 4: Analysis with Media URLs"
echo "-----------------------------------"
echo "Analyzing with logo and screenshot..."
curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "Developer-focused AI coding assistant",
    "submission_type": "startup",
    "media_urls": [
      "https://logo.clearbit.com/cursor.sh"
    ]
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Analysis ID: {data.get(\"id\", \"N/A\")}')
print(f'Confidence Score: {data.get(\"confidence_score\", \"N/A\")}/100')
print(f'Comparables Found: {len(data.get(\"comparables\", []))}')
print(f'Market Insights Generated: ✓')
"
echo ""
echo ""

echo "✨ All tests completed!"
echo ""
echo "📖 For more details, see SONAR_FINANCE_GUIDE.md"
echo "🔗 Frontend: http://localhost:3000"
echo "🔗 API Docs: http://localhost:8000/docs"

