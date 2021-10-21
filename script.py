import asyncio

import openpyxl

from constants import URL, settings
from database import BlockedNumbers, db

TASKS = []


async def parse_xlsx_file(path_to_xlsx_file: str = settings.excel_file_path) -> None:
    """Parse excel file to get all data with phone numbers from it"""
    await db.set_bind(URL.DB_URL_OUTSIDE_CONTAINER.value)
    phone_numbers_sheets = openpyxl.load_workbook(path_to_xlsx_file, data_only=True).worksheets
    for sheet in phone_numbers_sheets:
        for phone_number in sheet.iter_rows(values_only=True):
            TASKS.append(BlockedNumbers.create(phone_number=str(phone_number[0])))  # Because we get tuple
    await asyncio.gather(*TASKS)


if __name__ == '__main__':
    asyncio.run(parse_xlsx_file())
