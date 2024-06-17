import streamlit as st
from main import run_async_task

def handle_search_and_display(search_term: str, chosenButton: str):
    with st.spinner('Searching Wikipedia...'):
        paragraphs = run_async_task(search_term, chosenButton)
    if paragraphs != []:
        if len(paragraphs)>3:
            st.success("Here are the insights we found:")
            st.write(paragraphs[1])
            st.write(paragraphs[2])
            st.write(paragraphs[3])
        else:
            st.warning("Sorry, we couldn't find any information for the provided search term. 😕 Please try searching for something more generic.")

# cols = st.columns([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4])

cols = st.columns(5)
mainWikiButtons  = [
    # 'Commons',
    'Wikibooks', 'Wikiversity', 
    # 'Wikisource',
    # 'Meta-Wiki',
    'Wikinews', 'Wikiquote', 
    # 'Wikispecies',
    'Wiktionary', 
    # 'Wikidata',
    # 'MediaWiki',
    # 'Wikifunctions'
    ]

if 'chosenButton' not in st.session_state:
    st.session_state.chosenButton = ''

for i, button in enumerate(mainWikiButtons ):
    with cols[i]:
        if st.button(button):
            st.session_state.chosenButton = button


st.title('Dive into Wikipedia: Quick Insights!')
search_term = st.text_input('Enter a topic to search on Wikipedia')
if st.button('Search'):
    handle_search_and_display(search_term, st.session_state.chosenButton)
