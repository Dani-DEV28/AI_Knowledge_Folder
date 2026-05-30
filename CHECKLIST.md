# AI Knowledge Folder — Presentation Checklist

> 3-minute demo reference. All MVP features are implemented.

---

## What It Is (30 sec)

- A platform that turns Box folders into trusted, source-backed AI assistants
- Demo: **RCW Navigator AI** — answers questions about Washington State law
- No hallucination — answers grounded in uploaded documents and crawled websites

---

## Tech Stack (15 sec)

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16 + Bootstrap + Tailwind |
| Backend | FastAPI (Python) |
| AI | AWS Bedrock (Claude Haiku) with local fallback |
| Storage | Box (SDK Gen) |
| Crawling | Apify (Playwright Scraper) |
| OCR | AWS Textract (scanned PDFs) |

---

## Completed Features

### Admin Portal ✅

- [x] Create new AI assistants (name, description, folder)
- [x] Add website URLs for crawling
- [x] Upload documents (PDF, TXT, JSON)
- [x] View/manage knowledge sources per assistant
- [x] Delete sources (removes from Box + metadata)
- [x] Agent Manager UI with collapsible URL/Files sections

### Knowledge Ingestion ✅

- [x] Apify crawl triggered from UI → polls until done → auto-ingests
- [x] Manual ingest endpoint for completed runs
- [x] File upload → text extraction → upload to Box
- [x] PDF extraction: pdfplumber → PyPDF2 → Textract OCR fallback chain
- [x] TXT and JSON direct extraction
- [x] Crawled pages saved as .txt in Box with source URL metadata

### AI Chat ✅

- [x] Natural language question input
- [x] Keyword-based retrieval from Box folder + local seed files
- [x] AWS Bedrock Claude for grounded answer generation
- [x] Local fallback when Bedrock credentials unavailable
- [x] Source citations displayed with every answer
- [x] Grounded responses — refuses to answer if no sources found
- [x] Conversation history support (last 10 messages sent to model)

### Demo Assistant ✅

- [x] RCW Navigator AI pre-configured as default assistant
- [x] Seed directory support for pre-loaded content

### Frontend UI ✅

- [x] Chat window with message bubbles (user/assistant)
- [x] Sidebar with agent selector, chat history, admin panel
- [x] Agent Manager view (add URLs with scrape prompt, upload files)
- [x] Mobile-responsive sidebar (overlay + backdrop)
- [x] New chat creation
- [x] Source citations shown inline below answers
- [x] Error handling for backend connectivity

### Backend API ✅

- [x] `POST /assistants` — create assistant
- [x] `POST /chat` — ask question, get grounded answer
- [x] `POST /sources/website` — trigger Apify crawl + auto-ingest
- [x] `POST /sources/website/ingest/{run_id}` — manual ingest
- [x] `POST /sources/upload` — upload document
- [x] `GET /sources?assistant_id=` — list sources
- [x] `DELETE /sources/{id}` — delete source
- [x] `GET /health` — health check
- [x] CORS enabled for frontend

### Infrastructure ✅

- [x] Environment variable configuration (.env.example documented)
- [x] JSON file-based metadata store (no database dependency)
- [x] Git repository with proper .gitignore
- [x] Requirements.txt with pinned dependencies
- [x] Jest test setup for frontend

---

## Key Talking Points

1. **Problem**: Knowledge buried in PDFs, websites, internal docs — hard to search
2. **Solution**: Box folder → AI assistant in minutes, no custom RAG per use case
3. **Architecture**: Admin adds sources → Apify crawls / Box stores → Retrieval + Bedrock answers with citations
4. **Grounding**: Never hallucinates — if it can't find it in sources, it says so
5. **Reusable**: Same platform powers legal, HR, compliance, product docs assistants
6. **Built with**: AWS Kiro for accelerated development

---

## Out of Scope (by design)

- User authentication
- Multi-tenant support
- Large-scale crawling
- Fine-tuning models
- Complex permissions
- Advanced analytics

---

## How to Run

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in credentials
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```
