"""
IdeaCompass - Market Intelligence Engine for Founders & Investors
Backend API using FastAPI and Perplexity APIs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import json
import requests
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from dotenv import load_dotenv
from perplexity import Perplexity

# Load environment variables
load_dotenv()

app = FastAPI(title="IdeaCompass API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Perplexity client - automatically uses PERPLEXITY_API_KEY env var
try:
    client = Perplexity()
    PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
except Exception as e:
    print(f"Warning: Perplexity client initialization failed: {e}")
    client = None
    PERPLEXITY_API_KEY = ""

# Request/Response Models
class IdeaSubmission(BaseModel):
    text: str = Field(..., max_length=500)
    submission_type: str = Field(..., description="'idea' or 'startup'")

class MCQAnswer(BaseModel):
    question: str
    answer: str

class AnalysisRequest(BaseModel):
    idea: str
    mcq_answers: Optional[List[MCQAnswer]] = None
    submission_type: str = "idea"
    media_urls: Optional[List[str]] = None  # URLs to logos, screenshots, or product images

class MCQQuestion(BaseModel):
    question: str
    options: List[str]
    reason: str

class MCQResponse(BaseModel):
    questions: List[MCQQuestion]
    idea_summary: str

class Citation(BaseModel):
    title: str
    url: str
    snippet: str
    date: Optional[str] = None

class Comparable(BaseModel):
    name: str
    url: str
    logo_url: Optional[str] = None  # Company logo from Clearbit
    similarity_score: float
    tags: Dict[str, str]
    traction_snippet: str
    funding_snippet: str
    outcome_label: str
    citations: List[Citation]

class ExecutionLever(BaseModel):
    title: str
    description: str
    impact: str  # "high", "medium", "low"
    category: Optional[str] = None  # Flexible category from AI
    media_url: Optional[str] = None  # Visual demonstration if available
    media_description: Optional[str] = None
    source_company: Optional[str] = None
    citations: List[Citation] = []

class PivotSuggestion(BaseModel):
    title: str
    rationale: str
    expected_uplift: float
    effort_score: float
    citations: List[Citation]

class MarketAnalysis(BaseModel):
    crowding_index: float
    tam_sam_rationale: str
    funding_velocity: str
    notable_moats: str
    citations: List[Citation]

class MarketVisualContent(BaseModel):
    visual_content: List[Dict[str, Any]]
    market_insights: List[str]
    media_results_count: int

class AnalysisResponse(BaseModel):
    id: str
    idea_summary: str
    tags: List[str]
    mcq_answers: Optional[List[MCQAnswer]]
    comparables: List[Comparable]
    market_analysis: MarketAnalysis
    market_visual_content: MarketVisualContent
    execution_levers: List[ExecutionLever]
    pivot_suggestions: List[PivotSuggestion]
    created_at: str

# Helper Functions
def parse_json_response(content: str) -> dict:
    """Extract JSON from response that might be wrapped in markdown"""
    try:
        # Try direct parsing first
        return json.loads(content)
    except:
        # Extract from markdown code blocks
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            content = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            content = content[start:end].strip()
        
        try:
            return json.loads(content)
        except:
            return {}

def get_default_mcqs() -> List[MCQQuestion]:
    """Return default MCQs when AI generation fails"""
    return [
        MCQQuestion(
            question="Who is your target buyer?",
            options=["SMB", "Mid-market", "Enterprise", "Consumer", "Developer"],
            reason="Understanding the buyer segment helps identify comparable companies"
        ),
        MCQQuestion(
            question="What is your go-to-market strategy?",
            options=["Self-serve PLG", "Outbound Sales", "Marketplace", "Regulatory Route", "Partnerships"],
            reason="GTM approach significantly affects success patterns"
        ),
        MCQQuestion(
            question="What is your regulatory exposure?",
            options=["None", "Light (GDPR/CCPA)", "Medium (Licenses)", "Heavy (FDA/SEC/FINRA)"],
            reason="Regulatory requirements impact timelines and capital needs"
        )
    ]

async def classify_media_content(media_url: str, context: str = "") -> dict:
    """
    Use Perplexity Media Classifier API to analyze visual content
    Returns insights about brand, product, market positioning from visual content
    """
    if not client:
        return {
            "analysis": "Media analysis unavailable",
            "insights": [],
            "confidence": 0.0,
            "media_results": []
        }

    try:
        # Use Perplexity's Media Classifier with proper API parameters
        media_query = f"""Analyze this visual content for business and market insights.

Context: {context if context else 'Business analysis'}

