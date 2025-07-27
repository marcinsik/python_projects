# Dashboard Danych Publicznych (GUS)

Interaktywny dashboard do analizy danych publicznych z Głównego Urzędu Statystycznego.

## Funkcjonalności

- 📊 Interaktywne wykresy PKB i bezrobocia
- 🗺️ Filtrowanie po województwach
- 📅 Analiza trendów w czasie
- 📈 Porównanie regionów
- 🔄 Import własnych danych

## Technologie

Aplikacja została zbudowana z wykorzystaniem następujących technologii:

### Backend & Analiza Danych
- **Python ** - główny język programowania
- **Pandas ** - manipulacja i analiza danych
- **NumPy ** - obliczenia numeryczne

### Frontend & Wizualizacje
- **Streamlit ** - framework do tworzenia interaktywnych aplikacji webowych
- **Plotly ** - biblioteka do tworzenia interaktywnych wykresów i wizualizacji

### Import/Export Danych
- **OpenPyXL ** - obsługa plików Excel (.xlsx, .xls)
- **Requests ** - komunikacja HTTP (do przyszłych integracji z API)

### Architektura
- **Modularna struktura** - oddzielne moduły dla wczytywania danych i wizualizacji
- **Responsywny design** - dostosowuje się do różnych rozmiarów ekranów
- **Cache'owanie danych** - optymalizacja wydajności przez Streamlit

## Instalacja

```bash
pip install -r requirements.txt
```

## Uruchomienie

### Metoda 1: Bezpośrednie uruchomienie
```bash
streamlit run app.py
```

### Metoda 2: Używając skryptu (zalecane)
```bash
./run_app.sh
```

### Metoda 3: Z aktywowanym środowiskiem wirtualnym
```bash
source .venv/bin/activate
streamlit run app.py --server.port 8501
```

Po uruchomieniu aplikacja będzie dostępna pod adresem: **http://localhost:8501**

```
analytical_dashboard/
├── app.py                  # 🎯 Główna aplikacja Streamlit z interfejsem użytkownika
├── data_loader.py          # 📁 Moduł do wczytywania i przetwarzania danych
├── visualizations.py      # 📊 Funkcje do tworzenia wykresów Plotly
├── data/                   # 📂 Folder z danymi
│   └── sample_data.csv     #     Przykładowe dane GUS (PKB, bezrobocie)
├── .venv/                  # 🐍 Środowisko wirtualne Python
├── requirements.txt        # 📦 Lista zależności Python
├── run_app.sh             # 🚀 Skrypt do łatwego uruchomienia aplikacji
└── README.md              # 📖 Ten plik
```

### Opis modułów

#### `app.py` - Główna aplikacja Streamlit
- **Interface użytkownika**: Sidebar z filtrami i opcjami
- **Typy analiz**: Przegląd główny, analiza PKB, bezrobocie, korelacje, tempo wzrostu
- **Responsywny design**: Dostosowuje się do różnych rozmiarów ekranów
- **Interaktywność**: Dynamiczne filtry, wybór województw i zakresów czasowych

#### `data_loader.py` - Zarządzanie danymi
- **Klasa DataLoader**: Centralne zarządzanie danymi
- **Import danych**: Obsługa CSV, Excel (.xlsx, .xls)
- **Walidacja**: Sprawdzanie kompletności i poprawności danych
- **Transformacje**: Obliczanie PKB per capita, tempa wzrostu
- **Cache'owanie**: Optymalizacja wydajności przez Streamlit

#### `visualizations.py` - Wykresy i wizualizacje
- **Klasa Visualizations**: Gotowe funkcje do tworzenia wykresów
- **Rodzaje wykresów**: Liniowe, słupkowe, korelacji, rozrzutu
- **Plotly Integration**: Interaktywne wykresy z hover, zoom, pan
- **Stylizacja**: Spójny design, paleta kolorów, responsywność

## Dane przykładowe

Aplikacja zawiera przykładowe dane z lat 2019-2022 dla wszystkich 16 województw Polski:

- **PKB** (mld zł) - Produkt Krajowy Brutto według województw
- **Bezrobocie** (%) - Stopa bezrobocia rejestrowanego
- **Ludność** (tys.) - Liczba mieszkańców (opcjonalne dla PKB per capita)

## Możliwości rozszerzenia

### Planowane funkcjonalności
- 🌐 **Integracja z API GUS** - automatyczne pobieranie najnowszych danych
- 🗺️ **Mapa Polski** - wizualizacja choropleth z gradientem wartości
- 📈 **Więcej wskaźników** - inflacja, inwestycje, eksport/import
- 🔄 **Aktualizacje real-time** - automatyczne odświeżanie danych
- 📊 **Dashboard customowy** - możliwość konfiguracji układu

