from fastapi import FastAPI, HTTPException, status
from datetime import date
from pydantic import BaseModel
from models import PriceHistory, engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

class Indexes(BaseModel):
    sec_id: str
    trade_date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float

@app.get("/indexes_value", response_model=list[Indexes])

def get_indexes_value(sec_id, trade_date:date | None=None):
    session = SessionLocal()
    answer = select(PriceHistory).where(
    PriceHistory.sec_id == sec_id
    )
    if trade_date is not None:
        answer = select(PriceHistory).where(
        PriceHistory.sec_id == sec_id, PriceHistory.trade_date==trade_date
        )

    answer = session.execute(answer).scalars().all()
    #if not answer:
        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запрашиваемые данные не найдены")
    session.close()
    return answer





