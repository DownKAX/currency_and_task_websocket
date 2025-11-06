from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

BASE_URL = settings.DATABASE_URL
engine = create_async_engine(BASE_URL, echo=False) #echo - показывает сгенерированные SQL-запросы
AsyncSessionMaker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
#expire_on_commit позволяет данным оставаться доступным для чтения,
#которые были добавлены в бд, посокольку они остаются в объекте(не требуют запроса к SQL db)

async def get_db():
    async with AsyncSessionMaker() as session:
        yield session