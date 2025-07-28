"""
Session state management for the GUS Analytical Dashboard.
"""

import streamlit as st
from data_loader import DataLoader
from visualizations import Visualizations
from map_visualizations import MapVisualizations

class SessionManager:
    """Manages Streamlit session state."""
    
    @staticmethod
    def initialize_session():
        """Initialize session state with required objects."""
        if 'data_loader' not in st.session_state:
            st.session_state.data_loader = DataLoader()
            st.session_state.visualizations = Visualizations()
            st.session_state.map_visualizations = MapVisualizations()
            st.session_state.data_loaded = False
    
    @staticmethod
    def get_data_loader():
        """Get the data loader from session state."""
        return st.session_state.data_loader
    
    @staticmethod
    def get_visualizations():
        """Get the visualizations object from session state."""
        return st.session_state.visualizations
    
    @staticmethod
    def get_map_visualizations():
        """Get the map visualizations object from session state."""
        return st.session_state.map_visualizations
    
    @staticmethod
    def is_data_loaded():
        """Check if data is loaded."""
        return st.session_state.get('data_loaded', False)
    
    @staticmethod
    def set_data_loaded(status: bool):
        """Set data loaded status."""
        st.session_state.data_loaded = status
    
    @staticmethod
    def get_filtered_data(voivodeships=None, year_range=None):
        """Get filtered data based on current selections."""
        if not SessionManager.is_data_loaded():
            return None
        
        return st.session_state.data_loader.filter_data(
            voivodeships=voivodeships,
            year_range=year_range
        )
