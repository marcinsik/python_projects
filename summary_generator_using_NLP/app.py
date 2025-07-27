#!/usr/bin/env python3
"""
Główna aplikacja TextSummarizer - Etap 1: Podstawy NLP i Podsumowywanie Ekstrakcyjne

To narzędzie implementuje:
1. Czytanie plików tekstowych
2. Podstawowe przetwarzanie NLP (tokenizacja, usuwanie stop words)
3. Podsumowywanie ekstrakcyjne (TextRank i metoda częstotliwościowa)
4. Ekstrakcję słów kluczowych
"""

import os
import sys
from src.file_reader import read_text_file
from src.text_processor import TextProcessor
from src.summarizer import TextRankSummarizer, SimpleSummarizer


def print_separator():
    """Drukuje separator wizualny."""
    print("=" * 80)


def print_header(title: str):
    """Drukuje nagłówek sekcji."""
    print_separator()
    print(f"  {title}")
    print_separator()


def demonstrate_text_processing():
    """Demonstracja podstawowego przetwarzania tekstu."""
    print_header("DEMONSTRACJA PRZETWARZANIA TEKSTU NLP")
    
    # Przykładowy tekst
    sample_text = """
    Sztuczna inteligencja to dziedzina informatyki, która zajmuje się tworzeniem systemów 
    zdolnych do wykonywania zadań wymagających inteligencji. Uczenie maszynowe jest 
    poddziedziną sztucznej inteligencji. Głębokie uczenie wykorzystuje sieci neuronowe 
    do rozwiązywania skomplikowanych problemów. Przetwarzanie języka naturalnego pozwala 
    komputerom rozumieć i generować ludzki język.
    """
    
    processor = TextProcessor(language='polish')
    
    print("ORYGINALNY TEKST:")
    print(sample_text.strip())
    print()
    
    # Segmentacja zdań
    sentences = processor.sentence_tokenize(sample_text)
    print(f"SEGMENTACJA ZDAŃ ({len(sentences)} zdań):")
    for i, sentence in enumerate(sentences, 1):
        print(f"  {i}. {sentence}")
    print()
    
    # Tokenizacja słów
    words = processor.word_tokenize(sample_text)
    print(f"TOKENIZACJA SŁÓW ({len(words)} słów):")
    print(f"  {words[:15]}...")  # Pokazujemy pierwsze 15 słów
    print()
    
    # Usuwanie stop words
    words_no_stop = processor.remove_stopwords(words)
    print(f"PO USUNIĘCIU STOP WORDS ({len(words_no_stop)} słów):")
    print(f"  {words_no_stop}")
    print()
    
    # Częstotliwość słów
    word_freq = processor.calculate_word_frequency(words_no_stop)
    print("CZĘSTOTLIWOŚĆ SŁÓW:")
    for word, freq in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {word}: {freq}")
    print()


def demonstrate_summarization(text: str):
    """Demonstracja podsumowywania tekstu."""
    print_header("DEMONSTRACJA PODSUMOWYWANIA TEKSTU")
    
    print("ORYGINALNY TEKST:")
    print(text[:300] + "..." if len(text) > 300 else text)
    print()
    
    # TextRank Summarizer
    print("=== PODSUMOWANIE TEXTRANK ===")
    textrank_summarizer = TextRankSummarizer(language='polish')
    
    try:
        summary, sentences = textrank_summarizer.summarize(text, num_sentences=3)
        print("PODSUMOWANIE (3 zdania):")
        print(summary)
        print()
        
        print("WYBRANE ZDANIA:")
        for i, sentence in enumerate(sentences, 1):
            print(f"  {i}. {sentence}")
        print()
        
    except Exception as e:
        print(f"Błąd w TextRank: {e}")
        print("Używam prostszego algorytmu...")
        
        # Simple Summarizer jako fallback
        simple_summarizer = SimpleSummarizer(language='polish')
        summary, sentences = simple_summarizer.summarize(text, num_sentences=3)
        print("PODSUMOWANIE (metoda częstotliwościowa, 3 zdania):")
        print(summary)
        print()


