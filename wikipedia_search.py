from playwright.async_api import Playwright, async_playwright, expect

paragraphs=[]
async def run(playwright: Playwright, search_term: str, chosenButton: str) -> None:
    paragraphs=[]
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto("https://www.wikipedia.org/")

    if chosenButton == '':
        await page.locator("//a[@id='js-link-box-en'] ").click()
        await page.get_by_placeholder("Search Wikipedia").click()
        await page.get_by_placeholder("Search Wikipedia").fill(search_term)
        try:
            await page.locator("//li[@id='cdx-menu-item-1']").click()
        except:
            paragraphs = []
            await context.close()
            await browser.close()
            return paragraphs

        # sometimes my paragraphs.txt contains only 3 entries instead of the 41 entries it is supposed to contain
        # The issue you're encountering is likely due to the page not being fully loaded or the elements not being fully rendered when you attempt to retrieve the paragraphs. 
        await page.wait_for_load_state("networkidle")

        # Retrieve and print the text content of all paragraphs
        paragraphs = await page.locator('p').all_text_contents()
        print(paragraphs)
        await context.close()
        await browser.close()
        return paragraphs
    

    elif chosenButton == 'Wikinews' or chosenButton =='Wikibooks' or chosenButton == 'Wikiversity' or chosenButton == 'Wiktionary':
        await page.goto(f'https://www.{chosenButton.lower()}.org/')
        print(f'https://www.{chosenButton.lower()}.org/')
        await page.locator("input[id='searchInput']").click()
        await page.locator("input[id='searchInput']").fill(search_term)
        try:
            await page.locator('button.pure-button').click()
        except:
            paragraphs = []
            await context.close()
            await browser.close()
            return paragraphs
        
        await page.wait_for_load_state("networkidle")

        # headings = await page.locator("div[class='mw-search-result-heading']").all_text_contents()
        searchResults = await page.locator("div.mw-search-result-heading>a").all_text_contents()
        searchMatches = await page.locator("div[class='searchresult']").all_text_contents()
        if len(searchResults) == len(searchMatches):
            for searchResult, searchMatch in zip( searchResults, searchMatches):
                paragraphs.append( searchResult + searchMatch)
            print(paragraphs)
        # await page.wait_for_timeout(10000)  # 10 seconds

        await context.close()
        await browser.close()
        return paragraphs
    
    elif chosenButton == 'Wikiquote':
        await page.goto(f'https://www.{chosenButton.lower()}.org/')
        print(f'https://www.{chosenButton.lower()}.org/')
        await page.locator("input[id='searchInput']").click()
        await page.locator("input[id='searchInput']").fill(search_term)
        try:
            await page.locator('button.pure-button').click()
        except:
            paragraphs = []
            await context.close()
            await browser.close()
            return paragraphs
        
        await page.wait_for_load_state("networkidle")

        unorderedLists = await page.locator('//ul').all_text_contents()
        return unorderedLists
    



