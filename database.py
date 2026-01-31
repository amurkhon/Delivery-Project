import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection for database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
