import os
import sys
import time

from dotenv import load_dotenv, set_key
from playwright.sync_api import sync_playwright

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


# def login_and_get_token():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         def handle_request(request):
#             print(">>", request.method, request.url)
#             print(request.headers)

#             if "https://alai-standalone-backend.getalai.com" in request.url:
#                 auth = request.headers.get("authorization")
#                 if auth and "Bearer" in auth:
#                     token = auth.split("Bearer ")[1]
#                     set_key(ENV_PATH, "NEW_TOKEN", token)
#                     print("Token saved to .env")

#                     browser.close()
#                     sys.exit(0)

#         # Register just once
#         page.on("request", handle_request)
#         # context.on("request", handle_request)

#         # Step 1: Go to login page
#         page.goto("https://app.getalai.com/home")

#         page.click("a:has-text('Already have an account? Sign in')")

#         email_selector = 'input[type="email"]'
#         page.wait_for_selector(email_selector, timeout=15000)
#         page.fill(email_selector, EMAIL)

#         password_selector = "input[type='password']"
#         page.wait_for_selector(password_selector, timeout=15000)
#         page.fill(password_selector, PASSWORD)

#         page.on("request", handle_request)
#         page.click("button[type='submit']")

#         time.sleep(200)


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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Set up request tracking before creating the page
        context = browser.new_context()

        # Create a variable to store the token
        token_found = None

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

        # Register the handler at context level to catch ALL requests
        context.on("request", handle_request)

        page = context.new_page()

        # Step 1: Go to login page
        page.goto("https://app.getalai.com/home")

        page.click("a:has-text('Already have an account? Sign in')")

        email_selector = 'input[type="email"]'
        page.wait_for_selector(email_selector, timeout=15000)
        page.fill(email_selector, EMAIL)

        password_selector = "input[type='password']"
        page.wait_for_selector(password_selector, timeout=15000)
        page.fill(password_selector, PASSWORD)

        # Click submit and wait for navigation
        page.click("button[type='submit']")

        # Wait a bit to capture requests after login
        print("Waiting to capture requests...")

        # Wait for token or timeout
        end_time = time.time() + 20  # 20 seconds timeout
        while not token_found and time.time() < end_time:
            time.sleep(1)

        # Provide a longer wait to see more requests
        wait_time = 10
        print(f"Token {'found!' if token_found else 'not found.'} Continuing to monitor requests for {wait_time} more seconds...")
        time.sleep(wait_time)

        browser.close()


if __name__ == "__main__":
    login_and_get_token()
