# RCW Navigator AI

**RCW Navigator AI** is an AI-powered knowledge folder that lets users ask natural-language questions about selected Washington State RCW laws and receive answers sourced from official RCW documents.

Instead of manually opening multiple legal pages and using `Ctrl + F`, users can ask questions like:

* “Do drivers have to obey a police officer directing traffic?”
* “What does Washington law say about commercial text messages?”
* “What section talks about public records?”
* “Where is this rule mentioned in the RCW?”

The app searches a limited knowledge folder, retrieves the most relevant RCW text, and generates a short answer with source references.

> **Disclaimer:** RCW Navigator AI summarizes public legal information. It is not legal advice.

---

## Project Overview

RCW Navigator AI is built around the idea of an **AI Knowledge Folder**.

The system collects public Washington State RCW pages, stores them in a Box folder, and allows users to ask questions against only those stored documents. This keeps the AI grounded in a limited and trusted knowledge base instead of answering from general internet knowledge.

---

## Problem

Legal information is public, but it can be hard to search and understand quickly.

Users often need to:

* Find the right RCW section
* Understand what a law says in simple language
* Search across multiple RCW pages
* Keep track of where an answer came from

Traditional keyword search is useful, but it requires knowing the exact words to search for. RCW Navigator AI allows users to ask questions naturally and receive sourced answers.

---

## Solution

RCW Navigator AI provides a simple question-answering tool for Washington RCW documents.

The user asks a question, and the app:

1. Searches the Box knowledge folder
2. Finds the most relevant RCW document chunks
3. Generates a short AI answer
4. Shows the source RCW section, title, and URL
5. Refuses to answer when the information is not found in the selected documents

---

## Example Use Cases

### Traffic Law Search

User asks:

> Do drivers have to obey police officers?

The app searches the stored RCW traffic law documents and returns a short answer with the relevant RCW source.

### Consumer Protection Search

User asks:

> Can a business send commercial text messages to Washington residents?

The app retrieves the relevant RCW section and summarizes the rule.

### Public Records Search

User asks:

> What does the RCW say about public records?

The app searches the selected public records documents and returns a sourced answer.

---

## Key Features

* Natural-language search over RCW documents
* Answers grounded only in selected source files
* Source citations with RCW section numbers and URLs
* Box folder used as the knowledge base
* Apify used to collect public RCW pages
* Simple web interface for asking questions
* “I could not find that in the documents” response when no source is available
* Legal disclaimer included in the answer flow

---

## Tech Stack

* **Apify** — Scrapes public RCW pages and extracts text
* **Box.dev** — Stores scraped RCW documents in a secure knowledge folder
* **AWS Kiro** — Helps generate, organize, and build the application workflow
* **Python / JavaScript** — Backend and frontend logic
* **AI Model** — Generates answers from retrieved RCW text
* **JSON / TXT Files** — Stored RCW document format

---

## How It Works

```text
Public RCW Website
        ↓
Apify Actor
        ↓
Extracted RCW Text
        ↓
Box Knowledge Folder
        ↓
Search / Retrieval Layer
        ↓
AI Answer Generator
        ↓
Answer + Source Citation
```

---

## Data Flow

1. **Scrape RCW Pages**

   Apify collects selected RCW pages such as traffic laws, consumer protection rules, or public records laws.

2. **Store in Box**

   The scraped content is saved in a Box folder as text or JSON files.

3. **Ask a Question**

   The user enters a natural-language question in the app.

4. **Retrieve Relevant Text**

   The app searches the stored RCW files and selects the most relevant chunks.

5. **Generate an Answer**

   The AI generates a short answer based only on the retrieved source text.

6. **Show Sources**

   The app displays the RCW citation, document title, and original source URL.

---

## Example Folder Structure

```text
boxbrain-rcw-demo/
├── rcw_46_61_rules_of_the_road.json
├── rcw_46_61_020.txt
├── rcw_19_190_060_commercial_text_messages.txt
├── rcw_42_56_public_records_act.json
└── demo_questions.json
```

---

## Example Scraped Document Format

```json
{
  "title": "RCW 46.61.020",
  "section": "Refusal to give information to or cooperate with officer",
  "chapter": "Chapter 46.61 RCW",
  "source_url": "https://app.leg.wa.gov/rcw/default.aspx?cite=46.61.020",
  "text": "Full extracted RCW text goes here...",
  "scraped_at": "2026-05-29"
}
```

---

## Example Questions

```text
What does the RCW say about obeying police officers?
Can businesses send commercial texts to Washington residents?
What is the Public Records Act?
Which RCW section talks about rules of the road?
What does Washington law say about refusing to cooperate with an officer?
```

