"""
Main application controller for the GUS Analytical Dashboard.
"""

import streamlit as st
from config import setup_page
from session_manager import SessionManager
from ui_components import UIComponents
from analysis_views import AnalysisViews
from map_analysis_views import MapAnalysisViews
from indicators_view import IndicatorsManager

class DashboardApp:
    """Main application controller."""
    
    def __init__(self):
        """Initialize the dashboard application."""
        # Setup page configuration
        setup_page()
        
        # Initialize session state
        SessionManager.initialize_session()
        
        # Initialize indicators manager
        self.indicators_manager = IndicatorsManager()
    
    def run(self):
        """Run the main application."""
        # Render header
        UIComponents.render_header()
        
        # Render sidebar and get user selections
        year_range, selected_voivodeships, analysis_type = UIComponents.render_sidebar()
        
        # Main content area
        self._render_main_content(year_range, selected_voivodeships, analysis_type)
    
    def _render_main_content(self, year_range, selected_voivodeships, analysis_type):
        """Render the main content area based on user selections."""
        session_manager = SessionManager()
        
        if not session_manager.is_data_loaded():
            UIComponents.render_no_data_message()
            return
        
        # Check if we have valid filters
        if year_range is None or selected_voivodeships is None or analysis_type is None:
            st.info("Skonfiguruj filtry w panelu bocznym.")
            return
        
        # Get filtered data
        filtered_data = session_manager.get_filtered_data(
            voivodeships=selected_voivodeships,
            year_range=year_range
        )
        
        if filtered_data.empty:
            UIComponents.render_no_filtered_data_message()
            return
        
        # Route to appropriate analysis view
        self._route_analysis_view(analysis_type, filtered_data, selected_voivodeships)
    
    def _route_analysis_view(self, analysis_type, filtered_data, selected_voivodeships):
        """Route to the appropriate analysis view based on selection."""
        try:
            if analysis_type == "Przegląd główny":
                AnalysisViews.show_overview(filtered_data)
            elif analysis_type == "Analiza PKB":
                AnalysisViews.show_gdp_analysis(filtered_data)
            elif analysis_type == "Analiza bezrobocia":
                AnalysisViews.show_unemployment_analysis(filtered_data)
            elif analysis_type == "Porównanie województw":
                AnalysisViews.show_voivodeship_comparison(filtered_data, selected_voivodeships)
            elif analysis_type == "Mapa Polski":
                MapAnalysisViews.show_map_analysis(filtered_data)
            elif analysis_type == "Wskaźniki społeczno-ekonomiczne":
                self.show_indicators_analysis()
            elif analysis_type == "Korelacje":
                AnalysisViews.show_correlation_analysis(filtered_data)
            elif analysis_type == "Tempo wzrostu":
                AnalysisViews.show_growth_analysis(filtered_data)
            else:
                st.error(f"Nieznany typ analizy: {analysis_type}")
        
        except Exception as e:
            st.error(f"Błąd podczas wyświetlania analizy: {str(e)}")
            st.exception(e)  # Show full traceback in development
    
    def show_indicators_analysis(self):
        """Show the indicators analysis view."""
        st.markdown("# 📊 Wskaźniki społeczno-ekonomiczne")
        
        # Create sub-navigation for indicators
        indicator_mode = st.radio(
            "Wybierz tryb analizy:",
            ["Przegląd wszystkich wskaźników", "Analiza szczegółowa"],
            horizontal=True
        )
        
        if indicator_mode == "Przegląd wszystkich wskaźników":
            # Year selector for overview
            year_col, _ = st.columns([1, 3])
            with year_col:
                selected_year = st.selectbox("Rok do analizy:", [2019, 2020, 2021, 2022], index=3)
            
            self.indicators_manager.show_indicators_overview(year=selected_year)
            
        else:  # Detailed analysis
            # Category and analysis selection
            categories = {
                'demographics': '👥 Demografia',
                'industry': '🏭 Przemysł', 
                'construction': '🏠 Budownictwo',
                'education': '🎓 Edukacja',
                'labor_market': '💼 Rynek pracy'
            }
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_category = st.selectbox(
                    "Wybierz kategorię:",
                    list(categories.keys()),
                    format_func=lambda x: categories[x]
                )
            
            # Get sample data for detailed analysis
            all_data = self.indicators_manager.get_combined_sample_data()
            
            if all_data:
                self.indicators_manager.show_detailed_analysis(selected_category, all_data)
            else:
                st.warning("Nie udało się wczytać danych wskaźników.")

def main():
    """Main entry point for the application."""
    app = DashboardApp()
    app.run()

if __name__ == "__main__":
    main()
