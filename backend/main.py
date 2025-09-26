from fastapi import FastAPI
from app.api.router import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.core.paths import MEDIA_DIR
app = FastAPI()
# Serve files at /media/* from MEDIA_DIR
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# TODO
origins = [
    "http://localhost:3000",   # local dev
    "https://myfrontend.vercel.app",  # deployed frontend
    
    #App Dev
    "http://196.177.137.59:3000",     # your IP + port (if frontend runs on 3000)
    "http://196.177.137.59",          # default HTTP (port 80)
    "https://196.177.137.59",         # default HTTPS (port 443)
    
]

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)