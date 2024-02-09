import os

environment = {
    'origins': os.getenv("CORS_ORIGINS", "http://localhost:3000").split(',')
}