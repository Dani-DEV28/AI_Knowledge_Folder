# AI Knowledge Folder

> Build trusted AI assistants from Box folders, websites, and documents.

AI Knowledge Folder is a framework for creating domain-specific AI assistants powered by content stored in Box.

Instead of relying on general-purpose AI knowledge, AI Knowledge Folder grounds responses in curated documents, uploaded files, and web content collected through Apify.

The platform enables administrators to create specialized AI assistants without building a custom RAG application for every use case.

**RCW Navigator AI** serves as the MVP demonstration of the platform, showing how an AI assistant can answer questions about Washington State RCW laws using only trusted source documents.

---

# Vision

Organizations already store knowledge in documents.

The challenge is making that knowledge searchable, discoverable, and conversational.

AI Knowledge Folder transforms a Box folder into an AI-powered knowledge assistant that can:

* Answer questions
* Cite sources
* Search uploaded documents
* Search scraped websites
* Stay grounded in trusted content
* Be configured for different domains

Examples:

* RCW Navigator AI
* HR Policy Assistant
* Product Documentation Assistant
* Compliance Navigator
* Internal Knowledge Bot
* Legal Research Assistant

---

# Problem

Organizations struggle to find information buried across:

* PDFs
* Internal documents
* Policy manuals
* Knowledge bases
* Public websites
* Reference materials

Traditional search requires users to know:

* Exact keywords
* File names
* Document locations

General-purpose AI can answer questions, but often lacks access to organization-specific content.

---

# Solution

AI Knowledge Folder allows administrators to create AI assistants backed by trusted content.

The platform supports two primary content sources:

## Website Content

Administrators can provide URLs.

Apify Actors:

* Crawl websites
* Extract text
* Normalize content
* Save results into Box

## Uploaded Documents

Administrators can upload:

* PDFs
* Word documents
* Text files
* JSON files
* Knowledge exports

The files become part of the assistant's searchable knowledge base.

---

# Platform Architecture

```text
                Admin Portal
                      |
         +------------+------------+
         |                         |
         v                         v
   Website URLs           Document Uploads
         |                         |
         v                         v
      Apify                    Box Storage
         |                         |
         +------------+------------+
                      |
                      v
            AI Knowledge Folder
                      |
             Search & Retrieval
                      |
                      v
                AI Assistant
                      |
                      v
            Answer + Citations
```

---

# Core Platform Features

## Knowledge Folder Creation

Administrators can create a new AI assistant.

Example:

```text
Assistant Name:
RCW Navigator AI

Description:
Washington State law assistant

Knowledge Folder:
box://rcw-laws
```

---

## Website Ingestion

Administrators provide one or more URLs.

Example:

```text
https://app.leg.wa.gov/rcw
https://agency.example.gov/policies
```

The platform uses Apify to:

* Crawl pages
* Extract content
* Store results in Box
* Associate content with the assistant

---

## Document Upload

Administrators can upload:

* PDFs
* DOCX
* TXT
* JSON

The uploaded files become searchable knowledge sources.

---

## AI Chat Interface

Users ask questions naturally.

Example:

```text
What does the policy say about remote work?

How many vacation days do employees receive?

What does Washington law say about public records?
```

The assistant searches only its assigned knowledge folder.

---

## Source Citations

Every answer includes supporting sources.

Example:

```text
Answer:
Employees may work remotely up to three days per week.

Sources:
Employee Handbook.pdf
Page 12
```

The system avoids unsupported answers.

---

## Grounded Responses

If information cannot be found:

```text
I could not find information related to that question in the selected knowledge folder.
```

This prevents hallucinated responses.

---

# Admin Portal

The Admin Portal is the primary MVP feature.

Administrators can:

## Create Assistants

```text
+ New Assistant
```

Example:

```text
RCW Navigator AI
```

---

## Configure Data Sources

### Add Website

```text
https://app.leg.wa.gov/rcw
```

Trigger:

```text
Run Apify Crawl
```

---

### Upload Documents

Drag-and-drop support for:

```text
PDF
DOCX
TXT
JSON
```

Uploaded files are stored directly in Box.

---

## Manage Knowledge Sources

View:

* Uploaded files
* Scraped pages
* Crawl status
* Last update time

---

# Demo Implementation: RCW Navigator AI

RCW Navigator AI demonstrates how the platform can create a legal research assistant.

The assistant is configured using:

## Website Sources

```text
https://app.leg.wa.gov/rcw
```

Selected RCW chapters:

* Traffic laws
* Consumer protection
* Public records

---

## Uploaded Sources

Optional:

* Legal memos
* Research notes
* Internal reference documents

---

## Example Questions

```text
Do drivers have to obey police officers?

What does Washington law say about commercial text messages?

What section discusses public records?

Where is this requirement found in the RCW?
```

---

## Example Response

```text
Question:
Do drivers have to obey police officers directing traffic?

Answer:
Washington traffic laws include provisions requiring drivers to comply with lawful directions provided by authorized officers directing traffic.

Source:
RCW 46.61
https://app.leg.wa.gov/rcw
```

---

## Legal Disclaimer

RCW Navigator AI summarizes public legal information and is intended for educational purposes only.

It does not provide legal advice.

---

# Technology Stack

## Box

Acts as the system of record.

Responsibilities:

* Knowledge folder storage
* Uploaded document management
* Assistant content repository

---

## Apify

Responsible for:

* Website crawling
* Content extraction
* Data collection
* Scheduled updates

---

## AWS Bedrock

Provides:

* Question answering
* Summarization
* Citation-aware responses
* Grounded generation

---

## AWS Kiro

Accelerates development through:

* Project scaffolding
* API generation
* Workflow creation
* Documentation generation
* Testing support

---

## AWS Lambda

Handles:

* Ingestion workflows
* File processing
* Assistant orchestration
* Scheduled updates

---

# MVP Scope (5-Hour Hackathon)

## Primary Goal

Build the AI Knowledge Folder platform.

---

## MVP Features

### Admin Portal

* Create assistant
* Add website URLs
* Upload documents
* View knowledge sources

### Knowledge Ingestion

* Crawl websites with Apify
* Upload files to Box
* Store metadata

### AI Assistant

* Ask questions
* Retrieve relevant content
* Generate source-backed answers
* Display citations

### Demo Assistant

* RCW Navigator AI

---

## Out of Scope

* User authentication
* Multi-tenant support
* Large-scale crawling
* Fine-tuning models
* Complex permissions
* Advanced analytics

---

# Future Enhancements

* Multiple AI assistants
* Assistant templates
* Scheduled recrawling
* Semantic search with embeddings
* Box metadata integration
* Role-based access control
* Confidence scoring
* Highlighted source excerpts
* Exportable reports
* Chat history
* Assistant marketplace

---

# Why This Project Matters

Most AI assistants are built for a single purpose.

AI Knowledge Folder provides a reusable framework for creating many assistants from the same platform.

RCW Navigator AI demonstrates one implementation, but the same architecture can power:

* Legal assistants
* HR assistants
* Compliance assistants
* Product documentation assistants
* Internal knowledge bots

The result is a scalable platform that transforms Box folders into trusted, source-backed AI assistants.
