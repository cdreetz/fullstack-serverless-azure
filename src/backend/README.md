# Backend - FastAPI Application

This directory contains the FastAPI application that serves as the backend for our project.

## Structure

- `/app/`: Main application code
  - `/api/`: API routes
  - `/core/`: Core application code
  - `/models/`: Data models
  - `/services/`: Business logic services
- `/tests/`: Backend tests
- `requirements.txt`: Python dependencies

## Prerequisites

- Python 3.8+
- pip

## Setup

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix or MacOS: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Running Locally

1. Set environment variables (see `.env.example`)
2. Run the FastAPI application: `uvicorn app.main:app --reload`

## Testing

Run tests using pytest: `pytest tests/`

## Azure Functions Deployment

1. Ensure you have Azure Functions Core Tools installed
2. Update `azure-functions/host.json` and `azure-functions/local.settings.json` as needed
3. Deploy using Azure CLI or the CI/CD pipeline

## API Documentation

Once the application is running, you can access the Swagger UI documentation at `/docs` and the ReDoc documentation at `/redoc`.

## Authentication

This application uses Azure AD for authentication. Ensure you have the correct Azure AD configurations set up in your environment.

## Troubleshooting

- Check Azure Function logs in the Azure portal
- For local debugging, use VS Code with the Azure Functions extension
