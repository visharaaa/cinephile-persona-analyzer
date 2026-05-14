import streamlit as st
from src.scraper import get_user_favorites
from src.processor import get_movie_details
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Page Config
st.set_page_config(page_title="Cinephile Persona", page_icon="🎬")

# --- SESSION STATE ---
# This keeps track of which "page" we are on
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def go_to_results():
    st.session_state.page = 'results'

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    st.title("🎬 Cinephile Persona AI")
    st.subheader("Discover your cinematic DNA through AI analysis.")
    
    username = st.text_input("Enter your Letterboxd Username:", placeholder="e.g., zienefilm")
    
    if st.button("Generate My Persona"):
        if username:
            with st.spinner("Analyzing your film history..."):
                # 1. Scrape
                titles = get_user_favorites(username)
                
                # 2. Process (Limit to top 15 for speed in web app)
                movie_data = []
                for t in titles[:15]:
                    clean = t.split(',')[0]
                    details = get_movie_details(clean)
                    if details:
                        movie_data.append(details)
                
                # Store data and move page
                st.session_state.data = pd.DataFrame(movie_data)
                st.session_state.username = username
                st.session_state.page = 'results'
                st.rerun()
        else:
            st.error("Please enter a username!")

# --- RESULTS PAGE ---
elif st.session_state.page == 'results':
    st.title(f"Cinema Profile: {st.session_state.username}")
    
    df = st.session_state.data
    
    # NLP Analysis logic
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5)
    tfidf_matrix = vectorizer.fit_transform(df['overview'])
    keywords = vectorizer.get_feature_names_out()
    
    st.write("### Your Extracted Moods")
    cols = st.columns(len(keywords))
    for i, word in enumerate(keywords):
        cols[i].button(word.title(), key=i)

    # --- PERSONA MAPPING ---
    st.write("---")
    st.header("The AI Verdict")
    
    # Simple Mapping Logic
    if "love" in keywords or "family" in keywords:
        st.subheader("The Heart-Centered Humanist")
        st.write("You are drawn to the intricacies of human connection. Your films focus on how we relate to those closest to us.")
    elif "mysterious" in keywords or "world" in keywords:
        st.subheader("The Atmospheric Explorer")
        st.write("You love getting lost in complex worlds and unraveling puzzles. Cinema is an escape to the unknown for you.")
    else:
        st.subheader("The Modern Realist")
        st.write("You enjoy sharp, contemporary storytelling that explores the 'now'.")

    if st.button("Start Over"):
        st.session_state.page = 'landing'
        st.rerun()