# cinephile-persona-analyzer

**A RAG-powered AI that scrapes your Letterboxd history to decode your cinematic soul and recommend the films you've been missing.**

## Technical Log: The Scraper Evolution

Building the Letterboxd scraper involved navigating several layers of bot protection. Here is the evolution of our data retrieval strategy:

### Phase 1: The 'Requests' Approach (Failed)
- **Method:** Standard HTTP requests with fake headers.
- **Result:** Blocked by Cloudflare (Status 403).
- **Lesson:** Letterboxd uses advanced TLS fingerprinting to detect non-browser traffic.

### Phase 2: Browser Automation (Failed)
- **Method:** `SeleniumBase` with Undetected-Chromedriver (UC Mode).
- **Result:** Successfully bypassed Cloudflare, but Letterboxd triggered an "Adblocker Detected" overlay that obscured the UI elements.
- **Lesson:** UI-based scraping is fragile and easily disrupted by site-wide popups.

### Phase 3: The RSS Solution (Success)
- **Method:** Parsing the user's public RSS feed using `BeautifulSoup` and `lxml`.
- **Result:** Fast, reliable, and bypasses all browser-based blocks.
- **Outcome:** Successfully retrieved ~50 recent film entries including titles and ratings without triggering security flags.

### Phase 4: Data Enrichment (TMDB API)
- **Method:** Developed `processor.py` to map Letterboxd titles to TMDB movie IDs.
- **Data Points:** Extracted movie titles, release years, overviews, and popularity scores.
- **Outcome:** Created a structured `user_movie_data.csv` dataset, forming the "corpus" for the AI Persona analysis.

### Phase 5: AI Persona Analysis (NLP)
- **Method:** Applied `TfidfVectorizer` from `scikit-learn` to perform thematic extraction on movie metadata.
- **NLP Techniques:** Used stop-word filtering and n-gram analysis to identify unique cinematic fingerprints.
- **Outcome:** Automated generation of a "Cinephile Persona" based on recurring narrative patterns.

### Phase 6: Web Implementation & UI Deployment
- **Architecture:** Transitioned from CLI to a state-driven web application using **Streamlit**, implementing `session_state` for seamless multi-page navigation.
- **System Integration:** Refactored project structure into a modular Python package with `__init__.py` to handle complex cross-directory imports.
- **Dynamic Analysis:** Integrated the TF-IDF engine into the frontend to provide real-time thematic extraction from live Letterboxd data.
- **UX Design:** Focused on a "High-Trust" experience by abstracting API complexity into a clean, single-input landing page.