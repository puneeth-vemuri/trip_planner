---
title: Trip Planner AI
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.33.0"
app_file: webapp.py
pinned: false
license: mit
---

# 🌍 Trip Planner AI

An intelligent multi-agent trip planning system powered by CrewAI, OpenRouter, and Streamlit. Get personalized travel plans with real-time agent progress tracking.

## ✨ Features

- 🤖 **Multi-Agent System**: 4 specialized AI agents working together:
  - � Destination Research Specialist
  - ✈️ Flight Booking Specialist
  - 📋 Travel Itinerary Planner
  - 💰 Travel Budget Analyst
- � **Real-Time Progress**: Watch each agent complete their tasks step-by-step
- 👥 **Group Travel**: Plan trips for 1-20 people with per-person cost breakdowns
- 📄 **Professional PDFs**: Export beautifully formatted trip plans with proper styling
- 🎨 **Clean UI**: Modern, responsive interface with trip summaries

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenRouter API key ([get one here](https://openrouter.ai/))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/puneeth-vemuri/trip_planner.git
cd trip_planner
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create .env file
echo OPENROUTER_API_KEY=your-key-here > .env
```

5. Run the app:
```bash
streamlit run webapp.py
```

## 🌐 Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repo, branch: `main`, file: `webapp.py`
5. Advanced settings → Secrets: Add your API key in TOML format:
```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```
6. Click "Deploy"!

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web framework
- **AI Framework**: [CrewAI](https://www.crewai.com/) - Multi-agent orchestration
- **LLM Provider**: [OpenRouter](https://openrouter.ai/) - Access to Mistral-7B-Instruct
- **PDF Generation**: [ReportLab](https://www.reportlab.com/) - Professional PDF exports
- **Language**: Python 3.10+

## 📁 Project Structure

```
trip_planner/
├── agents/              # AI agent definitions
│   ├── booking_agent.py
│   ├── budget_estimator.py
│   ├── destination_researcher.py
│   └── itinerary_planner.py
├── utils/              # Utility functions
│   ├── api_utils.py
│   ├── export_utils.py
│   └── flight_search.py
├── .streamlit/         # Streamlit configuration
│   ├── config.toml
│   └── secrets.toml.example
├── crew_orchestrator.py  # Multi-agent coordination
├── webapp.py           # Main Streamlit app
├── main.py            # CLI launcher
├── requirements.txt   # Python dependencies
└── .env.example       # Environment template
```

## 🎯 How It Works

1. **User Input**: Fill out trip details (origin, destination, days, people, budget, preferences)
2. **Agent Orchestration**: CrewAI coordinates 4 specialized agents sequentially:
   - Research agent gathers destination info
   - Flight agent finds travel options
   - Itinerary agent creates day-by-day plans
   - Budget agent breaks down all costs
3. **Real-Time Updates**: UI shows progress as each agent completes their task
4. **Results**: Get a comprehensive trip plan with PDF export option

## 📝 License

© 2025 PUNEETH VEMURI - ALL RIGHTS RESERVED

---

**Built with ❤️ using CrewAI, OpenRouter, and Streamlit**

