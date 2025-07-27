#!/bin/bash
# 
# Przykłady użycia Batch File Editor
# ==================================
# 
# Ten skript zawiera przykłady wszystkich dostępnych operacji
# Uruchom: chmod +x examples.sh && ./examples.sh
#

# Kolory do wyświetlania
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Ścieżka do środowiska Python
PYTHON="/home/Marcin/Pulpit/python_projects/file_editor/.venv/bin/python"
SCRIPT="batch_file_editor.py"

echo -e "${BLUE}🔧 BATCH FILE EDITOR - PRZYKŁADY UŻYCIA${NC}"
echo "=" * 50

echo -e "\n${YELLOW}📁 Tworzenie plików testowych...${NC}"
$PYTHON demo.py create

echo -e "\n${GREEN}1. MASOWA ZMIANA NAZW PLIKÓW${NC}"
echo -e "${YELLOW}Podgląd - zmiana 'graphic_' na 'obraz_':${NC}"
$PYTHON $SCRIPT --directory test_files rename --pattern "graphic_" --replacement "obraz_"

echo -e "\n${YELLOW}Wykonanie zmiany nazw:${NC}"
read -p "Czy wykonać zmianę nazw? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PYTHON $SCRIPT --directory test_files --execute rename --pattern "graphic_" --replacement "obraz_"
else
    echo "Pominięto zmianę nazw"
fi

echo -e "\n${GREEN}2. KONWERSJA OBRAZÓW${NC}"
echo -e "${YELLOW}Podgląd konwersji PNG → JPEG:${NC}"
$PYTHON $SCRIPT --directory test_files convert --source png --target jpg --quality 85

echo -e "\n${YELLOW}Wykonanie konwersji:${NC}"
read -p "Czy wykonać konwersję? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PYTHON $SCRIPT --directory test_files --execute convert --source png --target jpg --quality 85
else
    echo "Pominięto konwersję"
fi

echo -e "\n${GREEN}3. KOMPRESJA OBRAZÓW${NC}"
echo -e "${YELLOW}Podgląd kompresji (jakość 60%, max 800x600):${NC}"
$PYTHON $SCRIPT --directory test_files compress --quality 60 --max-width 800 --max-height 600

echo -e "\n${YELLOW}Wykonanie kompresji:${NC}"
read -p "Czy wykonać kompresję? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PYTHON $SCRIPT --directory test_files --execute compress --quality 60 --max-width 800 --max-height 600
else
    echo "Pominięto kompresję"
fi

echo -e "\n${GREEN}4. FORMATOWANIE PLIKÓW TEKSTOWYCH${NC}"
echo -e "${YELLOW}Podgląd normalizacji formatowania:${NC}"
$PYTHON $SCRIPT --directory test_files format --operation normalize

echo -e "\n${YELLOW}Wykonanie formatowania:${NC}"
read -p "Czy wykonać formatowanie? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PYTHON $SCRIPT --directory test_files --execute format --operation normalize
else
    echo "Pominięto formatowanie"
fi

echo -e "\n${GREEN}5. ORGANIZACJA PLIKÓW${NC}"
echo -e "${YELLOW}Podgląd organizacji według rozszerzeń:${NC}"
$PYTHON $SCRIPT --directory test_files organize

echo -e "\n${YELLOW}Wykonanie organizacji:${NC}"
read -p "Czy wykonać organizację? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    $PYTHON $SCRIPT --directory test_files --execute organize
else
    echo "Pominięto organizację"
fi

echo -e "\n${BLUE}✅ DEMO ZAKOŃCZONE${NC}"
echo -e "\n${YELLOW}💡 WSKAZÓWKI:${NC}"
echo "- Wszystkie operacje można uruchomić bez --execute dla podglądu"
echo "- Sprawdź folder test_files/ aby zobaczyć rezultaty"
echo "- Użyj --help aby zobaczyć wszystkie opcje"
echo "- Kopie zapasowe są tworzone automatycznie"

echo -e "\n${GREEN}📋 LISTA WSZYSTKICH KOMEND:${NC}"
echo ""
echo "# Zmiana nazw (regex):"
echo "$PYTHON $SCRIPT --directory [FOLDER] rename --pattern '[WZORZEC]' --replacement '[ZAMIENNIK]' --execute"
echo ""
echo "# Konwersja obrazów:"
echo "$PYTHON $SCRIPT --directory [FOLDER] convert --source [FORMAT] --target [FORMAT] --execute"
echo ""
echo "# Kompresja:"
echo "$PYTHON $SCRIPT --directory [FOLDER] compress --quality [1-100] --max-width [PX] --execute"
echo ""
echo "# Formatowanie tekstów:"
echo "$PYTHON $SCRIPT --directory [FOLDER] format --operation [normalize|tabs_to_spaces|spaces_to_tabs] --execute"
echo ""
echo "# Organizacja plików:"
echo "$PYTHON $SCRIPT --directory [FOLDER] organize --execute"
