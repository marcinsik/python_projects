"""
Configuration settings for the GUS Analytical Dashboard.
"""

import streamlit as st

class Config:
    """Application configuration settings."""
    
    # Page configuration
    PAGE_TITLE = "Dashboard Danych Publicznych (GUS)"
    PAGE_ICON = "📊"
    LAYOUT = "wide"
    INITIAL_SIDEBAR_STATE = "expanded"
    
    # Data configuration
    DEFAULT_DATA_PATH = "data/sample_data.csv"
    SUPPORTED_FILE_TYPES = ['csv', 'xlsx', 'xls']
    
    # UI Configuration
    MAIN_HEADER_HTML = """
    <div class="main-header">📊 Dashboard Danych Publicznych (GUS)</div>
    """
    
    # CSS Styles
    CSS_STYLES = """
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: linear-gradient(90deg, #f0f8ff, #e6f3ff);
            border-radius: 10px;
        }
        
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #1f77b4;
        }
        
        .sidebar-info {
            background: #f0f8ff;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
    </style>
    """
    
    # Analysis types
    ANALYSIS_TYPES = [
        "Przegląd główny",
        "Analiza PKB",
        "Analiza bezrobocia", 
        "Porównanie województw",
        "Mapa Polski",
        "Wskaźniki społeczno-ekonomiczne",
        "Korelacje",
        "Tempo wzrostu"
    ]
    
    # Color scales for maps
    COLOR_SCALES = [
        'Viridis', 'Plasma', 'Inferno', 'Magma', 'Cividis',
        'Blues', 'Greens', 'Reds', 'YlOrRd', 'YlGnBu'
    ]
    
    # Metric options for maps
    METRIC_OPTIONS = {
        'PKB (mld zł)': 'pkb_mld_zl',
        'Bezrobocie (%)': 'bezrobocie_proc',
        'Ludność (tys.)': 'ludnosc_tys',
        'PKB per capita (zł)': 'pkb_per_capita'
    }

def setup_page():
    """Setup Streamlit page configuration and styles."""
    st.set_page_config(
        page_title=Config.PAGE_TITLE,
        page_icon=Config.PAGE_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state=Config.INITIAL_SIDEBAR_STATE
    )
    
    # Apply CSS styles
    st.markdown(Config.CSS_STYLES, unsafe_allow_html=True)
