"""
Moduł do podsumowywania tekstu przy użyciu algorytmu TextRank.
"""
import numpy as np
import networkx as nx
from typing import List, Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text_processor import TextProcessor


class TextRankSummarizer:
    """Klasa implementująca podsumowywanie ekstrakcyjne przy użyciu TextRank."""
    
    def __init__(self, language: str = 'polish'):
        """
        Inicjalizuje summarizer.
        
        Args:
            language (str): Język tekstu
        """
        self.language = language
        self.text_processor = TextProcessor(language)
    
    def _calculate_sentence_similarity(self, sentences: List[str]) -> np.ndarray:
        """
        Oblicza podobieństwo między zdaniami przy użyciu TF-IDF i cosine similarity.
        
        Args:
            sentences (List[str]): Lista zdań
            
        Returns:
            np.ndarray: Macierz podobieństwa zdań
        """
        # Przetwarzamy zdania
        processed_sentences = []
        for sentence in sentences:
            words = self.text_processor.preprocess_sentence(sentence)
            processed_sentences.append(' '.join(words))
        
        # Obliczamy TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(processed_sentences)
        
        # Obliczamy cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        return similarity_matrix
    
    def _build_similarity_graph(self, similarity_matrix: np.ndarray, threshold: float = 0.1) -> nx.Graph:
        """
        Buduje graf podobieństwa zdań.
        
        Args:
            similarity_matrix (np.ndarray): Macierz podobieństwa
            threshold (float): Próg podobieństwa dla tworzenia krawędzi
            
        Returns:
            nx.Graph: Graf podobieństwa
        """
        graph = nx.Graph()
        n_sentences = similarity_matrix.shape[0]
        
        # Dodajemy węzły
        for i in range(n_sentences):
            graph.add_node(i)
        
        # Dodajemy krawędzie na podstawie podobieństwa
        for i in range(n_sentences):
            for j in range(i + 1, n_sentences):
                similarity = similarity_matrix[i][j]
                if similarity > threshold:
                    graph.add_edge(i, j, weight=similarity)
        
        return graph
    
    def _calculate_textrank_scores(self, graph: nx.Graph) -> Dict[int, float]:
        """
        Oblicza wyniki TextRank dla każdego zdania.
        
        Args:
            graph (nx.Graph): Graf podobieństwa zdań
            
        Returns:
            Dict[int, float]: Słownik z wynikami TextRank dla każdego zdania
        """
        try:
            # Używamy PageRank do obliczenia wyników
            scores = nx.pagerank(graph, max_iter=100, tol=1e-4)
        except:
            # Jeśli graf jest pusty lub ma problemy, zwracamy równe wyniki
            scores = {node: 1.0 for node in graph.nodes()}
        
        return scores
    
    def summarize(self, text: str, num_sentences: int = 3) -> Tuple[str, List[str]]:
        """
        Tworzy podsumowanie tekstu.
        
        Args:
            text (str): Tekst do podsumowania
            num_sentences (int): Liczba zdań w podsumowaniu
            
        Returns:
            Tuple[str, List[str]]: Podsumowanie i lista najważniejszych zdań
        """
        # Dzielimy tekst na zdania
        sentences = self.text_processor.sentence_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text, sentences
        
        # Obliczamy podobieństwo zdań
        similarity_matrix = self._calculate_sentence_similarity(sentences)
        
        # Budujemy graf
        graph = self._build_similarity_graph(similarity_matrix)
        
        # Obliczamy wyniki TextRank
        scores = self._calculate_textrank_scores(graph)
        
        # Sortujemy zdania według wyników
        ranked_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Wybieramy top zdania
        top_sentence_indices = [idx for idx, score in ranked_sentences[:num_sentences]]
        top_sentence_indices.sort()  # Zachowujemy kolejność z oryginalnego tekstu
        
        top_sentences = [sentences[i] for i in top_sentence_indices]
        summary = ' '.join(top_sentences)
        
        return summary, top_sentences
    
    def extract_keywords(self, text: str, num_keywords: int = 10) -> List[Tuple[str, float]]:
        """
        Ekstraktuje słowa kluczowe z tekstu.
        
        Args:
            text (str): Tekst do analizy
            num_keywords (int): Liczba słów kluczowych do zwrócenia
            
        Returns:
            List[Tuple[str, float]]: Lista krotek (słowo, waga)
        """
        # Dzielimy tekst na zdania i przetwarzamy
        sentences = self.text_processor.sentence_tokenize(text)
        all_words = []
        
        for sentence in sentences:
            words = self.text_processor.preprocess_sentence(sentence)
            all_words.extend(words)
        
        # Obliczamy częstotliwość słów
        word_freq = self.text_processor.calculate_word_frequency(all_words)
        
        # Normalizujemy częstotliwości
        max_freq = max(word_freq.values()) if word_freq else 1
        normalized_freq = {word: freq / max_freq for word, freq in word_freq.items()}
        
        # Sortujemy i zwracamy top słowa
        sorted_words = sorted(normalized_freq.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_words[:num_keywords]


class SimpleSummarizer:
    """Prostsza wersja summarizera oparta na częstotliwości słów."""
    
    def __init__(self, language: str = 'polish'):
        """
        Inicjalizuje prosty summarizer.
        
        Args:
            language (str): Język tekstu
        """
        self.language = language
        self.text_processor = TextProcessor(language)
    
    def _score_sentences(self, sentences: List[str], word_freq: Dict[str, int]) -> List[Tuple[int, float]]:
        """
        Ocenia zdania na podstawie częstotliwości zawartych w nich słów.
        
        Args:
            sentences (List[str]): Lista zdań
            word_freq (Dict[str, int]): Częstotliwość słów
            
        Returns:
            List[Tuple[int, float]]: Lista krotek (indeks zdania, wynik)
        """
        sentence_scores = []
        
        for i, sentence in enumerate(sentences):
            words = self.text_processor.preprocess_sentence(sentence)
            if not words:
                sentence_scores.append((i, 0.0))
                continue
            
            # Obliczamy wynik jako średnią ważoną częstotliwości słów
            score = sum(word_freq.get(word, 0) for word in words) / len(words)
            sentence_scores.append((i, score))
        
        return sentence_scores
    
    def summarize(self, text: str, num_sentences: int = 3) -> Tuple[str, List[str]]:
        """
        Tworzy podsumowanie tekstu na podstawie częstotliwości słów.
        
        Args:
            text (str): Tekst do podsumowania
            num_sentences (int): Liczba zdań w podsumowaniu
            
        Returns:
            Tuple[str, List[str]]: Podsumowanie i lista najważniejszych zdań
        """
        # Dzielimy tekst na zdania
        sentences = self.text_processor.sentence_tokenize(text)
        
        if len(sentences) <= num_sentences:
            return text, sentences
        
        # Obliczamy częstotliwość słów w całym tekście
        all_words = []
        for sentence in sentences:
            words = self.text_processor.preprocess_sentence(sentence)
            all_words.extend(words)
        
        word_freq = self.text_processor.calculate_word_frequency(all_words)
        
        # Oceniamy zdania
        sentence_scores = self._score_sentences(sentences, word_freq)
        
        # Sortujemy według wyników
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Wybieramy top zdania
        top_sentence_indices = [idx for idx, score in sentence_scores[:num_sentences]]
        top_sentence_indices.sort()  # Zachowujemy kolejność z oryginalnego tekstu
        
        top_sentences = [sentences[i] for i in top_sentence_indices]
        summary = ' '.join(top_sentences)
        
        return summary, top_sentences
