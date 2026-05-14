import os
import requests
import pandas as pd
from dotenv import load_dotenv
try:
    from src.scraper import get_user_favorites 
except ImportError:
    from scraper import get_user_favorites
    
# 1. Setup Environment
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def get_movie_details(movie_title):
    """Searches TMDB for a title and returns its 'DNA'."""
    search_url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title
    }
    
    try:
        response = requests.get(search_url, params=params)
        results = response.json().get('results')
        
        if results:
            # We take the most likely match (index 0)
            movie = results[0]
            return {
                "title": movie['title'],
                "release_date": movie.get('release_date', 'N/A'),
                "overview": movie.get('overview', ''),
                "popularity": movie.get('popularity', 0)
            }
    except Exception as e:
        print(f"Error fetching {movie_title}: {e}")
    return None

def build_dataset(username):
    # Get the titles from your scraper
    raw_titles = get_user_favorites(username)
    
    movie_data = []
    print(f"\n--- Starting TMDB Lookup for {len(raw_titles)} titles ---")

    for full_title in raw_titles:
        # 1. CLEANING: If title is "Frances Ha, 2012", we only want "Frances Ha"
        # We split by comma and take the first part
        clean_title = full_title.split(',')[0].strip()
        
        # 2. FILTERING: Skip those Letterboxd 'List' names we saw earlier
        # Most lists don't have a year in the RSS feed
        if ',' not in full_title and len(full_title.split()) > 4:
            print(f"Skipping likely list: {full_title}")
            continue

        print(f"Searching: {clean_title}...")
        
        details = get_movie_details(clean_title)
        if details:
            movie_data.append(details)
        else:
            print(f"   ! No match found for: {clean_title}")
    
    if not movie_data:
        print("\nWarning: No movie details were found. Check your TMDB_API_KEY in .env!")
        return None

    # Create and Save
    df = pd.DataFrame(movie_data)
    df.to_csv("user_movie_data.csv", index=False)
    print(f"\nSuccess! Saved {len(df)} movies to 'user_movie_data.csv'")
    return df

if __name__ == "__main__":
    # Test it with your username
    target_user = "zienefilm" 
    build_dataset(target_user)