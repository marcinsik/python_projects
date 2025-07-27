# TextSummarizer - Automatyczny Generator Podsumowań

Narzędzie do automatycznego podsumowywania tekstu i ekstrakcji słów kluczowych z wykorzystaniem technik przetwarzania języka naturalnego (NLP).

## 🎯 Cel Projektu

Stworzenie inteligentnego narzędzia, które automatycznie:
- Podsumowuje długie teksty
- Ekstraktuje słowa kluczowe
- Przetwarza tekst z różnych źródeł

## 🚀 Aktualny Status: Etap 1 - Podstawy NLP

### ✅ Zaimplementowane Funkcjonalności

1. **Czytanie Plików Tekstowych**
   - Obsługa plików .txt z kodowaniem UTF-8
   - Walidacja i obsługa błędów

2. **Podstawowe Przetwarzanie NLP**
   - Segmentacja zdań (podział tekstu na zdania)
   - Tokenizacja słów
   - Usuwanie stop words (polskich i angielskich)
   - Obliczanie częstotliwości słów

3. **Podsumowywanie Ekstrakcyjne**
   - **TextRank Algorithm**: Zaawansowany algorytm oparty na grafach
   - **Metoda Częstotliwościowa**: Prostsza metoda fallback
   - Zwracanie N najważniejszych zdań z oryginalnego tekstu

4. **Ekstrakcja Słów Kluczowych**
   - Identyfikacja najważniejszych słów/fraz
   - Ranking według wagi/częstotliwości
   - Normalizacja wyników

## 🛠️ Technologie

- **Python 3.13+**
- **NLTK** - Przetwarzanie języka naturalnego
- **scikit-learn** - TF-IDF, cosine similarity
- **NetworkX** - Algorytmy grafowe (PageRank/TextRank)
- **NumPy** - Operacje na macierzach

## 📦 Instalacja

1. **Klonowanie projektu**:
```bash
cd /home/Marcin/Pulpit/python_projects/summary_generator_using_NLP
```

2. **Aktywacja środowiska wirtualnego**:
```bash
source .venv/bin/activate
```

3. **Instalacja zależności**:
```bash
pip install -r requirements.txt
```

4. **Pobieranie danych NLTK** (automatyczne przy pierwszym uruchomieniu):
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 🎮 Użycie

### Uruchomienie Demonstracji

```bash
python app.py
```

Program automatycznie:
1. Demonstruje podstawowe przetwarzanie NLP
2. Tworzy przykładowy plik tekstowy
3. Wykonuje podsumowanie i ekstrakcję słów kluczowych
4. Przetwarza wszystkie pliki .txt z katalogu `test_data/`

### Użycie Programistyczne

```python
from src.file_reader import read_text_file
from src.summarizer import TextRankSummarizer
from src.text_processor import TextProcessor

# Wczytanie tekstu
text = read_text_file("path/to/your/file.txt")

# Podsumowanie
summarizer = TextRankSummarizer(language='polish')
summary, sentences = summarizer.summarize(text, num_sentences=3)
keywords = summarizer.extract_keywords(text, num_keywords=10)

print("Podsumowanie:", summary)
print("Słowa kluczowe:", keywords)
```

## 📁 Struktura Projektu

```
summary_generator_using_NLP/
├── src/
│   ├── __init__.py              # Inicjalizacja pakietu
│   ├── file_reader.py           # Czytanie plików tekstowych
│   ├── text_processor.py        # Przetwarzanie NLP
│   └── summarizer.py            # Algorytmy podsumowywania
├── test_data/                   # Przykładowe pliki do testowania
│   └── sample_ai_article.txt    # Automatycznie generowany przykład
├── app.py                       # Główna aplikacja demonstracyjna
├── requirements.txt             # Zależności Python
└── README.md                    # Dokumentacja projektu
```

## 🧪 Przykład Działania

### Tekst Wejściowy:
```
Sztuczna inteligencja (AI) to dziedzina informatyki, która rozwija się w niezwykłym tempie. 
Współczesne systemy AI potrafią rozpoznawać obrazy, przetwarzać język naturalny i podejmować 
złożone decyzje. Uczenie maszynowe stanowi fundament większości nowoczesnych rozwiązań AI...
```

### Wynik Podsumowania:
```
Sztuczna inteligencja (AI) to dziedzina informatyki, która rozwija się w niezwykłym tempie. 
Głębokie uczenie, wykorzystujące sztuczne sieci neuronowe, rewolucjonizuje wiele dziedzin. 
Przyszłość sztucznej inteligencji wygląda obiecująco.
```

### Słowa Kluczowe:
```
1. inteligencja     (waga: 1.000)
2. uczenie          (waga: 0.857)
3. sztuczna         (waga: 0.714)
4. systemy          (waga: 0.571)
5. język            (waga: 0.429)
```

## 🔮 Planowane Rozszerzenia (Etap 2)

### 📄 Obsługa Różnych Źródeł
- **Pliki PDF**: PyPDF2/pdfplumber
- **Strony internetowe**: requests + BeautifulSoup
- **Dokumenty Word**: python-docx

### 🤖 Zaawansowane Modele NLP
- **Transformers (Hugging Face)**: T5, BART, mT5
- **Podsumowywanie abstrakcyjne**: Generowanie nowych zdań
- **Modele wielojęzyczne**: Obsługa różnych języków

### 🖥️ Interfejsy Użytkownika
- **CLI**: argparse/Click dla linii komend
- **Web GUI**: Streamlit dla interaktywnego dashboardu
- **API**: Flask/FastAPI dla integracji

## 🧠 Szczegóły Techniczne

### Algorytm TextRank

TextRank to algorytm oparty na PageRank, który:
1. Buduje graf zdań (węzły = zdania, krawędzie = podobieństwo)
2. Oblicza podobieństwo przy użyciu TF-IDF i cosine similarity
3. Znajduje najważniejsze zdania algorytmem PageRank
4. Zwraca N najlepiej ocenionych zdań

### Przetwarzanie Języka Polskiego

Projekt obsługuje język polski poprzez:
- Własną listę polskich stop words
- Segmentację zdań dostosowaną do polskiej interpunkcji
- Normalizację tekstu z polskimi znakami diakrytycznymi

## 📊 Wymagania Systemowe

- **Python**: 3.8+
- **RAM**: Minimum 2GB (4GB zalecane dla większych tekstów)
- **Miejsce na dysku**: ~500MB (z modelami NLTK)
- **System**: Linux, macOS, Windows

## 🤝 Jak Przyczynić się do Projektu

1. **Fork** repozytorium
2. Stwórz **branch** dla nowej funkcjonalności
3. **Testuj** zmiany na różnych typach tekstów
4. Stwórz **Pull Request** z opisem zmian

## 📝 Licencja

Projekt udostępniony na licencji MIT. Zobacz plik `LICENSE` dla szczegółów.

## 👨‍💻 Autor

**TextSummarizer** - Projekt edukacyjny demonstrujący zaawansowane techniki NLP w Pythonie.

---

*Projekt w ramach nauki przetwarzania języka naturalnego i technik podsumowywania tekstu.*
