from playwright.async_api import async_playwright, Playwright
import asyncio
from src.scraping.bills_scrapper import scrape_bills_widget, scrape_claims_widget
from src.login.standalone_onelogin_auth import OneLoginAuthenticator
from src.utils.settings import USER_DATA_DIR, base_url
from env_data import env
from src.login.logout import logout


async def automation_app(playwright: Playwright):

    async with OneLoginAuthenticator(
        subdomain=env.ONELOGIN_SUBDOMAIN,
        username=env.ONELOGIN_USERNAME,
        password=env.ONELOGIN_PASSWORD,
        client_id=env.ONELOGIN_CLIENT_ID,
        client_secret=env.ONELOGIN_CLIENT_SECRET,
        headless=False,
        user_data_dir=USER_DATA_DIR,
        enable_extension=True,
        target_app_url="dummy"
    ) as auth:


        try:  
        # 1️⃣ Login
            await auth.authenticate()
            page = auth.page


        # 2️⃣ Navigate to Financial page (same tab)
            await page.goto(f"{base_url}3882113")

        # 3️⃣ Wait for page to stabilize
            await page.wait_for_load_state("networkidle")

            print("📄 Current URL:", page.url)

        # 4️⃣ Wait ONLY ONCE for Bills widget
            await page.wait_for_selector(
                "span.badge.widget-type:has-text('Bills')",
                  timeout=300000
             )

        # 5️⃣ Scrape
            await scrape_bills_widget(page)
            await scrape_claims_widget(page)
        finally:
            # 6️⃣ ALWAYS logout (even if error happens)
            await logout(page)
            print("👋 Logout completed")
    
        


async def main():
    async with async_playwright() as playwright:
        await automation_app(playwright)


if __name__ == "__main__":
    asyncio.run(main())
