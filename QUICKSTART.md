# IdeaCompass Quick Start 🚀

Get IdeaCompass running in 5 minutes!

## Step 1: Get Your Perplexity API Key

1. Visit [https://www.perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)
2. Sign in or create an account
3. Click "Generate API Key"
4. Copy your key (starts with `pplx-`)

## Step 2: Add Your API Key

Open `backend/.env` and replace the placeholder:

```bash
PERPLEXITY_API_KEY=pplx-your-actual-key-here
```

## Step 3: Start the Application

### Option A: Automated (Recommended)

```bash
./start.sh
```

This single command will:
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ Start both backend and frontend servers

### Option B: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Step 4: Open Your Browser

Navigate to: **http://localhost:3000**

## Step 5: Test It Out

1. Click "I have an idea"
2. Enter: *"AI agent that reconciles invoices and cards for SMBs"*
3. Click "Analyze"
4. Answer the 3 MCQs
5. View your comprehensive analysis!

## What You'll See

### Dashboard Includes:
- 📊 **Outcome Probabilities** - P(next round), P(PMF), survival odds
- 🏢 **Similar Startups** - 10+ comparable companies with success/failure tags
- 🎯 **Market Analysis** - Crowding index, TAM/SAM, funding velocity
- ⚠️ **Risk Radar** - Regulatory, platform, pricing, distribution risks
- ⚡ **Execution Levers** - Top 3 prioritized actions
- 🔄 **Pivot Navigator** - Alternative paths with expected uplift
- 📚 **Citations** - Every claim linked to sources

## Understanding the Results

### Outcome Probabilities

```
Next Round: 43% [30%–55%]
```

This means:
- **43%** is the best estimate (mean)
- **[30%–55%]** is the 80% confidence interval
- These are based on similar companies in your reference class

### Similarity Scores

```
Company X: 85% match
```

- Higher scores mean more similar to your idea
- Based on buyer, model, GTM, regulatory factors

### Risk Radar (0-100 scale)

- **0-30**: Low risk
- **31-60**: Moderate risk
- **61-100**: High risk

## Cost Per Analysis

Each analysis costs approximately:
- **$0.10 - $0.24** using Perplexity APIs
- Monitor your usage at [Perplexity Settings](https://www.perplexity.ai/settings/api)

## Troubleshooting

### "PERPLEXITY_API_KEY not configured"
➡️ Add your key to `backend/.env`

### "Port already in use"
➡️ Kill existing processes:
```bash
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

### "Module not found"
➡️ Reinstall dependencies:
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Next Steps

1. ✅ Complete this quick start
2. 📖 Read [README.md](README.md) for detailed documentation
3. 🏗️ Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. 🔧 Review [SETUP.md](SETUP.md) for advanced configuration

## Need Help?

- 📚 **Perplexity Docs**: [https://docs.perplexity.ai](https://docs.perplexity.ai)
- 🔍 **API Reference**: [https://docs.perplexity.ai/api-reference](https://docs.perplexity.ai/api-reference)
- 💬 **Issues**: Create an issue in your repository

---

**Happy analyzing!** 🧭

Remember: IdeaCompass uses reference-class forecasting to provide **probabilistic** estimates, not certainties. Always combine these insights with your domain expertise and judgment.

