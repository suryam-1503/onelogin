import pandas as pd


async def scrape_claims_table(page):
    """
    Scrapes the Claims ng-table (already opened) and saves to Excel.
    Removes unwanted 'View Details' rows safely.
    """

    #  Wait until table rows are loaded
    await page.wait_for_selector(
        "table.ng-table tbody tr",
        timeout=30000
    )

    # Extra wait for Angular rendering
    await page.wait_for_timeout(1500)

    #  Extract table headers (skip checkbox column)
    headers = await page.eval_on_selector_all(
        "table.ng-table thead th:not(:first-child)",
        "ths => ths.map(th => th.innerText.trim()).filter(Boolean)"
    )

    #  Extract table rows (skip checkbox column)
    rows = await page.eval_on_selector_all(
        "table.ng-table tbody tr",
        """trs => trs.map(tr =>
            Array.from(tr.querySelectorAll("td"))
                .slice(1)
                .map(td => td.innerText.trim())
        )"""
    )

    if not rows:
        print(" No claims data found")
        return

    #  Normalize rows and REMOVE 'View Details'
    normalized_rows = []
    col_count = len(headers)

    for row in rows:

        #  Skip rows containing "View Details"
        if any("view details" in cell.lower() for cell in row):
            continue

        # Ensure row length matches header length
        if len(row) > col_count:
            row = row[:col_count]
        elif len(row) < col_count:
            row = row + [""] * (col_count - len(row))

        normalized_rows.append(row)

    if not normalized_rows:
        print(" All rows were filtered out")
        return

    
    print("Headers count:", len(headers))
    print("Columns per row:", len(normalized_rows[0]))
    print("Total valid rows:", len(normalized_rows))

    #  Create DataFrame
    df = pd.DataFrame(normalized_rows, columns=headers)

    #  Save to Excel
    output_file = "datas.xlsx"
    df.to_excel(output_file, index=False)

    print(f"✅ Claims table scraped and saved to {output_file}")
