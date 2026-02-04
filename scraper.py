import asyncio
import os
import httpx
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # DEBUG: This will tell us if the keys are missing without crashing
    if not token or not chat_id:
        print("❌ ERROR: Telegram secrets are NOT found in the environment!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": message})
        print("✅ Telegram message sent!")

async def check_price():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await stealth_async(page)
            
            print("🔗 Visiting website...")
            await page.goto("https://www.google.com", wait_until="networkidle")
            
            # Save screenshot early so we have it for debugging
            await page.screenshot(path="last_check.png")
            print("📸 Screenshot saved as last_check.png")
            
            # Simulated drop
            await send_telegram_msg("🚀 AI is online and tracking your holiday!")
            await browser.close()
    except Exception as e:
        print(f"❌ SCRAPER CRASHED: {e}")
        # Create a dummy file so the 'Upload' step doesn't fail
        with open("last_check.png", "w") as f: f.write("error")
        exit(1)

if __name__ == "__main__":
    asyncio.run(check_price())