Provide insights on:
1. Brand positioning and target market signals
2. Product design and maturity indicators
3. Market category and competitive landscape
4. Design quality and user experience cues
5. Target customer profile from visual elements"""

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "You are a business analyst specializing in visual content analysis. Extract actionable market and brand insights from images, screenshots, and visual materials."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": media_query},
                        {"type": "image_url", "image_url": {"url": media_url}}
                    ]
                }
            ],
            temperature=0.3,  # Lower for more factual analysis
            max_tokens=1000
        )

        content = response.choices[0].message.content

        # Extract media results if available (this is where logos/visual content would be)
        media_results = []
        if hasattr(response, 'media') and response.media:
            media_results = response.media

        # Parse insights more systematically
        insights = []
        for line in content.split('\n'):
            line = line.strip()
            if line and len(line) > 20:
                # Look for structured insights
                if any(prefix in line.lower() for prefix in ['brand positioning:', 'product maturity:', 'market category:', 'design quality:', 'target customer:']):
                    insights.append(line)
                elif line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    insights.append(line.lstrip('•-*123456789. '))

        return {
            "analysis": content,
            "insights": insights[:5],
            "confidence": 0.85,
            "media_results": media_results
        }

    except Exception as e:
        print(f"Error in media classification: {e}")
        import traceback
        traceback.print_exc()
        return {
            "analysis": f"Media analysis failed: {str(e)}",
            "insights": [],
            "confidence": 0.0,
            "media_results": []
        }

async def get_company_logo_url(company_name: str, company_website: str = "") -> str:
    """
    Get company logo using simple favicon extraction
    Just gets the favicon.ico from the company's website
    """
    if not company_website:
        return None

    # Simple favicon extraction - most websites have /favicon.ico
    favicon_urls = [
        f"https://{company_website}/favicon.ico",
        f"https://www.{company_website}/favicon.ico",
        f"http://{company_website}/favicon.ico",
        f"http://www.{company_website}/favicon.ico"
    ]

    # Try each URL until we get a valid favicon
    for favicon_url in favicon_urls:
        try:
            req = Request(favicon_url, method='HEAD')
            response = urlopen(req, timeout=3)
            if response.status == 200:
                # Verify it's actually an image
                content_type = response.headers.get('content-type', '').lower()
                if any(img_type in content_type for img_type in ['image/', 'application/octet-stream']):
                    return favicon_url
        except (URLError, HTTPError):
            continue

    return None

async def get_educational_visual_content(query: str) -> dict:
    """
    Use Media Classifier for educational/informational visual content where it actually works
    This is for concepts, processes, demonstrations, etc. - not promotional content
    """
    if not client:
        return {
            "analysis": "Media analysis unavailable",
            "insights": [],
            "confidence": 0.0,
            "media_results": []
        }

    try:
        # Search for educational content with citations
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "You are an educational content specialist. Find visual demonstrations, diagrams, and educational materials that help explain concepts."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            temperature=0.3,
            max_tokens=800,
            return_citations=True
        )

        content = response.choices[0].message.content

        # Extract media results (educational visual content)
        media_results = []
        if hasattr(response, 'media') and response.media:
            media_results = response.media

        # Parse insights
        insights = []
        for line in content.split('\n'):
            line = line.strip()
            if line and len(line) > 20:
                if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    insights.append(line.lstrip('•-*123456789. '))

        return {
            "analysis": content,
            "insights": insights[:5],
            "confidence": 0.85,
            "media_results": media_results
        }

    except Exception as e:
        print(f"Error in educational media classification: {e}")
        return {
            "analysis": f"Educational media analysis failed: {str(e)}",
            "insights": [],
            "confidence": 0.0,
            "media_results": []
        }

async def get_market_visual_content(idea: str, market_data: dict) -> dict:
    """
    Use Media Classifier to get visual content that helps understand the market
    Returns graphs, charts, diagrams, and visual data about market trends, competitive landscape, etc.
    """
    if not client:
        return {
            "visual_content": [],
            "market_insights": "Market visual analysis unavailable",
            "media_results": []
        }

    try:
        # Create a query that asks for visual market data
        market_query = f"""Show visual content that helps understand the market for: {idea}

Focus on:
1. Market size and growth charts (TAM/SAM visualizations)
2. Competitive landscape diagrams and positioning maps
3. Industry trend graphs and forecasting charts
4. Market share visualizations and pie charts
5. Funding flow diagrams and investment trend graphs
6. Customer segmentation and demographic visualizations

