from app.database import engine, Base
from app.models import Source, Article

def init_database():
    print("Creating database tables...")
    # This command creates all the tables defined in our models
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_database()