from fastapi import FastAPI

from db.base import Base
from db.session import engine
from routers import fruits, orders, users

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(fruits.router)
app.include_router(orders.router)
app.include_router(users.router)
