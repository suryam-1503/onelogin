from playwright.async_api import TimeoutError

async def click_continue_as_practice_staff(page):
    print("Waiting for Continue as Practice Staff page...")

    button = page.locator(
        "input[value='Continue as Practice Staff']"
    )

    await button.click(force=True)

    print("Clicked Continue as Practice Staff")
