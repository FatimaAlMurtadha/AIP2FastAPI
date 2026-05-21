from fastapi import FastAPI
from app.routs.issues import router as issues_router


app = FastAPI()


@app.get("/")
def health_check():
    return {"Status": "OK"}


app.include_router(issues_router)