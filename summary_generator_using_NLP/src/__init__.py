"""
TextSummarizer - Narzędzie do automatycznego podsumowywania tekstu i ekstrakcji słów kluczowych.
"""

from .file_reader import read_text_file, save_text_to_file
from .text_processor import TextProcessor
from .summarizer import TextRankSummarizer, SimpleSummarizer

__version__ = "1.0.0"
__author__ = "TextSummarizer"
