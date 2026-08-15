# Modus Enterprise AI Process Designer 🧠🏢

An AI-driven enterprise application built for the **Modus Enterprise AI Build Challenge**.

This tool researches, architects, and maps out how AI and automation transform traditional business processes within the Finance industry. Instead of generating unstructured paragraphs of text, it functions as a strict **Process Architecture Tool**, outputting queryable, structured JSON data that visually compares legacy workflows against future AI-driven states across a three-column pipeline: **Current Process → AI Interventions → Future Process**.

---

## 🎯 Challenge Alignment (Grading Checklist)

This project strictly adheres to the mandatory technical rules of the challenge:

- [x] **Built from Scratch:** The entire FastAPI backend and Vanilla JS/Tailwind CSS frontend were custom-engineered.
- [x] **Free / Local Runnable:** Built using standard open-source Python libraries, local JSON persistence, and the free-tier Groq API (`llama-3.1-8b-instant`). No paid software licenses are required.
- [x] **Full-Stack Architecture:** Implements a decoupled frontend UI, a FastAPI web server, a Pydantic validation layer, an LLM orchestration pipeline, and local persistence.
- [x] **Data Persistence:** Uses a structured database (`processes.json`). Restarting the application preserves all historical architectures.
- [x] **Structured Reasoning:** The LLM is forced via Pydantic schemas to output valid JSON containing Activities, Problems, AI Opportunities, Division of Labor, and Expected ROI metrics.
- [x] **Processes Multiple Records:** Supports generating, storing, browsing, and filtering an arbitrary number of process models.
- [x] **Queryable Components:** Supports complex filtering (e.g., searching by human roles or legacy systems) directly from the UI and backend routes.
- [x] **Traceability:** Features a "View AI Reasoning" inspector that exposes the raw LLM transcript/JSON payload to prove outputs are generated dynamically.
- [x] **Visual Comparison:** Renders a 3-column comparative view (Current State [Red], AI Interventions [Yellow], Future State [Green]).

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, Vanilla JavaScript (ES6+), Tailwind CSS (via CDN) |
| **Backend** | Python 3.8+, FastAPI, Uvicorn (ASGI server) |
| **Data Validation & Schemas** | Pydantic v2 |
| **Database & Persistence** | File-based JSON document store (`processes.json`) via a custom DAO pattern |
| **AI Engine & Inference** | Groq API leveraging `llama-3.1-8b-instant` for low-latency structured JSON generation |

---

## 🏗️ System Architecture

```text
[ User Interface ]  ---> (HTTP POST /api/analyze) ---> [ FastAPI Backend ]
  (HTML5 / Tailwind)                                          |
          ^                                                   v
          |                                        [ Pydantic Schema Engine ]
          |                                                   |
          |                                                   v
          |                                        [ Groq AI Inference Layer ]
          |                                        (llama-3.1-8b-instant)
          |                                                   |
          |                                                   v
  [ Visual Dashboard ] <--- (Validated JSON) <--- [ Local DB (processes.json) ]
```

---

## 🚀 Setup & Installation Instructions

### 1. Prerequisites

