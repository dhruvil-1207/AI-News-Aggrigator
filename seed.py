# seed.py
from app.database import SessionLocal
from app.models import Source

def seed_sources():
    db = SessionLocal()
    try:
        # 1. Define the YouTube Source
        mkbhd = Source(name="Marques Brownlee", type="youtube", url="UCBJycsmduvYEL83R_U4JriQ")
        
        # 2. Define the Blog Source
        techcrunch = Source(name="TechCrunch", type="blog", url="https://techcrunch.com/feed/")

        # 3. Add them safely (checking if they already exist so it doesn't crash)
        if not db.query(Source).filter(Source.url == mkbhd.url).first():
            db.add(mkbhd)
            
        if not db.query(Source).filter(Source.url == techcrunch.url).first():
            db.add(techcrunch)

        db.commit()
        print("✅ Seed data added! Your sources are now in Supabase.")
        
    finally:
        db.close()

if __name__ == "__main__":
    seed_sources()