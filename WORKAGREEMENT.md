# WORKAGREEMENT.md

# AI Knowledge Folder — Work Agreement

## Project

**Project Name:** AI Knowledge Folder  
**Demo Assistant:** RCW Navigator AI  
**Goal:** Build a web app MVP that lets users create a trusted AI assistant backed by Box folders, uploaded documents, and crawled website content.

RCW Navigator AI will demonstrate the platform by answering questions about selected Washington State RCW law content using only trusted source documents and citations.

---

## Team Size

This project will be built by a team of **2 people**.

The most efficient split is:

- **Person 1:** Backend, ingestion, Box, Apify, retrieval, and AI grounding
- **Person 2:** Frontend, Admin Portal, chat UI, demo flow, and polish

---

## MVP Principle

The MVP must prove one main idea:

> A user can ask questions, and the AI answers only from trusted knowledge sources with citations.

The AI must not hallucinate. If the answer cannot be found in the selected knowledge folder, it must clearly say that the information was not found.

---

## Out of Scope

To stay focused during the 5-hour hackathon, the following features are out of scope:

- User authentication
- Multi-tenant support
- Large-scale crawling
- Fine-tuning models
- Complex permissions
- Advanced analytics
- Full semantic search with embeddings
- Chat history
- Role-based access control

---

# Roles and Responsibilities

## Person 1 — Backend, Ingestion, Box, Apify, and AI Grounding

### Main Responsibility

Person 1 is responsible for making the knowledge folder system actually work.

This includes:

- Python backend
- Apify crawling
- Box storage
- Metadata handling
- Retrieval logic
- AI answer generation
- Citation enforcement
- Hallucination prevention

---

## Person 1 Tasks

### 1. Backend API

Build the backend using **Python FastAPI** or Flask.

Required endpoints:

```text
POST /assistants
POST /sources/website
POST /sources/upload
GET /sources
POST /chat
```

### 2. Apify Integration

Person 1 will connect the backend to Apify.

Responsibilities:

- Accept a website URL from the frontend
- Trigger an Apify crawl
- Extract page title, URL, and text
- Normalize scraped text
- Save the result as `.json` or `.txt`
- Return crawl status to the frontend

Example website source:

```text
https://app.leg.wa.gov/rcw
```

### 3. Box Integration

Person 1 will connect the backend to Box.

Responsibilities:

- Create or use a Box folder for `RCW Navigator AI`
- Upload scraped website content into Box
- Upload user documents into Box
- Keep Box as the source of record for stored knowledge

### 4. Metadata Storage

Person 1 will store simple metadata locally using JSON, SQLite, or another fast option.

Metadata should include:

```text
assistant_name
file_name
source_type
source_url
box_file_id
created_at
last_updated
```

### 5. Retrieval Logic

For the hackathon MVP, retrieval should stay simple.

Recommended approach:

- Load text from crawled/uploaded files
- Split text into chunks
- Use keyword matching or basic scoring
- Return the top 3–5 relevant chunks
- Include source title and URL/file name with each chunk

Embeddings are optional and should only be added if the basic MVP is already working.

### 6. AI Answer Generation

Person 1 will connect the retrieved source chunks to the AI model.

The AI must follow this rule:

```text
Answer only using the provided source excerpts.
If the answer is not found in the excerpts, say:
"I could not find information related to that question in the selected knowledge folder."
Always include source citations.
Do not provide legal advice.
```

### 7. Demo Seed Data

Person 1 will prepare a small set of RCW content for the demo.

Recommended demo topics:

- Traffic laws
- Consumer protection
- Public records

Recommended demo questions:

```text
Do drivers have to obey police officers directing traffic?
What does Washington law say about public records?
Where is this requirement found in the RCW?
What does Washington law say about commercial text messages?
```

---

# Person 2 — Frontend, Admin Portal, Chat UI, and Demo Polish

## Main Responsibility

Person 2 is responsible for making the app usable, clear, and demo-ready.

This includes:

- Web frontend
- Admin Portal
- Knowledge source dashboard
- Chat interface
- Citation display
- Loading states
- Error states
- Demo script and presentation polish

---

## Person 2 Tasks

### 1. Web App Frontend

Build the frontend using one of the following:

- React
- Next.js
- Plain HTML/CSS/JavaScript

Recommended pages:

```text
Admin Portal
Knowledge Sources
Chat Interface
```

### 2. Admin Portal

The Admin Portal should allow users to create an assistant.

Fields:

```text
Assistant Name
Description
Knowledge Folder Name
```

Example:

```text
Assistant Name: RCW Navigator AI
Description: Washington State law assistant
Knowledge Folder: rcw-laws
```

### 3. Add Website Source UI

Build a form where the admin can enter a website URL.

Required fields and buttons:

```text
Website URL input
Run Apify Crawl button
Crawl status message
```

Example URL:

```text
https://app.leg.wa.gov/rcw
```

### 4. Upload Documents UI

Build a simple document upload form.

Supported file types:

```text
PDF
DOCX
TXT
JSON
```

For the MVP, PDF/DOCX parsing can be limited if needed. TXT and JSON support are enough for a strong demo if time is limited.

### 5. Knowledge Source Dashboard

Build a dashboard showing the assistant's knowledge sources.

Display:

```text
Uploaded files
Scraped pages
Source type
Crawl status
Last update time
```

### 6. Chat Interface

Build the user-facing chat page.

Required elements:

