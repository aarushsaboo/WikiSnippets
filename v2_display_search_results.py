import asyncio
from playwright.async_api import Playwright, async_playwright, expect
import os
import streamlit as st

os.system('playwright install')
os.system('playwright install-deps')

paragraphs=[]
async def run(playwright: Playwright, search_term: str) -> None:
    global paragraphs
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.wikipedia.org/")
    await page.get_by_role("link", name="English 6,796,000+ articles").click()
    await page.get_by_placeholder("Search Wikipedia").click()
    await page.get_by_placeholder("Search Wikipedia").fill(search_term)
    try:
        await page.locator("//li[@id='cdx-menu-item-1']").click()
    except:
        paragraphs = []
        await context.close()
        await browser.close()
        return

    # sometimes my paragraphs.txt contains only 3 entries instead of the 41 entries it is supposed to contain
    # The issue you're encountering is likely due to the page not being fully loaded or the elements not being fully rendered when you attempt to retrieve the paragraphs. 
    await page.wait_for_load_state("networkidle")

    # Retrieve and print the text content of all paragraphs
    paragraphs = await page.locator('p').all_text_contents()
    
    await context.close()
    await browser.close()

async def main(search_term: str) -> None:
    async with async_playwright() as playwright:
        await run(playwright, search_term)

def run_async_task(search_term: str):
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(search_term))

# run_async_task()

st.title('Dive into Wikipedia: Quick Insights!')
search_term = st.text_input('Enter a topic to search on Wikipedia')
if st.button('Search'):
    with st.spinner('Searching Wikipedia...'):
        run_async_task(search_term)
    if paragraphs:
        if len(paragraphs)==3:
            st.success("Here are the insights we found:")
            st.write(paragraphs[1])
            st.write(paragraphs[2])
            st.write(paragraphs[3])
        else:
            st.warning("Sorry, we couldn't find any information for the provided search term. 😕 Please try searching for something more generic.")
