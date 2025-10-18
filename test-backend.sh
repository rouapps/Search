#!/bin/bash

echo "🧪 Testing IdeaCompass Backend..."
echo ""

# Test health endpoint
echo "1. Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "$HEALTH" | python3 -m json.tool
echo ""

API_CONFIGURED=$(echo "$HEALTH" | python3 -c "import sys, json; print(json.load(sys.stdin)['api_configured'])")

if [ "$API_CONFIGURED" = "True" ] || [ "$API_CONFIGURED" = "true" ]; then
    echo "✅ API key is configured"
    echo ""
    
    echo "2. Testing MCQ generation..."
    curl -s -X POST http://localhost:8000/api/generate-mcqs \
      -H "Content-Type: application/json" \
      -d '{"text": "AI expense management for SMBs", "submission_type": "idea"}' \
      | python3 -m json.tool | head -30
    
    echo ""
    echo "✅ Backend is working correctly!"
else
    echo "⚠️  API key not configured"
    echo ""
    echo "To add your API key, run:"
    echo "  ./setup-api-key.sh"
    echo ""
    echo "Or manually edit backend/.env:"
    echo "  PERPLEXITY_API_KEY=pplx-your-key-here"
fi

