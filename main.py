import requests

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from models import Base, engine, PriceHistory
from datetime import timedelta, date

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

indexes = [
    "IMOEX",
    "RTSI",
    "MOEXBC",
]

for index in indexes:
    needed_date = select(func.max(PriceHistory.trade_date)).where(PriceHistory.sec_id == index)
    max_date = session.scalar(needed_date)

    if max_date == None:
        used_date = date.today() - timedelta(days=30)
    else:
        added_time = timedelta(days=1)
        used_date = max_date+added_time


    params = {
            "from":used_date,
            "limit":100,
            "sort_order":"TRADEDATE",
            "iss.meta":"off",
            "iss.json":"extended",
            "lang":"ru"
            }

    url = 'https://iss.moex.com/iss/history/engines/stock/markets/index/securities/' + index + '.json'
    response = requests.get(
        url=url, params=params
    )

    response.raise_for_status()

    data = response.json()


    for record in data[1]["history"]:
        price = PriceHistory(
            sec_id=record["SECID"],
            trade_date=record["TRADEDATE"],
            open_price=record["OPEN"],
            high_price=record["HIGH"],
            low_price=record["LOW"],
            close_price=record["CLOSE"],
        )

        session.add(price)

    session.commit()
session.close()

