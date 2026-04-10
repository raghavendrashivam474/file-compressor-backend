from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import image, pdf, video
import uvicorn
import os

app = FastAPI(title="File Compressor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(image.router, prefix="/api/v1")
app.include_router(pdf.router, prefix="/api/v1")
app.include_router(video.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "File Compressor API Running 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)