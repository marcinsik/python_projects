# 🔐 SecurePass - Menedżer Haseł

Bezpieczny menedżer haseł z szyfrowaniem AES-256 i intuicyjnym interfejsem graficznym.

## ✨ Funkcjonalności

- **Szyfrowanie AES-256** - Wszystkie hasła są szyfrowane przy użyciu algorytmu AES-256 z PBKDF2
- **Generator haseł** - Automatyczne generowanie silnych, bezpiecznych haseł
- **Intuicyjny GUI** - Prosty w obsłudze interfejs graficzny oparty na Tkinter
- **Wyszukiwanie** - Szybkie znajdowanie wpisów po nazwie serwisu, użytkownika lub notatkach
- **Eksport/Import** - Bezpieczny eksport i import danych w zaszyfrowanym formacie
- **Analiza bezpieczeństwa** - Sprawdzanie siły haseł i wykrywanie duplikatów
- **Kopiowanie do schowka** - Szybkie kopiowanie haseł i nazw użytkowników

## 📋 Wymagania

- Python 3.7+
- Moduły Python:
  - `cryptography` - do szyfrowania
  - `pyperclip` - do kopiowania do schowka
  - `tkinter` - do GUI (zazwyczaj preinstalowany)

## 🚀 Instalacja

1. Sklonuj lub pobierz projekt:
```bash
git clone https://github.com/yourusername/securepass.git
cd securepass
```

2. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

3. Uruchom aplikację:
```bash
python main.py
```

## 📖 Instrukcja użycia

### Pierwsze uruchomienie

1. **Utwórz hasło główne** - Przy pierwszym uruchomieniu zostaniesz poproszony o utworzenie hasła głównego
2. **Pamiętaj hasło!** - Hasło główne nie może być odzyskane. Jeśli je zapomnisz, stracisz dostęp do wszystkich danych

### Dodawanie haseł

1. Kliknij przycisk "➕ Nowy wpis" lub użyj skrótu `Ctrl+N`
2. Wypełnij formularz:
   - **Serwis/Strona** - Nazwa serwisu (np. "Gmail", "Facebook")
   - **Nazwa użytkownika** - Login lub adres e-mail
   - **Hasło** - Możesz wpisać własne lub wygenerować automatycznie
   - **Notatki** - Opcjonalne dodatkowe informacje
3. Kliknij "Zapisz"

### Korzystanie z haseł

- **Kopiowanie hasła** - Podwójne kliknięcie na wpis lub klawisz Enter
- **Kopiowanie nazwy użytkownika** - Prawy przycisk myszy → "Kopiuj nazwę użytkownika"
- **Edycja wpisu** - Prawy przycisk myszy → "Edytuj"
- **Usuwanie wpisu** - Prawy przycisk myszy → "Usuń"

### Generator haseł

1. Otwórz "🔧 Generator" z paska narzędzi lub menu "Narzędzia"
2. Skonfiguruj opcje:
   - Długość hasła (4-128 znaków)
   - Typy znaków (wielkie/małe litery, cyfry, znaki specjalne)
   - Wykluczenie podobnych znaków
3. Kliknij "Generuj" aby utworzyć nowe hasło
4. Skopiuj hasło do schowka

### Wyszukiwanie

Użyj pola wyszukiwania w górnej części okna. Wyszukiwanie działa dla:
- Nazw serwisów
- Nazw użytkowników  
- Notatek

### Eksport i import danych

**Eksport:**
1. Menu "Plik" → "Eksportuj..."
2. Wybierz lokalizację i nazwę pliku
3. Dane zostaną zaszyfrowane tym samym hasłem głównym

**Import:**
1. Menu "Plik" → "Importuj..."
2. Wybierz plik z danymi (*.enc)
3. Duplikaty zostaną automatycznie pominięte

## 🔒 Bezpieczeństwo

### Szyfrowanie

- **AES-256-CBC** - Zaawansowany standard szyfrowania
- **PBKDF2-SHA256** - Wyprowadzanie klucza z 100,000 iteracji
- **Losowa sól** - Każde szyfrowanie używa unikalnej soli
- **Losowy IV** - Każda operacja szyfrowania używa unikalnego wektora inicjalizacji

### Najlepsze praktyki

1. **Silne hasło główne** - Użyj długiego, unikalnego hasła głównego
2. **Regularne kopie zapasowe** - Eksportuj dane i przechowuj kopie w bezpiecznym miejscu
3. **Unikalne hasła** - Używaj różnych haseł dla każdego serwisu
4. **Regularna zmiana** - Okresowo zmieniaj hasła, szczególnie do ważnych kont

### Analiza bezpieczeństwa

Aplikacja automatycznie analizuje Twoje hasła pod kątem:
- Słabych haseł (krócej niż 8 znaków)
- Duplikatów haseł
- Siły haseł (algorytm oceny 0-100 punktów)

## 📁 Struktura plików

```
securepass/
│
├── main.py                 # Główna aplikacja (GUI)
├── crypto_utils.py         # Szyfrowanie AES, zarządzanie kluczami
├── password_manager.py     # Logika zarządzania hasłami
├── generator.py            # Generator haseł
├── requirements.txt        # Zależności
├── README.md              # Ten plik
└── data.enc               # Plik z zaszyfrowanymi danymi (tworzony automatycznie)
```

## ⌨️ Skróty klawiszowe

- `Ctrl+N` - Nowy wpis
- `Ctrl+L` - Zablokuj sejf
- `F5` - Odśwież listę
- `Enter` - Kopiuj hasło (gdy wpis jest zaznaczony)
- `Escape` - Zamknij aktywne okno dialogowe

## 🔧 Rozwiązywanie problemów

### Błąd importu modułów

Jeśli widzisz błędy związane z brakiem modułów:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problemy z kopiowaniem do schowka

Na Linux może być potrzebne doinstalowanie:
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Fedora
sudo dnf install xclip
```

### Zapomniałem hasło główne

Niestety, nie ma możliwości odzyskania hasła głównego. Będziesz musiał:
1. Usunąć plik `data.enc`
2. Rozpocząć od nowa z nowym hasłem głównym

## 🔄 Kopie zapasowe

**WAŻNE:** Regularnie twórz kopie zapasowe!

1. Użyj funkcji eksportu w aplikacji
2. Przechowuj pliki *.enc w bezpiecznym miejscu
3. Testuj import z kopii zapasowych

## ⚡ Wydajność

- Aplikacja jest zoptymalizowana dla tysięcy wpisów
- Wyszukiwanie działa w czasie rzeczywistym
- Szyfrowanie używa zoptymalizowanych algorytmów

## 🛡️ Zgodność

- **Windows** - Pełna obsługa
- **macOS** - Pełna obsługa  
- **Linux** - Pełna obsługa (może wymagać xclip dla schowka)




