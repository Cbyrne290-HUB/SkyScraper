import asyncio
import os
import httpx
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def send_telegram_msg(message):
    """Sends a notification to your Telegram Bot."""
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Error: Telegram credentials missing in Environment Variables.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json={"chat_id": chat_id, "text": message})
            if response.status_code == 200:
                print("✅ Telegram alert sent successfully!")
            else:
                print(f"❌ Failed to send Telegram: {response.text}")
        except Exception as e:
            print(f"❌ Network error sending Telegram: {e}")

async def check_price():
    async with async_playwright() as p:
        # Launch browser hidden (headless)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Apply stealth to avoid bot detection
        await stealth_async(page)
        
        # TARGET DATA (Replace with real URL/Price later)
        target_url = "https://www.google.com/travel/flights"
        original_price = 1500
        current_found_price = 1400 # Simulated drop for the POC
        
        print(f"Checking price at: {target_url}")
        
        # For now, we just visit the page to prove it works
        await page.goto(target_url, wait_until="networkidle")
        await page.screenshot(path="last_check.png")
        
        # Logic to trigger the alert
        if current_found_price < original_price:
            savings = original_price - current_found_price
            msg = (f"🚨 PRICE DROP ALERT!\n\n"
                   f"The price dropped to €{current_found_price}.\n"
                   f"You save €{savings}!\n\n"
                   f"Book here: {target_url}")
            await send_telegram_msg(msg)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_price())