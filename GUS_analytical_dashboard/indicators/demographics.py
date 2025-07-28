"""
Demographics Indicators Module
Handles population, migration, and age structure data.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Optional


class DemographicsIndicators:
    """Class for demographics-related indicators and visualizations."""
    
    def __init__(self):
        """Initialize demographics indicators."""
        self.indicators = {
            'population_total': 'Populacja całkowita (tys.)',
            'population_density': 'Gęstość zaludnienia (os./km²)',
            'birth_rate': 'Współczynnik urodzeń (‰)',
            'death_rate': 'Współczynnik zgonów (‰)',
            'migration_balance': 'Saldo migracji (tys.)',
            'age_0_14': 'Populacja 0-14 lat (%)',
            'age_15_64': 'Populacja 15-64 lat (%)',
            'age_65_plus': 'Populacja 65+ lat (%)',
            'dependency_ratio': 'Współczynnik obciążenia demograficznego',
            'urbanization_rate': 'Wskaźnik urbanizacji (%)'
        }
        
        # Unit labels for charts
        self.unit_labels = {
            'population_total': 'Populacja (tys.)',
            'population_density': 'Gęstość (os./km²)',
            'birth_rate': 'Współczynnik urodzeń (‰)',
            'death_rate': 'Współczynnik zgonów (‰)',
            'migration_balance': 'Saldo migracji (tys.)',
            'age_0_14': 'Udział populacji (%)',
            'age_15_64': 'Udział populacji (%)',
            'age_65_plus': 'Udział populacji (%)',
            'dependency_ratio': 'Współczynnik',
            'urbanization_rate': 'Wskaźnik (%)',
            'aging_index': 'Indeks starzenia'
        }
    
    def get_sample_data(self) -> pd.DataFrame:
        """Generate sample demographics data for Polish voivodeships."""
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
                # Generate realistic sample data based on actual Polish demographics
                base_pop = {
                    'Mazowieckie': 5423, 'Śląskie': 4517, 'Wielkopolskie': 3496,
                    'Małopolskie': 3410, 'Dolnośląskie': 2901, 'Łódzkie': 2466,
                    'Pomorskie': 2333, 'Zachodniopomorskie': 1701, 
                    'Kujawsko-Pomorskie': 2077, 'Lubelskie': 2112,
                    'Podkarpackie': 2129, 'Warmińsko-Mazurskie': 1428,
                    'Świętokrzyskie': 1241, 'Podlaskie': 1181,
                    'Lubuskie': 1014, 'Opolskie': 988
                }
                
                pop = base_pop[voiv] * (0.99 + (year - 2019) * 0.002)  # Slight decline
                
                data.append({
                    'rok': year,
                    'wojewodztwo': voiv,
                    'population_total': round(pop, 1),
                    'population_density': round(pop / (20000 + hash(voiv) % 15000), 1),
                    'birth_rate': round(9.5 + (hash(voiv) % 100) / 100, 1),
                    'death_rate': round(10.8 + (hash(voiv) % 80) / 100, 1),
                    'migration_balance': round(-2 + (hash(voiv) % 80) / 10, 1),
                    'age_0_14': round(15.0 + (hash(voiv) % 40) / 10, 1),
                    'age_15_64': round(65.0 + (hash(voiv) % 60) / 10, 1),
                    'age_65_plus': round(20.0 + (hash(voiv) % 80) / 10, 1),
                    'dependency_ratio': round(50 + (hash(voiv) % 200) / 10, 1),
                    'urbanization_rate': round(55 + (hash(voiv) % 400) / 10, 1)
                })
        
        return pd.DataFrame(data)
    
    def create_population_pyramid(self, df: pd.DataFrame, voivodeship: str, year: int) -> go.Figure:
        """Create population pyramid for a specific voivodeship and year."""
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                st.warning(f"No data for {voivodeship} in {year}")
                return go.Figure()
            
            row = data.iloc[0]
            
            # Age groups for pyramid
            age_groups = ['0-14', '15-64', '65+']
            male_values = [row['age_0_14']/2, row['age_15_64']/2, row['age_65_plus']/2]
            female_values = [row['age_0_14']/2, row['age_15_64']/2, row['age_65_plus']/2]
            
            fig = go.Figure()
            
            # Male population (left side)
            fig.add_trace(go.Bar(
                y=age_groups,
                x=[-x for x in male_values],
                name='Mężczyźni',
                orientation='h',
                marker_color='lightblue'
            ))
            
            # Female population (right side)
            fig.add_trace(go.Bar(
                y=age_groups,
                x=female_values,
                name='Kobiety',
                orientation='h',
                marker_color='pink'
            ))
            
            fig.update_layout(
                title=f'Piramida wieku - {voivodeship} ({year})',
                xaxis_title='Populacja (%)',
                yaxis_title='Grupa wiekowa',
                barmode='relative',
                height=400
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating population pyramid: {str(e)}")
            return go.Figure()
    
    def create_migration_flow(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create migration flow visualization."""
        try:
            year_data = df[df['rok'] == year]
            
            if year_data.empty:
                return go.Figure()
            
            fig = px.bar(
                year_data.sort_values('migration_balance'),
                x='migration_balance',
                y='wojewodztwo',
                orientation='h',
                title=f'Saldo migracji według województw ({year})',
                labels={
                    'migration_balance': self.unit_labels['migration_balance'], 
                    'wojewodztwo': 'Województwo'
                },
                color='migration_balance',
                color_continuous_scale='RdYlGn'
            )
            
            fig.update_layout(
                height=600,
                xaxis_title=self.unit_labels['migration_balance']
            )
            return fig
            
        except Exception as e:
            st.error(f"Error creating migration flow: {str(e)}")
            return go.Figure()
    
    def create_aging_index(self, df: pd.DataFrame) -> go.Figure:
        """Create aging index visualization over time."""
        try:
            # Calculate aging index (65+ / 0-14 * 100)
            df_copy = df.copy()
            df_copy['aging_index'] = (df_copy['age_65_plus'] / df_copy['age_0_14']) * 100
            
            fig = px.line(
                df_copy,
                x='rok',
                y='aging_index',
                color='wojewodztwo',
                title='Indeks starzenia się społeczeństwa',
                labels={
                    'aging_index': self.unit_labels['aging_index'], 
                    'rok': 'Rok'
                }
            )
            
            # Add horizontal line at 100 (equal proportions)
            fig.add_hline(y=100, line_dash="dash", line_color="red", 
                         annotation_text="Równowaga demograficzna")
            
            fig.update_layout(
                xaxis_title="Rok",
                yaxis_title=self.unit_labels['aging_index']
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating aging index: {str(e)}")
            return go.Figure()
    
    def create_urbanization_map(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create urbanization rate map."""
        try:
            from map_visualizations import MapVisualizations
            
            map_viz = MapVisualizations()
            
            fig = map_viz.create_scatter_map(
                df=df,
                metric='urbanization_rate',
                year=year,
                title=f'Wskaźnik urbanizacji ({year})'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating urbanization map: {str(e)}")
            return go.Figure()
    
    def get_demographics_summary(self, df: pd.DataFrame, voivodeship: str, year: int) -> Dict:
        """Get demographics summary for a voivodeship."""
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                return {}
            
            row = data.iloc[0]
            
            return {
                'voivodeship': voivodeship,
                'year': year,
                'population': row['population_total'],
                'density': row['population_density'],
                'birth_rate': row['birth_rate'],
                'death_rate': row['death_rate'],
                'natural_increase': row['birth_rate'] - row['death_rate'],
                'migration_balance': row['migration_balance'],
                'aging_index': (row['age_65_plus'] / row['age_0_14']) * 100,
                'dependency_ratio': row['dependency_ratio'],
                'urbanization': row['urbanization_rate']
            }
            
        except Exception as e:
            st.error(f"Error getting demographics summary: {str(e)}")
            return {}
    
    def analyze_demographic_trends(self, df: pd.DataFrame, voivodeship: str) -> Dict:
        """Analyze demographic trends for a voivodeship."""
        try:
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            
            if len(voiv_data) < 2:
                return {}
            
            first_year = voiv_data.iloc[0]
            last_year = voiv_data.iloc[-1]
            years_span = last_year['rok'] - first_year['rok']
            
            # Calculate trends
            pop_change = last_year['population_total'] - first_year['population_total']
            pop_change_pct = (pop_change / first_year['population_total']) * 100
            
            birth_trend = (last_year['birth_rate'] - first_year['birth_rate']) / years_span
            death_trend = (last_year['death_rate'] - first_year['death_rate']) / years_span
            
            return {
                'population_change': pop_change,
                'population_change_pct': pop_change_pct,
                'birth_rate_trend': birth_trend,
                'death_rate_trend': death_trend,
                'aging_acceleration': (
                    (last_year['age_65_plus'] - first_year['age_65_plus']) / years_span
                )
            }
            
        except Exception as e:
            st.error(f"Error analyzing demographic trends: {str(e)}")
            return {}
    
    def create_population_trends(self, df: pd.DataFrame, selected_voivodeships: List[str]) -> go.Figure:
        """Create population trends for selected voivodeships."""
        try:
            # Filter data for selected voivodeships
            filtered_data = df[df['wojewodztwo'].isin(selected_voivodeships)]
            
            fig = go.Figure()
            
            colors = px.colors.qualitative.Set1
            
            for i, voiv in enumerate(selected_voivodeships):
                voiv_data = filtered_data[filtered_data['wojewodztwo'] == voiv].sort_values('rok')
                
                if not voiv_data.empty:
                    fig.add_trace(go.Scatter(
                        x=voiv_data['rok'],
                        y=voiv_data['population_total'],
                        mode='lines+markers',
                        name=voiv,
                        line=dict(color=colors[i % len(colors)], width=3),
                        marker=dict(size=8),
                        hovertemplate=f'<b>{voiv}</b><br>' +
                                    'Rok: %{x}<br>' +
                                    'Populacja: %{y:.1f} mln<br>' +
                                    '<extra></extra>'
                    ))
            
            fig.update_layout(
                title=f'Trendy populacji w wybranych województwach ({len(selected_voivodeships)} województw)',
                xaxis_title='Rok',
                yaxis_title='Populacja (mln)',
                hovermode='x unified',
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating population trends: {str(e)}")
            return go.Figure()
