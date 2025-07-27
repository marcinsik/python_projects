import secrets
import string
from typing import Optional

class PasswordGenerator:
    """Generator silnych haseł z konfigurowalnymi opcjami."""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
        exclude_similar: bool = True
    ) -> str:
        """
        Generuje silne hasło z określonymi parametrami.
        
        Args:
            length: Długość hasła (minimum 4)
            use_uppercase: Czy używać wielkich liter
            use_lowercase: Czy używać małych liter
            use_digits: Czy używać cyfr
            use_special: Czy używać znaków specjalnych
            exclude_similar: Czy wykluczyć podobne znaki (0, O, l, 1, etc.)
        
        Returns:
            Wygenerowane hasło jako string
        """
        if length < 4:
            raise ValueError("Długość hasła musi wynosić co najmniej 4 znaki")
        
        # Budowanie zestawu znaków
        charset = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if exclude_similar:
                chars = chars.replace('l', '').replace('o', '')
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_uppercase:
            chars = self.uppercase
            if exclude_similar:
                chars = chars.replace('I', '').replace('O', '')
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_digits:
            chars = self.digits
            if exclude_similar:
                chars = chars.replace('0', '').replace('1', '')
            charset += chars
            required_chars.append(secrets.choice(chars))
        
        if use_special:
            charset += self.special
            required_chars.append(secrets.choice(self.special))
        
        if not charset:
            raise ValueError("Musi być wybrany co najmniej jeden typ znaku")
        
        # Generowanie hasła
        password = required_chars.copy()
        
        # Dopełnienie do wymaganej długości
        for _ in range(length - len(required_chars)):
            password.append(secrets.choice(charset))
        
        # Mieszanie kolejności
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def check_password_strength(self, password: str) -> dict:
        """
        Sprawdza siłę hasła i zwraca szczegółową analizę.
        
        Args:
            password: Hasło do sprawdzenia
        
        Returns:
            Słownik z informacjami o sile hasła
        """
        if not password:
            return {
                'score': 0,
                'level': 'Bardzo słabe',
                'feedback': ['Hasło nie może być puste']
            }
        
        score = 0
        feedback = []
        
        # Długość
        length = len(password)
        if length >= 12:
            score += 25
        elif length >= 8:
            score += 15
        elif length >= 6:
            score += 10
        else:
            feedback.append('Hasło powinno mieć co najmniej 8 znaków')
        
        # Różnorodność znaków
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_special = any(c in self.special for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_special])
        score += char_types * 15
        
        if not has_lower:
            feedback.append('Dodaj małe litery')
        if not has_upper:
            feedback.append('Dodaj wielkie litery')
        if not has_digit:
            feedback.append('Dodaj cyfry')
        if not has_special:
            feedback.append('Dodaj znaki specjalne')
        
        # Powtarzające się znaki
        if len(set(password)) < len(password) * 0.7:
            score -= 10
            feedback.append('Unikaj powtarzających się znaków')
        
        # Kolejne znaki
        sequential_count = 0
        for i in range(len(password) - 2):
            if (ord(password[i]) + 1 == ord(password[i + 1]) and 
                ord(password[i + 1]) + 1 == ord(password[i + 2])):
                sequential_count += 1
        
        if sequential_count > 0:
            score -= sequential_count * 5
            feedback.append('Unikaj kolejnych znaków (abc, 123)')
        
        # Określenie poziomu
        if score >= 80:
            level = 'Bardzo silne'
        elif score >= 60:
            level = 'Silne'
        elif score >= 40:
            level = 'Średnie'
        elif score >= 20:
            level = 'Słabe'
        else:
            level = 'Bardzo słabe'
        
        return {
            'score': max(0, min(100, score)),
            'level': level,
            'feedback': feedback
        }
