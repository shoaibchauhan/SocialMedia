import os
import django
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Set the default settings module for the Django environment

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
# Initialize Django

django.setup()

from fastapi import FastAPI,Request
from myapp.router import router


app = FastAPI()



app.mount("/static", StaticFiles(directory="myapp/static"), name="static")

# Mount templates directory
templates = Jinja2Templates(directory="myapp/templates")

# Include API routes
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
