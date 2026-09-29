from fastapi import FastAPI
from aw_api.routers import jobcandidates, employees, products

app = FastAPI()

app.include_router(employees.router)
app.include_router(jobcandidates.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Hello, AdventureWorks"}