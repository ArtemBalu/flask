import atexit
import datetime

from sqlalchemy import DateTime, String, create_engine, func, Column, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

POSTGRES_PASSWORD = '00000'
POSTGRES_USER = 'postgres'
POSTGRES_DB = 'flasktest'
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = '5432'


PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    notes = relationship('Note', back_populates='owner')

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "registration_time": self.registration_time.isoformat()
        }


class Note(Base):
    __tablename__ = "app_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), index=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('app_users.id'))
    owner = relationship('User', back_populates='notes')
    
    @property
    def dict(self):
        return {
            "id": self.id,
            "header": self.header,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner_id": self.owner_id
        }

Base.metadata.create_all(bind=engine)