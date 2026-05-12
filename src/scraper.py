import requests
from bs4 import BeautifulSoup

def get_user_favorites(username):
    # Letterboxd provides an RSS feed of recent activity
    rss_url = f"https://letterboxd.com/{username}/rss/"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"Reading feed for: {username}...")
    
    try:
        response = requests.get(rss_url, headers=headers)
        if response.status_code != 200:
            print(f"Could not access RSS (Status {response.status_code})")
            return []

        # RSS is XML, so we use the xml parser
        soup = BeautifulSoup(response.content, "lxml-xml")
        items = soup.find_all("item")
        
        films = []
        for item in items:
            # The title in the RSS feed is usually "Movie Name, Year - Rating"
            # We just want the Movie Name
            full_title = item.title.text
            if " - " in full_title:
                movie_name = full_title.split(" - ")[0]
                # We can also check the rating here if we want to filter
                films.append(movie_name)
            else:
                films.append(full_title)

        return list(set(films)) # Remove duplicates

    except Exception as e:
        print(f"Error reading feed: {e}")
        return []

if __name__ == "__main__":
    user = "zienefilm"
    movies = get_user_favorites(user)
    
    if movies:
        print(f"\nSuccess! Found {len(movies)} recent films from feed:")
        for movie in movies[:10]:
            print(f" - {movie}")
    else:
        print("\nFeed was empty or could not be reached.")