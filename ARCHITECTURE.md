# IdeaCompass Architecture

Detailed technical architecture and implementation guide.

## System Overview

IdeaCompass is a full-stack web application that implements reference-class forecasting for business ideas using Perplexity's Search and Sonar APIs.

```
┌─────────────┐         ┌─────────────┐         ┌──────────────────┐
│   Browser   │ ◄─────► │   Next.js   │ ◄─────► │  FastAPI Server  │
│  (React UI) │         │  Frontend   │         │    (Python)      │
└─────────────┘         └─────────────┘         └──────────────────┘
                                                          │
                                                          ▼
                                                 ┌──────────────────┐
                                                 │  Perplexity API  │
                                                 │  - Search API    │
                                                 │  - Sonar/Pro     │
                                                 └──────────────────┘
```

## Technology Stack

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.9+ | Runtime environment |
| FastAPI | 0.109+ | Web framework |
| Uvicorn | 0.27+ | ASGI server |
| httpx | 0.26+ | Async HTTP client |
| Pydantic | 2.5+ | Data validation |

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14.1+ | React framework |
| React | 18.2+ | UI library |
| TypeScript | 5.0+ | Type safety |
| Tailwind CSS | 3.3+ | Styling |
| Recharts | 2.10+ | Data visualization |
| Axios | 1.6+ | HTTP client |

## Backend Architecture

### API Flow

```
User Input → FastAPI Endpoint → Perplexity APIs → Analysis Engine → JSON Response
```

### Core Endpoints

#### `POST /api/generate-mcqs`

Generates 3 multiple-choice questions to disambiguate the business idea.

**Flow:**
1. Receive idea text and submission type
2. Build system prompt for MCQ generation
3. Call Perplexity Chat Completions (Sonar Pro) with structured JSON schema
4. Parse and validate MCQ response
5. Return questions with options and reasoning

**Perplexity API Usage:**
- Model: `sonar-pro`
- Response format: JSON Schema
- Search context: `low` (minimal web search needed)
- Recency filter: `year`

**JSON Schema:**
```json
{
  "type": "object",
  "properties": {
    "questions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "question": {"type": "string"},
          "options": {"type": "array", "items": {"type": "string"}},
          "reason": {"type": "string"}
        }
      }
    },
    "idea_summary": {"type": "string"}
  }
}
```

#### `POST /api/analyze`

Performs comprehensive analysis on the idea.

**Flow:**
1. Build search queries from idea + MCQ answers
2. Call Search API with multi-query array
3. Extract comparable companies from results
4. Classify entities and compute similarity scores
5. Calculate outcome probabilities using reference-class forecasting
6. Generate risk assessments and pivot suggestions
7. Return comprehensive analysis with citations

**Analysis Pipeline:**

```
Input
  ↓
Query Generation (6 queries)
  ↓
Search API (multi-query, 10 results each)
  ↓
Entity Extraction (Sonar Pro, JSON)
  ↓
Similarity Scoring (0-100)
  ↓
Reference Class Selection (top 10-25)
  ↓
Base Rate Calculation
  ↓
Probability Adjustments
  ↓
Risk & Pivot Analysis
  ↓
Output (with citations)
```

### Data Models

#### Core Pydantic Models

```python
# Input Models
class IdeaSubmission(BaseModel):
    text: str
    submission_type: str  # 'idea' or 'startup'

class MCQAnswer(BaseModel):
    question: str
    answer: str

class AnalysisRequest(BaseModel):
    idea: str
    mcq_answers: Optional[List[MCQAnswer]]
    submission_type: str

# Output Models
class Citation(BaseModel):
    title: str
    url: str
    snippet: str
    date: Optional[str]

class Comparable(BaseModel):
    name: str
    url: str
    similarity_score: float
    tags: Dict[str, str]
    traction_snippet: str
    funding_snippet: str
    outcome_label: str
    citations: List[Citation]

class OutcomeProbabilities(BaseModel):
    next_round: Dict[str, float]
    pmf_proxy: Dict[str, float]
    survival_24m: Dict[str, float]
    capital_efficiency_percentile: float

class AnalysisResponse(BaseModel):
    id: str
    idea_summary: str
    tags: List[str]
    comparables: List[Comparable]
    outcome_probabilities: OutcomeProbabilities
    risk_radar: RiskRadar
    pivot_suggestions: List[PivotSuggestion]
    confidence_score: float
    # ... additional fields
```

