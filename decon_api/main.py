from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from decon_api.routers.v1.main import api_v1

app = FastAPI(
    title='DeconAPI',
    description='API for SIEM detection content',
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST',],
    allow_headers=["*"],
)

# Include v1 endpoints
app.include_router(api_v1, prefix='/api/v1')