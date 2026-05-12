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