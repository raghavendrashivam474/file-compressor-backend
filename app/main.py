from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import image, pdf, video  # ← Add video
import uvicorn

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
app.include_router(video.router, prefix="/api/v1")  # ← Add this

@app.get("/")
def root():
    return {"message": "File Compressor API Running 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)