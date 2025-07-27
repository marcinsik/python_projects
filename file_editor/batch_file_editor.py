#!/usr/bin/env python3
"""
Narzędzie do batchowej obróbki plików
=====================================

Funkcjonalności:
- Masowa zmiana nazw plików
- Konwersja obrazów (JPEG → PNG, PNG → JPEG, etc.)
- Kompresja zdjęć
- Zmiana formatowania plików tekstowych
- Organizacja plików według rozszerzeń

Autor: Batch File Editor
Data: 2025-07-27
"""

import os
import sys
import argparse
import re
import shutil
from pathlib import Path
from PIL import Image, ImageOps
import json


class BatchFileEditor:
    """Główna klasa do batchowej obróbki plików"""
    
    def __init__(self, directory="."):
        self.directory = Path(directory).resolve()
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        self.supported_text_formats = {'.txt', '.md', '.py', '.js', '.html', '.css', '.xml', '.json'}
        
    def get_files_by_extension(self, extensions):
        """Pobiera listę plików o określonych rozszerzeniach"""
        files = []
        for ext in extensions:
            files.extend(self.directory.glob(f"*{ext}"))
            files.extend(self.directory.glob(f"*{ext.upper()}"))
        return files
    
    def rename_files_batch(self, pattern, replacement, dry_run=True):
        """
        Masowa zmiana nazw plików
        
        Args:
            pattern (str): Wzorzec do wyszukania (regex)
            replacement (str): Tekst zastępczy
            dry_run (bool): Tylko podgląd zmian bez wykonywania
        """
        print(f"\n🔄 Masowa zmiana nazw w katalogu: {self.directory}")
        print(f"Wzorzec: '{pattern}' → '{replacement}'")
        
        files = [f for f in self.directory.iterdir() if f.is_file()]
        changes = []
        
        for file_path in files:
            old_name = file_path.name
            new_name = re.sub(pattern, replacement, old_name)
            
            if new_name != old_name:
                new_path = file_path.parent / new_name
                changes.append((file_path, new_path))
        
        if not changes:
            print("❌ Nie znaleziono plików do zmiany nazwy")
            return
        
        print(f"\n📋 Znaleziono {len(changes)} plików do zmiany:")
        for old_path, new_path in changes:
            print(f"  {old_path.name} → {new_path.name}")
        
        if dry_run:
            print("\n⚠️  To był tylko podgląd. Użyj --execute aby wykonać zmiany.")
            return
        
        # Wykonaj zmiany
        success_count = 0
        for old_path, new_path in changes:
            try:
                if new_path.exists():
                    print(f"⚠️  Plik {new_path.name} już istnieje - pomijam")
                    continue
                old_path.rename(new_path)
                success_count += 1
            except Exception as e:
                print(f"❌ Błąd przy zmianie {old_path.name}: {e}")
        
        print(f"\n✅ Pomyślnie zmieniono nazwy {success_count} plików")
    
    def convert_images(self, source_format, target_format, quality=85, dry_run=True):
        """
        Konwersja obrazów między formatami
        
        Args:
            source_format (str): Format źródłowy (np. 'jpg', 'png')
            target_format (str): Format docelowy (np. 'png', 'jpg')
            quality (int): Jakość dla formatów stratnych (1-100)
            dry_run (bool): Tylko podgląd
        """
        print(f"\n🖼️  Konwersja obrazów {source_format.upper()} → {target_format.upper()}")
        
        source_ext = f".{source_format.lower()}"
        target_ext = f".{target_format.lower()}"
        
        image_files = self.get_files_by_extension([source_ext])
        
        if not image_files:
            print(f"❌ Nie znaleziono plików {source_format.upper()}")
            return
        
        print(f"📋 Znaleziono {len(image_files)} plików do konwersji:")
        for img_file in image_files:
            target_name = img_file.stem + target_ext
            print(f"  {img_file.name} → {target_name}")
        
        if dry_run:
            print("\n⚠️  To był tylko podgląd. Użyj --execute aby wykonać konwersję.")
            return
        
        success_count = 0
        for img_file in image_files:
            try:
                target_path = img_file.parent / (img_file.stem + target_ext)
                
                if target_path.exists():
                    print(f"⚠️  Plik {target_path.name} już istnieje - pomijam")
                    continue
                
                with Image.open(img_file) as img:
                    # Konwersja RGB dla JPEG
                    if target_format.lower() == 'jpg' and img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    # Zapisz z odpowiednią jakością
                    if target_format.lower() in ['jpg', 'jpeg']:
                        img.save(target_path, format='JPEG', quality=quality, optimize=True)
                    else:
                        img.save(target_path, format=target_format.upper())
                
                success_count += 1
                print(f"✅ Skonwertowano: {img_file.name}")
                
            except Exception as e:
                print(f"❌ Błąd przy konwersji {img_file.name}: {e}")
        
        print(f"\n🎉 Pomyślnie skonwertowano {success_count} obrazów")
    
    def compress_images(self, quality=70, max_width=1920, max_height=1080, dry_run=True):
        """
        Kompresja zdjęć z opcjonalną zmianą rozmiaru
        
        Args:
            quality (int): Jakość JPEG (1-100)
            max_width (int): Maksymalna szerokość
            max_height (int): Maksymalna wysokość
            dry_run (bool): Tylko podgląd
        """
        print(f"\n📉 Kompresja obrazów (jakość: {quality}%, max: {max_width}x{max_height})")
        
        image_files = self.get_files_by_extension(self.supported_image_formats)
        
        if not image_files:
            print("❌ Nie znaleziono obrazów do kompresji")
            return
        
        total_size_before = sum(f.stat().st_size for f in image_files)
        
        print(f"📋 Znaleziono {len(image_files)} obrazów")
        print(f"📊 Łączny rozmiar przed kompresją: {self.format_size(total_size_before)}")
        
        if dry_run:
            print("\n⚠️  To był tylko podgląd. Użyj --execute aby wykonać kompresję.")
            return
        
        # Utwórz folder na skompresowane pliki
        compressed_dir = self.directory / "compressed"
        compressed_dir.mkdir(exist_ok=True)
        
        success_count = 0
        total_size_after = 0
        
        for img_file in image_files:
            try:
                compressed_path = compressed_dir / img_file.name
                
                with Image.open(img_file) as img:
                    # Zmień rozmiar jeśli potrzeba
                    if img.width > max_width or img.height > max_height:
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # Konwertuj do RGB dla JPEG
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    # Zapisz z kompresją
                    img.save(compressed_path, format='JPEG', quality=quality, optimize=True)
                
                size_after = compressed_path.stat().st_size
                total_size_after += size_after
                
                size_before = img_file.stat().st_size
                reduction = ((size_before - size_after) / size_before) * 100
                
                print(f"✅ {img_file.name}: {self.format_size(size_before)} → {self.format_size(size_after)} (-{reduction:.1f}%)")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Błąd przy kompresji {img_file.name}: {e}")
        
        total_reduction = ((total_size_before - total_size_after) / total_size_before) * 100
        print(f"\n🎉 Skompresowano {success_count} obrazów")
        print(f"📊 Oszczędność miejsca: {self.format_size(total_size_before - total_size_after)} (-{total_reduction:.1f}%)")
    
    def format_text_files(self, operation='normalize', encoding='utf-8', dry_run=True):
        """
        Formatowanie plików tekstowych
        
        Args:
            operation (str): 'normalize' (usuwa nadmiarowe spacje/newline), 'tabs_to_spaces', 'spaces_to_tabs'
            encoding (str): Kodowanie plików
            dry_run (bool): Tylko podgląd
        """
        print(f"\n📝 Formatowanie plików tekstowych: {operation}")
        
        text_files = self.get_files_by_extension(self.supported_text_formats)
        
        if not text_files:
            print("❌ Nie znaleziono plików tekstowych")
            return
        
        print(f"📋 Znaleziono {len(text_files)} plików tekstowych")
        
        if dry_run:
            print("\n⚠️  To był tylko podgląd. Użyj --execute aby wykonać formatowanie.")
            return
        
        # Utwórz folder backup
        backup_dir = self.directory / "backup_text"
        backup_dir.mkdir(exist_ok=True)
        
        success_count = 0
        
        for text_file in text_files:
            try:
                # Backup oryginalnego pliku
                backup_path = backup_dir / text_file.name
                shutil.copy2(text_file, backup_path)
                
                # Wczytaj zawartość
                with open(text_file, 'r', encoding=encoding) as f:
                    content = f.read()
                
                original_lines = len(content.splitlines())
                
                # Zastosuj formatowanie
                if operation == 'normalize':
                    # Usuń nadmiarowe spacje i newline
                    lines = content.splitlines()
                    lines = [line.rstrip() for line in lines]  # Usuń spacje na końcu linii
                    # Usuń wielokrotne puste linie
                    normalized_lines = []
                    prev_empty = False
                    for line in lines:
                        if line.strip() == '':
                            if not prev_empty:
                                normalized_lines.append('')
                            prev_empty = True
                        else:
                            normalized_lines.append(line)
                            prev_empty = False
                    content = '\n'.join(normalized_lines)
                
                elif operation == 'tabs_to_spaces':
                    content = content.expandtabs(4)  # Konwertuj tab na 4 spacje
                
                elif operation == 'spaces_to_tabs':
                    lines = content.splitlines()
                    converted_lines = []
                    for line in lines:
                        # Konwertuj leading spaces na taby
                        leading_spaces = len(line) - len(line.lstrip(' '))
                        if leading_spaces > 0:
                            tabs = leading_spaces // 4
                            remaining_spaces = leading_spaces % 4
                            line = '\t' * tabs + ' ' * remaining_spaces + line.lstrip(' ')
                        converted_lines.append(line)
                    content = '\n'.join(converted_lines)
                
                # Zapisz sformatowaną zawartość
                with open(text_file, 'w', encoding=encoding) as f:
                    f.write(content)
                
                new_lines = len(content.splitlines())
                print(f"✅ {text_file.name}: {original_lines} → {new_lines} linii")
                success_count += 1
                
            except Exception as e:
                print(f"❌ Błąd przy formatowaniu {text_file.name}: {e}")
        
        print(f"\n🎉 Sformatowano {success_count} plików")
        print(f"💾 Kopie zapasowe w: {backup_dir}")
    
    def organize_files_by_extension(self, dry_run=True):
        """Organizuje pliki w foldery według rozszerzeń"""
        print(f"\n📁 Organizacja plików według rozszerzeń")
        
        files = [f for f in self.directory.iterdir() if f.is_file()]
        
        if not files:
            print("❌ Nie znaleziono plików do organizacji")
            return
        
        # Grupuj pliki według rozszerzeń
        extensions = {}
        for file_path in files:
            ext = file_path.suffix.lower()
            if ext == '':
                ext = 'no_extension'
            if ext not in extensions:
                extensions[ext] = []
            extensions[ext].append(file_path)
        
        print(f"📋 Znaleziono pliki z {len(extensions)} różnymi rozszerzeniami:")
        for ext, file_list in extensions.items():
            print(f"  {ext}: {len(file_list)} plików")
        
        if dry_run:
            print("\n⚠️  To był tylko podgląd. Użyj --execute aby wykonać organizację.")
            return
        
        success_count = 0
        for ext, file_list in extensions.items():
            try:
                # Utwórz folder dla rozszerzenia
                if ext == 'no_extension':
                    folder_name = 'bez_rozszerzenia'
                else:
                    folder_name = ext[1:]  # Usuń kropkę
                
                ext_dir = self.directory / folder_name
                ext_dir.mkdir(exist_ok=True)
                
                # Przenieś pliki
                for file_path in file_list:
                    target_path = ext_dir / file_path.name
                    if target_path.exists():
                        print(f"⚠️  Plik {target_path.name} już istnieje w {folder_name}/")
                        continue
                    file_path.rename(target_path)
                    success_count += 1
                
                print(f"✅ Przeniesiono {len(file_list)} plików do {folder_name}/")
                
            except Exception as e:
                print(f"❌ Błąd przy organizacji {ext}: {e}")
        
        print(f"\n🎉 Zorganizowano {success_count} plików")
    
    @staticmethod
    def format_size(size_bytes):
        """Formatuje rozmiar pliku w czytelny sposób"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"


def main():
    parser = argparse.ArgumentParser(
        description="Narzędzie do batchowej obróbki plików",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:

1. Zmiana nazw plików (podgląd):
   python batch_file_editor.py rename --pattern "IMG_(\\d+)" --replacement "Zdjecie_\\1" --directory ./photos

2. Konwersja JPEG → PNG (wykonanie):
   python batch_file_editor.py convert --source jpg --target png --execute

3. Kompresja obrazów:
   python batch_file_editor.py compress --quality 60 --max-width 1600 --execute

4. Formatowanie plików tekstowych:
   python batch_file_editor.py format --operation normalize --execute

5. Organizacja plików według rozszerzeń:
   python batch_file_editor.py organize --execute
        """
    )
    
    parser.add_argument('--directory', '-d', default='.', 
                       help='Katalog do przetworzenia (domyślnie: bieżący)')
    parser.add_argument('--execute', action='store_true',
                       help='Wykonaj operację (bez tego flagi będzie tylko podgląd)')
    
    subparsers = parser.add_subparsers(dest='command', help='Dostępne operacje')
    
    # Rename command
    rename_parser = subparsers.add_parser('rename', help='Masowa zmiana nazw plików')
    rename_parser.add_argument('--pattern', required=True, help='Wzorzec regex do wyszukania')
    rename_parser.add_argument('--replacement', required=True, help='Tekst zastępczy')
    
    # Convert command  
    convert_parser = subparsers.add_parser('convert', help='Konwersja obrazów')
    convert_parser.add_argument('--source', required=True, help='Format źródłowy (jpg, png, etc.)')
    convert_parser.add_argument('--target', required=True, help='Format docelowy (jpg, png, etc.)')
    convert_parser.add_argument('--quality', type=int, default=85, help='Jakość dla JPEG (1-100)')
    
    # Compress command
    compress_parser = subparsers.add_parser('compress', help='Kompresja obrazów')
    compress_parser.add_argument('--quality', type=int, default=70, help='Jakość JPEG (1-100)')
    compress_parser.add_argument('--max-width', type=int, default=1920, help='Maksymalna szerokość')
    compress_parser.add_argument('--max-height', type=int, default=1080, help='Maksymalna wysokość')
    
    # Format command
    format_parser = subparsers.add_parser('format', help='Formatowanie plików tekstowych')
    format_parser.add_argument('--operation', choices=['normalize', 'tabs_to_spaces', 'spaces_to_tabs'],
                              default='normalize', help='Typ formatowania')
    format_parser.add_argument('--encoding', default='utf-8', help='Kodowanie plików')
    
    # Organize command
    organize_parser = subparsers.add_parser('organize', help='Organizacja plików według rozszerzeń')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Sprawdź czy katalog istnieje
    if not os.path.exists(args.directory):
        print(f"❌ Katalog {args.directory} nie istnieje!")
        return
    
    editor = BatchFileEditor(args.directory)
    dry_run = not args.execute
    
    if dry_run:
        print("🔍 TRYB PODGLĄDU - żadne pliki nie zostaną zmienione")
        print("Użyj flagi --execute aby wykonać operację\n")
    
    try:
        if args.command == 'rename':
            editor.rename_files_batch(args.pattern, args.replacement, dry_run)
            
        elif args.command == 'convert':
            editor.convert_images(args.source, args.target, args.quality, dry_run)
            
        elif args.command == 'compress':
            editor.compress_images(args.quality, args.max_width, args.max_height, dry_run)
            
        elif args.command == 'format':
            editor.format_text_files(args.operation, args.encoding, dry_run)
            
        elif args.command == 'organize':
            editor.organize_files_by_extension(dry_run)
            
    except KeyboardInterrupt:
        print("\n⚠️  Operacja przerwana przez użytkownika")
    except Exception as e:
        print(f"\n❌ Błąd: {e}")


if __name__ == "__main__":
    main()
