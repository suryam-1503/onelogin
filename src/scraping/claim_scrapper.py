import pandas as pd
import asyncio

async def scrape_claims_table(page):

    await page.wait_for_selector("table.ng-table tbody tr")

    # Extract headers once
    headers = await page.eval_on_selector_all(
        "table.ng-table thead th:not(:first-child)",
        "ths => ths.map(th => th.innerText.trim()).filter(Boolean)"
    )

    all_rows = []
    col_count = len(headers)

    # Find total pages
    page_numbers = await page.eval_on_selector_all(
        "a[data-identifier^='pagination-'] span",
        "spans => spans.map(s => parseInt(s.innerText))"
    )

    total_pages = max(page_numbers)
    print("📄 Total pages:", total_pages)

    for page_no in range(1, total_pages + 1):

        print(f"➡️ Scraping page {page_no}")

        # Click page number
        await page.click(
            f"a[data-identifier='pagination-{page_no}']"
        )

        # Wait for table reload
        await page.wait_for_timeout(1500)

        rows = await page.eval_on_selector_all(
            "table.ng-table tbody tr",
            """trs => trs.map(tr =>
                Array.from(tr.querySelectorAll("td"))
                    .slice(1)
                    .map(td => td.innerText.trim())
            )"""
        )

        for row in rows:
            if any("view details" in cell.lower() for cell in row):
                continue

            if len(row) > col_count:
                row = row[:col_count]
            elif len(row) < col_count:
                row += [""] * (col_count - len(row))

            all_rows.append(row)

    if not all_rows:
        print("❌ No data found")
        return

    df = pd.DataFrame(all_rows, columns=headers)
    df.to_excel("datasclaim.xlsx", index=False)

    print(f"✅ Scraped {len(all_rows)} rows from {total_pages} pages")
