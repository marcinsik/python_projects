#!/bin/bash

# Skrypt do uruchomienia Dashboard Danych Publicznych (GUS)

echo "🚀 Uruchamianie Dashboard Danych Publicznych (GUS)..."
echo "📊 Aplikacja będzie dostępna pod adresem: http://localhost:8501"
echo ""

# Aktywuj środowisko wirtualne i uruchom aplikację
source .venv/bin/activate
streamlit run app.py --server.port 8501 --server.address localhost

echo ""
echo "✅ Aplikacja zakończona."
