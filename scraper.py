import asyncio
import os
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import httpx # This sends the Telegram message

async def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": message})

async def check_price():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await stealth_async(page)
        
        # TESTING: Using a dummy URL for now
        await page.goto("https://www.google.com/travel/flights", wait_until="networkidle")
        
        # LOGIC: For the POC, we simulate finding a drop
        current_price = 1400 
        original_price = 1500
        
        if current_price < original_price:
            diff = original_price - current_price
            msg = f"🚨 PRICE DROP ALERT! \nYour holiday is now €{current_price}. You save €{diff}! \nCheck here: https://google.com/travel/flights"
            await send_telegram_msg(msg)
            print("Alert sent to Telegram!")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_price())