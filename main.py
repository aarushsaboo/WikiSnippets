import asyncio
from playwright.async_api import Playwright, async_playwright, expect
import os

from wikipedia_search import run
os.system('playwright install')
os.system('playwright install-deps')

async def main(search_term: str, chosenButton: str) -> None:
    async with async_playwright() as playwright:
        paragraphs =await run(playwright, search_term, chosenButton)
        return paragraphs

def run_async_task(search_term: str, chosenButton: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    paragraphs = loop.run_until_complete(main(search_term, chosenButton))
    return paragraphs

