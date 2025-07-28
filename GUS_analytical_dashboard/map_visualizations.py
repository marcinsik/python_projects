"""
Module for creating interactive maps for the GUS analytical dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from typing import List, Optional, Dict
import json


class MapVisualizations:
    """Class responsible for creating interactive maps and choropleth visualizations."""
    
    def __init__(self):
        """Initialize the map visualizations class."""
        self.voivodeship_mapping = {
            # Mapping Polish voivodeship names to standard codes/IDs
            'Mazowieckie': 'PL-MZ',
            'Śląskie': 'PL-SL',
            'Wielkopolskie': 'PL-WP',
            'Małopolskie': 'PL-MA',
            'Dolnośląskie': 'PL-DS',
            'Łódzkie': 'PL-LD',
            'Pomorskie': 'PL-PM',
            'Zachodniopomorskie': 'PL-ZP',
            'Kujawsko-Pomorskie': 'PL-KP',
            'Lubelskie': 'PL-LU',
            'Podkarpackie': 'PL-PK',
            'Warmińsko-Mazurskie': 'PL-WN',
            'Świętokrzyskie': 'PL-SK',
            'Podlaskie': 'PL-PD',
            'Lubuskie': 'PL-LB',
            'Opolskie': 'PL-OP'
        }
        
        # GeoJSON coordinates for Polish voivodeships (simplified)
        self.poland_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Mazowieckie", "code": "PL-MZ"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[20.5, 52.5], [21.5, 52.5], [21.5, 51.5], [20.5, 51.5], [20.5, 52.5]]]
                    }
                },
                # Note: This is a simplified example. In production, you would use proper GeoJSON data
                # You can get detailed Polish voivodeship boundaries from:
                # - Natural Earth Data
                # - OpenStreetMap
                # - Polish government GIS data
            ]
        }
    
    def create_choropleth_map(self, 
                             df: pd.DataFrame,
                             metric: str,
                             year: int,
                             title: str,
                             color_scale: str = "Viridis") -> go.Figure:
        """
        Creates a choropleth map of Poland showing the selected metric by voivodeship.
        
        Args:
            df: DataFrame with data
            metric: Column name for the metric to visualize
            year: Year to filter data for
            title: Title for the map
            color_scale: Color scale for the choropleth
            
        Returns:
            Plotly figure with choropleth map
        """
        try:
            # Filter data for the selected year
            year_data = df[df['rok'] == year].copy()
            
            if year_data.empty:
                st.warning(f"No data available for year {year}")
                return go.Figure()
            
            # Add voivodeship codes for mapping
            year_data['voivodeship_code'] = year_data['wojewodztwo'].map(self.voivodeship_mapping)
            
            # Create the choropleth map using built-in country data
            # Note: For proper Polish voivodeship boundaries, you'd need actual GeoJSON data
            fig = px.choropleth(
                year_data,
                locations='voivodeship_code',
                color=metric,
                hover_name='wojewodztwo',
                hover_data={
                    metric: ':.2f',
                    'voivodeship_code': False
                },
                color_continuous_scale=color_scale,
                title=f'{title} - {year}',
                labels={metric: self._get_metric_label(metric)}
            )
            
            # Update layout for better appearance
            fig.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='mercator',
                    center=dict(lat=52.0, lon=19.0),  # Center on Poland
                    scope='europe'
                ),
                title_x=0.5,
                width=800,
                height=600
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating choropleth map: {str(e)}")
            return go.Figure()
    
    def create_scatter_map(self, 
                          df: pd.DataFrame,
                          metric: str,
                          year: int,
                          title: str) -> go.Figure:
        """
        Creates a scatter map showing voivodeships as circles sized by the metric.
        
        Args:
            df: DataFrame with data
            metric: Column name for the metric to visualize
            year: Year to filter data for
            title: Title for the map
            
        Returns:
            Plotly figure with scatter map
        """
        try:
            # Filter data for the selected year
            year_data = df[df['rok'] == year].copy()
            
            if year_data.empty:
                st.warning(f"No data available for year {year}")
                return go.Figure()
            
            # Approximate coordinates for Polish voivodeship capitals
            coordinates = {
                'Mazowieckie': (52.2297, 21.0122),      # Warsaw
                'Śląskie': (50.2649, 19.0238),          # Katowice
                'Wielkopolskie': (52.4064, 16.9252),    # Poznań
                'Małopolskie': (50.0647, 19.9450),      # Kraków
                'Dolnośląskie': (51.1079, 17.0385),     # Wrocław
                'Łódzkie': (51.7592, 19.4560),          # Łódź
                'Pomorskie': (54.3520, 18.6466),        # Gdańsk
                'Zachodniopomorskie': (53.4285, 14.5528), # Szczecin
                'Kujawsko-Pomorskie': (53.0138, 18.5984), # Bydgoszcz
                'Lubelskie': (51.2465, 22.5684),        # Lublin
                'Podkarpackie': (50.0374, 21.9991),     # Rzeszów
                'Warmińsko-Mazurskie': (53.7784, 20.4801), # Olsztyn
                'Świętokrzyskie': (50.8661, 20.6286),   # Kielce
                'Podlaskie': (53.1325, 23.1688),        # Białystok
                'Lubuskie': (51.9356, 15.5062),         # Zielona Góra
                'Opolskie': (50.6751, 17.9213)          # Opole
            }
            
            # Add coordinates to the data
            year_data['lat'] = year_data['wojewodztwo'].map(lambda x: coordinates.get(x, (52, 19))[0])
            year_data['lon'] = year_data['wojewodztwo'].map(lambda x: coordinates.get(x, (52, 19))[1])
            
            # Create scatter map
            fig = px.scatter_mapbox(
                year_data,
                lat='lat',
                lon='lon',
                size=metric,
                color=metric,
                hover_name='wojewodztwo',
                hover_data={
                    metric: ':.2f',
                    'lat': False,
                    'lon': False
                },
                color_continuous_scale='Viridis',
                size_max=50,
                zoom=5,
                mapbox_style='open-street-map',
                title=f'{title} - {year}',
                labels={metric: self._get_metric_label(metric)}
            )
            
            # Update layout
            fig.update_layout(
                mapbox=dict(
                    center=dict(lat=52.0, lon=19.0),
                    zoom=5
                ),
                title_x=0.5,
                width=800,
                height=600
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating scatter map: {str(e)}")
            return go.Figure()
    
    def create_animated_scatter_map(self, 
                                   df: pd.DataFrame,
                                   metric: str,
                                   title: str,
                                   color_scale: str = "Viridis") -> go.Figure:
        """
        Creates an animated scatter map showing changes over time.
        
        Args:
            df: DataFrame with data
            metric: Column name for the metric to visualize
            title: Title for the map
            color_scale: Color scale for the visualization
            
        Returns:
            Plotly figure with animated scatter map
        """
        try:
            # Approximate coordinates for Polish voivodeship capitals
            coordinates = {
                'Mazowieckie': (52.2297, 21.0122),      # Warsaw
                'Śląskie': (50.2649, 19.0238),          # Katowice
                'Wielkopolskie': (52.4064, 16.9252),    # Poznań
                'Małopolskie': (50.0647, 19.9450),      # Kraków
                'Dolnośląskie': (51.1079, 17.0385),     # Wrocław
                'Łódzkie': (51.7592, 19.4560),          # Łódź
                'Pomorskie': (54.3520, 18.6466),        # Gdańsk
                'Zachodniopomorskie': (53.4285, 14.5528), # Szczecin
                'Kujawsko-Pomorskie': (53.0138, 18.5984), # Bydgoszcz
                'Lubelskie': (51.2465, 22.5684),        # Lublin
                'Podkarpackie': (50.0374, 21.9991),     # Rzeszów
                'Warmińsko-Mazurskie': (53.7784, 20.4801), # Olsztyn
                'Świętokrzyskie': (50.8661, 20.6286),   # Kielce
                'Podlaskie': (53.1325, 23.1688),        # Białystok
                'Lubuskie': (51.9356, 15.5062),         # Zielona Góra
                'Opolskie': (50.6751, 17.9213)          # Opole
            }
            
            # Add coordinates to the data
            df_copy = df.copy()
            df_copy['lat'] = df_copy['wojewodztwo'].map(lambda x: coordinates.get(x, (52, 19))[0])
            df_copy['lon'] = df_copy['wojewodztwo'].map(lambda x: coordinates.get(x, (52, 19))[1])
            
            # Create animated scatter map
            fig = px.scatter_mapbox(
                df_copy,
                lat='lat',
                lon='lon',
                size=metric,
                color=metric,
                hover_name='wojewodztwo',
                hover_data={
                    metric: ':.2f',
                    'lat': False,
                    'lon': False
                },
                animation_frame='rok',
                color_continuous_scale=color_scale,
                size_max=50,
                zoom=5,
                mapbox_style='open-street-map',
                title=title,
                labels={metric: self._get_metric_label(metric)}
            )
            
            # Update layout
            fig.update_layout(
                mapbox=dict(
                    center=dict(lat=52.0, lon=19.0),
                    zoom=5
                ),
                title_x=0.5,
                width=800,
                height=700
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating animated scatter map: {str(e)}")
            return go.Figure()
    
    def create_animated_bar_chart_map(self, 
                                     df: pd.DataFrame,
                                     metric: str,
                                     title: str) -> go.Figure:
        """
        Creates an animated bar chart showing ranking changes over time.
        
        Args:
            df: DataFrame with data
            metric: Column name for the metric to visualize
            title: Title for the chart
            
        Returns:
            Plotly figure with animated bar chart
        """
        try:
            # Create animated bar chart
            fig = px.bar(
                df,
                x='wojewodztwo',
                y=metric,
                color=metric,
                animation_frame='rok',
                hover_data={metric: ':.2f'},
                color_continuous_scale='viridis',
                title=title,
                labels={
                    'wojewodztwo': 'Województwo',
                    metric: self._get_metric_label(metric)
                }
            )
            
            # Update layout for better readability
            fig.update_layout(
                xaxis_tickangle=-45,
                title_x=0.5,
                width=800,
                height=600,
                template="plotly_white"
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating animated bar chart: {str(e)}")
            return go.Figure()

    def _get_metric_label(self, metric: str) -> str:
        """
        Returns a formatted label for the metric.
        
        Args:
            metric: Column name
            
        Returns:
            Formatted label
        """
        labels = {
            'pkb_mld_zl': 'GDP (billion PLN)',
            'bezrobocie_proc': 'Unemployment (%)',
            'ludnosc_tys': 'Population (thousands)',
            'pkb_per_capita': 'GDP per capita (PLN)'
        }
        return labels.get(metric, metric.replace('_', ' ').title())
    
    def get_voivodeship_summary(self, 
                               df: pd.DataFrame, 
                               voivodeship: str, 
                               year: int) -> Dict:
        """
        Returns summary statistics for a specific voivodeship and year.
        
        Args:
            df: DataFrame with data
            voivodeship: Voivodeship name
            year: Year
            
        Returns:
            Dictionary with summary statistics
        """
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                return {}
            
            row = data.iloc[0]
            
            summary = {
                'voivodeship': voivodeship,
                'year': year,
                'gdp': row.get('pkb_mld_zl', 0),
                'unemployment': row.get('bezrobocie_proc', 0),
                'population': row.get('ludnosc_tys', 0)
            }
            
            # Calculate GDP per capita if population data is available
            if summary['population'] > 0:
                summary['gdp_per_capita'] = (summary['gdp'] * 1000000) / (summary['population'] * 1000)
            
            return summary
            
        except Exception as e:
            st.error(f"Error getting voivodeship summary: {str(e)}")
            return {}
