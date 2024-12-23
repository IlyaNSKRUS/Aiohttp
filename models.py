import os
import datetime
import uuid
from typing import List, Type

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import  Integer, String, DateTime, Date, ForeignKey, func, UUID


POSTGRES_DB = os.getenv("POSTGRES_DB", "netology_aiohttp_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "qwerty12")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):

    @property
    def id_dict(self):
        return {'id': self.id}


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(72), nullable=False)
    email: Mapped[str] = mapped_column(String(72), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    tokens: Mapped[List["Token"]] = relationship(
        "Token", back_populates="user", cascade="all, delete-orphan"
    )
    advs: Mapped[List["Advertisement"]] = relationship(
        "Advertisement", back_populates="user", cascade="all, delete-orphan"
    )


    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'registration_time': self.registration_time.isoformat(),
            'advertisement': [advs.id for advs in self.advs]
        }

    @property
    def dict_id(self):
        return {
            'id': self.id
        }

class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, server_default=func.gen_random_uuid(), unique=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("app_user.id"))
    user: Mapped[User] = relationship(User, back_populates="tokens")

    @property
    def dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "user_id": self.user_id
        }

class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    heading: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    creator: Mapped[int] = mapped_column(Integer, ForeignKey('app_user.id'), nullable=False)
    date_creation: Mapped[datetime.date] = mapped_column(Date, server_default=func.current_date())

    # user = relationship(User, backref='adv')
    user: Mapped[User] = relationship(User, back_populates="advs")

    @property
    def dict(self):
        return {
            'id': self.id,
            'heading': self.heading,
            'description': self.description,
            'date_creation': self.date_creation.isoformat(),
            'creator': self.creator,
        }

MODEL_TYPE = Type[User | Token | Advertisement]
MODEL = User | Token | Advertisement

async def init_orm():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()
























