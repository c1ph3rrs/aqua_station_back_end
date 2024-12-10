from fastapi import FastAPI
from routes.login_route import router as login_router
from routes.profile_route import router as profile_router
from routes.report_problem_route import router as report_router
from routes.vending_machine_route import router as vending_machine_router
from routes.configurations_route import router as configuration_route
from routes.recharge_route import router as recharge_route


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(login_router, prefix="/api/auth")
app.include_router(profile_router, prefix="/api/profile")
app.include_router(report_router, prefix="/api/report")
app.include_router(vending_machine_router, prefix="/api/machines")
app.include_router(configuration_route, prefix="/api/configurations")
app.include_router(recharge_route, prefix="/api/recharge_balance")