#!/bin/bash

# Step 1: Run the seeder
echo "--- Running Database Seeder ---"
python seeder.py

# Step 2: Start the Uvicorn server for the new app location
echo "--- Starting FastAPI Application ---"
uvicorn app.main:app --host 0.0.0.0 --port 8000
