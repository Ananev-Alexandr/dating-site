from fastapi import FastAPI

from app.routers.matches.matches_routers import router as match_router
from app.routers.users.user_routers import router as user_router

app = FastAPI()


app.include_router(user_router)
app.include_router(match_router)
