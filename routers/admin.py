from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json
import os
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Admin PIN - Change this to your desired PIN
ADMIN_PIN = "2025"

def verify_pin(pin: str) -> bool:
    """Verify if the provided PIN is correct"""
    return pin == ADMIN_PIN

def load_events():
    """Load events from events.json file"""
    try:
        with open("data/events.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"upcoming": [], "past": []}

def save_events(events_data):
    """Save events to events.json file"""
    try:
        with open("data/events.json", "w") as f:
            json.dump(events_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving events: {e}")
        return False

@router.get("/login", response_class=HTMLResponse)
async def admin_login(request: Request):
    """Admin login page"""
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/login")
async def admin_login_post(request: Request, pin: str = Form(...)):
    """Handle admin login"""
    if verify_pin(pin):
        response = RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="admin_authenticated", value="true", max_age=3600)  # 1 hour
        return response
    else:
        return templates.TemplateResponse("admin/login.html", {
            "request": request, 
            "error": "Invalid PIN. Please try again."
        })

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard"""
    # Check authentication
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    events_data = load_events()
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "upcoming_events": events_data.get("upcoming", []),
        "past_events": events_data.get("past", [])
    })

@router.get("/add-event", response_class=HTMLResponse)
async def add_event_form(request: Request):
    """Add event form"""
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    return templates.TemplateResponse("admin/add_event.html", {"request": request})

@router.post("/add-event")
async def add_event(
    request: Request,
    title: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    venue: str = Form(...),
    description: str = Form(...),
    event_type: str = Form(...),  # "upcoming" or "past"
    registration_link: str = Form(None),
    gallery_link: str = Form(None),
    attendees: int = Form(None),
    image: str = Form(None)
):
    """Add a new event"""
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    events_data = load_events()
    
    new_event = {
        "title": title,
        "date": date,
        "time": time,
        "venue": venue,
        "description": description,
        "organizer": "MLSC MGMCOET"
    }
    
    if image:
        new_event["image"] = image
    
    if event_type == "upcoming":
        if registration_link:
            new_event["registration_link"] = registration_link
        events_data["upcoming"].append(new_event)
    else:  # past event
        if gallery_link:
            new_event["gallery_link"] = gallery_link
        if attendees:
            new_event["attendees"] = attendees
        events_data["past"].append(new_event)
    
    if save_events(events_data):
        return RedirectResponse(url="/admin/dashboard?success=Event added successfully", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("admin/add_event.html", {
            "request": request,
            "error": "Failed to save event. Please try again."
        })

@router.get("/edit-event/{event_type}/{event_index}", response_class=HTMLResponse)
async def edit_event_form(request: Request, event_type: str, event_index: int):
    """Edit event form"""
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    events_data = load_events()
    
    if event_type not in ["upcoming", "past"]:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    events_list = events_data.get(event_type, [])
    if event_index >= len(events_list):
        raise HTTPException(status_code=404, detail="Event not found")
    
    event = events_list[event_index]
    
    return templates.TemplateResponse("admin/edit_event.html", {
        "request": request,
        "event": event,
        "event_type": event_type,
        "event_index": event_index
    })

@router.post("/edit-event/{event_type}/{event_index}")
async def edit_event(
    request: Request,
    event_type: str,
    event_index: int,
    title: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    venue: str = Form(...),
    description: str = Form(...),
    registration_link: str = Form(None),
    gallery_link: str = Form(None),
    attendees: int = Form(None),
    image: str = Form(None)
):
    """Update an existing event"""
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    events_data = load_events()
    
    if event_type not in ["upcoming", "past"]:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    events_list = events_data.get(event_type, [])
    if event_index >= len(events_list):
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update event
    events_list[event_index].update({
        "title": title,
        "date": date,
        "time": time,
        "venue": venue,
        "description": description,
        "organizer": "MLSC MGMCOET"
    })
    
    if image:
        events_list[event_index]["image"] = image
    
    if event_type == "upcoming":
        if registration_link:
            events_list[event_index]["registration_link"] = registration_link
        elif "registration_link" in events_list[event_index]:
            del events_list[event_index]["registration_link"]
    else:  # past event
        if gallery_link:
            events_list[event_index]["gallery_link"] = gallery_link
        if attendees:
            events_list[event_index]["attendees"] = attendees
    
    if save_events(events_data):
        return RedirectResponse(url="/admin/dashboard?success=Event updated successfully", status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse("admin/edit_event.html", {
            "request": request,
            "event": events_list[event_index],
            "event_type": event_type,
            "event_index": event_index,
            "error": "Failed to update event. Please try again."
        })

@router.post("/delete-event/{event_type}/{event_index}")
async def delete_event(request: Request, event_type: str, event_index: int):
    """Delete an event"""
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    events_data = load_events()
    
    if event_type not in ["upcoming", "past"]:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    events_list = events_data.get(event_type, [])
    if event_index >= len(events_list):
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Remove event
    events_list.pop(event_index)
    
    if save_events(events_data):
        return RedirectResponse(url="/admin/dashboard?success=Event deleted successfully", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/admin/dashboard?error=Failed to delete event", status_code=status.HTTP_302_FOUND)

@router.post("/move-event/{event_type}/{event_index}")
async def move_event(request: Request, event_type: str, event_index: int):
    """Move event between upcoming and past"""
    if request.cookies.get("admin_authenticated") != "true":
        return RedirectResponse(url="/admin/login")
    
    events_data = load_events()
    
    if event_type not in ["upcoming", "past"]:
        raise HTTPException(status_code=404, detail="Event type not found")
    
    source_list = events_data.get(event_type, [])
    if event_index >= len(source_list):
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Move event
    event = source_list.pop(event_index)
    target_type = "past" if event_type == "upcoming" else "upcoming"
    
    # Clean up event data based on target type
    if target_type == "past":
        # Remove registration_link if moving to past
        if "registration_link" in event:
            del event["registration_link"]
    else:
        # Remove past-specific fields if moving to upcoming
        if "attendees" in event:
            del event["attendees"]
        if "gallery_link" in event:
            del event["gallery_link"]
    
    events_data[target_type].append(event)
    
    if save_events(events_data):
        return RedirectResponse(url="/admin/dashboard?success=Event moved successfully", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(url="/admin/dashboard?error=Failed to move event", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
async def admin_logout(request: Request):
    """Admin logout"""
    response = RedirectResponse(url="/admin/login?message=Logged out successfully", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="admin_authenticated")
    return response
