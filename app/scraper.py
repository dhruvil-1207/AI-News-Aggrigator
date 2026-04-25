import feedparser

def get_latest_youtube_videos(channel_id):
    """
    Fetches the latest videos from a given YouTube channel using its RSS feed.
    """
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    # feedparser does all the heavy lifting of reading the XML data
    feed = feedparser.parse(feed_url)
    
    videos = []
    
    # Loop through the entries and grab what we need
    for entry in feed.entries:
        videos.append({
            "title": entry.title,
            "link": entry.link,
            "published_at": entry.published
        })
        
    return videos

# --- TESTING BLOCK ---
if __name__ == "__main__":
    test_channel_id = "UCBJycsmduvYEL83R_U4JriQ" 
    
    print(f"Fetching latest videos for channel: {test_channel_id}...\n")
    
    latest_videos = get_latest_youtube_videos(test_channel_id)
    
    if not latest_videos:
        print("Whoops! Still getting nothing. The feed might be empty or failing.")
    
    # Print out the top 3 most recent videos to the terminal
    for video in latest_videos[:3]:
        print(f"Title: {video['title']}")
        print(f"Link: {video['link']}")
        print(f"Date: {video['published_at']}")
        print("-" * 40)