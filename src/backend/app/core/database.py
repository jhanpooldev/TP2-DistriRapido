from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

settings = get_settings()

def get_database_url(test: bool = False) -> str:
    db_name = settings.DB_NAME_TEST if test else settings.DB_NAME
    return f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}"

engine = create_engine(get_database_url(), pool_pre_ping=True)
TestingEngine = create_engine(get_database_url(test=True), pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestingEngine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(test: bool = False):
    Base.metadata.create_all(bind=TestingEngine if test else engine)