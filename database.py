from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings  # Settings sınıfını içe aktar

# SQLAlchemy için bağlantı URL'sini oluştur
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

# Veritabanı motoru oluştur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Oturum oluşturma sınıfı
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı taban sınıfı
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
