import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def get_travel_price():
    async with async_playwright() as p:
        # Launch browser in 'headless' mode (hidden)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # This makes the AI look like a real human to avoid being blocked
        await stealth_async(page)
        
        # STEP: Put the URL of the holiday/flight you want to track here
        target_url = "https://www.google.com/travel/flights" 
        print(f"Checking price at: {target_url}")
        
        await page.goto(target_url, wait_until="networkidle")
        
        # For the POC, we just take a screenshot to prove the AI 'saw' the page
        await page.screenshot(path="last_check.png")
        print("Screenshot saved! The AI successfully reached the site.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_travel_price())