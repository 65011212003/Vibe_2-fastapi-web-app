from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["pages"])

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the index page."""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "FastAPI Web App"}
    )

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Render the about page."""
    return templates.TemplateResponse(
        "about.html", 
        {"request": request, "title": "About"}
    )

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Render the login page."""
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Login"}
    )

@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """Render the registration page."""
    return templates.TemplateResponse(
        "register.html", 
        {"request": request, "title": "Register"}
    )

@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    """Render the user profile page."""
    return templates.TemplateResponse(
        "profile.html", 
        {"request": request, "title": "Profile"}
    )

@router.get("/items", response_class=HTMLResponse)
async def items(request: Request):
    """Render the items management page."""
    return templates.TemplateResponse(
        "items.html", 
        {"request": request, "title": "Item Management"}
    ) 