- **Python:** Version 3.8 or higher.
- **Groq API Key:** Obtain a free key from the [Groq Console](https://console.groq.com).

### 2. Environment Setup

Clone or download the project files into your working directory and set up your virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment

# On Linux/macOS:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install required dependencies
pip install fastapi uvicorn pydantic groq
```

### 3. Environment Variable Configuration

Set your Groq API key in your terminal session prior to starting the backend:

**Linux / macOS:**
```bash
export GROQ_API_KEY="gsk_your_actual_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="gsk_your_actual_api_key_here"
```

### 4. Running the Backend Server

Start the FastAPI backend with hot-reloading enabled:

```bash
uvicorn main:app --reload --port 8000
```

The server will run on [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Launching the Frontend Application

You can access the UI in one of two ways:

- **Direct Browser Execution:** Double-click the `index.html` file to open it directly in Chrome, Edge, or Firefox.
- **Local HTTP Server (Recommended):** Open a second terminal window in the frontend directory and run:

```bash
python -m http.server 3000
```

Navigate to [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📡 API Documentation

FastAPI provides an interactive OpenAPI (Swagger) document at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Below are the core endpoints:

### 1. Generate Process Transformation

**Endpoint:** `POST /api/analyze`

**Description:** Accepts a business process name, invokes Groq for structured reasoning, persists the result, and returns the process model.

**Request Body:**
```json
{
  "process_name": "Accounts Payable Invoice Processing",
  "industry": "Finance"
}
```

**Response:** `200 OK` — Returns a complete `ProcessModel` object containing `current_state`, `ai_opportunities`, `future_state`, and `expected_benefits`.

### 2. Retrieve All Processes

**Endpoint:** `GET /api/processes`

**Description:** Returns an array of all historical process models stored in `processes.json`.

### 3. Search / Query Processes

**Endpoint:** `GET /api/processes/search`

**Query Parameters:**

| Parameter | Type | Description |
|---|---|---|
| `role` | string (optional) | Filter processes containing a specific role (e.g., Clerk, Manager) |
| `system` | string (optional) | Filter processes utilizing a specific tool or ERP (e.g., SAP, Excel) |

**Example:** `GET /api/processes/search?role=Manager`

### 4. Get Process Details by ID

**Endpoint:** `GET /api/processes/{process_id}`

**Description:** Retrieves a single process by its UUID string.

### 5. Delete Process

**Endpoint:** `DELETE /api/processes/{process_id}`

**Description:** Deletes a process entry from the JSON database by ID.

---

## ⚠️ Important Warnings & Troubleshooting

### 1. Missing API Key (`GROQ_API_KEY`)

**Symptom:** Backend returns `HTTP 500 Internal Server Error` when generating a process.

**Fix:** Verify that `GROQ_API_KEY` is exported in the exact terminal session running Uvicorn. If using an IDE (e.g., VS Code or PyCharm), configure the environment variable in your launch settings.

### 2. Rate Limits & Free-Tier Quotas

**Symptom:** `429 Too Many Requests` error from Groq.

**Fix:** The free tier of Groq has a rate limit per minute (RPM) and tokens per minute (TPM). Wait 60 seconds before making additional process generation calls, or switch models in `llm_service.py` to `llama3-8b-8192`.

### 3. File Permissions for Local Database

**Symptom:** `PermissionDeniedError` or failure to write to `processes.json`.

**Fix:** Ensure the backend directory has write permissions. If `processes.json` becomes corrupted, delete the file; the application will automatically create a clean `[]` database on the next request.

### 4. CORS Issues in Production

**Symptom:** Browser console displays "Blocked by CORS Policy."

**Fix:** In `main.py`, `CORSMiddleware` is set to `allow_origins=["*"]` for ease of local testing. In production environments, replace `*` with your frontend domain URL.

---

## 🛡️ Service Fallback Strategy

**What happens if Groq becomes paid or unavailable?**

The architecture is strictly decoupled and vendor-agnostic. Because the LLM service utilizes standard JSON schemas, the backend can be migrated to a local, open-source model without changing any frontend or business logic:

1. Install Ollama or vLLM locally.
2. Download an open-source model: `ollama pull llama3:8b`.
3. Update `llm_service.py` to target `http://localhost:11434/v1` instead of Groq's endpoint.

---

## 📁 Repository File Structure

```text
├── main.py              # FastAPI Web Application & API Route Controllers
├── models.py             # Pydantic Schemas & Data Validation Layer
├── db.py                 # Persistence Handler (DAO for processes.json)
├── llm_service.py         # Groq AI Orchestration & System Prompt Logic
├── index.html             # Full Interactive Dashboard (Tailwind CSS + ES6 JS)
├── processes.json         # Local JSON Database (Auto-generated)
└── requirements.txt        # Python Dependencies List
```# Assignment-3-AI-Future-Process-Designer
