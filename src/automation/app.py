from playwright.async_api import async_playwright,Playwright, TimeoutError
from src.login.practice_staff import click_continue_as_practice_staff
from src.login.financial_page import click_claims_tab
from src.scraping.claim_scrapper import scrape_claims_table
#from src.login.logout import logout
#from src.scraping.bills_scrapper import scrape_bills_widget, scrape_claims_widget
from src.login.standalone_onelogin_auth import OneLoginAuthenticator
from src.utils.settings import USER_DATA_DIR, base_url
from env_data import env
import asyncio


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
        target_app_url= "dummy"
    ) as auth:

        try:
            #  Login
            await auth.authenticate()
            page = auth.page

            
            # Navigate to practice
            await page.goto(f"{base_url}3882113")
            await page.wait_for_load_state("networkidle")
          
            await click_continue_as_practice_staff(page)

            await click_claims_tab(page)

            await scrape_claims_table(page)
            #await logout(page)

            # Scrape
            # await scrape_bills_widget(page)
            # await scrape_claims_widget(page)

        finally:
           print("Automation finished — closing session")

async def main():
    async with async_playwright() as playwright:
        await automation_app(playwright)


if __name__ == "__main__":
    asyncio.run(main())
