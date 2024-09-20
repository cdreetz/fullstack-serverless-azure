# Source Code

This directory contains the source code for both the backend and frontend of our application.

## Structure

- `/backend/`: FastAPI application code
- `/frontend/`: React/Next.js application code
- `/shared/`: Shared code between frontend and backend (if any)

## Backend

The backend is a FastAPI application designed to be deployed as Azure Functions. For more details, see the README in the `/backend` directory.

## Frontend

The frontend is a React/Next.js application that will be hosted on Azure Static Web Apps. For more details, see the README in the `/frontend` directory.

## Development

1. Set up the backend and frontend according to their respective READMEs
2. Use the scripts in the `/scripts` directory at the root of the project for common development tasks

## Testing

Each component has its own testing suite. Refer to the individual READMEs for specific testing instructions.

## Building

Build processes are typically handled by the CI/CD pipeline, but you can find manual build instructions in each component's README.

## Deployment

Deployment is managed through the CI/CD pipeline defined in `/.github/workflows/`. For manual deployment steps, refer to the individual component READMEs.
