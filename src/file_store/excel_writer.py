from pathlib import Path
from openpyxl import Workbook

BASE_DIR = Path(__file__).resolve().parents[2]

def write_to_excel(data, file_name):
    file_path = BASE_DIR / file_name

    if file_path.exists():
        file_path.unlink()  # Windows-safe overwrite

    wb = Workbook()
    ws = wb.active
    ws.title = "Widget Data"

    for row in data:
        ws.append(row)

    wb.save(file_path)
    print("✅ Excel saved at:", file_path)
