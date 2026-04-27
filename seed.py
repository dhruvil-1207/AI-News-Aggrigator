from app.database import SessionLocal
from app.models import Source

def seed_sources():
    db = SessionLocal()
    try:
        # --- YouTube Sources ---
        # 1. Fireship (Fast-paced Developer News)
        fireship = Source(name="Fireship", type="youtube", url="UCsBjURrPoezykLs9EqgamOA")
        
        # 2. Matt Wolfe (Daily AI News & Tools)
        matt_wolfe = Source(name="Matt Wolfe", type="youtube", url="UCkBvlZiahy21q2T1z21A70g")
        
        # --- Blog/Article Sources ---
        # 3. TechCrunch (Startup & Tech Business)
        techcrunch = Source(name="TechCrunch", type="blog", url="https://techcrunch.com/feed/")
        
        # 4. The Verge (Tech & Gadgets)
        the_verge = Source(name="The Verge", type="blog", url="https://www.theverge.com/rss/index.xml")
        
        # 5. Wired AI (Deep-dive AI Journalism)
        wired_ai = Source(name="Wired AI", type="blog", url="https://www.wired.com/feed/category/artificial-intelligence/latest/rss")

        sources_to_add = [fireship, matt_wolfe, techcrunch, the_verge, wired_ai]

        # Add them safely (checking if they already exist)
        for source in sources_to_add:
            if not db.query(Source).filter(Source.url == source.url).first():
                db.add(source)

        db.commit()
        print("✅ Seed data completely updated! Your high-signal sources are locked in.")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_sources()