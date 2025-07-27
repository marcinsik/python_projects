# Batch File Editor 🔧

Zaawansowane narzędzie do batchowej obróbki plików w Pythonie. Umożliwia masowe przetwarzanie plików: zmianę nazw, konwersję obrazów, kompresję zdjęć i formatowanie tekstów.

## 🚀 Funkcjonalności

- **Masowa zmiana nazw plików** - używa wyrażeń regularnych
- **Konwersja obrazów** - między formatami JPEG, PNG, BMP, TIFF, WebP
- **Kompresja zdjęć** - z opcjonalną zmianą rozmiaru
- **Formatowanie plików tekstowych** - normalizacja, konwersja tab↔spacje
- **Organizacja plików** - automatyczne sortowanie według rozszerzeń
- **Tryb podglądu** - bezpieczne testowanie operacji

## 📦 Instalacja

```bash
# Sklonuj projekt
cd /home/Marcin/Pulpit/python_projects/file_editor

# Zainstaluj zależności
pip install -r requirements.txt

# Nadaj uprawnienia wykonania (opcjonalnie)
chmod +x batch_file_editor.py
```

## 🛠️ Użytkowanie

### Składnia podstawowa
```bash
python batch_file_editor.py [OPERACJA] [OPCJE] [--execute]
```

**⚠️ Ważne:** Bez flagi `--execute` narzędzie działa w trybie podglądu!

### 1. Masowa zmiana nazw plików

```bash
# Podgląd zmian
python batch_file_editor.py rename --pattern "IMG_(\d+)" --replacement "Zdjecie_\1"

# Wykonanie zmian
python batch_file_editor.py rename --pattern "IMG_(\d+)" --replacement "Zdjecie_\1" --execute

# Zmiana w konkretnym katalogu
python batch_file_editor.py rename --pattern "old" --replacement "new" --directory ./photos --execute
```

**Przykłady wzorców:**
- `IMG_(\d+)` → `Zdjecie_\1` (IMG_001.jpg → Zdjecie_001.jpg)
- `(.+)\.txt` → `\1_backup.txt` (dodaje _backup przed rozszerzeniem)
- `\s+` → `_` (zamienia spacje na podkreślenia)

### 2. Konwersja obrazów

```bash
# JPEG → PNG
python batch_file_editor.py convert --source jpg --target png --execute

# PNG → JPEG z jakością 90%
python batch_file_editor.py convert --source png --target jpg --quality 90 --execute

# Wszystkie obsługiwane formaty: jpg, jpeg, png, bmp, tiff, webp
```

### 3. Kompresja obrazów

```bash
# Kompresja z domyślnymi ustawieniami (70% jakości, max 1920x1080)
python batch_file_editor.py compress --execute

# Niestandardowe ustawienia
python batch_file_editor.py compress --quality 50 --max-width 1600 --max-height 900 --execute

# Tylko zmiana jakości bez resize
python batch_file_editor.py compress --quality 60 --max-width 9999 --max-height 9999 --execute
```

**Rezultat:** Skompresowane pliki trafiają do folderu `compressed/`

### 4. Formatowanie plików tekstowych

```bash
# Normalizacja (usuwa nadmiarowe spacje i puste linie)
python batch_file_editor.py format --operation normalize --execute

# Konwersja tabulatorów na spacje
python batch_file_editor.py format --operation tabs_to_spaces --execute

# Konwersja spacji na tabulatory
python batch_file_editor.py format --operation spaces_to_tabs --execute

# Z konkretnym kodowaniem
python batch_file_editor.py format --operation normalize --encoding utf-8 --execute
```

**Obsługiwane formaty:** .txt, .md, .py, .js, .html, .css, .xml, .json

**Kopie zapasowe:** Oryginalne pliki są zapisywane w `backup_text/`

### 5. Organizacja plików według rozszerzeń

```bash
# Automatycznie tworzy foldery i przenosi pliki
python batch_file_editor.py organize --execute
```

**Rezultat:**
```
folder/
├── jpg/         # wszystkie pliki .jpg
├── png/         # wszystkie pliki .png  
├── txt/         # wszystkie pliki .txt
├── pdf/         # wszystkie pliki .pdf
└── bez_rozszerzenia/  # pliki bez rozszerzenia
```

## 📊 Przykłady zastosowań

### Scenario 1: Obróbka zdjęć z aparatu
```bash
# 1. Zmień nazwy IMG_001.jpg → Wakacje_001.jpg
python batch_file_editor.py rename --pattern "IMG_(\d+)" --replacement "Wakacje_\1" --execute

# 2. Skompresuj zdjęcia do 1600px i 75% jakości
python batch_file_editor.py compress --quality 75 --max-width 1600 --execute
```

### Scenario 2: Czyszczenie kodu źródłowego
```bash
# 1. Normalizuj formatowanie wszystkich plików tekstowych
python batch_file_editor.py format --operation normalize --execute

# 2. Konwertuj taby na spacje (Python PEP 8)
python batch_file_editor.py format --operation tabs_to_spaces --execute
```

### Scenario 3: Przygotowanie grafik do web
```bash
# 1. Konwertuj PNG na JPEG (mniejsze pliki)
python batch_file_editor.py convert --source png --target jpg --quality 85 --execute

# 2. Kompresuj do rozmiaru web
python batch_file_editor.py compress --quality 80 --max-width 1200 --execute
```

## 🔒 Bezpieczeństwo

- **Tryb podglądu** - domyślnie wszystkie operacje pokazują tylko preview
- **Kopie zapasowe** - dla formatowania tekstów i kompresji obrazów
- **Sprawdzanie konfliktów** - ostrzeżenia o istniejących plikach
- **Walidacja formatów** - obsługa tylko bezpiecznych rozszerzeń

## 📋 Wymagania systemowe

- Python 3.6+
- Pillow (PIL) dla obsługi obrazów
- System plików obsługujący Unicode (nazwy plików)

## 🐛 Rozwiązywanie problemów

### Błąd: "No module named 'PIL'"
```bash
pip install Pillow
```

### Błąd kodowania przy plikach tekstowych
```bash
# Spróbuj z innym kodowaniem
python batch_file_editor.py format --encoding cp1250 --execute
```

### Pliki są zablokowane/zajęte
- Zamknij wszystkie programy korzystające z plików
- Upewnij się, że masz uprawnienia do zapisu

## 📝 Licencja

Projekt open-source - możesz swobodnie modyfikować i dystrybuować.

## 🤝 Wkład w rozwój

Sugestie i poprawki są mile widziane! Utwórz issue lub pull request.

---

**Autor:** Batch File Editor Tool  
**Data:** 2025-07-27  
**Wersja:** 1.0
