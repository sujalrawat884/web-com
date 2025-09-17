from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

# Import routers
from routers import home, events, about, admin

# Create FastAPI app instance
app = FastAPI(
    title="MLSC MGMCOET Community Website",
    description="Official website for Microsoft Learn Student Community at MGMCOET",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(home.router, tags=["home"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(about.router, prefix="/about", tags=["about"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# Root redirect to home
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "MLSC MGMCOET website is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
