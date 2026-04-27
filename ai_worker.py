# ai_worker.py
import os
import time
from google import genai
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models import Article

# Load the API key from .env
load_dotenv()

# Modern client initialization
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_article(text):
    """Sends the raw text to Gemini with strict formatting rules."""
    prompt = f"""
    You are an expert tech newsletter editor. Summarize the following text.
    You MUST format your response exactly like this, with nothing else:
    
    Title: [A Catchy, Engaging Headline]
    * [First punchy bullet point summarizing a key takeaway]
    * [Second punchy bullet point summarizing another key takeaway]
    
    Here is the text to summarize:
    {text}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error communicating with AI: {e}")
        return None

def run_ai_processor():
    db = SessionLocal()
    print("🧠 Starting AI Processor...")

    # Find all articles where the ai_summary column is empty
    unprocessed_articles = db.query(Article).filter(Article.ai_summary == None).all()
    
    if not unprocessed_articles:
        print("✅ All articles are already summarized. Nothing to do!")
        db.close()
        return

    print(f"Found {len(unprocessed_articles)} articles to summarize.")

    for article in unprocessed_articles:
        print(f"  -> Summarizing: {article.title[:40]}...")
        
        
        if not article.content or len(article.content) < 50:
            article.ai_summary = "Content too short to summarize."
            continue

        summary = summarize_article(article.content)
        
        if summary:
            article.ai_summary = summary
            db.commit() 
            print("✅ AI Processing complete! Your newsletter content is ready.")
            
        # pause to avoid free-tier rate limit
        time.sleep(15)

    db.close()

if __name__ == "__main__":
    run_ai_processor()