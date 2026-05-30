from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import assistants, sources, chat

app = FastAPI(title="AI Knowledge Folder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistants.router)
app.include_router(sources.router)
app.include_router(chat.router)


@app.get("/health")
def health():
    return {"status": "ok"}
