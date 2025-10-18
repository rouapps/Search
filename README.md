# IdeaCompass 🧭

> A live, cited market intelligence engine for founders & investors

IdeaCompass applies **reference-class forecasting** to business ideas, providing probabilistic outcome estimates grounded in real web evidence from Perplexity's Search APIs. Get comparable companies, risk analysis, and pivot suggestions—all with citations.

## 🎯 What It Does

- **Reference Class Matching**: Compare your idea to thousands of similar past cases
- **🔥 NEW: Real Crunchbase Data-Driven Outcomes** with plain-English explanations:
  - P(raising next round) - calculated from **real Crunchbase data** (e.g., "28 of 87 startups funded")
  - P(achieving PMF) - based on actual traction signals and funding velocity
  - 24-month survival - adjusted for market moats and competition
  - Capital efficiency - shows average funding amounts from Crunchbase (e.g., "$6.5M average")
  - Each metric backed by verifiable data, not estimates or AI hallucinations
- **🔥 NEW: Real-Time Market Intelligence** (Powered by Sonar Finance):
  - Live TAM/SAM data from recent market reports
  - Dynamic funding velocity tracking (deals, amounts, investors)
  - Real-time crowding index calculation
  - Competitive moats analysis from financial sources
  - Cited financial data from PitchBook, Crunchbase, SEC filings
- **🔥 NEW: Media Classifier API**: 
  - Properly enabled with `enable_media_classifier=True`
  - Analyze logos, screenshots, and product images
  - Extract brand positioning and target market signals
  - Competitive insights from visual content
  - Product quality assessment from UI/UX
  - Automatic detection of when visual content enhances analysis
- **Risk Radar**: Regulatory, platform dependency, pricing pressure, and distribution risks
- **Pivot Navigator**: Top 2-3 closest viable pivots with expected uplift
- **Full Citations**: Every claim links back to sources

📖 **[Read the Sonar Finance & Media Classifier Guide →](./SONAR_FINANCE_GUIDE.md)**
📖 **[Read the Real Crunchbase Integration Guide →](./CRUNCHBASE_INTEGRATION.md)**

## 🏗️ Architecture

### Backend (Python + FastAPI)
- FastAPI server with Perplexity API integration
- Uses Search API for finding comparables
- Uses Sonar/Sonar-Pro for analysis with structured JSON outputs
- Implements reference-class forecasting logic

