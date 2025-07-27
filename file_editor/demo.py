#!/usr/bin/env python3
"""
Demo i testy dla Batch File Editor
==================================

Ten skrypt tworzy przykładowe pliki do testowania funkcjonalności
narzędzia batch_file_editor.py
"""

import os
from pathlib import Path
from PIL import Image
import random


def create_test_files():
    """Tworzy przykładowe pliki do testowania"""
    
    # Utwórz folder testowy
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    print(f"🔧 Tworzenie plików testowych w {test_dir}/")
    
    # 1. Obrazy testowe
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    for i in range(5):
        # Utwórz prostą kolorową grafikę
        img = Image.new('RGB', (800, 600), colors[i])
        
        # Zapisz jako JPEG
        img.save(test_dir / f"IMG_{i+1:03d}.jpg", quality=95)
        
        # Zapisz jako PNG z przezroczystością
        img_rgba = Image.new('RGBA', (400, 300), colors[i] + (128,))
        img_rgba.save(test_dir / f"graphic_{i+1}.png")
    
    # 2. Pliki tekstowe
    sample_texts = [
        "To jest przykładowy plik tekstowy.\n\n\n\nZ wieloma pustymi liniami.   \n\nI spacjami na końcu.     ",
        "Ten plik ma\ttabulatory\tmixed\tz\tspacjami   \n\tI różne wcięcia  ",
        "Normalny tekst bez problemów formatowania.\nProsty i czysty.",
        "#!/usr/bin/env python3\n\ndef hello():\n    print('Hello World')    \n\n\n    return True\n",
        "// JavaScript code\nfunction test() {\n\tconsole.log('test');  \n\n\treturn 42;\n}\n"
    ]
    
    extensions = ['.txt', '.py', '.js', '.md', '.html']
    
    for i, (text, ext) in enumerate(zip(sample_texts, extensions)):
        with open(test_dir / f"sample_{i+1}{ext}", 'w', encoding='utf-8') as f:
            f.write(text)
    
    # 3. Pliki różnych formatów do organizacji
    misc_files = [
        ('document.pdf', b'%PDF-1.4 fake pdf content'),
        ('data.json', '{"name": "test", "value": 123}'),
        ('style.css', 'body { margin: 0; padding: 0; }'),
        ('readme.txt', 'This is a readme file'),
        ('noextension', 'File without extension'),
    ]
    
    for filename, content in misc_files:
        filepath = test_dir / filename
        if isinstance(content, str):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            with open(filepath, 'wb') as f:
                f.write(content)
    
    print(f"✅ Utworzono pliki testowe:")
    print(f"   - 5 obrazów JPEG (IMG_001.jpg - IMG_005.jpg)")
    print(f"   - 5 obrazów PNG (graphic_1.png - graphic_5.png)")
    print(f"   - 5 plików tekstowych (.txt, .py, .js, .md, .html)")
    print(f"   - 5 plików różnych formatów (do organizacji)")
    print(f"\n🚀 Możesz teraz testować narzędzie!")


def run_demo():
    """Uruchamia demonstrację wszystkich funkcji"""
    
    print("🎬 DEMONSTRACJA BATCH FILE EDITOR")
    print("=" * 50)
    
    # Sprawdź czy istnieją pliki testowe
    test_dir = Path("test_files")
    if not test_dir.exists() or not any(test_dir.iterdir()):
        print("📁 Tworzę pliki testowe...")
        create_test_files()
    
    demo_commands = [
        {
            'title': '1. Podgląd zmiany nazw (IMG_xxx → Zdjecie_xxx)',
            'command': 'python batch_file_editor.py rename --pattern "IMG_(\\d+)" --replacement "Zdjecie_\\1" --directory test_files'
        },
        {
            'title': '2. Podgląd konwersji PNG → JPEG',
            'command': 'python batch_file_editor.py convert --source png --target jpg --directory test_files'
        },
        {
            'title': '3. Podgląd kompresji obrazów',
            'command': 'python batch_file_editor.py compress --quality 60 --max-width 600 --directory test_files'
        },
        {
            'title': '4. Podgląd formatowania plików tekstowych',
            'command': 'python batch_file_editor.py format --operation normalize --directory test_files'
        },
        {
            'title': '5. Podgląd organizacji plików',
            'command': 'python batch_file_editor.py organize --directory test_files'
        }
    ]
    
    print("\n📋 LISTA KOMEND DO TESTOWANIA:")
    print("(Usuń słowo 'podgląd' i dodaj --execute aby wykonać)")
    print("-" * 50)
    
    for demo in demo_commands:
        print(f"\n{demo['title']}")
        print(f"Komenda: {demo['command']}")
    
    print("\n" + "=" * 50)
    print("💡 WSKAZÓWKI:")
    print("- Wszystkie komendy powyżej są w trybie podglądu (bezpieczne)")
    print("- Dodaj --execute na końcu aby wykonać operację")
    print("- Użyj --help aby zobaczyć wszystkie opcje")
    print("- Sprawdź folder test_files/ z przykładowymi plikami")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        create_test_files()
    else:
        run_demo()
