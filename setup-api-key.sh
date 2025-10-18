#!/bin/bash

echo "🔑 IdeaCompass - API Key Setup"
echo ""

# Check if API key is provided as argument
if [ -n "$1" ]; then
    API_KEY="$1"
else
    echo "Please enter your Perplexity API key:"
    echo "(Get it from: https://www.perplexity.ai/settings/api)"
    echo ""
    read -p "API Key: " API_KEY
fi

# Validate API key format
if [[ ! "$API_KEY" =~ ^pplx- ]]; then
    echo "❌ Invalid API key format. Key should start with 'pplx-'"
    exit 1
fi

# Write to backend/.env
echo "PERPLEXITY_API_KEY=$API_KEY" > backend/.env

echo ""
echo "✅ API key saved to backend/.env"
echo ""
echo "Next steps:"
echo "1. Run: ./start.sh"
echo "2. Open: http://localhost:3000"
echo ""

