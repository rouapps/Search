# IdeaCompass Setup Guide

Complete setup instructions for the IdeaCompass platform.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Perplexity API Key** - [Get API Key](https://www.perplexity.ai/settings/api)

## Quick Start (Automated)

The easiest way to get started is using the startup script:

```bash
# Make the script executable
chmod +x start.sh

# Run the startup script
./start.sh
```

This will:
1. Check for required dependencies
2. Set up Python virtual environment
3. Install backend dependencies
4. Start the FastAPI backend server
5. Install frontend dependencies
6. Start the Next.js frontend server

## Manual Setup

If you prefer to set up each component manually:

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your PERPLEXITY_API_KEY
nano .env  # or use your preferred editor

# Start the server
python main.py
```

The backend API will be available at `http://localhost:8000`

#### Backend API Documentation

Once the backend is running, you can access:
- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`

### 2. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.local.example .env.local
# Edit .env.local if backend is not on localhost:8000

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Backend Environment Variables

Edit `backend/.env`:

```bash
# Required: Your Perplexity API key
PERPLEXITY_API_KEY=pplx-your-key-here
```

### Frontend Environment Variables

Edit `frontend/.env.local`:

```bash
# API endpoint (default: http://localhost:8000)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Verifying Installation

### Test Backend

```bash
# In a new terminal
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-10-18T..."
}
```

### Test Frontend

1. Open your browser to `http://localhost:3000`
2. You should see the IdeaCompass landing page
3. Try submitting a test idea

## Getting Your Perplexity API Key

1. Visit [Perplexity Settings](https://www.perplexity.ai/settings/api)
2. Log in or create an account
3. Navigate to the API section
4. Generate a new API key
5. Copy the key (starts with `pplx-`)
6. Add it to `backend/.env`

## Common Issues

### Issue: "PERPLEXITY_API_KEY not configured"

**Solution**: Make sure you've added your API key to `backend/.env`

### Issue: "Port 8000 already in use"

**Solution**: 
```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9

# Or change the port in backend/main.py (last line)
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Issue: "Port 3000 already in use"

**Solution**:
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or run on a different port
npm run dev -- -p 3001
```

### Issue: Module not found errors

**Solution**:
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Development Workflow

### Backend Development

```bash
cd backend
source venv/bin/activate

# The server auto-reloads on file changes
python main.py
```

### Frontend Development

```bash
cd frontend

# Next.js has hot-reload enabled by default
npm run dev
```

## Production Build

### Backend

```bash
cd backend
source venv/bin/activate

# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Build for production
npm run build

# Start production server
npm start
```

## Project Structure

```
Search/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── .env.example         # Environment template
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main page
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── components/          # React components
│   ├── lib/                 # Utilities and API client
│   ├── types/               # TypeScript types
│   ├── package.json         # Node dependencies
│   └── .env.local           # Frontend config
├── README.md                # Project documentation
├── SETUP.md                 # This file
└── start.sh                 # Startup script
```

## Next Steps

1. ✅ Complete setup following this guide
2. 🔑 Add your Perplexity API key
3. 🚀 Start both servers
4. 🧪 Test with a sample idea
5. 📖 Read the main [README.md](README.md) for usage details
6. 🎨 Customize the UI and branding as needed

## Support

For issues, questions, or contributions:
- Check the [README.md](README.md) for detailed documentation
- Review the API docs at `http://localhost:8000/docs`
- Check Perplexity API docs: [https://docs.perplexity.ai](https://docs.perplexity.ai)

## Cost Considerations

Each idea analysis typically costs:
- 8-12 Search API calls: ~$0.04-$0.06
- 2-3 Sonar/Sonar-Pro calls: ~$0.06-$0.18
- **Total: ~$0.10-$0.24 per analysis**

Monitor your usage at [Perplexity Settings](https://www.perplexity.ai/settings/api)

---

Happy analyzing! 🧭

