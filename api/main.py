from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import github, papers, admin, auth, user

app = FastAPI(title="TechVision API", description="API for TechVision website")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(github.router)
app.include_router(papers.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TechVision API"}
