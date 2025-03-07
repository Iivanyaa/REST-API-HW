import asyncpg
import config
import atexit
import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped


engine = create_async_engine(config.PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    
    @property
    def id_dict(self):
        return {"id": self.id}


class Advertisment(Base):
    __tablename__ = "advertisments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Title: Mapped[str] = mapped_column(String, nullable=False)
    Price: Mapped[int] = mapped_column(Integer, nullable=False)
    Description: Mapped[str] = mapped_column(String, nullable=False)
    Author: Mapped[str] = mapped_column(String, nullable=False)
    Create_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    

    @property
    def dict(self):
        return {
            "id": self.id,
            "Title": self.Title,
            "Price": self.Price,
            "Description": self.Description,
            "Author": self.Author,
            "Create_time": self.Create_time.isoformat()
        }


ORM_OBJ = Advertisment
ORM_CLS = type[Advertisment]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()


