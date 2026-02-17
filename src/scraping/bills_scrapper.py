from src.file_store.excel_writer import write_to_excel


async def scrape_widget_by_badge(page, badge_text: str, excel_file_name: str):
    """
    Generic scraper for widgets like Bills, Claims, etc.
    """

    print(f"➡️ Waiting for {badge_text} widget badge...")

    # 1️⃣ Wait for badge
    await page.wait_for_selector(
        f"span.badge.widget-type:has-text('{badge_text}')",
        timeout=60000
    )

    # 2️⃣ Get widget container for this badge
    widget = page.locator(
        "div.widget-container",
        has=page.locator("span.badge.widget-type", has_text=badge_text)
    ).first

    await widget.wait_for(state="visible", timeout=60000)
    print(f"✅ {badge_text} widget container found")

    # 3️⃣ Prepare Excel data
    data = []
    data.append(["Days Range", "Value"])

    # 4️⃣ Get rows
    items = widget.locator(".item")
    await items.first.wait_for(state="visible", timeout=60000)

    count = await items.count()
    print(f"🧮 {badge_text} rows found:", count)

    for i in range(count):
        row = items.nth(i)

        # Angular-safe text extraction
        row_text = (await row.inner_text()).strip()
        # Example: "0-30 Days 14,051"

        parts = row_text.rsplit(" ", 1)

        if len(parts) == 2:
            days, value = parts
        else:
            days = row_text
            value = ""

        data.append([days.strip(), value.strip()])

    print(f"✅ {badge_text} DATA SCRAPED:", data)

    # 5️⃣ Save Excel
    write_to_excel(data, excel_file_name)


# ----------------------------
# Specific wrappers
# ----------------------------

async def scrape_bills_widget(page):
    await scrape_widget_by_badge(
        page,
        badge_text="Bills",
        excel_file_name="bills_widget.xlsx"
    )


async def scrape_claims_widget(page):
    await scrape_widget_by_badge(
        page,
        badge_text="Claims",
        excel_file_name="claims_widget.xlsx"
    )
