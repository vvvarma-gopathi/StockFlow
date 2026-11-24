from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.dependencies.database import Base, engine
from app.config import FRONTEND_ORIGINS
from app.routes.auth import router as auth_router
from app.routes.dashboard import router as dashboard_router
from app.routes.products import router as products_router
from app.routes.settings import router as settings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if engine is not None:
        Base.metadata.create_all(bind=engine)
    yield
    if engine is not None:
        engine.dispose()

app = FastAPI(title="StockFlow API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-liard-alpha-26.vercel.app",
        "https://stockflow-vishnuvardhangopathi-6448.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(settings_router, prefix="/api")

@app.get("/")
def root():
    return {"APP": "StockFlow MVP"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
