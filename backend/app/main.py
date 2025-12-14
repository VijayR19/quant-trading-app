from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.routers import auth, predict

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Quant Trading App")

app.middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router)
app.include_router(predict.router)

@app.get("/")
def health():
    return {"status": "ok"}