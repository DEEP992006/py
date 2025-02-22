from fastapi import FastAPI, Depends, HTTPException, Header
from google import genai
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os
app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables from .env file

load_dotenv()

# Initialize the Gemini AI client
client = genai.Client(api_key=os.getenv("MY_API_KEY"))

@app.get("/{d}")  # Corrected route parameter
async def read_root(d:str):  # Accept 'd' as a function parameter
    response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=d,)
    return {"message": response.text}  # Return response text properly
@app.get("/")
async def read_root():
    return {"message": "Hi"}