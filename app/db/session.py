from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://fa_user:fa_password@db/product_fa")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """dependency db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
