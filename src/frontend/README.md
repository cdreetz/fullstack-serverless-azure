# Frontend - React/Next.js Application

This directory contains the React or Next.js application that serves as the frontend for our project.

## Structure

- `/components/`: React components
- `/pages/`: Next.js pages (if using Next.js)
- `/public/`: Static assets
- `/styles/`: CSS or styled-components
- `package.json`: Node.js dependencies

## Prerequisites

- Node.js 14+
- npm or yarn

## Setup

1. Install dependencies: `npm install` or `yarn install`

## Running Locally

1. Set environment variables (see `.env.example`)
2. Start the development server:
   - React: `npm start` or `yarn start`
   - Next.js: `npm run dev` or `yarn dev`

## Building for Production

- React: `npm run build` or `yarn build`
- Next.js: `npm run build` or `yarn build`

## Testing

Run tests: `npm test` or `yarn test`

## Azure Static Web Apps Deployment

Deployment is typically handled by the CI/CD pipeline. For manual deployment:

1. Build the project
2. Use Azure Static Web Apps CLI to deploy

## Authentication

This application integrates with Azure AD for authentication. Ensure you have the correct Azure AD configurations in your environment variables.

## API Integration

The frontend communicates with the backend API. Update the API endpoint in the environment variables.

## Troubleshooting

- Check browser console for frontend errors
- Ensure environment variables are correctly set
- For deployment issues, check Azure Static Web Apps logs in the Azure portal
