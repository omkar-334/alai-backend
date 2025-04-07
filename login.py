import asyncio
import os
import sys
import time
from datetime import datetime

import jwt
from dotenv import load_dotenv, set_key
from playwright.async_api import async_playwright

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


async def refresh_token():
    token = os.getenv("TOKEN")
    if not token or is_token_expired():
        print("Token expired or not found. Logging in...")
        await login_and_get_token()
    token = os.getenv("TOKEN")
    return token


def is_token_expired():
    token = os.getenv("TOKEN")
    decoded_time = jwt.decode(token, options={"verify_signature": False})["exp"]
    expiry = datetime.fromtimestamp(decoded_time)
    print("Token expires at:", expiry)

    current_time = int(time.time())

    return current_time > decoded_time


async def login_and_get_token():
    token_found = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, devtools=True)
        context = await browser.new_context()

        def handle_request(request):
            nonlocal token_found
            url = request.url

            if "https://alai-standalone-backend.getalai.com" in url:
                print(f">> {request.method} {url}")

                auth = request.headers.get("authorization")
                if auth and "Bearer" in auth:
                    token = auth.split("Bearer ")[1]
                    token_found = token
                    set_key(ENV_PATH, "TOKEN", token)
                    set_key(ENV_PATH, "TOKEN_TIMESTAMP", str(int(time.time())))
                    print("Token saved to .env")
                    sys.exit(0)

        context.on("request", handle_request)

        page = await context.new_page()
        await page.goto("https://app.getalai.com/home")

        await page.click("a:has-text('Already have an account? Sign in')")

        email_selector = 'input[type="email"]'
        await page.wait_for_selector(email_selector, timeout=15000)
        await page.fill(email_selector, EMAIL)

        password_selector = "input[type='password']"
        await page.wait_for_selector(password_selector, timeout=15000)
        await page.fill(password_selector, PASSWORD)

        await page.click("button[type='submit']")

        wait_time = 300
        if not token_found:
            print(f"Token not found. Waiting for {wait_time} seconds...")
            end_time = time.time() + wait_time
            while not token_found and time.time() < end_time:
                await asyncio.sleep(1)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(refresh_token())
