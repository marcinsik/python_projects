"""
Moduł do wczytywania i przetwarzania danych dla dashboard'u.
"""

import pandas as pd
import streamlit as st
from typing import Optional, List
import os


class DataLoader:
    """Klasa odpowiedzialna za wczytywanie i przetwarzanie danych."""
    
    def __init__(self, data_path: str = "data/sample_data.csv"):
        """
        Inicjalizacja loadera danych.
        
        Args:
            data_path: Ścieżka do pliku z danymi
        """
        self.data_path = data_path
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Wczytuje dane z pliku CSV.
        
        Returns:
            DataFrame z danymi
        """
        try:
            if os.path.exists(self.data_path):
                self.data = pd.read_csv(self.data_path)
                # Podstawowe czyszczenie danych
                self.data = self._clean_data(self.data)
                return self.data
            else:
                st.error(f"Nie znaleziono pliku danych: {self.data_path}")
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Błąd podczas wczytywania danych: {str(e)}")
            return pd.DataFrame()
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Czyści i przygotowuje dane.
        
        Args:
            df: DataFrame do oczyszczenia
            
        Returns:
            Oczyszczony DataFrame
        """
        # Usuń wiersze z brakującymi danymi
        df = df.dropna()
        
        # Sprawdź czy mamy wymagane kolumny
        required_columns = ['rok', 'wojewodztwo', 'pkb_mld_zl', 'bezrobocie_proc']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Brakuje wymaganej kolumny: {col}")
                return pd.DataFrame()
        
        # Konwertuj typy danych
        df['rok'] = pd.to_numeric(df['rok'], errors='coerce')
        df['pkb_mld_zl'] = pd.to_numeric(df['pkb_mld_zl'], errors='coerce')
        df['bezrobocie_proc'] = pd.to_numeric(df['bezrobocie_proc'], errors='coerce')
        
        # Usuń wiersze z błędnymi konwersjami
        df = df.dropna()
        
        # Dodaj PKB per capita jeśli mamy dane o ludności
        if 'ludnosc_tys' in df.columns:
            df['ludnosc_tys'] = pd.to_numeric(df['ludnosc_tys'], errors='coerce')
            df['pkb_per_capita'] = (df['pkb_mld_zl'] * 1000) / df['ludnosc_tys']
        
        return df
    
    def get_available_years(self) -> List[int]:
        """
        Zwraca listę dostępnych lat w danych.
        
        Returns:
            Lista lat
        """
        if self.data is not None:
            return sorted(self.data['rok'].unique().tolist())
        return []
    
    def get_available_voivodeships(self) -> List[str]:
        """
        Zwraca listę dostępnych województw.
        
        Returns:
            Lista województw
        """
        if self.data is not None:
            return sorted(self.data['wojewodztwo'].unique().tolist())
        return []
    
    def filter_data(self, 
                   voivodeships: Optional[List[str]] = None,
                   year_range: Optional[tuple] = None) -> pd.DataFrame:
        """
        Filtruje dane według województw i zakresu lat.
        
        Args:
            voivodeships: Lista województw do filtrowania
            year_range: Tuple (rok_start, rok_end)
            
        Returns:
            Przefiltrowany DataFrame
        """
        if self.data is None:
            return pd.DataFrame()
        
        filtered_data = self.data.copy()
        
        # Filtruj po województwach
        if voivodeships:
            filtered_data = filtered_data[filtered_data['wojewodztwo'].isin(voivodeships)]
        
        # Filtruj po latach
        if year_range:
            start_year, end_year = year_range
            filtered_data = filtered_data[
                (filtered_data['rok'] >= start_year) & 
                (filtered_data['rok'] <= end_year)
            ]
        
        return filtered_data
    
    def calculate_growth_rate(self, df: pd.DataFrame, metric: str, voivodeship: str) -> pd.DataFrame:
        """
        Oblicza tempo wzrostu dla danej metryki i województwa.
        
        Args:
            df: DataFrame z danymi
            metric: Nazwa kolumny z metryką
            voivodeship: Nazwa województwa
            
        Returns:
            DataFrame z tempem wzrostu
        """
        voiv_data = df[df['wojewodztwo'] == voivodeship].copy()
        voiv_data = voiv_data.sort_values('rok')
        
        if len(voiv_data) > 1:
            voiv_data[f'{metric}_wzrost_proc'] = voiv_data[metric].pct_change() * 100
        
        return voiv_data
    
    @st.cache_data
    def load_uploaded_file(_self, uploaded_file) -> pd.DataFrame:
        """
        Wczytuje dane z przesłanego pliku.
        
        Args:
            uploaded_file: Plik przesłany przez użytkownika
            
        Returns:
            DataFrame z danymi
        """
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Obsługiwane formaty: CSV, Excel (.xlsx, .xls)")
                return pd.DataFrame()
            
            return _self._clean_data(df)
        except Exception as e:
            st.error(f"Błąd podczas wczytywania pliku: {str(e)}")
            return pd.DataFrame()


def get_sample_data_info() -> dict:
    """
    Zwraca informacje o strukturze przykładowych danych.
    
    Returns:
        Słownik z informacjami o danych
    """
    return {
        "required_columns": [
            "rok",
            "wojewodztwo", 
            "pkb_mld_zl",
            "bezrobocie_proc"
        ],
        "optional_columns": [
            "ludnosc_tys"
        ],
        "description": "Dane powinny zawierać informacje o PKB i bezrobociu dla województw w poszczególnych latach."
    }
