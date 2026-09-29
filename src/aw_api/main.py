from fastapi import FastAPI
from aw_api.routers import jobcandidates, employees

app = FastAPI()

app.include_router(employees.router)
app.include_router(jobcandidates.router)