from datetime import date

from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv
import os

load_dotenv()
database_url = os.getenv('DATABASE_URL')

engine = create_engine(database_url)


class Base(DeclarativeBase):
    pass


class PriceHistory(Base):
    __tablename__ = "price_history"
    __table_args__ = (UniqueConstraint('sec_id', 'trade_date', name='unique_index_index'),)
    id: Mapped[int] = mapped_column(primary_key=True)
    sec_id: Mapped[str]
    trade_date: Mapped[date]
    open_price: Mapped[float]
    high_price: Mapped[float]
    low_price: Mapped[float]
    close_price: Mapped[float]