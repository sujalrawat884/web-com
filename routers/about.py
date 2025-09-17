from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def load_team_data():
    """Load team data from team.json file"""
    try:
        with open("data/team.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"leadership": [], "teams": {}}

@router.get("/", response_class=HTMLResponse)
async def about(request: Request):
    """About page route"""
    team_data = load_team_data()
    
    # Get leadership and teams data
    leadership = team_data.get("leadership", [])
    teams = team_data.get("teams", {})
    
    # Define team order for consistent display
    team_order = [
        "UI/UX Design",
        "Social Media",
        "CP & DSA",
        "PR & Partnership", 
        "Event Management",
        "Web Development"
    ]
    
    # Organize teams in the specified order
    organized_teams = []
    for team_name in team_order:
        if team_name in teams:
            organized_teams.append({
                "name": team_name,
                "members": teams[team_name]
            })
    
    context = {
        "request": request,
        "page_title": "About Us - MLSC MGMCOET",
        "leadership": leadership,
        "teams": organized_teams
    }
    
    return templates.TemplateResponse("about.html", context)
