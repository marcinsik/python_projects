# TextSummarizer - Automatic Summary Generator

A tool for automatic text summarization and keyword extraction using natural language processing (NLP) techniques.

## 🎯 Project Goal

Create an intelligent tool that automatically:
- Summarizes long texts
- Extracts keywords
- Processes text from various sources

## 🚀 Current Status: Stage 1 - NLP Basics

### ✅ Implemented Features

1. **Reading Text Files**
   - Support for .txt files with UTF-8 encoding
   - Validation and error handling

2. **Basic NLP Processing**
   - Sentence segmentation (splitting text into sentences)
   - Word tokenization
   - Stop words removal (Polish and English)
   - Word frequency calculation

3. **Extractive Summarization**
   - **TextRank Algorithm**: Advanced graph-based algorithm
   - **Frequency Method**: Simpler fallback method
   - Returns N most important sentences from the original text

4. **Keyword Extraction**
   - Identification of the most important words/phrases
   - Ranking by weight/frequency
   - Normalization of results

## 🛠️ Technologies

- **Python 3.13+**
- **NLTK** - Natural language processing
- **scikit-learn** - TF-IDF, cosine similarity
- **NetworkX** - Graph algorithms (PageRank/TextRank)
- **NumPy** - Matrix operations

## 📦 Installation

1. **Clone the project**:
```bash
cd /home/Marcin/Pulpit/python_projects/summary_generator_using_NLP
```

2. **Activate the virtual environment**:
```bash
source .venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download NLTK data** (automatically on first run):
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## 🎮 Usage

### Run the Demo

```bash
python app.py
```

The program will automatically:
1. Demonstrate basic NLP processing
2. Create a sample text file
3. Perform summarization and keyword extraction
4. Process all .txt files in the `test_data/` directory

### Programmatic Usage

```python
from src.file_reader import read_text_file
from src.summarizer import TextRankSummarizer
from src.text_processor import TextProcessor

# Load text
text = read_text_file("path/to/your/file.txt")

# Summarization
summarizer = TextRankSummarizer(language='polish')
summary, sentences = summarizer.summarize(text, num_sentences=3)
keywords = summarizer.extract_keywords(text, num_keywords=10)

print("Summary:", summary)
print("Keywords:", keywords)
```

## 📁 Project Structure

```
summary_generator_using_NLP/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── file_reader.py           # Reading text files
│   ├── text_processor.py        # NLP processing
│   └── summarizer.py            # Summarization algorithms
├── test_data/                   # Sample files for testing
│   └── sample_ai_article.txt    # Automatically generated example
├── app.py                       # Main demo application
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## 🧪 Example Output

### Input Text:
```
Artificial intelligence (AI) is a field of computer science that is developing at an extraordinary pace.
Modern AI systems can recognize images, process natural language, and make complex decisions. Machine learning is the foundation of most modern AI solutions...
```

### Summary Output:
```
Artificial intelligence (AI) is a field of computer science that is developing at an extraordinary pace.
Deep learning, using artificial neural networks, is revolutionizing many fields.
The future of artificial intelligence looks promising.
```

### Keywords:
```
1. intelligence     (weight: 1.000)
2. learning         (weight: 0.857)
3. artificial       (weight: 0.714)
4. systems          (weight: 0.571)
5. language         (weight: 0.429)
```

## 🔮 Planned Extensions (Stage 2)

### 📄 Support for Various Sources
- **PDF files**: PyPDF2/pdfplumber
- **Web pages**: requests + BeautifulSoup
- **Word documents**: python-docx

### 🤖 Advanced NLP Models
- **Transformers (Hugging Face)**: T5, BART, mT5
- **Abstractive summarization**: Generating new sentences
- **Multilingual models**: Support for various languages

### 🖥️ User Interfaces
- **CLI**: argparse/Click for command line
- **Web GUI**: Streamlit for interactive dashboard
- **API**: Flask/FastAPI for integration

## 🧠 Technical Details

### TextRank Algorithm

TextRank is a PageRank-based algorithm that:
1. Builds a sentence graph (nodes = sentences, edges = similarity)
2. Calculates similarity using TF-IDF and cosine similarity
3. Finds the most important sentences with the PageRank algorithm
4. Returns N top-ranked sentences

### Polish Language Processing

The project supports Polish by:
- Custom list of Polish stop words
- Sentence segmentation adapted to Polish punctuation
- Text normalization with Polish diacritics




