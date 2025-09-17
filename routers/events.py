from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json
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

def format_event_date(date_str):
    """Format event date for display"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except ValueError:
        return date_str

@router.get("/", response_class=HTMLResponse)
async def events(request: Request):
    """Events page route"""
    events_data = load_events()
    
    # Format dates for display
    upcoming_events = events_data.get("upcoming", [])
    past_events = events_data.get("past", [])
    
    for event in upcoming_events + past_events:
        event["formatted_date"] = format_event_date(event["date"])
    
    # Sort upcoming events by date (earliest first)
    upcoming_events.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
    
    # Sort past events by date (most recent first)
    past_events.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    
    context = {
        "request": request,
        "page_title": "Events - MLSC MGMCOET",
        "upcoming_events": upcoming_events,
        "past_events": past_events
    }
    
    return templates.TemplateResponse("events.html", context)
