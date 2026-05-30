import httpx
import os
from db.metadata import save_source

# playwright-scraper is a free public actor available on all Apify plans
ACTOR_ID = "apify~playwright-scraper"


async def trigger_crawl(url: str, assistant_id: str) -> dict:
    """
    Trigger an Apify crawl for the given URL using playwright-scraper (free).
    Extracts page URL, title, and body text.
    Token is passed via Authorization header (not in the URL).
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
        "maxPagesPerCrawl": 10,
        "pageFunction": (
            "async function pageFunction({ page, request }) {"
            "  const title = await page.title();"
            "  const text = await page.evaluate(() => document.body.innerText);"
            "  return { url: request.url, title, text: text.slice(0, 5000) };"
            "}"
        ),
    }

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

    return {"status": "crawl_started", "run_id": run_id, "url": url}
