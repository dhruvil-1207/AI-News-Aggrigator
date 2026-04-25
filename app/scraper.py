# app/scraper.py
import feedparser
from datetime import datetime
from app.database import SessionLocal
from app.models import Source, Article

def get_latest_youtube_videos(channel_id):
    """Fetches the latest videos from a YouTube channel using its RSS feed."""
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    
    videos = []
    for entry in feed.entries:
        videos.append({
            "title": entry.title,
            "link": entry.link,
            # We convert the string date to a real Python datetime object for PostgreSQL
            "published_at": datetime.fromisoformat(entry.published) 
        })
    return videos

def save_videos_to_db(videos, channel_name, channel_id):
    """Saves videos to PostgreSQL, ensuring no duplicates."""
    db = SessionLocal()
    
    try:
        # 1. Check if the YouTube channel (Source) exists in DB. If not, add it.
        source = db.query(Source).filter(Source.url == channel_id).first()
        if not source:
            source = Source(name=channel_name, type="youtube", url=channel_id)
            db.add(source)
            db.commit()
            db.refresh(source)
            print(f"Created new source: {channel_name}")
        
        # 2. Add videos, but ONLY if the link doesn't already exist
        added_count = 0
        for video in videos:
            existing_article = db.query(Article).filter(Article.link == video['link']).first()
            
            if not existing_article:
                new_article = Article(
                    title=video['title'],
                    link=video['link'],
                    published_at=video['published_at'],
                    source_id=source.id
                )
                db.add(new_article)
                added_count += 1
                
        db.commit()
        print(f"Successfully added {added_count} NEW videos to the database!")
        
    finally:
        # Always close the database connection
        db.close()

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_channel_id = "UCBJycsmduvYEL83R_U4JriQ" 
    channel_name = "Marques Brownlee"
    
    print(f"Fetching latest videos for {channel_name}...")
    latest_videos = get_latest_youtube_videos(test_channel_id)
    
    print("Saving to database...")
    save_videos_to_db(latest_videos, channel_name, test_channel_id)