from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
import os
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def load_events():
    """Load events from events.json file"""
    try:
        with open("data/events.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"upcoming": [], "past": []}

def get_next_event():
    """Get the next upcoming event"""
    events_data = load_events()
    upcoming_events = events_data.get("upcoming", [])
    
    if not upcoming_events:
        return None
    
    # Sort by date and return the earliest upcoming event
    upcoming_events.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
    return upcoming_events[0] if upcoming_events else None

@router.get("/", response_class=HTMLResponse)
@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """Home page route"""
    next_event = get_next_event()
    
    context = {
        "request": request,
        "page_title": "Home - MLSC MGMCOET",
        "next_event": next_event
    }
    
    return templates.TemplateResponse("home.html", context)