```text
Question input
Submit button
AI answer display
Sources section
Citation display
Unsupported-answer message
```

### 7. Citation Display

Every answer should show sources clearly.

Example:

```text
Sources:
- RCW 46.61
- https://app.leg.wa.gov/rcw
```

### 8. Legal Disclaimer

The RCW Navigator AI demo must include this disclaimer:

```text
RCW Navigator AI summarizes public legal information for educational purposes only. It does not provide legal advice.
```

### 9. Demo Flow and Presentation

Person 2 will prepare the demo script.

The demo should show:

1. Admin creates `RCW Navigator AI`
2. Admin adds the RCW website URL
3. Apify crawls selected content
4. Content is stored in Box
5. User asks a law question
6. AI answers with citations
7. User asks an unsupported question
8. AI refuses to guess

---

# Shared Responsibilities

Both team members are responsible for:

- Keeping the scope small
- Testing the app together
- Making sure the demo works
- Preparing backup screenshots
- Explaining the product clearly
- Making sure the AI does not hallucinate

---

# 5-Hour Timeline

## Hour 0–0.5 — Setup Together

Both people agree on:

```text
Project name: AI Knowledge Folder
Demo assistant: RCW Navigator AI
Backend: Python FastAPI
Frontend: React, Next.js, or plain HTML/JS
Storage: Box
Crawler: Apify
AI: AWS Bedrock or fallback LLM
```

Person 1 starts the backend skeleton.

Person 2 starts the frontend skeleton.

---

## Hour 0.5–2 — Build Core Separately

### Person 1

- Build `/sources/website`
- Connect Apify
- Save crawled result to Box
- Store metadata locally
- Start simple keyword retrieval

### Person 2

- Build Admin Portal
- Build source list page
- Build basic chat UI
- Add RCW Navigator branding
- Add legal disclaimer

---

## Hour 2–3.5 — Connect the System

### Person 1

- Finish `/chat`
- Add citation format
- Add unsupported-answer fallback
- Test with RCW data

### Person 2

- Connect frontend to backend
- Display AI answers
- Display citations
- Display crawl/upload status
- Add sample RCW questions

---

## Hour 3.5–4.5 — Demo Hardening

### Person 1

- Make hallucination prevention stricter
- Test unsupported questions
- Make sure retrieved chunks are passed correctly to the AI
- Add fallback response when no source matches

### Person 2

- Improve UI polish
- Add clean layout
- Add loading states
- Add error messages
- Add visible source section under every answer

---

## Hour 4.5–5 — Final Demo Prep

Together:

- Test one successful answer
- Test one unsupported question
- Test source citation display
- Test Box source listing
- Prepare a 2-minute pitch
- Prepare backup screenshots in case APIs fail

---

# Ownership Map

| Feature | Person 1 | Person 2 |
|---|---:|---:|
| FastAPI backend | Primary | Support |
| Apify crawl | Primary | — |
| Box upload/storage | Primary | — |
| Metadata storage | Primary | — |
| Retrieval/search | Primary | — |
| Bedrock/AI prompt | Primary | Support |
| Admin Portal UI | — | Primary |
| Upload/source forms | Support | Primary |
| Chat interface | Support | Primary |
| Citation display | Support | Primary |
| Demo script | Support | Primary |
| Final testing | Both | Both |

---

# MVP Priority Order

Build in this order:

1. Chat with hardcoded RCW sample text
2. Keyword retrieval with citations
3. Box upload/storage
4. Apify crawl
5. Admin Portal
6. Document upload
7. UI polish

This order is important because the demo depends most on proving trustworthy answers with citations.

Even if Apify or Box has issues, the team can still demo the core idea with preloaded RCW content.

---

# Definition of Done

The MVP is done when:

- A user can create or select `RCW Navigator AI`
- A website URL can be submitted
- At least one RCW source is stored or represented as a knowledge source
- A user can ask a question
- The backend retrieves relevant source text
- The AI answers using only retrieved content
- The answer includes citations
- Unsupported questions return a truthful “not found” response
- The UI shows sources clearly
- The legal disclaimer is visible

---

# Demo Pitch

AI Knowledge Folder turns a Box folder into a trusted AI assistant.

Instead of relying on general AI knowledge, the assistant only answers from approved documents and crawled websites. For this demo, RCW Navigator AI answers questions about Washington State RCW laws using selected RCW source content.

The key value is trust:

- The assistant searches only approved knowledge sources
- Every answer includes citations
- If the answer is not found, the assistant says so
- The same platform can later support HR policies, compliance documents, legal research, product documentation, and internal knowledge bases

---

# Backup Plan

If Apify takes too long:

- Use pre-scraped RCW text files
- Still show the Add Website UI
- Explain that Apify handles crawling in the full flow

If Box integration takes too long:

- Store files locally during the demo
- Keep the Box folder structure visible in the architecture
- Explain that Box is the system of record in production

If Bedrock setup takes too long:

- Use another LLM temporarily
- Keep the prompt grounded
- Make sure the answer uses only retrieved excerpts

If document parsing takes too long:

- Support TXT and JSON first
- Leave PDF/DOCX as visible upload types but mark them as future parsing support

---

# Final Agreement

Both team members agree to focus on a working demo over unnecessary complexity.

The project should prioritize:

1. Trusted answers
2. Clear citations
3. No hallucinations
4. Simple admin workflow
5. Clean demo experience

The team should avoid adding advanced features until the core MVP works end to end.
