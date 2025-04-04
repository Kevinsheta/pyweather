import requests
import streamlit as st
from datetime import datetime

def show_more_news():
    st.session_state["news_page"] = True

def back_to_main():
    st.session_state["news_page"] = False

def filter_relevant_articles(articles):
    """
    Filters articles to only include those with relevant weather terms in the title or description.
    """
    relevant_terms = ["weather", "forecast", "storm", "rain", "hurricane", "snow", "climate", "temperature", "thunderstorm", "flood", "drought", "tornado"]
    filtered_articles = []

    for article in articles:
        title = article.get("title", "") or ""  # Ensure it's not None
        description = article.get("description", "") or ""  # Ensure it's not None
        content = article.get("content", "") or ""

        title = title.lower()
        description = description.lower()
        content= description.lower()
        
        if any(term in title or term in description or term in content for term in relevant_terms):
            filtered_articles.append(article)

    return filtered_articles

def fetch_weather_news():
    NEWS_API_KEY = "d670d7f8666742a18e8cbb401c9a32b5"
    url = f"https://newsapi.org/v2/everything?q=weather&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            return filter_relevant_articles(articles)
        else:
            st.error("Error fetching weather news: " + response.text)
            return []
    except Exception as e:
        st.error(f"Exception occurred while fetching news: {e}")
        return []
    
def display_weather_news_summary(articles):
    st.markdown("## 🌦 Weather News")
    
    if articles:
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "No description available.")
            url = article.get("url", "#")
            image_url = article.get("urlToImage", None)
            published_at = article.get("publishedAt", "")
            
            st.markdown(f"### [{title}]({url})")
            if image_url:
                st.image(image_url, width=400)
            st.write(description)
            if published_at:
                try:
                    published_dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                    st.write(f"*Published at: {published_dt.strftime('%Y-%m-%d %I:%M %p')}*")
                except Exception:
                    st.write(f"*Published at: {published_at}*")
            st.markdown("---")
        
    else:
        st.info("No weather news available at this time.")

def display_all_news(articles):
    if articles:
        # Display all articles
        for article in articles:
            title = article.get("title", "No Title")
            description = article.get("description", "No description available.")
            url = article.get("url", "#")
            image_url = article.get("urlToImage", None)
            published_at = article.get("publishedAt", "")
            
            st.markdown(f"### [{title}]({url})")
            if image_url:
                st.image(image_url, width=400)
            st.write(description)
            if published_at:
                try:
                    published_dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                    st.write(f"*Published at: {published_dt.strftime('%Y-%m-%d %I:%M %p')}*")
                except Exception:
                    st.write(f"*Published at: {published_at}*")
            st.markdown("---")
    else:
        st.info("No weather news available at this time.")