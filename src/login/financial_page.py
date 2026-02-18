from playwright.async_api import TimeoutError

async def click_claims_tab(page):
    print("➡️ Clicking Claims tab...")
    claims_link = page.locator(
        "a#home\\.claims, a[ui-sref='home.claims']"
    )


    await claims_link.first.click()
    print("✅ Claims tab clicked")

