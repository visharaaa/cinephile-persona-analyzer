import streamlit as st
from src.scraper import get_user_favorites
from src.processor import get_movie_details
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. MUST BE FIRST
st.set_page_config(page_title="Cinephile Persona", page_icon="🎬", layout="wide")

# 2. Load CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --- LANDING PAGE ---
if st.session_state.page == 'landing':
    st.title("🎬 Cinephile Persona AI")
    username = st.text_input("Enter your Letterboxd Username:", placeholder="e.g., zienefilm")
    
    if st.button("Generate My Persona"):
        if username:
            with st.spinner("Analyzing your film history..."):
                titles = get_user_favorites(username)
                movie_data = []
                for t in titles[:15]:
                    clean = t.split(',')[0]
                    details = get_movie_details(clean)
                    if details:
                        movie_data.append(details)
                
                st.session_state.data = pd.DataFrame(movie_data)
                st.session_state.username = username
                st.session_state.page = 'results'
                st.rerun()

# --- RESULTS PAGE ---
elif st.session_state.page == 'results':
    df = st.session_state.data
    
    # Silent NLP Logic
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5)
    tfidf_matrix = vectorizer.fit_transform(df['overview'])
    keywords = list(vectorizer.get_feature_names_out())
    
    # Mapping
    title = "The Modern Realist"
    description = "You enjoy sharp, contemporary storytelling that explores the 'now'. Your taste suggests a preference for grounded narratives."

    if any(word in keywords for word in ["love", "family", "life", "relationship"]):
        title = "The Heart-Centered Humanist"
        description = "You are drawn to the intricacies of human connection. Your films focus on how we relate to those closest to us, prioritizing emotional realism over spectacle."
    elif any(word in keywords for word in ["mysterious", "world", "space", "war", "discovery"]):
        title = "The Atmospheric Explorer"
        description = "You love getting lost in complex worlds and unraveling puzzles. Cinema is an escape to the unknown for you, where atmosphere defines the experience."

    # 3. CUSTOM UI OUTPUT (Matching your image)
    st.markdown(f"""
        <div class="persona-container">
            <div class="persona-left">
                <div class="persona-header">YOUR<br>CINEPHILE<br>PERSONA</div>
            </div>
            <div class="persona-right">
                <span class="persona-title-highlight">{title}</span>
                {description}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Back button placed at the bottom
    st.write("<br><br>", unsafe_allow_html=True)
    if st.button("← Analyze Another User"):
        st.session_state.page = 'landing'
        st.rerun()