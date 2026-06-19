import os
import uuid
import requests
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, HttpUrl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Module 21 AI Agent Backend",
    description="FastAPI Backend integration with n8n workflow for scraping, summarizing, and logging articles.",
    version="1.0.0"
)

# CORS configurations so frontend (Streamlit) can call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo purposes, allow all origins. Can be restricted to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read environment variables
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")
N8N_WEBHOOK_SECRET = os.getenv("N8N_WEBHOOK_SECRET", "")

def check_configuration():
    """Validates that n8n webhook environment variables are properly configured."""
    if not N8N_WEBHOOK_URL or "PASTE_MY_ACTIVE_N8N" in N8N_WEBHOOK_URL or N8N_WEBHOOK_URL.strip() == "":
        return "N8N_WEBHOOK_URL is not set or still contains the placeholder value"
    if not N8N_WEBHOOK_SECRET or "PASTE_MY_N8N_HEADER" in N8N_WEBHOOK_SECRET or N8N_WEBHOOK_SECRET.strip() == "":
        return "N8N_WEBHOOK_SECRET is not set or still contains the placeholder value"
    return None

# Pydantic models for request validation
class ArticleProcessRequest(BaseModel):
    email: EmailStr
    article_url: HttpUrl

# Custom request validation handler for clean, beginner-friendly error messages
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        # Clean up the field name location path
        field = error["loc"][-1] if error["loc"] else "field"
        msg = error["msg"]
        errors.append(f"Invalid {field}: {msg}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "detail": "Validation Error",
            "errors": errors
        }
    )

@app.get("/")
def read_root():
    """Simple API root check endpoint."""
    return {
        "message": "Welcome to the Module 21 AI Agent Backend API!",
        "status": "online",
        "endpoints": {
            "GET /": "API Health check & welcome",
            "POST /process-article": "Process user email and article url, then forward to n8n workflow"
        }
    }

@app.post("/process-article")
def process_article(payload: ArticleProcessRequest):
    """
    Receives email and article_url from the frontend, generates a UUID session_id,
    and forwards the payload with authorization headers to the active n8n webhook.
    """
    # 1. Verify environment configuration
    config_error = check_configuration()
    if config_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration Error: {config_error}. Please configure the .env file in the backend directory."
        )

    # 2. Generate a unique session_id using UUID4
    session_id = str(uuid.uuid4())

    # 3. Form the payload to forward to n8n webhook
    n8n_payload = {
        "email": payload.email,
        "article_url": str(payload.article_url),
        "session_id": session_id
    }

    # 4. Set Header Authentication when sending request to n8n
    headers = {
        "x-agent-secret": N8N_WEBHOOK_SECRET,
        "Content-Type": "application/json"
    }

    # 5. Forward request to n8n webhook
    try:
        # n8n executes: Webhook -> Scrape -> Groq Summary/Insights -> Sheets -> Email -> Respond.
        # This execution might take 10-25 seconds, so we set a generous timeout of 35 seconds.
        response = requests.post(
            N8N_WEBHOOK_URL,
            json=n8n_payload,
            headers=headers,
            timeout=35.0
        )
        
        # Handle non-successful responses from n8n
        if not response.ok:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"n8n webhook error (Status {response.status_code}): {response.text}"
            )
        
        # Try to parse JSON response, fallback to text if n8n response is plain text
        try:
            n8n_data = response.json()
        except ValueError:
            n8n_data = {"message": response.text}

        # Return session_id along with the response from n8n back to frontend
        return {
            "status": "success",
            "session_id": session_id,
            "n8n_response": n8n_data
        }

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The connection to the n8n webhook timed out. The workflow execution took too long to respond."
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to communicate with n8n webhook: {str(e)}"
        )
