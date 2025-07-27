import os
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from typing import Optional

class CryptoUtils:
    """Klasa do szyfrowania i odszyfrowywania danych przy użyciu AES."""
    
    def __init__(self):
        self.backend = default_backend()
        self.key_length = 32  # 256 bitów
        self.iv_length = 16   # 128 bitów
        self.salt_length = 16 # 128 bitów
        self.iterations = 100000  # Liczba iteracji PBKDF2
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Wyprowadza klucz szyfrowania z hasła głównego przy użyciu PBKDF2.
        
        Args:
            password: Hasło główne
            salt: Sól do wyprowadzenia klucza
        
        Returns:
            Wyprowadzony klucz
        """
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        return kdf.derive(password_bytes)
    
    def encrypt_data(self, data: str, password: str) -> str:
        """
        Szyfruje dane przy użyciu AES-256-CBC.
        
        Args:
            data: Dane do zaszyfrowania
            password: Hasło główne
        
        Returns:
            Zaszyfrowane dane zakodowane w base64
        """
        # Generowanie losowej soli i IV
        salt = os.urandom(self.salt_length)
        iv = os.urandom(self.iv_length)
        
        # Wyprowadzenie klucza
        key = self._derive_key(password, salt)
        
        # Szyfrowanie
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Padding do wielokrotności 16 bajtów (PKCS7)
        data_bytes = data.encode('utf-8')
        padding_length = 16 - (len(data_bytes) % 16)
        padded_data = data_bytes + bytes([padding_length] * padding_length)
        
        # Szyfrowanie danych
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        
        combined = salt + iv + encrypted_data
        
        # Kodowanie w base64
        return base64.b64encode(combined).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str, password: str) -> str:
        """
        Odszyfrowuje dane zaszyfrowane przy użyciu AES-256-CBC.
        
        Args:
            encrypted_data: Zaszyfrowane dane w base64
            password: Hasło główne
        
        Returns:
            Odszyfrowane dane
        
        Raises:
            ValueError: Gdy hasło jest nieprawidłowe lub dane są uszkodzone
        """
        try:
            # Dekodowanie z base64
            combined = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Rozdzielenie soli, IV i danych
            salt = combined[:self.salt_length]
            iv = combined[self.salt_length:self.salt_length + self.iv_length]
            encrypted_bytes = combined[self.salt_length + self.iv_length:]
            
            # Wyprowadzenie klucza
            key = self._derive_key(password, salt)
            
            # Odszyfrowywanie
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # Odszyfrowanie danych
            padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
            
            # Usunięcie paddingu
            padding_length = padded_data[-1]
            data_bytes = padded_data[:-padding_length]
            
            return data_bytes.decode('utf-8')
            
        except Exception as e:
            raise ValueError("Nieprawidłowe hasło główne lub uszkodzone dane") from e
    
    def hash_password(self, password: str) -> str:
        """
        Tworzy hash hasła do weryfikacji hasła głównego.
        
        Args:
            password: Hasło do zahashowania
        
        Returns:
            Hash hasła w base64
        """
        # Generowanie losowej soli
        salt = os.urandom(self.salt_length)
        
        # Tworzenie hashu
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=salt,
            iterations=self.iterations,
            backend=self.backend
        )
        hash_bytes = kdf.derive(password_bytes)
        
        # Łączenie soli i hashu
        combined = salt + hash_bytes
        return base64.b64encode(combined).decode('utf-8')
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """
        Weryfikuje hasło przeciwko zapisanemu hashowi.
        
        Args:
            password: Hasło do weryfikacji
            stored_hash: Zapisany hash hasła
        
        Returns:
            True jeśli hasło jest prawidłowe, False w przeciwnym razie
        """
        try:
            # Dekodowanie hashu
            combined = base64.b64decode(stored_hash.encode('utf-8'))
            salt = combined[:self.salt_length]
            stored_hash_bytes = combined[self.salt_length:]
            
            # Tworzenie hashu z podanego hasła
            password_bytes = password.encode('utf-8')
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=self.key_length,
                salt=salt,
                iterations=self.iterations,
                backend=self.backend
            )
            hash_bytes = kdf.derive(password_bytes)
            
            # Porównanie hashów
            return hash_bytes == stored_hash_bytes
            
        except Exception:
            return False
