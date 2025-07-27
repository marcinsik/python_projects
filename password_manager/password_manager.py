import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from crypto_utils import CryptoUtils

class PasswordEntry:
    """Klasa reprezentująca pojedynczy wpis hasła."""
    
    def __init__(self, service: str, username: str, password: str, 
                 notes: str = "", created_at: str = None, updated_at: str = None):
        self.service = service
        self.username = username
        self.password = password
        self.notes = notes
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Konwertuje wpis do słownika."""
        return {
            'service': self.service,
            'username': self.username,
            'password': self.password,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordEntry':
        """Tworzy wpis ze słownika."""
        return cls(
            service=data['service'],
            username=data['username'],
            password=data['password'],
            notes=data.get('notes', ''),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def update(self, service: str = None, username: str = None, 
               password: str = None, notes: str = None):
        """Aktualizuje wpis."""
        if service is not None:
            self.service = service
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if notes is not None:
            self.notes = notes
        self.updated_at = datetime.now().isoformat()

class PasswordManager:
    """Główna klasa zarządzająca hasłami."""
    
    def __init__(self, data_file: str = "data.enc"):
        self.data_file = data_file
        self.crypto = CryptoUtils()
        self.entries: List[PasswordEntry] = []
        self.master_password = None
        self.is_unlocked = False
    
    def create_vault(self, master_password: str) -> bool:
        """
        Tworzy nowy sejf z hasłem głównym.
        
        Args:
            master_password: Hasło główne do sejfu
        
        Returns:
            True jeśli sejf został utworzony pomyślnie
        """
        try:
            # Sprawdzenie czy plik już istnieje
            if os.path.exists(self.data_file):
                return False
            
            self.master_password = master_password
            self.entries = []
            self.is_unlocked = True
            
            # Zapisanie pustego sejfu
            self._save_data()
            return True
            
        except Exception:
            return False
    
    def unlock_vault(self, master_password: str) -> bool:
        """
        Odblokowuje sejf przy użyciu hasła głównego.
        
        Args:
            master_password: Hasło główne
        
        Returns:
            True jeśli sejf został odblokowany pomyślnie
        """
        try:
            if not os.path.exists(self.data_file):
                return False
            
            # Próba odczytania danych
            self._load_data(master_password)
            self.master_password = master_password
            self.is_unlocked = True
            return True
            
        except Exception:
            return False
    
    def lock_vault(self):
        """Blokuje sejf."""
        self.master_password = None
        self.is_unlocked = False
        self.entries = []
    
    def add_entry(self, service: str, username: str, password: str, notes: str = "") -> bool:
        """
        Dodaje nowy wpis do sejfu.
        
        Args:
            service: Nazwa serwisu
            username: Nazwa użytkownika
            password: Hasło
            notes: Dodatkowe notatki
        
        Returns:
            True jeśli wpis został dodany pomyślnie
        """
        if not self.is_unlocked:
            return False
        
        try:
            # Sprawdzenie czy wpis już istnieje
            for entry in self.entries:
                if entry.service.lower() == service.lower() and entry.username.lower() == username.lower():
                    return False
            
            # Dodanie nowego wpisu
            new_entry = PasswordEntry(service, username, password, notes)
            self.entries.append(new_entry)
            
            # Zapisanie danych
            self._save_data()
            return True
            
        except Exception:
            return False
    
    def update_entry(self, index: int, service: str = None, username: str = None, 
                    password: str = None, notes: str = None) -> bool:
        """
        Aktualizuje istniejący wpis.
        
        Args:
            index: Indeks wpisu do aktualizacji
            service: Nowa nazwa serwisu
            username: Nowa nazwa użytkownika
            password: Nowe hasło
            notes: Nowe notatki
        
        Returns:
            True jeśli wpis został zaktualizowany pomyślnie
        """
        if not self.is_unlocked or index < 0 or index >= len(self.entries):
            return False
        
        try:
            self.entries[index].update(service, username, password, notes)
            self._save_data()
            return True
            
        except Exception:
            return False
    
    def delete_entry(self, index: int) -> bool:
        """
        Usuwa wpis z sejfu.
        
        Args:
            index: Indeks wpisu do usunięcia
        
        Returns:
            True jeśli wpis został usunięty pomyślnie
        """
        if not self.is_unlocked or index < 0 or index >= len(self.entries):
            return False
        
        try:
            del self.entries[index]
            self._save_data()
            return True
            
        except Exception:
            return False
    
    def search_entries(self, query: str) -> List[int]:
        """
        Wyszukuje wpisy zawierające zapytanie.
        
        Args:
            query: Zapytanie do wyszukania
        
        Returns:
            Lista indeksów pasujących wpisów
        """
        if not self.is_unlocked:
            return []
        
        query_lower = query.lower()
        results = []
        
        for i, entry in enumerate(self.entries):
            if (query_lower in entry.service.lower() or 
                query_lower in entry.username.lower() or
                query_lower in entry.notes.lower()):
                results.append(i)
        
        return results
    
    def get_entries(self) -> List[PasswordEntry]:
        """
        Zwraca listę wszystkich wpisów.
        
        Returns:
            Lista wpisów lub pusta lista jeśli sejf jest zablokowany
        """
        if not self.is_unlocked:
            return []
        return self.entries.copy()
    
    def export_data(self, export_file: str) -> bool:
        """
        Eksportuje dane do pliku.
        
        Args:
            export_file: Ścieżka do pliku eksportu
        
        Returns:
            True jeśli eksport zakończył się pomyślnie
        """
        if not self.is_unlocked:
            return False
        
        try:
            # Przygotowanie danych do eksportu
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'entries': [entry.to_dict() for entry in self.entries]
            }
            
            # Szyfrowanie i zapis
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
            encrypted_data = self.crypto.encrypt_data(json_data, self.master_password)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(encrypted_data)
            
            return True
            
        except Exception:
            return False
    
    def import_data(self, import_file: str) -> bool:
        """
        Importuje dane z pliku.
        
        Args:
            import_file: Ścieżka do pliku importu
        
        Returns:
            True jeśli import zakończył się pomyślnie
        """
        if not self.is_unlocked:
            return False
        
        try:
            # Odczyt i odszyfrowanie danych
            with open(import_file, 'r', encoding='utf-8') as f:
                encrypted_data = f.read()
            
            json_data = self.crypto.decrypt_data(encrypted_data, self.master_password)
            import_data = json.loads(json_data)
            
            # Dodanie wpisów (bez duplikatów)
            for entry_data in import_data['entries']:
                entry = PasswordEntry.from_dict(entry_data)
                
                # Sprawdzenie duplikatów
                is_duplicate = any(
                    e.service.lower() == entry.service.lower() and 
                    e.username.lower() == entry.username.lower()
                    for e in self.entries
                )
                
                if not is_duplicate:
                    self.entries.append(entry)
            
            self._save_data()
            return True
            
        except Exception:
            return False
    
    def _save_data(self):
        """Zapisuje dane do zaszyfrowanego pliku."""
        data = {
            'entries': [entry.to_dict() for entry in self.entries]
        }
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        encrypted_data = self.crypto.encrypt_data(json_data, self.master_password)
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_data)
    
    def _load_data(self, master_password: str):
        """Wczytuje dane z zaszyfrowanego pliku."""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            encrypted_data = f.read()
        
        json_data = self.crypto.decrypt_data(encrypted_data, master_password)
        data = json.loads(json_data)
        
        self.entries = [PasswordEntry.from_dict(entry_data) 
                       for entry_data in data.get('entries', [])]
    
    def vault_exists(self) -> bool:
        """Sprawdza czy sejf już istnieje."""
        return os.path.exists(self.data_file)
    
    def get_vault_stats(self) -> Dict:
        """
        Zwraca statystyki sejfu.
        
        Returns:
            Słownik ze statystykami
        """
        if not self.is_unlocked:
            return {}
        
        total_entries = len(self.entries)
        if total_entries == 0:
            return {'total_entries': 0}
        
        # Analiza haseł
        weak_passwords = 0
        duplicate_passwords = {}
        
        for entry in self.entries:
            # Sprawdzenie słabych haseł (mniej niż 8 znaków)
            if len(entry.password) < 8:
                weak_passwords += 1
            
            # Sprawdzenie duplikatów
            if entry.password in duplicate_passwords:
                duplicate_passwords[entry.password] += 1
            else:
                duplicate_passwords[entry.password] = 1
        
        duplicate_count = sum(1 for count in duplicate_passwords.values() if count > 1)
        
        return {
            'total_entries': total_entries,
            'weak_passwords': weak_passwords,
            'duplicate_passwords': duplicate_count,
            'oldest_entry': min(entry.created_at for entry in self.entries),
            'newest_entry': max(entry.created_at for entry in self.entries)
        }
