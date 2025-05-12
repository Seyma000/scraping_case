import asyncio
from playwright.async_api import async_playwright

async def sniff_api_calls():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        async def log_request(request):
            if "search" in request.url and request.method == "GET":
                print(f"🔎 Captured URL: {request.url}")

        page.on("request", log_request)
        await page.goto("https://thedyrt.com/search")

        print("Move your mouse on the map to trigger API calls...")
        await page.wait_for_timeout(15000)  # Wait 15 seconds to manually interact

        await browser.close()

if __name__ == "__main__":
    asyncio.run(sniff_api_calls())