### Perplexity API Integration

#### Search API Usage

```python
{
    "query": [
        "AI expense management startup SMB 2024..2025",
        "accounts payable automation seed funding",
        "SMB finance workflow startup failure"
    ],
    "max_results": 10,
    "max_tokens_per_page": 1024
}
```

**Rate Limits:**
- 3 QPS (burst of 3)
- Async batching for multiple queries

**Cost:** $5 per 1,000 requests (~$0.005 per request)

#### Chat Completions Usage

```python
{
    "model": "sonar-pro",
    "messages": [...],
    "response_format": {
        "type": "json_schema",
        "json_schema": {...}
    },
    "web_search_options": {
        "search_context_size": "high"
    },
    "search_recency_filter": "year",
    "search_domain_filter": ["gov", "edu", "sec.gov"]
}
```

**Models:**
- `sonar`: Fast, cost-effective
- `sonar-pro`: Higher quality, more reasoning
- `sonar-deep-research`: Multi-step research (optional)

**Cost:** ~$0.02-$0.06 per call depending on complexity

## Frontend Architecture

### Component Hierarchy

```
App (page.tsx)
├── Header
├── Input Section
│   ├── Tab Selection (Idea vs Startup)
│   └── Textarea + Submit Button
├── MCQStep Component
│   ├── Progress Bar
│   ├── Question Display
│   ├── Option Buttons
│   └── Navigation
└── Dashboard Component
    ├── Header Card
    │   ├── Summary
    │   ├── Tags
    │   └── Confidence Score
    ├── Left Column (2/3)
    │   ├── Outcome Probabilities
    │   │   └── ProbabilityChart
    │   ├── Comparable Companies
    │   └── Execution Levers
    └── Right Column (1/3)
        ├── Market & Competition
        ├── Risk Radar
        │   └── RiskRadarChart
        ├── Pivot Navigator
        └── Evidence Summary
```

### State Management

```typescript
// Main App State
const [step, setStep] = useState<'input' | 'mcq' | 'results'>('input')
const [submissionType, setSubmissionType] = useState<'idea' | 'startup'>('idea')
const [ideaText, setIdeaText] = useState('')
const [mcqQuestions, setMcqQuestions] = useState<MCQQuestion[]>([])
const [mcqAnswers, setMcqAnswers] = useState<MCQAnswer[]>([])
const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
const [loading, setLoading] = useState(false)
const [error, setError] = useState<string | null>(null)
```

### User Flow

```
Landing Page
    ↓
Tab Selection (Idea vs Startup)
    ↓
Text Input
    ↓
Submit → Generate MCQs (if Idea)
    ↓
MCQ Step (3 questions)
    ↓
Answer All → Analyze
    ↓
Loading State (with progress)
    ↓
Dashboard Results
    ↓
Reset or Export
```

### API Client

```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function generateMCQs(
  text: string,
  submissionType: 'idea' | 'startup'
): Promise<{ questions: MCQQuestion[]; idea_summary: string }>

export async function analyzeIdea(
  idea: string,
  mcqAnswers: MCQAnswer[],
  submissionType: 'idea' | 'startup'
): Promise<AnalysisResult>
```

### Styling System

#### Design Tokens

```css
/* Colors */
--background: 0 0% 100%
--foreground: 222.2 84% 4.9%
--primary: 222.2 47.4% 11.2%
--secondary: 210 40% 96.1%
--accent: 210 40% 96.1%
--muted: 210 40% 96.1%

/* Typography */
--font-instrument-serif: Instrument Serif
--font-inter: Inter
```

#### Component Patterns

```typescript
// Card Pattern
<div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-8">
  {/* Content */}
</div>

// Button Pattern
<button className="bg-slate-900 text-white px-6 py-4 rounded-xl font-medium hover:bg-slate-800 transition-all">
  {/* Label */}
</button>

// Input Pattern
<textarea className="w-full px-4 py-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-slate-900">
```

## Reference-Class Forecasting Algorithm

### Step 1: Query Generation

```python
def build_search_queries(idea: str, mcq_answers: List[MCQAnswer]) -> List[str]:
    queries = [
        f"{idea} startup case study 2024..2025",
        f"{idea} seed funding success 2023..2025",
        f"{idea} startup failure post-mortem"
    ]
    
    # Add MCQ-informed queries
    if buyer_type:
        queries.append(f"{buyer_type} {idea} startup")
    if gtm_approach:
        queries.append(f"{gtm_approach} {idea} company")
    
    return queries[:6]
```

