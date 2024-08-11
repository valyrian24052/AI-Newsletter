import streamlit as st 
import requests
import json 
import numpy as np

from newspaper import Article, ArticleException
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate, LLMChain, OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def is_unique(new_article, articles, threshold=0.6):
    """Check if the fetched news articles are unique based on similarity."""
    if not articles:
        return True

    vectorizer = TfidfVectorizer().fit([new_article] + articles)
    vectors = vectorizer.transform([new_article] + articles)
    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])

    return np.max(similarity_scores) <= threshold

def get_latest_results(query, api_key):
    """Fetch and parse the latest news articles using SerpAPI."""
    params = {
        "q": query,
        "location": "United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "tbs": "qdr:d",
        "api_key": api_key,
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = json.loads(response.text)
    excluded_websites = ["ft.com", "cointelegraph.com", "cell.com", "futuretools.io"]
    urls = [
        r["link"]
        for r in results.get("organic_results", [])
        if not any(excluded_site in r["link"] for excluded_site in excluded_websites)
    ][:40]

    parsed_texts = []
    article_texts = []
    text_splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=200)

    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()

            if not is_unique(article.text, article_texts):
                continue

            splitted_texts = text_splitter.split_text(article.text)
            if splitted_texts:
                parsed_texts.append((splitted_texts, url))
                article_texts.append(article.text)

        except ArticleException:
            print(f"Failed to download and parse article: {url}")

    return parsed_texts

class Document:
    """A simple class to represent a document."""
    def __init__(self, title, text):
        self.title = title
        self.page_content = text
        self.metadata = {"stop": []}

def summarize_text(to_summarize_texts, openai_api_key):
    """Summarize the texts using the OpenAI API."""
    summarized_texts_titles_urls = []
    llm = OpenAI(api_key=openai_api_key, temperature=0.8)
    chain_summarize = load_summarize_chain(llm, chain_type="map_reduce")

    prompt = PromptTemplate(
        input_variables=["text"],
        template="Write an appropriate, clickbaity news article title in less than 70 characters for this text: {text}"
    )

    for to_summarize_text, url in to_summarize_texts:
        to_summarize_text = [Document('Dummy Title', text) for text in to_summarize_text]
        if not to_summarize_text:
            print(f"No text to summarize for URL: {url}")
            continue

        summarized_text = chain_summarize.run(to_summarize_text)
        chain_prompt = LLMChain(llm=llm, prompt=prompt)
        clickbait_title = chain_prompt.run(summarized_text)

        summarized_texts_titles_urls.append((clickbait_title, summarized_text, url))

    return summarized_texts_titles_urls

def send_email_mailgun(subject, body, to, from_email, mailgun_domain, mailgun_api_key):
    """Send an email using the Mailgun API."""
    response = requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", mailgun_api_key),
        data={"from": from_email, "to": to, "subject": subject, "text": body}
    )

    print("Status code:", response.status_code)
    print("Response data:", response.text)
    
    return response
