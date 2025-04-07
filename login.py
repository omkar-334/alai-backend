import os
import sys
import time

from dotenv import load_dotenv, set_key
from playwright.sync_api import sync_playwright

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def refresh_token():
    token = os.getenv("TOKEN")
    if not token or is_token_expired():
        login_and_get_token()
    token = os.getenv("TOKEN")
    return token


def is_token_expired():
    token_timestamp = os.getenv("TOKEN_TIMESTAMP")
    if not token_timestamp:
        return True

    timestamp = int(token_timestamp)
    current_time = int(time.time())
    elapsed_minutes = (current_time - timestamp) / 60

    return elapsed_minutes > 15


def login_and_get_token():
    token_found = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

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
                    set_key(ENV_PATH, "TOKEN_TIMESTAMP", int(time.time()))
                    print("Token saved to .env")
                    sys.exit(0)

        context.on("request", handle_request)

        page = context.new_page()
        page.goto("https://app.getalai.com/home")

        page.click("a:has-text('Already have an account? Sign in')")

        email_selector = 'input[type="email"]'
        page.wait_for_selector(email_selector, timeout=15000)
        page.fill(email_selector, EMAIL)

        password_selector = "input[type='password']"
        page.wait_for_selector(password_selector, timeout=15000)
        page.fill(password_selector, PASSWORD)

        page.click("button[type='submit']")

        wait_time = 100
        if not token_found:
            print(f"Token not found. Waiting for {wait_time} seconds...")
            end_time = time.time() + wait_time
            while not token_found and time.time() < end_time:
                time.sleep(1)

        browser.close()


if __name__ == "__main__":
    login_and_get_token()