### Step 2: Similarity Scoring

```python
def compute_similarity(idea: str, comparable: Dict) -> float:
    score = 0.0
    
    # Semantic overlap (40%)
    score += semantic_similarity(idea, comparable['snippet']) * 0.4
    
    # Tag match (30%)
    score += tag_overlap(idea_tags, comparable['tags']) * 0.3
    
    # Buyer match (20%)
    score += buyer_match(idea_buyer, comparable['buyer']) * 0.2
    
    # Recency bonus (10%)
    score += recency_bonus(comparable['date']) * 0.1
    
    return min(100, score * 100)
```

### Step 3: Probability Calculation

```python
def calculate_probabilities(comparables: List[Comparable]) -> OutcomeProbabilities:
    # Base rate from reference class
    wins = sum(1 for c in comparables if c.outcome_label == 'win')
    base_rate = wins / len(comparables)
    
    # Adjustments
    crowding_penalty = compute_crowding_penalty(comparables)
    regulatory_penalty = compute_regulatory_penalty(idea, comparables)
    market_momentum = compute_market_momentum(comparables)
    
    # Final probability with uncertainty
    p_next_round = base_rate + market_momentum - crowding_penalty - regulatory_penalty
    
    return {
        'mean': p_next_round,
        'lower_ci': max(0, p_next_round - 0.15),
        'upper_ci': min(1, p_next_round + 0.15)
    }
```

## Security Considerations

### Backend

- **CORS**: Restricted to frontend origins
- **API Key**: Stored in environment variables
- **Rate Limiting**: Relies on Perplexity's rate limits
- **Input Validation**: Pydantic models validate all inputs
- **Error Handling**: No sensitive data in error messages

### Frontend

- **Environment Variables**: API URL in `NEXT_PUBLIC_*`
- **XSS Protection**: React's built-in escaping
- **HTTPS**: Required in production
- **No API Keys**: All keys stay on backend

## Performance Optimization

### Backend

- **Async/Await**: All API calls are async
- **Connection Pooling**: httpx client reuse
- **Timeout Handling**: 60-90s timeouts
- **Error Recovery**: Graceful fallbacks

### Frontend

- **Code Splitting**: Next.js automatic
- **Image Optimization**: Next.js Image component
- **CSS Optimization**: Tailwind purges unused styles
- **Lazy Loading**: Components load on demand

## Monitoring & Debugging

### Backend Logging

```python
print(f"Searching with queries: {search_queries}")
print(f"Search API error: {e}")
```

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Debugging

```typescript
console.log('Analysis result:', analysisResult)
```

### Health Checks

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

## Deployment Considerations

### Backend Deployment

```bash
# Use production ASGI server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Environment
export PERPLEXITY_API_KEY=pplx-...
```

### Frontend Deployment

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Environment Variables

```bash
# Backend
PERPLEXITY_API_KEY=pplx-...

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdom
ain.com
```

## Cost Analysis

### Per Analysis

| Component | Calls | Unit Cost | Total |
|-----------|-------|-----------|-------|
| Search API | 6-8 | $0.005 | $0.03-$0.04 |
| Sonar Pro | 2-3 | $0.02-$0.06 | $0.04-$0.18 |
| **Total** | | | **$0.07-$0.22** |

### Monthly Estimates

| Volume | Cost/Month |
|--------|------------|
| 100 analyses | $7-$22 |
| 1,000 analyses | $70-$220 |
| 10,000 analyses | $700-$2,200 |

## Testing Strategy

### Backend Tests

```python
# Unit tests for API endpoints
pytest backend/tests/

# Integration tests with mock Perplexity responses
pytest backend/tests/integration/
```

### Frontend Tests

```bash
# Component tests
npm run test

# E2E tests
npm run test:e2e
```

## Future Enhancements

1. **Caching Layer**: Redis for repeated queries
2. **Database**: PostgreSQL for analysis history
3. **Authentication**: User accounts and saved analyses
4. **Real-time Updates**: WebSocket for streaming results
5. **Export Features**: PDF generation with citations
6. **Leaderboard**: Multi-idea comparison scatter plot
7. **Industry Modules**: Specialized analysis for fintech, health, etc.

---

For implementation details, see the source code and inline comments.

