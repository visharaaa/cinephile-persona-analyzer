import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_persona():
    # Load the data generated with the processor
    try:
        df = pd.read_csv("user_movie_data.csv")
    except FileNotFoundError:
        print("Error: user_movie_data.csv not found. Run processor.py first!")
        return

    # Drop any movies that have empty overviews
    df = df.dropna(subset=['overview'])
    
    # Setup TF-IDF Vectorizer
    # stop_words='english' removes common words like 'the', 'and', 'a'
    # ngram_range=(1,2) used to catch phrases like 'new york' or 'science fiction'
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100, ngram_range=(1, 2))
    
    # Fit and transform the movie overviews
    tfidf_matrix = vectorizer.fit_transform(df['overview'])
    
    # Extract the top keywords across all movies
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    word_scores = dict(zip(feature_names, scores))
    
    # Sort keywords by their TF-IDF importance
    sorted_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, score in sorted_keywords[:10]]

    # Display the Persona Report
    print("\n" + "="*30)
    print("      CINEPHILE PERSONA")
    print("="*30)
    print(f"Total Movies Analyzed: {len(df)}")
    print("\nCore Cinematic Themes Identified:")
    for i, word in enumerate(top_keywords, 1):
        print(f"{i}. {word.title()}")

    print("\n--- AI Analysis ---")
    generate_summary(top_keywords)

def generate_summary(keywords):
    """A simple logic-based summary generator based on extracted themes."""
    summary_map = {
        "life": "You appreciate human-centric stories and realistic character studies.",
        "world": "You are drawn to expansive world-building and global perspectives.",
        "love": "There's a romantic or emotional core to your cinematic tastes.",
        "new": "You likely enjoy discovery, modern settings, or 'new' beginnings.",
        "young": "Coming-of-age stories or youthful energy seem to resonate with you.",
        "finds": "You are attracted to narratives involving mystery, search, or self-discovery."
    }
    
    persona_traits = [summary_map[k] for k in keywords if k in summary_map]
    
    if persona_traits:
        for trait in persona_traits[:3]:
            print(f"• {trait}")
    else:
        print("• Your taste is highly niche and unique, defying standard thematic categories!")

if __name__ == "__main__":
    generate_persona()