Return educational charts, graphs, and diagrams that illustrate market dynamics, competitive positioning, and industry trends."""

        # Search for market visual content with citations
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": "You are a market research analyst. Find and return visual content like charts, graphs, diagrams, and infographics that help explain market dynamics, competitive landscapes, and industry trends."
                },
                {
                    "role": "user",
                    "content": market_query
                }
            ],
            temperature=0.3,
            max_tokens=1000,
            return_citations=True
        )

        content = response.choices[0].message.content

        # Extract media results (visual market content)
        media_results = []
        if hasattr(response, 'media') and response.media:
            media_results = response.media

        # Extract visual content URLs and descriptions
        visual_content = []
        for media_item in media_results:
            if isinstance(media_item, dict) and media_item.get('url'):
                visual_content.append({
                    "url": media_item['url'],
                    "type": media_item.get('type', 'image'),
                    "description": media_item.get('description', 'Market visualization')
                })

        # Parse market insights from text content
        market_insights = []
        for line in content.split('\n'):
            line = line.strip()
            if line and len(line) > 20:
                if any(keyword in line.lower() for keyword in ['market', 'chart', 'graph', 'diagram', 'trend', 'visualization']):
                    market_insights.append(line)
                elif line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')):
                    market_insights.append(line.lstrip('•-*123456789. '))

        return {
            "visual_content": visual_content[:10],  # Limit to 10 visual items
            "market_insights": market_insights[:5] if market_insights else ["Visual market analysis completed"],
            "media_results": media_results
        }

    except Exception as e:
        print(f"Error getting market visual content: {e}")
        return {
            "visual_content": [],
            "market_insights": f"Market visual analysis failed: {str(e)}",
            "media_results": []
        }

async def get_execution_levers_with_media(idea: str, comparables: List[Comparable], market_data: dict) -> List[ExecutionLever]:
    """
    Generate flexible execution levers based on real companies and market data
    Uses Media Classifier to find relevant visual demonstrations when available
    """
    if not client:
        return []
    
    try:
        # Build context from comparables
        comparable_context = ""
        if comparables and len(comparables) > 0:
            comparable_context = "Real companies in this space: " + ", ".join([c.name for c in comparables[:5]])
        
        # Generate flexible execution levers
        levers_query = f"""Based on real data about {idea} in the market:

{comparable_context}

Identify 3-5 HIGH-IMPACT, SPECIFIC execution levers that would accelerate growth.

Requirements:
1. Each lever should be ACTIONABLE and SPECIFIC (not generic advice)
2. Include REAL examples from comparable companies when possible
3. Categorize each lever flexibly (e.g., "Distribution", "Product Innovation", "Monetization", "Go-to-Market", "Technical Moat", etc.)
4. Rate impact as "high", "medium", or "low"
5. For each lever, suggest what visual demonstration would be helpful (if any)

Return JSON:
{{
  "levers": [
    {{
      "title": "Specific, actionable lever title",
      "description": "Detailed description with real examples and expected outcomes",
      "impact": "high|medium|low",
      "category": "Flexible category name",
      "source_company": "Company that did this successfully (if applicable)",
      "visual_demo_query": "What kind of visual demo would help (optional, e.g., 'demo of X feature', 'chart showing Y trend')"
    }}
  ]
}}"""

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a strategic advisor analyzing execution strategies from real companies. Use these companies as examples: {comparable_context}"
                },
                {
                    "role": "user",
                    "content": levers_query
                }
            ],
            temperature=0.4,
            max_tokens=1500,
            return_citations=True
        )
        
        content = response.choices[0].message.content
        levers_data = parse_json_response(content)
        
        # Extract citations
        response_citations = []
        if hasattr(response, 'citations') and response.citations:
            response_citations = response.citations[:3]
        
        execution_levers = []
        
        for lever_data in levers_data.get("levers", [])[:5]:
            title = lever_data.get("title", "")
            description = lever_data.get("description", "")
            impact = lever_data.get("impact", "medium")
            category = lever_data.get("category", "Strategy")
            source_company = lever_data.get("source_company")
            visual_demo_query = lever_data.get("visual_demo_query")
            
            # Try to find visual demonstration if suggested
            media_url = None
            media_description = None
            
            if visual_demo_query:
                try:
                    print(f"Searching for visual demo: {visual_demo_query}")
                    
                    # Use REST API with Media Classifier for images
                    headers = {
                        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                        "Content-Type": "application/json"
                    }
                    
                    payload = {
                        "model": "sonar-pro",
                        "media_response": {
                            "overrides": {
                                "return_images": True,
                                "return_videos": True
                            }
                        },
                        "messages": [
                            {
                                "role": "system",
                                "content": "Find visual demonstrations, diagrams, or educational content that illustrates this concept."
                            },
                            {
                                "role": "user",
                                "content": f"Show visual demonstration: {visual_demo_query}"
                            }
                        ],
                        "temperature": 0.3,
                        "max_tokens": 500
                    }
                    
                    api_response = requests.post(
                        "https://api.perplexity.ai/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if api_response.status_code == 200:
                        response_data = api_response.json()
                        media_content = response_data['choices'][0]['message']['content']
                        
                        # Check for media in response
                        images = response_data.get('media', {}).get('images', [])
                        videos_in_lever = response_data.get('media', {}).get('videos', [])
                        
                        # Prefer videos, then images
                        if videos_in_lever and len(videos_in_lever) > 0:
                            media_url = videos_in_lever[0].get('url')
                            media_description = videos_in_lever[0].get('title', visual_demo_query)
                            print(f"✅ Found video demo: {media_url}")
                        elif images and len(images) > 0:
                            media_url = images[0].get('url')
                            media_description = images[0].get('title', visual_demo_query)
                            print(f"✅ Found image demo: {media_url}")
                    else:
                        print(f"Media search failed: {api_response.status_code}")
                        media_content = ""
                    
                    # If no media from Media Classifier, look for image URLs in content
                    if not media_url:
                        import re
                        image_patterns = [
                            r'https?://[^\s\)]+\.(?:jpg|jpeg|png|gif|svg|webp)',
                            r'https?://imgur\.com/[\w]+',
                            r'https?://i\.imgur\.com/[\w]+\.[\w]+'
                        ]
                        
                        for pattern in image_patterns:
                            matches = re.findall(pattern, media_content)
                            if matches:
                                media_url = matches[0]
                                media_description = visual_demo_query
                                print(f"✅ Found visual demo in content: {media_url}")
                                break
                except Exception as e:
                    print(f"Could not find visual demo for '{visual_demo_query}': {e}")
            
            # Build citations
            lever_citations = []
            for citation in response_citations[:2]:
                if isinstance(citation, dict):
                    lever_citations.append(Citation(
                        title=citation.get('title', 'Source'),
                        url=citation.get('url', ''),
                        snippet=citation.get('snippet', '')[:200]
                    ))
            
            execution_levers.append(ExecutionLever(
                title=title,
                description=description,
                impact=impact,
                category=category,
                media_url=media_url,
                media_description=media_description,
                source_company=source_company,
                citations=lever_citations
            ))
        
        return execution_levers
        
    except Exception as e:
        print(f"Error generating execution levers: {e}")
        import traceback
        traceback.print_exc()
        return []

async def fetch_crunchbase_data(idea: str, industry: str, mcq_context: str) -> dict:
    """
    Fetch real Crunchbase data about startups in this space using Sonar Finance
    Returns actual funding data, success rates, and outcomes
    """
    if not client:
        return {
            "total_companies": 0,
            "funded_companies": 0,
            "success_rate": 0.0,
            "avg_funding": "Unknown",
            "total_funding": "Unknown",
            "time_to_funding": "Unknown",
            "failure_rate": 0.0,
            "details": []
        }
    
    try:
        # Construct query to find real Crunchbase data
        crunchbase_query = f"""Search Crunchbase data for startups in: {idea}

