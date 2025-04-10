from sqlalchemy import Column, ForeignKey
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from app.database.db import engine

Base = sqlalchemy.orm.declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    register_date: Mapped[datetime] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default='user')

class Tasks(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    created_by: Mapped[str] = mapped_column(ForeignKey('users.username'), nullable=True)
    finished_by: Mapped[str] = mapped_column(ForeignKey('users.username'), nullable=True, default=None)
    date_of_start: Mapped[datetime] = mapped_column(nullable=False)
    date_of_finish: Mapped[datetime] = mapped_column(default=None, nullable=True)

