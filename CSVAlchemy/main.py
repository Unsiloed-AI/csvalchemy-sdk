import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from .api.v1 import v1_router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Spreadsheet Processing API",
    description="API for processing and analyzing spreadsheets using LLMs",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log request timing and status

    This middleware tracks the processing time for each request and adds
    timing information to response headers for debugging purposes.

    Args:
        request: The incoming HTTP request
        call_next: The next middleware or route handler in the chain

    Returns:
        The HTTP response with added timing information
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.3f}s"
    )
    return response


# Add exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions

    This handler catches all unhandled exceptions, logs them, and returns
    a standardized error response to the client.

    Args:
        request: The incoming HTTP request
        exc: The exception that was raised

    Returns:
        A JSON response with error details
    """
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )


# Include API routers
app.include_router(v1_router)


# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint

    Returns basic information about the API service including
    version and links to documentation.

    Returns:
        Dict containing API metadata
    """
    return {
        "name": "Spreadsheet Processing API",
        "docs": "/docs",
        "health": "/health",
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint

    Provides status information for monitoring and load balancers.

    Returns:
        Dict containing health status and version information
    """
    return {"status": "ok"}


# Run with: uvicorn src.main:app --reload
if __name__ == "__main__":
    import uvicorn

    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))

    # Run app
    uvicorn.run("CSVAlchemy.main:app", host="0.0.0.0", port=port, reload=True)