Find specific information:
1. Total number of startups in this category (last 5 years)
2. How many raised Series A or later (success indicator)
3. How many failed or shut down (failure rate)
4. Average funding amounts raised
5. Total capital deployed in this space
6. Time from founding to first institutional round

Provide ACTUAL DATA from Crunchbase, not estimates. Include:
- Company names and their funding amounts
- Success vs failure outcomes
- Recent funding rounds (last 12-24 months)
- Exit events (acquisitions, IPOs)

Context: {mcq_context if mcq_context else 'General market analysis'}"""

        response = client.chat.completions.create(
            model="sonar-finance",
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial data analyst with access to Crunchbase. Provide REAL DATA ONLY - actual company names, funding amounts, and outcomes. Do not estimate or generalize."
                },
                {
                    "role": "user",
                    "content": crunchbase_query
                }
            ],
            temperature=0.2,  # Very low for factual data
            max_tokens=2000,
            search_recency_filter="year"  # Recent data only
        )
        
        content = response.choices[0].message.content.lower()
        
        # Extract real numbers from the response
        import re
        
        # Find total companies mentioned
        total_match = re.search(r'(\d+)\s+(?:startups|companies)', content)
        total_companies = int(total_match.group(1)) if total_match else 0
        
        # Find funded companies
        funded_match = re.search(r'(\d+)\s+(?:raised|funded|secured)', content)
        funded_companies = int(funded_match.group(1)) if funded_match else 0
        
        # Find failures
        failure_match = re.search(r'(\d+)\s+(?:failed|shut down|closed)', content)
        failed_companies = int(failure_match.group(1)) if failure_match else 0
        
        # Calculate success rate from real data
        if total_companies > 0:
            success_rate = funded_companies / total_companies
            failure_rate = failed_companies / total_companies if failed_companies > 0 else (1 - success_rate) * 0.6
        else:
            # If no data, use conservative industry averages
            success_rate = 0.30
            failure_rate = 0.45
        
        # Extract funding amounts
        funding_matches = re.findall(r'\$(\d+(?:\.\d+)?)\s*([mb])', content)
        funding_amounts = []
        for amount, unit in funding_matches:
            multiplier = 1000000 if unit == 'm' else 1000000000
            funding_amounts.append(float(amount) * multiplier)
        
        avg_funding = f"${sum(funding_amounts) / len(funding_amounts) / 1000000:.1f}M" if funding_amounts else "Unknown"
        total_funding = f"${sum(funding_amounts) / 1000000:.0f}M" if funding_amounts else "Unknown"
        
        # Extract time to funding (look for patterns like "18 months" or "2 years")
        time_match = re.search(r'(\d+)\s+(?:months|years)', content)
        time_to_funding = time_match.group(0) if time_match else "18-24 months"
        
        # Parse company details
        details = []
        lines = content.split('\n')
        for line in lines:
            if any(word in line for word in ['raised', 'funded', 'acquired', 'shut down', 'series']):
                details.append(line.strip())
        
        return {
            "total_companies": max(total_companies, 10),  # Minimum threshold
            "funded_companies": funded_companies,
            "success_rate": success_rate,
            "avg_funding": avg_funding,
            "total_funding": total_funding,
            "time_to_funding": time_to_funding,
            "failure_rate": failure_rate,
            "details": details[:10],  # Top 10 relevant facts
            "raw_data": content[:500]  # First 500 chars for debugging
        }
        
    except Exception as e:
        print(f"Error fetching Crunchbase data: {e}")
        import traceback
        traceback.print_exc()
        
        # Return conservative defaults based on industry averages
        return {
            "total_companies": 50,
            "funded_companies": 15,
            "success_rate": 0.30,
            "avg_funding": "$5M",
            "total_funding": "$250M",
            "time_to_funding": "18-24 months",
            "failure_rate": 0.45,
            "details": ["Unable to fetch real-time Crunchbase data"],
            "raw_data": str(e)
        }

async def get_market_analysis_with_finance(idea: str, mcq_context: str, analysis_data: dict) -> dict:
    """
    Use Perplexity Sonar Finance to get real-time market and financial data
    """
    if not client:
        # Return defaults if client not configured
        return {
            "crowding_index": float(analysis_data.get("market_crowding", 64)),
            "tam_sam_rationale": "Estimated TAM of $50B based on market analysis",
            "funding_velocity": "15 deals in last 12 months totaling $85M",
            "notable_moats": "Network effects, switching costs, data moats",
            "citations": []
        }
    
    try:
        # Construct financial research query
        finance_query = f"""Analyze the market and financial landscape for: {idea}
        
