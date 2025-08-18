from fastapi import FastAPI
from .database import Base, engine
from .routers import employees, leaves, health, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Leave Management System")

app.include_router(employees.router)
app.include_router(leaves.router)
app.include_router(health.router)
app.include_router(auth.router)