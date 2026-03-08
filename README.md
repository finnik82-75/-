# AI Competitor Monitoring Platform

**AI-powered system for automated competitor content analysis**

A production-oriented platform for media, marketing, and strategy teams that automates competitor monitoring: it scrapes news portals, analyzes text and visuals with LLM and Vision API, and delivers structured insights. No more manual tracking—get systematic analysis of editorial policy, tone, themes, and visual style across competitors, with history and optional desktop client.

Suitable for **media holdings**, **marketing agencies**, **regional publishers**, and **digital teams** who need to benchmark competitors and inform content strategy.

---

## Business Problem

| Pain point | Impact |
|------------|--------|
| **Manual competitor monitoring** | Consumes hours every week with little structure. |
| **No systematic view of editorial policy** | Hard to see what competitors focus on and how they frame stories. |
| **No automated comparison of content and visuals** | Text and design are assessed ad hoc, not at scale. |
| **Difficulty tracking strategy shifts** | Changes in tone, topics, or format go unnoticed until too late. |

The platform addresses these by automating collection, AI analysis (text + images), and storage so teams can focus on decisions instead of manual monitoring.

---

## Solution

End-to-end flow:

**User** → **REST API** → **Parser (Selenium)** → **LLM (GPT-4o)** → **Vision API** → **Storage** → **Dashboard / Desktop client**

- **Bulk article analysis**: parse multiple competitor URLs in one run.
- **Theme and tone detection**: identify main topics and sentiment from text.
- **Visual style analysis**: screenshots analyzed for layout, style, and UX.
- **Competitor comparison**: side-by-side insights across configured portals.
- **History**: last analyses stored for quick access and trend review.

---

## Architecture

| Layer | Technology | Role |
|-------|------------|------|
| **Backend** | FastAPI | REST API, routing, orchestration. |
| **Parsing** | Selenium | Scraping pages, screenshots, extracting title/headings/text. |
| **AI (text)** | OpenAI GPT-4o | Editorial policy, strengths/weaknesses, recommendations. |
| **AI (vision)** | OpenAI Vision API | Visual style, layout, and content presentation. |
| **Storage** | Local DB / JSON | Persisted history of analyses. |
| **Client** | PyQt6 desktop app | Desktop UI for running analyses and viewing results. |
| **Config** | `.env` | API keys, endpoints, ports. |

---

## Tech Stack

- **Python**
- **FastAPI** — REST API
- **OpenAI API** — GPT-4o (text + vision)
- **Selenium** — browser automation and scraping
- **PyQt6** — desktop client
- **python-dotenv** — environment configuration
- **REST** — standard HTTP API design

---

## Key Features

- **Automated competitor scraping** — scheduled or on-demand parsing of configured portals.
- **AI text analysis** — themes, tone, strengths/weaknesses, and recommendations.
- **Visual content analysis** — screenshots evaluated for style and structure.
- **Trend detection** — historical data for comparing runs over time.
- **Historical data tracking** — recent analyses stored and retrievable.
- **Desktop client support** — PyQt6 app for running analyses without a browser.
- **Production-ready API** — clear endpoints, CORS, logging, and docs (Swagger/ReDoc).

---

## Use Cases

- **Media holdings** — monitor rival outlets and align own editorial strategy.
- **Marketing agencies** — benchmark client competitors’ content and creative.
- **Regional publishers** — track local competitors and differentiate.
- **Strategy and insights** — evidence-based reports on competitor moves.
- **Digital teams** — regular competitor snapshots for product and content decisions.

---

## How to Run

### 1. Clone and prepare environment

```bash
git clone https://github.com/yourusername/pem08-master.git
cd pem08-master

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/macOS

pip install -r requirements.txt
```

Optional desktop client:

```bash
pip install -r desktop/requirements.txt
```

### 2. Environment configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_key_here
```

For OpenAI-compatible proxies (e.g. ProxyAPI), you can use:

```env
PROXY_API_KEY=your_key_here
```

Optional: `OPENAI_MODEL`, `OPENAI_VISION_MODEL`, `API_HOST`, `API_PORT`. See `env.example.txt`.

### 3. Configure competitors

Edit `backend/config.py` and set `competitor_urls` to your target portals.

### 4. Start the backend

```bash
uvicorn backend.main:app --reload
```

Or use the launcher:

```bash
python run.py
```

- API: **http://localhost:8000**
- Swagger: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**

### 5. (Optional) Desktop client

With the backend running:

```bash
cd desktop
python main.py
```

---

## Portfolio Positioning

This project demonstrates:

- **AI system design** — combining LLM and Vision in one product.
- **Backend architecture** — FastAPI, services, and clear API boundaries.
- **LLM integration** — structured prompts and parsing for editorial analysis.
- **Vision API integration** — image-based evaluation of competitor sites.
- **Automated content intelligence** — from URLs to actionable insights.
- **Business-focused AI implementation** — built for real monitoring and strategy use cases.

---

## License

MIT License. Contributions and issues are welcome.
