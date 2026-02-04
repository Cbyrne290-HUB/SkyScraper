import asyncio
import os
import sys

# logical check to ensure libraries are installed
try:
    import httpx
    from playwright.async_api import async_playwright
    from playwright_stealth import stealth_async
except ImportError as e:
    print(f"❌ CRITICAL ERROR: Library missing! {e}")
    print("Did you update requirements.txt?")
    sys.exit(1)

async def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("❌ ERROR: Telegram secrets are NOT found in the environment!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json={"chat_id": chat_id, "text": message})
            print("✅ Telegram message sent!")
        except Exception as e:
            print(f"❌ Failed to send Telegram: {e}")

async def check_price():
    print("🚀 Starting Scraper...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await stealth_async(page)
            
            print("🔗 Visiting Google (Test)...")
            await page.goto("https://www.google.com", wait_until="networkidle")
            
            # Save screenshot early so we have it for debugging
            await page.screenshot(path="last_check.png")
            print("📸 Screenshot saved as last_check.png")
            
            # Send Test Message
            await send_telegram_msg("🚀 AI is online and tracking your holiday!")
            await browser.close()
            
    except Exception as e:
        print(f"❌ SCRAPER CRASHED: {e}")
        # Create a dummy image file so the GitHub Action step doesn't fail
        with open("last_check.png", "w") as f: 
            f.write("error_log")
        # We still exit with error code 1 so you see the Red Cross in GitHub
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(check_price())