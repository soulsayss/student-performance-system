#!/bin/bash
# Build script for Render deployment
# This runs automatically during deployment

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python init_db.py

echo "Build complete!"