---

## Example Answer Format

```text
Question:
Do drivers have to obey police officers?

Answer:
Washington law includes rules requiring drivers to cooperate with law enforcement officers in traffic-related situations. The exact requirement depends on the specific RCW section and context.

Source:
RCW 46.61.020 — Refusal to give information to or cooperate with officer
https://app.leg.wa.gov/rcw/default.aspx?cite=46.61.020

Disclaimer:
This is a summary of public legal information and is not legal advice.
```

---

## 5-Hour MVP Scope

The goal of the first version is to build a simple but working demo.

### MVP Features

* Scrape 10–30 selected RCW pages
* Save scraped pages to Box
* Display a simple question input
* Search stored RCW files
* Generate an answer from the retrieved content
* Show source citation
* Include legal disclaimer

### Out of Scope for MVP

* Scraping the entire RCW website
* User authentication
* Advanced legal reasoning
* Legal recommendations
* Real-time law updates
* Production-grade compliance review

---

## Recommended Demo Dataset

For a quick demo, use a small set of RCW topics:

### Traffic Laws

* Chapter 46.61 RCW — Rules of the Road
* Useful for questions about driving, officers, road signs, and traffic rules

### Consumer Protection

* RCW 19.190.060 — Commercial electronic text messages
* Useful for questions about business texting rules

### Public Records

* Chapter 42.56 RCW — Public Records Act
* Useful for questions about public records and disclosure

---

## Team Roles

### Person 1 — Data Pipeline

Responsible for:

* Setting up the Apify actor
* Scraping selected RCW pages
* Cleaning extracted text
* Saving output as JSON or TXT
* Uploading files to Box

### Person 2 — App + AI Layer

Responsible for:

* Building the simple frontend
* Connecting to Box files
* Implementing search/retrieval
* Sending relevant chunks to the AI model
* Displaying answers and sources

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rcw-navigator-ai.git
cd rcw-navigator-ai
```

### 2. Create Environment File

Create a `.env` file:

```env
BOX_CLIENT_ID=your_box_client_id
BOX_CLIENT_SECRET=your_box_client_secret
BOX_DEVELOPER_TOKEN=your_box_developer_token
BOX_FOLDER_ID=your_box_folder_id

APIFY_TOKEN=your_apify_token
AI_API_KEY=your_ai_api_key
```

### 3. Install Dependencies

Example for a Python backend:

```bash
pip install -r requirements.txt
```

Example for a JavaScript frontend:

```bash
npm install
```

### 4. Run the App

```bash
npm run dev
```

or:

```bash
python app.py
```

---

## Possible API Routes

```text
GET /files
Returns files from the selected Box folder.

POST /ask
Accepts a user question and returns an AI answer with sources.

POST /scrape
Runs or triggers an Apify actor for selected RCW URLs.

POST /upload
Uploads scraped RCW files to Box.
```

---

## Example `/ask` Request

```json
{
  "question": "Can businesses send commercial texts to Washington residents?"
}
```

---

## Example `/ask` Response

```json
{
  "answer": "Washington law restricts businesses from sending certain commercial electronic text messages to Washington residents.",
  "sources": [
    {
      "title": "RCW 19.190.060",
      "url": "https://app.leg.wa.gov/rcw/default.aspx?cite=19.190.060"
    }
  ],
  "disclaimer": "This is a summary of public legal information and is not legal advice."
}
```

---

## Why This Project Matters

RCW Navigator AI shows how AI can make public information easier to search while still staying grounded in source documents.

This project is useful for:

* Citizens trying to understand public laws
* Students researching Washington law
* Legal support teams organizing reference documents
* Government or nonprofit teams creating internal knowledge tools
* Hackathon teams demonstrating source-backed AI search

---

## Future Improvements

* Add semantic search with embeddings
* Add Box metadata for RCW title, chapter, and section
* Add automatic update checks for changed RCW pages
* Add document upload support for custom legal files
* Add user authentication
* Add confidence scoring
* Add side-by-side source highlighting
* Add support for WAC documents
* Add export to PDF report
* Add chat history

---

## Legal Disclaimer

RCW Navigator AI is for informational and educational purposes only. It summarizes public legal text and provides source references, but it does not provide legal advice. Users should consult a licensed attorney or official government source for legal decisions.

---

## Project Pitch

RCW Navigator AI is a source-backed AI search tool for Washington State laws. It uses Apify to collect public RCW pages, Box.dev to store them in a knowledge folder, and AI to answer user questions only from those documents. The result is a lightweight legal knowledge assistant that feels like `Ctrl + F` across a law folder, but with natural-language answers and source citations.