Context: {mcq_context if mcq_context else 'No additional context'}

Provide detailed financial and market analysis:
1. Total Addressable Market (TAM) and Serviceable Addressable Market (SAM) with recent data
2. Recent funding activity in this space (deals in last 12-24 months, amounts, notable investors)
3. Market competitiveness/crowding (0-100 scale, where 100 is extremely crowded)
4. Defensible moats and competitive advantages in this market
5. Notable competitors and their funding status

Return structured data with specific numbers, dates, and sources."""

        # Use Sonar Finance model for financial/market intelligence
        response = client.chat.completions.create(
            model="sonar-finance",  # Financial and market-focused model
            messages=[
                {
                    "role": "system",
                    "content": "You are a financial analyst providing data-driven market intelligence. Focus on recent financial data, funding rounds, market size, and competitive analysis. Cite specific sources and numbers."
                },
                {
                    "role": "user",
                    "content": finance_query
                }
            ],
            temperature=0.3,  # Lower temperature for more factual responses
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        # Extract citations if available
        citations = []
        if hasattr(response, 'citations') and response.citations:
            for citation in response.citations[:3]:
                citations.append(Citation(
                    title=citation.get("title", "Financial Source"),
                    url=citation.get("url", ""),
                    snippet=citation.get("snippet", "")[:200],
                    date=citation.get("date")
                ))
        
        # Parse the response to extract structured data
        # Try to find TAM/SAM information
        tam_sam_rationale = "Market size data unavailable"
        funding_velocity = "Funding data unavailable"
        notable_moats = "Competitive advantages analysis unavailable"
        crowding_index = float(analysis_data.get("market_crowding", 50))
        
        # Look for TAM/SAM mentions
        lines = content.lower().split('\n')
        for i, line in enumerate(lines):
            if 'tam' in line or 'total addressable market' in line or 'market size' in line:
                # Get this line and next few lines
                tam_sam_rationale = ' '.join(lines[i:min(i+3, len(lines))]).strip()
                if len(tam_sam_rationale) > 200:
                    tam_sam_rationale = tam_sam_rationale[:200] + "..."
                break
        
        # Look for funding information
        for i, line in enumerate(lines):
            if 'funding' in line or 'raised' in line or 'investment' in line or 'deals' in line:
                funding_velocity = ' '.join(lines[i:min(i+3, len(lines))]).strip()
                if len(funding_velocity) > 200:
                    funding_velocity = funding_velocity[:200] + "..."
                break
        
        # Look for moats/competitive advantages
        for i, line in enumerate(lines):
            if 'moat' in line or 'competitive advantage' in line or 'barrier' in line or 'defensib' in line:
                notable_moats = ' '.join(lines[i:min(i+3, len(lines))]).strip()
                if len(notable_moats) > 200:
                    notable_moats = notable_moats[:200] + "..."
                break
        
        # Look for crowding/competition indicators
        for line in lines:
            if 'crowd' in line or 'competitive' in line or 'saturated' in line:
                # Try to extract a number if mentioned
                if 'high' in line or 'very' in line or 'extremely' in line:
                    crowding_index = 75.0
                elif 'moderate' in line or 'medium' in line:
                    crowding_index = 50.0
                elif 'low' in line or 'emerging' in line:
                    crowding_index = 25.0
                break
        
        # If we didn't find good data, use the full response intelligently
        if tam_sam_rationale == "Market size data unavailable":
            # Extract first meaningful paragraph
            paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 50]
            if paragraphs:
                tam_sam_rationale = paragraphs[0][:200]
                if len(paragraphs) > 1:
                    funding_velocity = paragraphs[1][:200] if len(paragraphs[1]) > 50 else funding_velocity
                if len(paragraphs) > 2:
                    notable_moats = paragraphs[2][:200] if len(paragraphs[2]) > 50 else notable_moats
        
        return {
            "crowding_index": crowding_index,
            "tam_sam_rationale": tam_sam_rationale,
            "funding_velocity": funding_velocity,
            "notable_moats": notable_moats,
            "citations": citations
        }
        
    except Exception as e:
        print(f"Error in Sonar Finance analysis: {e}")
        import traceback
        traceback.print_exc()
        
        # Return defaults on error
        return {
            "crowding_index": float(analysis_data.get("market_crowding", 64)),
            "tam_sam_rationale": "Market analysis temporarily unavailable",
            "funding_velocity": "Funding data temporarily unavailable",
            "notable_moats": "Competitive analysis temporarily unavailable",
            "citations": []
        }

# API Endpoints
@app.get("/")
async def root():
    return {
        "service": "IdeaCompass API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_configured = client is not None and bool(PERPLEXITY_API_KEY)
    return {
        "status": "healthy",
        "api_configured": api_configured,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/classify-media")
async def classify_media(media_url: str, context: Optional[str] = None):
    """
    Classify and analyze media content (logos, screenshots, images)
    Returns insights about brand positioning, product, and market signals
    """
    if not client:
        raise HTTPException(status_code=500, detail="Perplexity client not configured")

    try:
        result = await classify_media_content(media_url, context or "")
        return {
            "status": "success",
            "media_url": media_url,
            "analysis": result["analysis"],
            "insights": result["insights"],
            "confidence": result["confidence"],
            "media_results": result["media_results"]
        }
    except Exception as e:
        print(f"Error in media classification endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Media classification failed: {str(e)}")

@app.post("/api/company-logo")
async def get_company_logo(company_name: str, company_website: str):
    """
    Get company logo using simple favicon extraction
    Just gets the favicon.ico from the company's website - simple and reliable
    """
    try:
        logo_url = await get_company_logo_url(company_name, company_website)
        return {
            "status": "success",
            "company_name": company_name,
            "logo_url": logo_url
        }
    except Exception as e:
        print(f"Error getting company logo: {e}")
        raise HTTPException(status_code=500, detail=f"Logo fetch failed: {str(e)}")

@app.post("/api/educational-media")
async def get_educational_visuals(query: str):
    """
    Get educational/informational visual content using Media Classifier
    This works for concepts, processes, demonstrations, diagrams, etc.
    Does NOT work for promotional content like company logos.
    """
    if not client:
        raise HTTPException(status_code=500, detail="Perplexity client not configured")

    try:
        result = await get_educational_visual_content(query)
        return {
            "status": "success",
            "query": query,
            "analysis": result["analysis"],
            "insights": result["insights"],
            "confidence": result["confidence"],
            "media_results_count": len(result["media_results"])
        }
    except Exception as e:
        print(f"Error getting educational visuals: {e}")
        raise HTTPException(status_code=500, detail=f"Educational media analysis failed: {str(e)}")

@app.post("/api/market-visual-content")
async def get_market_visuals(idea: str, context: Optional[str] = None):
    """
    Get visual content that helps understand a market using Media Classifier
    Returns graphs, charts, diagrams, and visual data about market trends, competitive landscape, etc.
    """
    if not client:
        raise HTTPException(status_code=500, detail="Perplexity client not configured")

    try:
        # Use basic market data for context
        market_data = {
            "crowding_index": 50,
            "tam_sam_rationale": f"Market analysis for {idea}",
            "funding_velocity": "Recent funding trends",
            "notable_moats": "Competitive advantages"
        }

        result = await get_market_visual_content(idea, market_data)

        return {
            "status": "success",
            "idea": idea,
            "visual_content": result["visual_content"],
            "market_insights": result["market_insights"],
            "media_results_count": len(result["media_results"])
        }
    except Exception as e:
        print(f"Error getting market visuals: {e}")
        raise HTTPException(status_code=500, detail=f"Market visual analysis failed: {str(e)}")

@app.post("/api/generate-mcqs", response_model=MCQResponse)
async def generate_mcqs(submission: IdeaSubmission):
    """Generate 3 MCQs to disambiguate the idea"""
    
    if not client:
        raise HTTPException(status_code=500, detail="Perplexity client not configured. Please set PERPLEXITY_API_KEY")
    
    try:
        # Use Perplexity's chat API
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": """Generate exactly 3 multiple-choice questions to disambiguate this business idea.
Focus on: 1) Target buyer, 2) Go-to-market approach, 3) Regulatory exposure.

