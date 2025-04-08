#!/bin/bash

# Create a zip file of the frontend directory for Netlify deployment
echo "Creating zip file of frontend for Netlify deployment..."
cd frontend
zip -r ../discobots_frontend.zip *
cd ..
echo "Created discobots_frontend.zip - Upload this file to Netlify"

# Create a zip file of the backend API for other hosting
echo "Creating zip file of backend API for hosting..."
zip -r discobots_api.zip discobots_api.py api_requirements.txt
echo "Created discobots_api.zip - Deploy this to your Python hosting service"

echo "Done!"