from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Import the middleware
from pathlib import Path
from recommendation_engine import generate_recommendation, get_prospect_data
import os
import pandas as pd
from pydantic import BaseModel

# Define input data model
class ProspectInput(BaseModel):
    name: str
    transcript: str = None  # Transcript is optional

# Initialize FastAPI
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up templates and static files
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mock data
DATA_PATH = "expanded_mock_data.csv"
data = pd.read_csv(DATA_PATH)

@app.get("/")
def read_root():
    """
    Serve the frontend page.
    """
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/prospects")
def get_prospects():
    """
    Get a list of all prospects.
    """
    try:
        return {"prospects": data["Prospect Name"].tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading prospects: {str(e)}")

@app.post("/recommend")
def recommend_post(prospect: ProspectInput):
    """
    Generate a recommendation for a specific prospect.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    name = prospect.name
    transcript = prospect.transcript

    prospect_data = get_prospect_data(name)

    if not prospect_data:
        raise HTTPException(status_code=404, detail="Prospect not found")

    try:
        recommendation = generate_recommendation(api_key, prospect_data, transcript)
        return recommendation  # Return the structured response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")