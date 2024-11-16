from fastapi import FastAPI
from routes.login import router as login_router
from routes.properties import router as property_router
from routes.profiles import router as profile_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(login_router, prefix="/api/auth")
app.include_router(property_router, prefix="/api/properties")
app.include_router(profile_router, prefix="/api/profile")