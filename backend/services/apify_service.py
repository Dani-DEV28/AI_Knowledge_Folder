import httpx
import os
from db.metadata import save_source

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

# Using the built-in Apify web-scraper actor
ACTOR_ID = "apify~web-scraper"


async def trigger_crawl(url: str, assistant_id: str) -> dict:
    """
    Trigger an Apify crawl for the given URL.
    Saves the source record to metadata and returns the run ID and status.

    The actor extracts: page URL, title, and body text.
    Results are stored in Apify's dataset — fetch them later via the Apify API
    and upload to Box once the run completes.
    """
    endpoint = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"

    payload = {
        "startUrls": [{"url": url}],
        "maxPagesPerCrawl": 20,
        "pageFunction": (
            "async function pageFunction(context) {"
            "  return {"
            "    url: context.request.url,"
            "    title: document.title,"
            "    text: document.body.innerText"
            "  };"
            "}"
        ),
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(endpoint, json=payload)
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

    return {"status": "crawl_started", "run_id": run_id, "url": url}
