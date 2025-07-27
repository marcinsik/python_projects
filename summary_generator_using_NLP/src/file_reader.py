"""
Moduł do czytania plików tekstowych.
"""
import os
from typing import Optional


def read_text_file(file_path: str) -> Optional[str]:
    """
    Wczytuje zawartość pliku tekstowego do zmiennej Pythona.
    
    Args:
        file_path (str): Ścieżka do pliku tekstowego
        
    Returns:
        Optional[str]: Zawartość pliku lub None w przypadku błędu
    """
    try:
        if not os.path.exists(file_path):
            print(f"Błąd: Plik {file_path} nie istnieje.")
            return None
            
        if not file_path.lower().endswith('.txt'):
            print(f"Ostrzeżenie: Plik {file_path} może nie być plikiem tekstowym.")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if not content.strip():
            print(f"Ostrzeżenie: Plik {file_path} jest pusty.")
            return None
            
        return content
        
    except UnicodeDecodeError:
        print(f"Błąd: Nie można odczytać pliku {file_path}. Sprawdź kodowanie.")
        return None
    except Exception as e:
        print(f"Błąd podczas czytania pliku {file_path}: {str(e)}")
        return None


def save_text_to_file(text: str, file_path: str) -> bool:
    """
    Zapisuje tekst do pliku.
    
    Args:
        text (str): Tekst do zapisania
        file_path (str): Ścieżka do pliku docelowego
        
    Returns:
        bool: True jeśli operacja się powiodła, False w przeciwnym przypadku
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        return True
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku {file_path}: {str(e)}")
        return False
