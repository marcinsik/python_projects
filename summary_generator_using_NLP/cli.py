#!/usr/bin/env python3
"""
Prosty interfejs CLI dla TextSummarizer
Użycie: python cli.py <ścieżka_do_pliku> [--sentences N] [--keywords N]
"""

import sys
import argparse
from src.file_reader import read_text_file
from src.summarizer import TextRankSummarizer, SimpleSummarizer


def main():
    parser = argparse.ArgumentParser(
        description='TextSummarizer - Automatyczne podsumowywanie tekstu i ekstrakcja słów kluczowych'
    )
    
    parser.add_argument(
        'file_path', 
        help='Ścieżka do pliku tekstowego (.txt)'
    )
    
    parser.add_argument(
        '--sentences', '-s', 
        type=int, 
        default=3, 
        help='Liczba zdań w podsumowaniu (domyślnie: 3)'
    )
    
    parser.add_argument(
        '--keywords', '-k', 
        type=int, 
        default=10, 
        help='Liczba słów kluczowych (domyślnie: 10)'
    )
    
    parser.add_argument(
        '--language', '-l', 
        choices=['polish', 'english'], 
        default='polish', 
        help='Język tekstu (domyślnie: polish)'
    )
    
    parser.add_argument(
        '--simple', 
        action='store_true', 
        help='Użyj prostszego algorytmu częstotliwościowego zamiast TextRank'
    )
    
    args = parser.parse_args()
    
    # Wczytaj plik
    print(f"Wczytuję plik: {args.file_path}")
    text = read_text_file(args.file_path)
    
    if text is None:
        print("Błąd: Nie można wczytać pliku.")
        sys.exit(1)
    
    print(f"Wczytano {len(text)} znaków.")
    print()
    
    # Wybierz algorytm
    if args.simple:
        print("Używam prostego algorytmu częstotliwościowego...")
        summarizer = SimpleSummarizer(language=args.language)
    else:
        print("Używam algorytmu TextRank...")
        summarizer = TextRankSummarizer(language=args.language)
    
    # Generuj podsumowanie
    try:
        summary, sentences = summarizer.summarize(text, num_sentences=args.sentences)
        
        print("=" * 60)
        print("PODSUMOWANIE:")
        print("=" * 60)
        print(summary)
        print()
        
        print("WYBRANE ZDANIA:")
        for i, sentence in enumerate(sentences, 1):
            print(f"{i}. {sentence}")
        print()
        
    except Exception as e:
        print(f"Błąd podczas podsumowywania: {e}")
        if not args.simple:
            print("Próbuję z prostszym algorytmem...")
            simple_summarizer = SimpleSummarizer(language=args.language)
            summary, sentences = simple_summarizer.summarize(text, num_sentences=args.sentences)
            
            print("=" * 60)
            print("PODSUMOWANIE (algorytm częstotliwościowy):")
            print("=" * 60)
            print(summary)
            print()
    
    # Ekstraktuj słowa kluczowe
    if hasattr(summarizer, 'extract_keywords'):
        try:
            keywords = summarizer.extract_keywords(text, num_keywords=args.keywords)
            
            print("=" * 60)
            print("SŁOWA KLUCZOWE:")
            print("=" * 60)
            for i, (word, score) in enumerate(keywords, 1):
                print(f"{i:2d}. {word:<15} (waga: {score:.3f})")
            print()
            
        except Exception as e:
            print(f"Błąd podczas ekstrakcji słów kluczowych: {e}")
    
    print("Zakończono przetwarzanie.")


if __name__ == "__main__":
    main()