def demonstrate_keyword_extraction(text: str):
    """Demonstracja ekstrakcji słów kluczowych."""
    print_header("DEMONSTRACJA EKSTRAKCJI SŁÓW KLUCZOWYCH")
    
    try:
        summarizer = TextRankSummarizer(language='polish')
        keywords = summarizer.extract_keywords(text, num_keywords=10)
        
        print("TOP 10 SŁÓW KLUCZOWYCH:")
        for i, (word, score) in enumerate(keywords, 1):
            print(f"  {i:2d}. {word:<15} (waga: {score:.3f})")
        print()
        
    except Exception as e:
        print(f"Błąd w ekstrakcji słów kluczowych: {e}")
        
        # Fallback - używamy prostej częstotliwości
        processor = TextProcessor(language='polish')
        sentences = processor.sentence_tokenize(text)
        all_words = []
        
        for sentence in sentences:
            words = processor.preprocess_sentence(sentence)
            all_words.extend(words)
        
        top_words = processor.get_top_words(all_words, top_k=10)
        
        print("TOP 10 SŁÓW (według częstotliwości):")
        for i, (word, freq) in enumerate(top_words, 1):
            print(f"  {i:2d}. {word:<15} (częstotliwość: {freq})")
        print()


def process_file(file_path: str):
    """Przetwarza plik tekstowy."""
    print_header(f"PRZETWARZANIE PLIKU: {file_path}")
    
    # Wczytujemy plik
    content = read_text_file(file_path)
    if content is None:
        print("Nie można wczytać pliku.")
        return
    
    print(f"Wczytano plik o długości: {len(content)} znaków")
    print()
    
    # Wykonujemy analizę
    demonstrate_summarization(content)
    demonstrate_keyword_extraction(content)


def create_sample_file():
    """Tworzy przykładowy plik do testowania."""
    sample_content = """
Sztuczna inteligencja (AI) to dziedzina informatyki, która rozwija się w niezwykłym tempie. 
Współczesne systemy AI potrafią rozpoznawać obrazy, przetwarzać język naturalny i podejmować 
złożone decyzje. Uczenie maszynowe stanowi fundament większości nowoczesnych rozwiązań AI.

Algorytmy uczenia maszynowego uczą się na podstawie danych, bez konieczności jawnego 
programowania każdej reguły. Istnieją różne typy uczenia: nadzorowane, nienadzorowane 
i uczenie ze wzmocnieniem. Każdy z tych typów ma swoje unikalne zastosowania.

Głębokie uczenie, wykorzystujące sztuczne sieci neuronowe, rewolucjonizuje wiele dziedzin. 
Od rozpoznawania mowy po autonomiczne pojazdy - sieci neuronowe znajdują zastosowanie 
wszędzie. Architektura transformerów zmieniła sposób przetwarzania języka naturalnego.

Przetwarzanie języka naturalnego (NLP) pozwala komputerom rozumieć i generować ludzki język. 
Nowoczesne modele językowe potrafią tworzyć spójne teksty, tłumaczyć między językami 
i odpowiadać na pytania. ChatGPT to przykład zaawansowanego modelu NLP.

Etyka w AI staje się coraz ważniejsza. Konieczne jest zapewnienie, że systemy AI są 
sprawiedliwe, przejrzyste i nie dyskryminują. Regulacje prawne dotyczące AI są 
obecnie opracowywane na całym świecie.

Przyszłość sztucznej inteligencji wygląda obiecująco. Oczekuje się przełomów w obszarach 
takich jak medycyna, edukacja i ochrona środowiska. AI może pomóc w rozwiązywaniu 
globalnych wyzwań ludzkości.
"""
    
    file_path = "/home/Marcin/Pulpit/python_projects/summary_generator_using_NLP/test_data/sample_ai_article.txt"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_content.strip())
    
    return file_path


def main():
    """Główna funkcja aplikacji."""
    print_header("TEXTSUMMARIZER - ETAP 1: PODSTAWY NLP")
    print("Narzędzie do automatycznego podsumowywania tekstu i ekstrakcji słów kluczowych")
    print()
    
    # Demonstracja podstawowego przetwarzania
    demonstrate_text_processing()
    
    # Sprawdzamy, czy istnieją pliki do przetworzenia
    test_data_dir = "/home/Marcin/Pulpit/python_projects/summary_generator_using_NLP/test_data"
    
    # Tworzymy przykładowy plik, jeśli nie istnieje
    sample_file = create_sample_file()
    print(f"Utworzono przykładowy plik: {sample_file}")
    print()
    
    # Przetwarzamy przykładowy plik
    process_file(sample_file)
    
    # Sprawdzamy inne pliki w katalogu test_data
    if os.path.exists(test_data_dir):
        txt_files = [f for f in os.listdir(test_data_dir) if f.endswith('.txt') and f != 'sample_ai_article.txt']
        
        if txt_files:
            print_header("DODATKOWE PLIKI DO PRZETWORZENIA")
            for txt_file in txt_files:
                file_path = os.path.join(test_data_dir, txt_file)
                process_file(file_path)
    
    print_header("ZAKOŃCZONO PRZETWARZANIE")



if __name__ == "__main__":
    main()
