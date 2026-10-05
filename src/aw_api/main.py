from fastapi import FastAPI
from aw_api.routers import jobcandidates, employees, products

app = FastAPI()

# NOTE: this is where the routers are added from, no longer is the router in the main.py
app.include_router(employees.router)
app.include_router(jobcandidates.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "Hello, AdventureWorks"}