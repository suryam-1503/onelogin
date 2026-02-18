# #src/login/logout.py

async def logout(page):
    print("Logging out...")

    await page.wait_for_selector(
        "#app-logout",
        state="visible",
        timeout=30000
    )

    await page.click("#app-logout")

    await page.wait_for_url(
        lambda url: "logout" in url or "login" in url,
        timeout=30000
    )

    print("Logged out successfully")
