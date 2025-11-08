from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Строка подключения для SQLite
DATABASE_URL = "sqlite:///ecommerce.db"      # relative path
## sqlite:////absolute/path/to/ecommerce.db  # absolute path example
# dialect+driver://username:password@host:port/database

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)

# Определяем базовый класс для моделей
class Base(DeclarativeBase):
    pass
