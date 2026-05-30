# Box AI Pre-Screen Lambda

Two-stage pipeline: **Box AI** pre-screens documents → **Bedrock Claude** generates the final grounded answer.

## Architecture

```
User Question
     │
     ▼
Box Search (find relevant files in folder)
     │
     ▼
Box AI Ask (extract relevant passages)
     │
     ▼
Bedrock Claude (final answer + citations)
     │
     ▼
Grounded Response with Sources
```

## Why Pre-Screen?

- **Reduces noise** — only relevant excerpts reach Bedrock
- **Lowers cost** — fewer tokens sent to the model
- **Better accuracy** — focused context instead of raw full documents
- **Source tracking** — file metadata preserved through both stages

## Deploy

```bash
cd lambda
sam build
sam deploy --guided
```

## Test Locally

```bash
sam local invoke BoxAiPrescreenFunction -e event.json
```

## Request Format

```json
{
  "question": "What does the law say about public records?",
  "folder_id": "123456789",
  "history": []
}
```

## Response Format

```json
{
  "answer": "According to RCW 42.56...",
  "sources": [
    {"source_title": "RCW_42_56.txt", "text": "...", "source_url": ""}
  ]
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BOX_ACCESS_TOKEN` | Developer token (testing) |
| `BOX_JWT_CONFIG` | JWT config JSON (production) |
| `BOX_FOLDER_ID` | Default folder to search |
| `BEDROCK_REGION` | AWS region for Bedrock |
| `BEDROCK_MODEL_ID` | Claude model ID |