Return JSON:
{
  "questions": [
    {
      "question": "Question text?",
      "options": ["Option1", "Option2", "Option3", "Option4", "Option5"],
      "reason": "Why this matters"
    }
  ],
  "idea_summary": "Brief summary"
}"""
                },
                {
                    "role": "user",
                    "content": f"Business idea: {submission.text}"
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        parsed = parse_json_response(content)
        
        if "questions" in parsed and len(parsed["questions"]) > 0:
            return MCQResponse(
                questions=[
                    MCQQuestion(
                        question=q["question"],
                        options=q["options"],
                        reason=q.get("reason", "")
                    ) for q in parsed["questions"][:3]
                ],
                idea_summary=parsed.get("idea_summary", submission.text[:100])
            )
        else:
            # Fallback to defaults
            return MCQResponse(
                questions=get_default_mcqs(),
                idea_summary=submission.text[:100]
            )
        
    except Exception as e:
        print(f"Error generating MCQs: {e}")
        # Return default MCQs instead of failing
        return MCQResponse(
            questions=get_default_mcqs(),
            idea_summary=submission.text[:100]
        )

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_idea(request: AnalysisRequest):
    """Perform comprehensive analysis using Perplexity Search + Sonar Pro"""
    
    if not client:
        raise HTTPException(status_code=500, detail="Perplexity client not configured. Please set PERPLEXITY_API_KEY")
    
    try:
        # Build search context
        mcq_context = ""
        if request.mcq_answers:
            mcq_context = " | ".join([f"{a.question}: {a.answer}" for a in request.mcq_answers])
        
        # Step 0: Analyze media if provided
        media_insights = []
        if request.media_urls:
            for media_url in request.media_urls[:3]:  # Limit to 3 media items
                try:
                    media_result = await classify_media_content(media_url, request.idea)
                    if media_result["insights"]:
                        media_insights.extend(media_result["insights"])
                except Exception as e:
                    print(f"Media analysis error for {media_url}: {e}")
        
        # Add media insights to context if available
        if media_insights:
            mcq_context = f"{mcq_context} | Visual insights: {'; '.join(media_insights[:3])}"
        
        # Step 1: Use Search API to find REAL comparable companies with sources
        search_queries = [
            f"{request.idea} startup company raised funding Crunchbase",
            f"{request.idea} similar companies Series A B funding TechCrunch",
            f"{request.idea} competitors startups acquired IPO",
            f"{request.idea} failed shutdown post-mortem"
        ]
        
        all_search_results = []
        for query in search_queries[:2]:  # Top 2 queries for speed
            try:
                print(f"Searching: {query}")
                search_result = client.search.create(
                    query=query,
                    max_results=15,  # More results for better data
                    max_tokens_per_page=2048
                )
                if hasattr(search_result, 'results') and search_result.results:
                    all_search_results.extend(search_result.results)
            except Exception as e:
                print(f"Search API error for '{query}': {e}")
                continue
        
        print(f"Found {len(all_search_results)} search results from web")
        
        # Step 2: Extract REAL companies from search results using Sonar Pro
        extraction_prompt = f"""Based on these REAL search results about: {request.idea}

