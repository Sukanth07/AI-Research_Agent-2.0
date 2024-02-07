# Import Libraries
import requests
import json
import os
from bs4 import BeautifulSoup
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
load_dotenv()


# Module 1: Webscraping URLs from Google Search

serper_api_key = os.environ.get("SERP_API_KEY")

def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    return response.text


# Module 2: Webscraping the content of the URLs

def scrape_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")

        # Assuming navigation bar elements have class "navbar-item" and footer has ID "footer"
        paragraphs = soup.find_all("p")

        # data = [p.text.strip() for p in paragraphs if p.text.strip() != ""]
        data = ""
        for p in paragraphs:
            if p.text.strip() != "":
                data += p.text.strip() + "\n\n"
        
        return data

    except Exception as e:
        print(f"Error scraping data from {url}: {e}")
        return None
    
    
# Module 3: Gemini Model
    
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def get_model_result(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text


# Module 4: Reference Links

def add_reference_links(links):
    reference_links = "\n\nReference Links:\n"
    for link in links:
        reference_links += f"- {link}\n"
    return reference_links


# Module 5: Streamlit UI

def streamlit_app():
    st.set_page_config(page_title="AI research agent", page_icon=":robot_face:")

    st.header("AI research agent :robot_face:")
    query = st.text_input("Research goal", "Eg: Write an article about ICC World Cup 2023")
    
    if query:
        st.write("Doing research for ", query)

        try:

            results = search(query)
            results = json.loads(results)
            organic_links = [result["link"] for result in results["organic"]]

            scraped_data = ""
        
            for url in results:
                data = scrape_data_from_url(url)
                if data:
                    scraped_data += data + "\n\n"

            reference_links = add_reference_links(organic_links)
            
            messages = [
            {'role':'user',
            'parts': [f"You are a powerful AI assistant. Your job is to summarize the unstructured content into meaningful article form based on the user's query. Highlight the headings of each paragraphs. \n\nThe user's query is {query}. \n\nThe Data is: \n{data}. \n\nAlso, include the reference links in the end of the article you made: \n{reference_links}"]},
            ]

            model_result = get_model_result(messages)

            st.info(model_result)

        except Exception as e:
            st.error(f"Some error occurred: {e}. Try Again!")


if __name__ == "__main__":
    streamlit_app()