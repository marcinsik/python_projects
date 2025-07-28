"""
Construction Indicators Module
Handles construction permits, real estate prices, and building activity data.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Optional


class ConstructionIndicators:
    """Class for construction and real estate indicators."""
    
    def __init__(self):
        """Initialize construction indicators."""
        self.indicators = {
            'building_permits': 'Pozwolenia na budowę (szt.)',
            'dwellings_completed': 'Mieszkania oddane do użytku (szt.)',
            'dwellings_started': 'Mieszkania rozpoczęte (szt.)',
            'housing_price_m2': 'Cena mieszkań (zł/m²)',
            'commercial_permits': 'Pozwolenia na budynki komercyjne (szt.)',
            'infrastructure_investment': 'Inwestycje infrastrukturalne (mln zł)',
            'construction_employment': 'Zatrudnienie w budownictwie (tys.)',
            'construction_output': 'Produkcja budowlana (mld zł)',
            'renovation_permits': 'Pozwolenia na remonty (szt.)',
            'public_construction': 'Budownictwo publiczne (mln zł)'
        }
        
        self.building_types = {
            'residential': 'Mieszkaniowe',
            'commercial': 'Komercyjne',
            'industrial': 'Przemysłowe',
            'public': 'Użyteczności publicznej',
            'infrastructure': 'Infrastrukturalne'
        }
    
    def get_sample_data(self) -> pd.DataFrame:
        """Generate sample construction data for Polish voivodeships."""
        voivodeships = [
            'Mazowieckie', 'Śląskie', 'Wielkopolskie', 'Małopolskie',
            'Dolnośląskie', 'Łódzkie', 'Pomorskie', 'Zachodniopomorskie',
            'Kujawsko-Pomorskie', 'Lubelskie', 'Podkarpackie', 
            'Warmińsko-Mazurskie', 'Świętokrzyskie', 'Podlaskie',
            'Lubuskie', 'Opolskie'
        ]
        
        years = [2019, 2020, 2021, 2022]
        
        data = []
        for year in years:
            for voiv in voivodeships:
                # Base construction activity by voivodeship
                construction_base = {
                    'Mazowieckie': 15500, 'Śląskie': 8200, 'Wielkopolskie': 12800,
                    'Małopolskie': 11400, 'Dolnośląskie': 9100, 'Łódzkie': 4900,
                    'Pomorskie': 7800, 'Zachodniopomorskie': 4200, 
                    'Kujawsko-Pomorskie': 3800, 'Lubelskie': 3200,
                    'Podkarpackie': 4400, 'Warmińsko-Mazurskie': 2800,
                    'Świętokrzyskie': 2100, 'Podlaskie': 1900,
                    'Lubuskie': 2400, 'Opolskie': 1800
                }
                
                # Housing prices base (major cities effect)
                price_base = {
                    'Mazowieckie': 8500, 'Małopolskie': 7200, 'Pomorskie': 6800,
                    'Dolnośląskie': 6500, 'Wielkopolskie': 6000, 'Śląskie': 5200,
                    'Łódzkie': 4800, 'Zachodniopomorskie': 5500, 
                    'Kujawsko-Pomorskie': 4200, 'Lubelskie': 4000,
                    'Podkarpackie': 4100, 'Warmińsko-Mazurskie': 3800,
                    'Świętokrzyskie': 3500, 'Podlaskie': 3600,
                    'Lubuskie': 3900, 'Opolskie': 3400
                }
                
                # COVID and post-COVID boom
                covid_factor = 0.85 if year == 2020 else (1.15 if year == 2021 else 1.25 if year == 2022 else 1.0)
                price_growth = 1.0 + (year - 2019) * 0.08  # 8% annual growth
                
                import random
                random.seed(hash(f"{voiv}_{year}_construction"))
                
                base_permits = construction_base[voiv] * covid_factor
                base_price = price_base[voiv] * price_growth
                
                data.append({
                    'rok': year,
                    'wojewodztwo': voiv,
                    'building_permits': int(base_permits * (0.9 + random.random() * 0.2)),
                    'dwellings_completed': int(base_permits * 0.8 * (0.9 + random.random() * 0.2)),
                    'dwellings_started': int(base_permits * 1.1 * (0.9 + random.random() * 0.2)),
                    'housing_price_m2': round(base_price * (0.95 + random.random() * 0.1), 0),
                    'commercial_permits': int(base_permits * 0.15 * (0.8 + random.random() * 0.4)),
                    'infrastructure_investment': round(base_permits * 0.5 * (0.8 + random.random() * 0.4), 1),
                    'construction_employment': round(base_permits * 0.008 * (0.95 + random.random() * 0.1), 1),
                    'construction_output': round(base_permits * 0.002 * (0.9 + random.random() * 0.2), 1),
                    'renovation_permits': int(base_permits * 0.3 * (0.9 + random.random() * 0.2)),
                    'public_construction': round(base_permits * 0.2 * (0.8 + random.random() * 0.4), 1)
                })
        
        return pd.DataFrame(data)
    
    def create_housing_market_overview(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create housing market overview."""
        try:
            year_data = df[df['rok'] == year]
            
            if year_data.empty:
                return go.Figure()
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Pozwolenia na budowę (szt.)', 'Ceny mieszkań (zł/m²)', 
                               'Mieszkania oddane (szt.)', 'Mieszkania rozpoczęte (szt.)'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Sort data for better visualization
            permits_data = year_data.nlargest(10, 'building_permits')
            prices_data = year_data.nlargest(10, 'housing_price_m2')
            completed_data = year_data.nlargest(10, 'dwellings_completed')
            started_data = year_data.nlargest(10, 'dwellings_started')
            
            # Building permits
            fig.add_trace(
                go.Bar(x=permits_data['wojewodztwo'], y=permits_data['building_permits'],
                       name='Pozwolenia', marker_color='steelblue'),
                row=1, col=1
            )
            
            # Housing prices
            fig.add_trace(
                go.Bar(x=prices_data['wojewodztwo'], y=prices_data['housing_price_m2'],
                       name='Ceny', marker_color='orange'),
                row=1, col=2
            )
            
            # Completed dwellings
            fig.add_trace(
                go.Bar(x=completed_data['wojewodztwo'], y=completed_data['dwellings_completed'],
                       name='Oddane', marker_color='green'),
                row=2, col=1
            )
            
            # Started dwellings
            fig.add_trace(
                go.Bar(x=started_data['wojewodztwo'], y=started_data['dwellings_started'],
                       name='Rozpoczęte', marker_color='red'),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'Rynek mieszkaniowy - przegląd ({year})',
                showlegend=False,
                height=600
            )
            
            # Update axis labels with units
            fig.update_yaxes(title_text="Liczba pozwoleń (szt.)", row=1, col=1)
            fig.update_yaxes(title_text="Cena (zł/m²)", row=1, col=2)
            fig.update_yaxes(title_text="Liczba mieszkań (szt.)", row=2, col=1)
            fig.update_yaxes(title_text="Liczba mieszkań (szt.)", row=2, col=2)
            
            # Rotate x-axis labels
            fig.update_xaxes(tickangle=45)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating housing market overview: {str(e)}")
            return go.Figure()
    
    def create_price_trends(self, df: pd.DataFrame) -> go.Figure:
        """Create housing price trends over time."""
        try:
            # Select major voivodeships for trend analysis
            major_voivodeships = ['Mazowieckie', 'Małopolskie', 'Śląskie', 'Wielkopolskie', 'Dolnośląskie']
            
            fig = go.Figure()
            
            colors = ['blue', 'red', 'green', 'orange', 'purple']
            
            for i, voiv in enumerate(major_voivodeships):
                voiv_data = df[df['wojewodztwo'] == voiv].sort_values('rok')
                
                fig.add_trace(go.Scatter(
                    x=voiv_data['rok'],
                    y=voiv_data['housing_price_m2'],
                    mode='lines+markers',
                    name=voiv,
                    line=dict(color=colors[i], width=3),
                    marker=dict(size=8)
                ))
            
            fig.update_layout(
                title='Trendy cen mieszkań w głównych województwach',
                xaxis_title='Rok',
                yaxis_title='Cena mieszkań (zł/m²)',
                hovermode='x unified',
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating price trends: {str(e)}")
            return go.Figure()
    
    def create_construction_activity_map(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create construction activity map."""
        try:
            from map_visualizations import MapVisualizations
            
            map_viz = MapVisualizations()
            
            fig = map_viz.create_scatter_map(
                df=df,
                metric='building_permits',
                year=year,
                title=f'Aktywność budowlana - pozwolenia na budowę ({year})'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating construction activity map: {str(e)}")
            return go.Figure()
    
    def create_supply_demand_analysis(self, df: pd.DataFrame, voivodeship: str) -> go.Figure:
        """Create supply-demand analysis for housing market."""
        try:
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Podaż mieszkań (szt.)', 'Ceny mieszkań (zł/m²)'),
                shared_xaxes=True
            )
            
            # Supply indicators
            fig.add_trace(
                go.Scatter(x=voiv_data['rok'], y=voiv_data['dwellings_started'],
                          mode='lines+markers', name='Rozpoczęte',
                          line=dict(color='blue')),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=voiv_data['rok'], y=voiv_data['dwellings_completed'],
                          mode='lines+markers', name='Oddane',
                          line=dict(color='green')),
                row=1, col=1
            )
            
            # Price trend
            fig.add_trace(
                go.Scatter(x=voiv_data['rok'], y=voiv_data['housing_price_m2'],
                          mode='lines+markers', name='Cena (zł/m²)',
                          line=dict(color='red', width=3)),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f'Analiza podaży i popytu - {voivodeship}',
                height=600
            )
            
            fig.update_xaxes(title_text="Rok", row=2, col=1)
            fig.update_yaxes(title_text="Liczba mieszkań (szt.)", row=1, col=1)
            fig.update_yaxes(title_text="Cena mieszkań (zł/m²)", row=2, col=1)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating supply-demand analysis: {str(e)}")
            return go.Figure()
    
    def create_building_types_breakdown(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create building types breakdown."""
        try:
            year_data = df[df['rok'] == year]
            
            # Calculate total construction activity
            total_permits = year_data['building_permits'].sum()
            commercial_permits = year_data['commercial_permits'].sum()
            renovation_permits = year_data['renovation_permits'].sum()
            
            # Estimate other types
            industrial_permits = total_permits * 0.1
            public_permits = total_permits * 0.05
            residential_permits = total_permits - commercial_permits - renovation_permits
            
            types_data = {
                'Mieszkaniowe': residential_permits,
                'Komercyjne': commercial_permits,
                'Remonty': renovation_permits,
                'Przemysłowe': industrial_permits,
                'Użyteczności publicznej': public_permits
            }
            
            fig = px.pie(
                values=list(types_data.values()),
                names=list(types_data.keys()),
                title=f'Struktura pozwoleń na budowę ({year}) - łączna liczba: {int(total_permits):,} szt.'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating building types breakdown: {str(e)}")
            return go.Figure()
    
    def get_construction_summary(self, df: pd.DataFrame, voivodeship: str, year: int) -> Dict:
        """Get construction summary for a voivodeship."""
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                return {}
            
            row = data.iloc[0]
            
            # Calculate derived metrics
            completion_rate = (row['dwellings_completed'] / row['dwellings_started']) * 100 if row['dwellings_started'] > 0 else 0
            price_per_permit = row['housing_price_m2'] / (row['building_permits'] / 1000) if row['building_permits'] > 0 else 0
            
            return {
                'voivodeship': voivodeship,
                'year': year,
                'building_permits': row['building_permits'],
                'dwellings_completed': row['dwellings_completed'],
                'dwellings_started': row['dwellings_started'],
                'completion_rate': completion_rate,
                'housing_price_m2': row['housing_price_m2'],
                'construction_output': row['construction_output'],
                'employment': row['construction_employment'],
                'infrastructure_investment': row['infrastructure_investment']
            }
            
        except Exception as e:
            st.error(f"Error getting construction summary: {str(e)}")
            return {}
    
    def analyze_market_dynamics(self, df: pd.DataFrame, voivodeship: str) -> Dict:
        """Analyze construction market dynamics."""
        try:
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            
            if len(voiv_data) < 2:
                return {}
            
            latest = voiv_data.iloc[-1]
            previous = voiv_data.iloc[-2]
            
            # Calculate year-over-year changes
            permits_change = ((latest['building_permits'] - previous['building_permits']) / previous['building_permits']) * 100
            price_change = ((latest['housing_price_m2'] - previous['housing_price_m2']) / previous['housing_price_m2']) * 100
            output_change = ((latest['construction_output'] - previous['construction_output']) / previous['construction_output']) * 100
            
            # Market momentum indicators
            supply_trend = 'increasing' if latest['dwellings_started'] > previous['dwellings_started'] else 'decreasing'
            demand_pressure = 'high' if price_change > 5 else ('moderate' if price_change > 0 else 'low')
            
            return {
                'permits_change_yoy': permits_change,
                'price_change_yoy': price_change,
                'output_change_yoy': output_change,
                'supply_trend': supply_trend,
                'demand_pressure': demand_pressure,
                'market_heat': 'hot' if permits_change > 10 and price_change > 5 else 'moderate'
            }
            
        except Exception as e:
            st.error(f"Error analyzing market dynamics: {str(e)}")
            return {}