### Frontend (Next.js + TypeScript)
- Modern React UI with Instrument Serif typography
- Two input paths: "I have an idea" vs. "I have a startup"
- Auto-generated MCQs for better reference-class matching
- Beautiful dashboard with charts and visualizations
- Fully responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Perplexity API key ([get one here](https://www.perplexity.ai/settings/api))

### Easy Setup (Recommended)

1. **Get your Perplexity API key** from https://www.perplexity.ai/settings/api

2. **Add your API key:**
```bash
./setup-api-key.sh
# Or manually: echo "PERPLEXITY_API_KEY=pplx-your-key" > backend/.env
```

3. **Start the application:**
```bash
./start.sh
```

4. **Open your browser:** http://localhost:3000

### Manual Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "PERPLEXITY_API_KEY=pplx-your-key-here" > .env

# Run the server
python main.py
```

The backend will be available at `http://localhost:8000`

### Test Your Backend

```bash
./test-backend.sh
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📖 Usage

### Path A: "I have an idea"
1. Paste your business idea (≤25 words ideal)
2. Answer 3 auto-generated MCQs to disambiguate:
   - Target buyer/user
   - Go-to-market approach
   - Regulatory exposure
3. Click "Analyze" to get your dashboard

### Path B: "I have a startup"
1. Enter your company name or domain
2. Skip MCQs—we infer everything from your site/about page
3. Get instant analysis

## 🎨 Design Philosophy

- **Instrument Serif** font for elegant, readable typography
- **Probabilistic, not binary**: We show uncertainty with confidence intervals
- **Cited evidence**: Every claim is backed by sources
- **Outside view**: Reference-class forecasting reduces optimism bias
- **Enjoyable UX**: Smooth animations, clear hierarchy, intuitive flow

## 📊 Dashboard Sections

### Fixed Sections
1. **Idea Snapshot** - Summary, tags, MCQ responses, confidence score
2. **Similar Startups** - 10-25 comparable companies with similarity scores
3. **Outcome Probabilities** - Calibrated estimates with 80% CI
4. **Market & Competition** - Crowding index, TAM/SAM, funding velocity
5. **Risk Radar** - Multi-dimensional risk assessment
6. **Execution Levers** - 3 prioritized actions with impact ratings
7. **Pivot Navigator** - Top 2-3 closest viable pivots
8. **Evidence Summary** - Source breakdown and quality metrics

### Variable (Industry-Specific)
- **Fintech**: Licensing paths, partner bank exposure, interchange realism
- **Health**: FDA pathways, CPT codes, payer dynamics
- **Dev Tools**: Open-source traction, integration surface
- **Consumer**: Retention proxies, network effects, take-rate realism
- **Hardware/Climate**: BoM risk, supply chain, certification timelines

## 🔌 API Endpoints

### `POST /api/generate-mcqs`
Generate 3 multiple-choice questions to disambiguate an idea.

```json
{
  "text": "AI agent that reconciles invoices for SMBs",
  "submission_type": "idea"
}
```

### `POST /api/analyze`
Perform comprehensive analysis on an idea or startup.

```json
{
  "idea": "AI agent that reconciles invoices for SMBs",
  "mcq_answers": [
    {"question": "Target user?", "answer": "SMB"}
  ],
  "submission_type": "idea",
  "media_urls": [
    "https://example.com/logo.png",
    "https://example.com/screenshot.png"
  ]
}
```

### `POST /api/classify-media` 🔥 NEW
Analyze logos, screenshots, or product images for market insights.

```json
{
  "media_url": "https://example.com/logo.png",
  "context": "AI invoice reconciliation tool"
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": "Full text analysis of visual content...",
  "insights": [
    "Professional B2B branding",
    "Enterprise-focused design language",
    "Modern SaaS positioning"
  ],
  "confidence": 0.75
}
```

## 🧪 How It Works

### 1. Reference Class Selection
- Build 6-10 sub-queries from idea + MCQ responses
- Use Search API with `max_results=10-20`, `max_tokens_per_page=1024-2048`
- Extract entities and tag features (buyer, GTM, regulatory, pricing)

### 2. Similarity Scoring
- Semantic overlap between idea and result snippets
- Business model tags match
- Buyer/persona alignment
- Distribution channel overlap
- Regulatory category match
- Weight recent, high-quality domains

### 3. Outcome Models
- Start with base rates from reference class
- Adjust for:
  - Funding climate (category-specific deal volume)
  - Competition crowding
  - Founder-idea fit (if provided)
  - Regulatory friction
- Show uncertainty with confidence intervals

### 4. Citation Tracking
- All claims link to Perplexity's `search_results` with titles, URLs, dates
- Source quality scoring (gov/edu/SEC > tier-1 media > blogs)
- Recency and independence checks

## 💡 Key Insights

Based on extensive research:

- **Failure is predictable**: Top causes (no market need, cash, pricing, competition) are visible in public data
- **Inside view fails**: Founders overestimate their odds; outside view (reference classes) improves accuracy
- **Power law outcomes**: <4% of VC deals return 10x+; better screening matters
- **Diligence is slow**: Averages 118 hours/deal; we compress scoping to minutes
- **Pivoting works**: When deliberate and grounded in reference-class evidence

## 🔒 Privacy & Ethics

- **No investment advice**: We report probabilities with uncertainty and evidence
- **Bias checks**: Show source diversity and opposing evidence
- **Public data only**: No proprietary or user-shared data
- **No training**: Perplexity doesn't train on customer data

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **httpx**: Async HTTP client for Perplexity APIs
- **Pydantic**: Data validation and settings management

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Beautiful, responsive charts
- **Lucide React**: Modern icon set

### APIs
- **Perplexity Search API**: Multi-query web search with content extraction
- **Perplexity Chat Completions (Sonar/Sonar-Pro)**: Cited synthesis with structured JSON outputs
- **🔥 Perplexity Sonar Finance**: Real-time financial and market intelligence
- **🔥 Perplexity Vision/Media**: Image and visual content analysis
- **Perplexity Deep Research** (optional): Multi-step research for featured ideas

## 📈 Cost Estimates

Per idea analysis (typical):
- 8-12 Search API calls: ~$0.04-$0.06
- 2-3 Sonar/Sonar-Pro calls: ~$0.06-$0.18
- 🔥 1 Sonar Finance call: ~$0.03-$0.05
- 🔥 Media classification (optional): ~$0.02-$0.04 per image
- **Total: ~$0.13-$0.29/idea** (without media) or **~$0.15-$0.37/idea** (with media)
- Deep Research (optional): +$0.41 for flagship memo

## 🚧 Roadmap

- [ ] Live leaderboard with scatter plot (opportunity vs. confidence)
- [ ] Industry-specific micro-modules (fintech, health, dev tools)
- [ ] PDF export with embedded citations
- [ ] Session-based memory for iterative refinement
- [ ] Historical cohort tracking for calibration
- [ ] A/B test pivot suggestions

## 📚 Research Foundation

This tool is grounded in:

- **Reference-class forecasting** (Kahneman & Lovallo)
- **Outside view** reduces optimism bias
- **Base rates** improve prediction accuracy
- **CBInsights post-mortems** on startup failure
- **Correlation Ventures** power law analysis
- **HBS pivot research** (2019)
- **VC diligence studies** (Crunchbase, 700+ firms)

## 🤝 Contributing

This project was built for the Perplexity AI Hackathon. Contributions, issues, and feature requests are welcome!

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Perplexity AI** for the powerful Search and Sonar APIs
- **CB Insights** for startup failure research
- **Daniel Kahneman** for outside-view forecasting research
- All the founders who shared their post-mortems

---

Built with ❤️ using Perplexity APIs | [Documentation](https://docs.perplexity.ai) | [API Reference](https://docs.perplexity.ai/api-reference)
