from fastapi import FastAPI
from routes.login_route import router as login_router
from routes.profile_route import router as profile_router
from routes.report_problem_route import router as report_router


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(login_router, prefix="/api/auth")
app.include_router(profile_router, prefix="/api/profile")
app.include_router(report_router, prefix="/api/report")