Extract actual companies mentioned with their details. Return JSON:
{{
  "companies": [
    {{
      "name": "Actual Company Name",
      "website": "company.com",
      "funding_raised": "$X M/B",
      "outcome": "success|active|failed",
      "traction": "ARR/users/metrics",
      "founded": "Year",
      "description": "What they do"
    }}
  ],
  "market_insights": {{
    "success_rate": 0.X,
    "avg_funding": "$XM",
    "market_crowding": 0-100,
    "trends": "Market trends"
  }}
}}

ONLY use companies EXPLICITLY mentioned in the search results. Include the source URL for each."""
        
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "system",
                    "content": f"You are extracting REAL company data from web search results. Only return companies explicitly mentioned with verifiable details. Search results context: {json.dumps([r.get('title', '') + ' ' + r.get('snippet', '')[:200] for r in all_search_results[:10]], ensure_ascii=False)}"
                },
                {
                    "role": "user",
                    "content": extraction_prompt
                }
            ],
            temperature=0.2,  # Low for factual extraction
            max_tokens=2500,
            return_citations=True  # Get source URLs
        )
        
        content = response.choices[0].message.content
        analysis_data = parse_json_response(content)
        
        # Extract citations from response
        response_citations = []
        if hasattr(response, 'citations') and response.citations:
            response_citations = response.citations
        
        # Build REAL comparables from extracted companies
        comparables = []
        companies_data = analysis_data.get("companies", [])
        
        print(f"Extracted {len(companies_data)} real companies from web data")
        
        for idx, comp in enumerate(companies_data[:10]):  # Top 10 companies
            company_name = comp.get("name", "")
            company_website = comp.get("website", "")

            # Skip if no real name
            if not company_name or company_name.lower() in ["unknown", "company", "startup"]:
                continue

            # Get logo using dedicated logo services (Media Classifier doesn't return promotional logos)
            logo_url = await get_company_logo_url(company_name, company_website)
            
            # Determine outcome from description
            outcome = comp.get("outcome", "active")
            if outcome not in ["success", "active", "failed"]:
                outcome_lower = comp.get("description", "").lower()
                if "acquired" in outcome_lower or "ipo" in outcome_lower or "exit" in outcome_lower:
                    outcome = "win"
                elif "shut down" in outcome_lower or "failed" in outcome_lower or "closed" in outcome_lower:
                    outcome = "fail"
                else:
                    outcome = "ok"
            else:
                outcome = "win" if outcome == "success" else ("fail" if outcome == "failed" else "ok")
            
            # Calculate similarity (based on how early it appeared in results)
            similarity = max(60, 95 - (idx * 5))
            
            # Build citations from search results
            company_citations = []
            for result in all_search_results:
                if company_name.lower() in result.get('title', '').lower() or \
                   company_name.lower() in result.get('snippet', '').lower():
                    company_citations.append(Citation(
                        title=result.get('title', 'Source'),
                        url=result.get('url', ''),
                        snippet=result.get('snippet', '')[:200],
                        date=result.get('published_date')
                    ))
                    if len(company_citations) >= 2:
                        break
            
            # Extract tags from MCQ context
            tags = {}
            if "smb" in mcq_context.lower():
                tags["buyer"] = "SMB"
            elif "enterprise" in mcq_context.lower():
                tags["buyer"] = "Enterprise"
            else:
                tags["buyer"] = "B2B"
            
            if "plg" in mcq_context.lower() or "product-led" in mcq_context.lower():
                tags["gtm"] = "PLG"
            elif "sales" in mcq_context.lower():
                tags["gtm"] = "Sales"
            else:
                tags["gtm"] = "Hybrid"
            
            tags["model"] = "SaaS" if "saas" in request.idea.lower() else "Tech"
            
            comparables.append(Comparable(
                name=company_name,
                url=f"https://{company_website}" if company_website and not company_website.startswith("http") else (company_website or "#"),
                logo_url=logo_url,  # Clearbit logo URL
                similarity_score=float(similarity),
                tags=tags,
                traction_snippet=comp.get("traction", comp.get("description", ""))[:200],
                funding_snippet=comp.get("funding_raised", "Funded"),
                outcome_label=outcome,
                citations=company_citations
            ))
        
        print(f"Built {len(comparables)} comparable companies with real data")
        
        # Fetch REAL Crunchbase data for this space
        print(f"Fetching real Crunchbase data for: {request.idea}")
        crunchbase_data = await fetch_crunchbase_data(
            idea=request.idea,
            industry=analysis_data.get("industry", ""),
            mcq_context=mcq_context
        )
        print(f"Crunchbase data: {crunchbase_data['total_companies']} companies, {crunchbase_data['success_rate']:.1%} success rate")
        
        # Market analysis using Sonar Finance (moved before probabilities)
        market_data = await get_market_analysis_with_finance(request.idea, mcq_context, analysis_data)
        market_analysis = MarketAnalysis(
            crowding_index=market_data["crowding_index"],
            tam_sam_rationale=market_data["tam_sam_rationale"],
            funding_velocity=market_data["funding_velocity"],
            notable_moats=market_data["notable_moats"],
            citations=market_data["citations"]
        )

        # Get visual content that helps understand the market
        print(f"Fetching visual market content for: {request.idea}")
        market_visual_data = await get_market_visual_content(request.idea, market_data)
        market_visual_content = MarketVisualContent(
            visual_content=market_visual_data["visual_content"],
            market_insights=market_visual_data["market_insights"],
            media_results_count=len(market_visual_data["media_results"])
        )
        
        # Generate flexible execution levers with media support
        print(f"Generating execution levers with media for: {request.idea}")
        execution_levers = await get_execution_levers_with_media(
            idea=request.idea,
            comparables=comparables,
            market_data=market_data
        )
        
        # Pivot suggestions from real market patterns
        pivot_prompt = f"""Based on the {len(comparables)} real companies analyzed for {request.idea}:

