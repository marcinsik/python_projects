"""
UI components for the GUS Analytical Dashboard.
"""

import streamlit as st
import pandas as pd
from config import Config
from session_manager import SessionManager
from data_loader import get_sample_data_info

class UIComponents:
    """Handles UI component rendering."""
    
    @staticmethod
    def render_header():
        """Render the main header."""
        st.markdown(Config.MAIN_HEADER_HTML, unsafe_allow_html=True)
    
    @staticmethod
    def render_data_source_section():
        """Render data source selection section."""
        st.markdown("### 📁 Źródło danych")
        
        data_source = st.radio(
            "Wybierz źródło danych:",
            ["Dane przykładowe", "Prześlij własny plik"],
            help="Wybierz między danymi przykładowymi a przesłaniem własnego pliku"
        )
        
        return UIComponents._handle_data_source(data_source)
    
    @staticmethod
    def _handle_data_source(data_source):
        """Handle data source selection logic."""
        session_manager = SessionManager()
        
        if data_source == "Prześlij własny plik":
            uploaded_file = st.file_uploader(
                "Prześlij plik CSV lub Excel",
                type=Config.SUPPORTED_FILE_TYPES,
                help="Plik powinien zawierać kolumny: rok, wojewodztwo, pkb_mld_zl, bezrobocie_proc"
            )
            
            if uploaded_file is not None:
                with st.spinner("Wczytywanie danych..."):
                    df = session_manager.get_data_loader().load_uploaded_file(uploaded_file)
                    if not df.empty:
                        session_manager.get_data_loader().data = df
                        session_manager.set_data_loaded(True)
                        st.success("✅ Dane zostały wczytane!")
                    else:
                        st.error("❌ Nie udało się wczytać danych")
        else:
            # Load sample data
            if not session_manager.is_data_loaded():
                with st.spinner("Wczytywanie danych przykładowych..."):
                    df = session_manager.get_data_loader().load_data()
                    if not df.empty:
                        session_manager.set_data_loaded(True)
                        st.success("✅ Dane przykładowe wczytane!")
                    else:
                        st.error("❌ Nie udało się wczytać danych przykładowych")
        
        return data_source
    
    @staticmethod
    def render_filters():
        """Render filter controls."""
        session_manager = SessionManager()
        
        if not session_manager.is_data_loaded():
            return None, None, None
        
        st.markdown("### 🔍 Filtry")
        
        # Get available options
        years = session_manager.get_data_loader().get_available_years()
        voivodeships = session_manager.get_data_loader().get_available_voivodeships()
        
        if not years or not voivodeships:
            return None, None, None
        
        # Year range slider
        year_range = st.slider(
            "Zakres lat:",
            min_value=min(years),
            max_value=max(years),
            value=(min(years), max(years)),
            help="Wybierz zakres lat do analizy"
        )
        
        # Voivodeship selection
        selected_voivodeships = st.multiselect(
            "Wybierz województwa:",
            options=voivodeships,
            default=voivodeships[:5],  # Default to first 5
            help="Wybierz województwa do analizy"
        )
        
        # Analysis type selection
        st.markdown("### 📊 Typ analizy")
        analysis_type = st.selectbox(
            "Wybierz typ analizy:",
            Config.ANALYSIS_TYPES
        )
        
        return year_range, selected_voivodeships, analysis_type
    
    @staticmethod
    def render_data_info():
        """Render data information section."""
        with st.expander("ℹ️ Informacje o danych"):
            info = get_sample_data_info()
            st.markdown("**Wymagane kolumny:**")
            for col in info["required_columns"]:
                st.markdown(f"• `{col}`")
            
            st.markdown("**Opcjonalne kolumny:**")
            for col in info["optional_columns"]:
                st.markdown(f"• `{col}`")
            
            st.markdown(f"**Opis:** {info['description']}")
    
    @staticmethod
    def render_sidebar():
        """Render complete sidebar."""
        with st.sidebar:
            st.markdown("## ⚙️ Ustawienia")
            
            # Data source section
            data_source = UIComponents.render_data_source_section()
            
            # Filters (only if data is loaded)
            year_range, selected_voivodeships, analysis_type = UIComponents.render_filters()
            
            # Data info
            UIComponents.render_data_info()
            
            return year_range, selected_voivodeships, analysis_type
    
    @staticmethod
    def render_no_data_message():
        """Render message when no data is loaded."""
        st.info("👆 Wybierz źródło danych w panelu bocznym, aby rozpocząć analizę.")
        
        # Show sample data structure
        st.markdown("## 📋 Przykładowa struktura danych")
        sample_df = pd.DataFrame({
            'rok': [2019, 2019, 2020, 2020],
            'wojewodztwo': ['Mazowieckie', 'Śląskie', 'Mazowieckie', 'Śląskie'],
            'pkb_mld_zl': [298.5, 158.2, 285.3, 148.7],
            'bezrobocie_proc': [3.8, 4.2, 4.5, 5.1]
        })
        st.dataframe(sample_df, use_container_width=True)
    
    @staticmethod
    def render_no_filtered_data_message():
        """Render message when no data matches filters."""
        st.warning("⚠️ Brak danych dla wybranych filtrów.")
    
    @staticmethod
    def render_metrics(df: pd.DataFrame):
        """Render overview metrics."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Liczba województw",
                len(df['wojewodztwo'].unique()),
                help="Liczba województw w analizie"
            )
        
        with col2:
            st.metric(
                "Zakres lat",
                f"{df['rok'].min()} - {df['rok'].max()}",
                help="Zakres czasowy danych"
            )
        
        with col3:
            avg_gdp = df.groupby('rok')['pkb_mld_zl'].sum().mean()
            st.metric(
                "Średnie PKB (mld zł)",
                f"{avg_gdp:.1f}",
                help="Średnie całkowite PKB we wszystkich latach"
            )
        
        with col4:
            avg_unemployment = df['bezrobocie_proc'].mean()
            st.metric(
                "Średnie bezrobocie (%)",
                f"{avg_unemployment:.1f}",
                help="Średni poziom bezrobocia"
            )
