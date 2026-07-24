from contextlib import asynccontextmanager
from app.core.database import get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.ticket_routes import router as ticket_router
from app.api.ai import router as ai_router
from app.core.config import settings
from app.core.database import Base, engine

# Importing the model registers the tickets table
from app.models.ticket import Ticket  # noqa: F401



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Ticket CRUD API for AI Service Desk",
    lifespan=lifespan
)


app.include_router(ticket_router)
app.include_router(ai_router)


@app.get("/", tags=["Root"])
def home():
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
        "documentation": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "ok"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )