# MCP-Powered Lead Gen & Outreach System

A full-stack demo system that uses the Model Context Protocol (MCP) concepts to orchestrate a lead generation pipeline (Generate -> Enrich -> Message -> Send).

## Architecture
- **Backend**: Python (FastAPI). Implements "MCP Tools" as API endpoints.
- **Frontend**: React + Vite. Monitors the pipeline status.
- **Orchestration**: n8n (via `n8n_workflow.json`) or Client-Side Agent (builtin).
- **Database**: SQLite (`leads.db`).

## Setup

### Prerequisites
- Python 3.10+
- Node.js & npm

### 1. Backend Setup
1. Navigate to `backend/`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python mcp_server.py
   ```
   The API will be available at `http://localhost:8000`.

### 2. Frontend Setup
1. Navigate to `frontend/`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

## Orchestration

### Option A: Built-in Agent (Recommended for Demo)
1. Open the Frontend (`http://localhost:5173`).
2. Click **"+ Generate 10 Leads"**.
3. Click **"▶ Run Agent Pipeline"**.
4. Watch the status update in real-time as the "Agent" iterates through the leads and calls the MCP tools.

### Option B: n8n Workflow
1. Import `orchestration/n8n_workflow.json` into n8n.
2. Ensure n8n can access `http://localhost:8000` (if running locally, you might need a tunnel like ngrok or run n8n locally).
3. Execute the workflow.

## MCP Tool Implementation
The backend exposes the following "Tools" (endpoints) that adhere to the MCP logic:

- `POST /tools/generate_leads`: Generates valid leads using Faker.
- `POST /tools/enrich_lead`: Enriches data (Company Size, Persona, Pain Points).
- `POST /tools/generate_messages`: Creates personalized Email/LinkedIn drafts.
- `POST /tools/send_message`: Simulates sending (Dry Run / Live).
- `GET /tools/get_stats`: Returns pipeline metrics.

## Design Decisions
- **FastAPI**: Used to provide a specific HTTP interface for both the Frontend and n8n while maintaining the logical structure of an MCP server.
- **SQLite**: Simple, file-based persistence as requested.
- **Faker**: Used to generate realistic dummy data without external API dependencies.
