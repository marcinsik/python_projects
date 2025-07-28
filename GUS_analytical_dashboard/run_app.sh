#!/bin/bash

# Script to run the Public Data Dashboard (Statistics Poland - GUS)

echo "🚀 Starting Public Data Dashboard (Statistics Poland - GUS)..."
echo "📊 Application will be available at: http://localhost:8501"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Please run: python -m venv .venv"
    exit 1
fi

# Activate virtual environment and run the application
source .venv/bin/activate
.venv/bin/python -m streamlit run app.py --server.port 8501 --server.address localhost

echo ""
echo "✅ Application terminated."