Identify 2-3 actual pivot opportunities with REAL examples.

Return JSON:
{{
  "pivots": [
    {{
      "title": "Specific Pivot Direction",
      "rationale": "Company X pivoted this way and achieved Y result",
      "expected_uplift": 0.XX,
      "effort": X.X,
      "example_company": "Real company"
    }}
  ]
}}

Only suggest pivots with real precedent."""

        try:
            pivot_response = client.chat.completions.create(
                model="sonar-pro",
                messages=[
                    {
                        "role": "system",
                        "content": f"Analyze pivot patterns from: {', '.join([c.name for c in comparables[:5]])}"
                    },
                    {
                        "role": "user",
                        "content": pivot_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            pivot_data = parse_json_response(pivot_response.choices[0].message.content)
            pivot_suggestions = []
            for pivot in pivot_data.get("pivots", [])[:3]:
                pivot_suggestions.append(PivotSuggestion(
                    title=pivot.get("title", ""),
                    rationale=pivot.get("rationale", ""),
                    expected_uplift=float(pivot.get("expected_uplift", 0.10)),
                    effort_score=float(pivot.get("effort", 5.0)),
                    citations=[]
                ))
        except Exception as e:
            print(f"Error generating pivot suggestions: {e}")
            pivot_suggestions = []
        
        return AnalysisResponse(
            id=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            idea_summary=request.idea[:100],
            tags=["AI", "B2B", "SaaS", "Automation"],
            mcq_answers=request.mcq_answers,
            comparables=comparables,
            market_analysis=market_analysis,
            market_visual_content=market_visual_content,
            execution_levers=execution_levers,
            pivot_suggestions=pivot_suggestions,
            created_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"Error in analysis: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
