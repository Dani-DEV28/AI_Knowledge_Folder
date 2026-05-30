import httpx
import os
import re
from db.metadata import save_source, get_assistant
from services.box_service import upload_file_to_box

# playwright-scraper is a free public actor available on all Apify plans
ACTOR_ID = "apify~playwright-scraper"


async def trigger_crawl(url: str, assistant_id: str) -> dict:
    """
    Trigger an Apify crawl, poll until complete, then auto-ingest results.
    Returns final ingestion result with pages_ingested count.
    """
    token = os.getenv("APIFY_API_TOKEN", "")
    if not token:
        raise ValueError("APIFY_API_TOKEN is not set in .env")

    endpoint = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "startUrls": [{"url": url}],
        "maxPagesPerCrawl": 1,
        "pageFunction": (
            "async function pageFunction({ page, request }) {"
            "  const title = await page.title();"
            "  const text = await page.evaluate(() => document.body.innerText);"
            "  return { url: request.url, title, text: text.slice(0, 8000) };"
            "}"
        ),
    }

    # Start the crawl
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(endpoint, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    run_id = data.get("data", {}).get("id", "unknown")

    save_source(
        assistant_id=assistant_id,
        file_name=url,
        source_type="website",
        source_url=url,
        box_file_id=None,
    )

    # Poll until done (max 5 minutes, check every 10 seconds)
    import asyncio
    for _ in range(30):
        await asyncio.sleep(10)
        status = await fetch_run_status(run_id)
        if status == "SUCCEEDED":
            result = await ingest_run_results(run_id, assistant_id)
            return {**result, "run_id": run_id, "url": url}
        elif status in ("FAILED", "TIMED-OUT", "ABORTED"):
            return {"status": status, "run_id": run_id, "url": url, "pages_ingested": 0}

    # Timed out waiting — return run_id so user can ingest manually later
    return {"status": "crawl_started", "run_id": run_id, "url": url, "pages_ingested": 0}


async def fetch_run_status(run_id: str) -> str:
    """
    Check the status of an Apify run.
    Returns: READY, RUNNING, SUCCEEDED, FAILED, TIMED-OUT, ABORTED
    """
    token = os.getenv("APIFY_API_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(
            f"https://api.apify.com/v2/actor-runs/{run_id}",
            headers=headers,
        )
        resp.raise_for_status()
        return resp.json().get("data", {}).get("status", "UNKNOWN")


async def ingest_run_results(run_id: str, assistant_id: str) -> dict:
    """
    Fetch completed Apify run results, save each page as a .txt file
    in crawled/<assistant_id>/, upload to Box, and make available for retrieval.
    """
    token = os.getenv("APIFY_API_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"}

    # Check run status first
    status = await fetch_run_status(run_id)
    if status != "SUCCEEDED":
        return {
            "status": status,
            "message": f"Run is not complete yet. Current status: {status}",
            "pages_ingested": 0,
        }

    # Fetch dataset items
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items?format=json&limit=50",
            headers=headers,
        )
        resp.raise_for_status()
        items = resp.json()

    if not items:
        return {
            "status": "empty",
            "message": "Crawl completed but no pages were extracted.",
            "pages_ingested": 0,
        }

    # Save each page as a .txt file and upload to Box
    assistant = get_assistant(assistant_id)
    folder_name = assistant["folder_name"] if assistant else assistant_id

    pages_ingested = 0
    for item in items:
        page_url = item.get("url", "unknown")
        title = item.get("title", "Untitled").strip()
        text = item.get("text", "").strip()

        if not text:
            continue

        # Safe filename from URL
        safe_name = re.sub(r"[^\w\-]", "_", page_url)[:80]
        filename = f"{safe_name}.txt"
        content = f"{title}\nSource: {page_url}\n\n{text}"

        # Upload to Box (source of truth)
        box_file_id = None
        try:
            box_file_id = upload_file_to_box(filename, content.encode("utf-8"), folder_name)
        except Exception:
            pass

        save_source(
            assistant_id=assistant_id,
            file_name=filename,
            source_type="crawled",
            source_url=page_url,
            box_file_id=box_file_id,
        )
        pages_ingested += 1

    return {
        "status": "ingested",
        "run_id": run_id,
        "pages_ingested": pages_ingested,
        "assistant_id": assistant_id,
    }
