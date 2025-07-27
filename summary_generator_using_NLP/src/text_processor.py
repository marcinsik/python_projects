"""
Moduł do podstawowego przetwarzania języka naturalnego (NLP).
"""
import nltk
import re
from typing import List, Set
from collections import Counter
import string


class TextProcessor:
    """Klasa do przetwarzania tekstu przy użyciu NLTK."""
    
    def __init__(self, language: str = 'polish'):
        """
        Inicjalizuje procesor tekstu.
        
        Args:
            language (str): Język tekstu ('polish' lub 'english')
        """
        self.language = language
        self._download_nltk_data()
        self._load_stopwords()
    
    def _download_nltk_data(self):
        """Pobiera niezbędne dane NLTK."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("Pobieranie danych NLTK punkt...")
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Pobieranie danych NLTK stopwords...")
            nltk.download('stopwords')
    
    def _load_stopwords(self):
        """Ładuje listę stop words dla wybranego języka."""
        from nltk.corpus import stopwords
        
        if self.language == 'polish':
            # NLTK może nie mieć polskich stop words, więc tworzymy własną listę
            self.stop_words = set([
                'i', 'a', 'o', 'e', 'w', 'z', 'na', 'do', 'za', 'się', 'nie', 'że', 'to',
                'jest', 'są', 'było', 'były', 'będzie', 'będą', 'ma', 'mają', 'miał', 'miała',
                'może', 'można', 'oraz', 'lub', 'ale', 'gdy', 'jak', 'gdzie', 'dlaczego',
                'co', 'kto', 'które', 'która', 'który', 'przez', 'przed', 'po', 'pod',
                'nad', 'przy', 'bez', 'dla', 'od', 'bardzo', 'też', 'też', 'już', 'jeszcze',
                'tylko', 'także', 'również', 'więc', 'więcej', 'wszystko', 'wszystkie',
                'każdy', 'każda', 'każde', 'tego', 'tej', 'tych', 'tym', 'te', 'ta', 'ten'
            ])
        else:
            self.stop_words = set(stopwords.words('english'))
    
    def sentence_tokenize(self, text: str) -> List[str]:
        """
        Dzieli tekst na zdania.
        
        Args:
            text (str): Tekst do podziału
            
        Returns:
            List[str]: Lista zdań
        """
        # Czyścimy tekst z nadmiernych białych znaków
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Używamy NLTK do segmentacji zdań
        sentences = nltk.sent_tokenize(text)
        
        # Filtrujemy bardzo krótkie "zdania" (prawdopodobnie błędy)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        return sentences
    
    def word_tokenize(self, text: str) -> List[str]:
        """
        Dzieli tekst na słowa.
        
        Args:
            text (str): Tekst do podziału
            
        Returns:
            List[str]: Lista słów
        """
        # Tokenizujemy słowa
        words = nltk.word_tokenize(text.lower())
        
        # Usuwamy znaki interpunkcyjne i cyfry
        words = [word for word in words if word.isalpha()]
        
        return words
    
    def remove_stopwords(self, words: List[str]) -> List[str]:
        """
        Usuwa stop words z listy słów.
        
        Args:
            words (List[str]): Lista słów
            
        Returns:
            List[str]: Lista słów bez stop words
        """
        return [word for word in words if word.lower() not in self.stop_words]
    
    def preprocess_sentence(self, sentence: str) -> List[str]:
        """
        Przetwarza zdanie: tokenizuje i usuwa stop words.
        
        Args:
            sentence (str): Zdanie do przetworzenia
            
        Returns:
            List[str]: Lista przetworzonych słów
        """
        words = self.word_tokenize(sentence)
        words = self.remove_stopwords(words)
        return words
    
    def calculate_word_frequency(self, words: List[str]) -> dict:
        """
        Oblicza częstotliwość występowania słów.
        
        Args:
            words (List[str]): Lista słów
            
        Returns:
            dict: Słownik z częstotliwościami słów
        """
        return dict(Counter(words))
    
    def get_top_words(self, words: List[str], top_k: int = 10) -> List[tuple]:
        """
        Zwraca top-K najczęstszych słów.
        
        Args:
            words (List[str]): Lista słów
            top_k (int): Liczba słów do zwrócenia
            
        Returns:
            List[tuple]: Lista krotek (słowo, częstotliwość)
        """
        word_freq = self.calculate_word_frequency(words)
        return Counter(word_freq).most_common(top_k)
