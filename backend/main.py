from fastapi import FastAPI
from app.api.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


