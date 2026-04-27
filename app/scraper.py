# app/scraper.py
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from app.database import SessionLocal
from app.models import Source, Article
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_youtube_transcript(video_link):
    """Bypasses YouTube API to securely fetch video transcripts."""
    try:
        video_id = video_link.split("v=")[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return TextFormatter().format_transcript(transcript_list)
    except Exception:
        return "Transcript not available."

def scrape_youtube(source):
    """Hits the hidden YouTube RSS feed to find recent videos."""
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={source.url}"
    feed = feedparser.parse(feed_url)
    articles_data = []

    for entry in feed.entries:
        articles_data.append({
            "title": entry.title,
            "link": entry.link,
            "published_at": datetime.fromisoformat(entry.published),
            # We use a lambda function here so we ONLY download the transcript if the video is new
            "content_fetcher": lambda link=entry.link: get_youtube_transcript(link)
        })
    return articles_data

def scrape_blog(source):
    """Parses standard web RSS feeds and extracts clean HTML text."""
    feed = feedparser.parse(source.url)
    articles_data = []

    for entry in feed.entries:
        # Safely parse the blog date (blogs use weird date formats sometimes)
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        else:
            pub_date = datetime.now(timezone.utc)

        # Look for the actual article content in the feed
        content_html = ""
        if 'content' in entry:
            content_html = entry.content[0].value
        elif 'summary' in entry:
            content_html = entry.summary

        articles_data.append({
            "title": entry.title,
            "link": entry.link,
            "published_at": pub_date,
            # BeautifulSoup strips away all the messy <div> and <img> tags, leaving just text
            "content_fetcher": lambda html=content_html: BeautifulSoup(html, "html.parser").get_text(separator=' ', strip=True) if html else "No content available."
        })
    return articles_data

def run_scraper():
    """The main engine that loops through your database sources."""
    db = SessionLocal()
    print("🚀 Starting Daily Scraper Engine...")

    # 1. Ask the database what sources we are tracking today
    sources = db.query(Source).all()
    
    # 2. Set the 24-hour cutoff rule
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    added = 0

    try:
        for source in sources:
            print(f"📡 Checking {source.name}...")
            
            # Route to the correct logic
            if source.type == "youtube":
                items = scrape_youtube(source)
            else:
                items = scrape_blog(source)

            for item in items:
                # 3. Apply the 24-hour rule
                if item["published_at"] > cutoff:
                    # 4. Check if we already scraped this specific link
                    existing = db.query(Article).filter(Article.link == item["link"]).first()
                    
                    if not existing:
                        print(f"  -> Fetching text for: {item['title'][:40]}...")
                        
                        # Save it to Supabase!
                        new_article = Article(
                            title=item["title"],
                            link=item["link"],
                            published_at=item["published_at"],
                            content=item["content_fetcher"](),
                            source_id=source.id
                        )
                        db.add(new_article)
                        added += 1
                        
        db.commit()
        print(f"✅ Success! Added {added} fresh articles to Supabase.")
        
    finally:
        db.close()

if __name__ == "__main__":
    run_scraper()