from fastapi import FastAPI
from routes.login_route import router as login_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(login_router, prefix="/api/auth")