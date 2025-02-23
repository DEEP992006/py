from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google GenAI Client
client = genai.Client(api_key=os.getenv("MY_API_KEY"))

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["mydatabase"]  # Replace with your database name
users_collection = db["users"]  # Users collection

# Pydantic model for user registration
class RegisterUser(BaseModel):
    email: str

# Route to store email in MongoDB (without bson)
@app.post("/register")
async def register_user(user: RegisterUser):
    # Check if email already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Insert new user
    user_doc = {"email": user.email}
    result = await users_collection.insert_one(user_doc)
    
    return {"message": "User registered successfully", "id": str(result.inserted_id)}

# Route to generate content using Google GenAI
@app.get("/{d}")
async def generate_content(d: str):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=d,
    )
    return {"message": response.text}  # Return response text properly

# Default route to check API status
@app.get("/")
async def read_root():
    return {"message": "Hi deep"}
