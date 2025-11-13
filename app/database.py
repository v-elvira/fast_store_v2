# --------------- Асинхронное подключение к PostgreSQL -------------------------

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Строка подключения для PostgreSQl
DATABASE_URL = "postgresql+asyncpg://ecommerce_user:eco@localhost:5432/ecommerce_db"
#               postgresql+asyncpg://username:password@host:port/database

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


## alembic init -t async app/migrations   # for async alembic


# --------------- Синхронное подключение к SQLite -------------------------

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase

# # Строка подключения для SQLite
# DATABASE_URL = "sqlite:///ecommerce.db"      # relative path
# ## sqlite:////absolute/path/to/ecommerce.db  # absolute path example
# # dialect+driver://username:password@host:port/database
#
# # Создаём Engine
# engine = create_engine(DATABASE_URL, echo=True)
#
# # Настраиваем фабрику сеансов
# SessionLocal = sessionmaker(bind=engine)


# Определяем базовый класс для моделей
class Base(DeclarativeBase):
    pass
