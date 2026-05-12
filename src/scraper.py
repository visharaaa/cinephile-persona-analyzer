import requests
from bs4 import BeautifulSoup
import time

def get_user_favorites(username):
    # Target specifically for 4-5 star rated films for high quality details about persona
    url = f"https://letterboxd.com/{username}/films/rated/4-5/by/date/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    print(f"Fetching high rated films for: {username}")

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Could not access profile (status {response.status_code})")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Letterboxd stores movies in <li> tags with class 'poster-container'
        films = []
        posters = soup.find_all('li', class_='poster-container')

        for poster in posters:
            # The movie title is hidden in the 'alt' attribute of the poster image
            img = poster.find('img')
            if img and 'alt' in img.attrs:
                films.append(img['alt'])

        return films
    
    except Exception as e:
        print (f"An unexpected error occurred: {e}")
        return []
    
if __name__ == "__main__":
    # Test using an example username
    test_user = input("Enter Letterboxd username to test: ")
    movies = get_user_favorites(test_user)

    print(f"\nSuccess! Found {len(movies)} top-rated movies:")
    for movie in movies[:15]:
        print(f"  - {movie}")