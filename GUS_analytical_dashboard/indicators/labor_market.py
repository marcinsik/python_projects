"""
Labor Market Indicators Module
Handles employment activity, wages, and labor market statistics.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Optional


class LaborMarketIndicators:
    """Class for labor market indicators and visualizations."""
    
    def __init__(self):
        """Initialize labor market indicators."""
        self.indicators = {
            'employment_rate': 'Wskaźnik zatrudnienia (%)',
            'activity_rate': 'Wskaźnik aktywności zawodowej (%)',
            'unemployment_rate': 'Stopa bezrobocia (%)',
            'avg_wage': 'Przeciętne wynagrodzenie (zł)',
            'wage_growth': 'Wzrost wynagrodzeń (%)',
            'job_vacancies': 'Wolne miejsca pracy (tys.)',
            'job_seekers': 'Poszukujący pracy (tys.)',
            'part_time_employment': 'Zatrudnienie w niepełnym wymiarze (%)',
            'temporary_employment': 'Zatrudnienie tymczasowe (%)',
            'remote_work': 'Praca zdalna (%)'
        }
        
        self.employment_sectors = {
            'agriculture': 'Rolnictwo',
            'industry': 'Przemysł',
            'construction': 'Budownictwo',
            'trade': 'Handel',
            'transport': 'Transport',
            'accommodation': 'Zakwaterowanie',
            'finance': 'Finanse',
            'real_estate': 'Nieruchomości',
            'professional': 'Usługi profesjonalne',
            'public_admin': 'Administracja publiczna',
            'education': 'Edukacja',
            'health': 'Ochrona zdrowia',
            'culture': 'Kultura i rozrywka'
        }
        
        self.skill_levels = {
            'low': 'Niskie kwalifikacje',
            'medium': 'Średnie kwalifikacje', 
            'high': 'Wysokie kwalifikacje',
            'specialist': 'Specjalistyczne'
        }
    
    def get_sample_data(self) -> pd.DataFrame:
        """Generate sample labor market data for Polish voivodeships."""
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
                # Base unemployment rates (inverse correlation with development)
                unemployment_base = {
                    'Mazowieckie': 3.8, 'Wielkopolskie': 3.1, 'Śląskie': 4.2,
                    'Dolnośląskie': 4.1, 'Małopolskie': 4.5, 'Pomorskie': 4.3,
                    'Łódzkie': 5.8, 'Lubuskie': 5.7, 'Opolskie': 6.8,
                    'Zachodniopomorskie': 6.2, 'Kujawsko-Pomorskie': 6.4,
                    'Podlaskie': 6.9, 'Lubelskie': 7.2, 'Podkarpackie': 7.8,
                    'Świętokrzyskie': 8.4, 'Warmińsko-Mazurskie': 9.1
                }
                
                # Wage levels (higher in developed regions)
                wage_base = {
                    'Mazowieckie': 6200, 'Dolnośląskie': 4800, 'Śląskie': 4600,
                    'Małopolskie': 4500, 'Wielkopolskie': 4400, 'Pomorskie': 4300,
                    'Łódzkie': 4200, 'Zachodniopomorskie': 4100, 'Lubuskie': 4000,
                    'Kujawsko-Pomorskie': 3900, 'Opolskie': 3800, 'Podlaskie': 3700,
                    'Lubelskie': 3600, 'Podkarpackie': 3500, 'Świętokrzyskie': 3400,
                    'Warmińsko-Mazurskie': 3300
                }
                
                # COVID impact on labor market
                covid_unemployment = 1.3 if year == 2020 else (1.1 if year == 2021 else 0.9 if year == 2022 else 1.0)
                covid_wage = 0.98 if year == 2020 else (1.02 if year == 2021 else 1.06 if year == 2022 else 1.0)
                
                import random
                random.seed(hash(f"{voiv}_{year}_labor"))
                
                base_unemployment = unemployment_base[voiv] * covid_unemployment
                base_wage = wage_base[voiv] * covid_wage
                
                # Calculate derived metrics
                employment_rate = 100 - base_unemployment - 15  # Simplified calculation
                activity_rate = employment_rate + base_unemployment
                
                data.append({
                    'rok': year,
                    'wojewodztwo': voiv,
                    'employment_rate': round(employment_rate * (0.98 + random.random() * 0.04), 1),
                    'activity_rate': round(activity_rate * (0.98 + random.random() * 0.04), 1),
                    'unemployment_rate': round(base_unemployment * (0.9 + random.random() * 0.2), 1),
                    'avg_wage': round(base_wage * (0.95 + random.random() * 0.1), 0),
                    'wage_growth': round(3 + random.random() * 8, 1),
                    'job_vacancies': round(base_unemployment * 10 * (0.8 + random.random() * 0.4), 1),
                    'job_seekers': round(base_unemployment * 15 * (0.9 + random.random() * 0.2), 1),
                    'part_time_employment': round(5 + random.random() * 10, 1),
                    'temporary_employment': round(20 + random.random() * 15, 1),
                    'remote_work': round(8 + random.random() * 12, 1) if year >= 2020 else round(2 + random.random() * 3, 1)
                })
        
        return pd.DataFrame(data)
    
    def create_labor_market_overview(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create labor market overview."""
        try:
            year_data = df[df['rok'] == year]
            
            if year_data.empty:
                return go.Figure()
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Stopa bezrobocia (%)', 'Przeciętne wynagrodzenie (zł)', 
                               'Wskaźnik zatrudnienia (%)', 'Wolne miejsca pracy (tys.)'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Sort data for better visualization
            unemployment_data = year_data.sort_values('unemployment_rate', ascending=True).head(10)
            wage_data = year_data.nlargest(10, 'avg_wage')
            employment_data = year_data.nlargest(10, 'employment_rate')
            vacancies_data = year_data.nlargest(10, 'job_vacancies')
            
            # Unemployment (lower is better - green for lowest)
            fig.add_trace(
                go.Bar(x=unemployment_data['wojewodztwo'], y=unemployment_data['unemployment_rate'],
                       name='Bezrobocie', marker_color='lightcoral'),
                row=1, col=1
            )
            
            # Wages
            fig.add_trace(
                go.Bar(x=wage_data['wojewodztwo'], y=wage_data['avg_wage'],
                       name='Wynagrodzenia', marker_color='steelblue'),
                row=1, col=2
            )
            
            # Employment rate
            fig.add_trace(
                go.Bar(x=employment_data['wojewodztwo'], y=employment_data['employment_rate'],
                       name='Zatrudnienie', marker_color='green'),
                row=2, col=1
            )
            
            # Job vacancies
            fig.add_trace(
                go.Bar(x=vacancies_data['wojewodztwo'], y=vacancies_data['job_vacancies'],
                       name='Wolne miejsca', marker_color='orange'),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'Rynek pracy - kluczowe wskaźniki ({year})',
                showlegend=False,
                height=600
            )
            
            # Update axis labels with units
            fig.update_yaxes(title_text="Stopa bezrobocia (%)", row=1, col=1)
            fig.update_yaxes(title_text="Wynagrodzenie (zł)", row=1, col=2)
            fig.update_yaxes(title_text="Wskaźnik zatrudnienia (%)", row=2, col=1)
            fig.update_yaxes(title_text="Wolne miejsca pracy (tys.)", row=2, col=2)
            
            fig.update_xaxes(tickangle=45)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating labor market overview: {str(e)}")
            return go.Figure()
    
    def create_employment_trends(self, df: pd.DataFrame, selected_voivodeships: List[str] = None) -> go.Figure:
        """Create employment trends analysis."""
        try:
            if selected_voivodeships:
                data = df[df['wojewodztwo'].isin(selected_voivodeships)]
                title_suffix = f" - wybrane województwa: {', '.join(selected_voivodeships)}"
            else:
                data = df
                title_suffix = " - cała Polska"
                
            # Aggregated data by year
            aggregated_data = data.groupby('rok').agg({
                'employment_rate': 'mean',
                'unemployment_rate': 'mean',
                'activity_rate': 'mean',
                'avg_wage': 'mean'
            }).reset_index()
            
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Wskaźniki zatrudnienia (%)', 'Przeciętne wynagrodzenie (zł)'),
                shared_xaxes=True
            )
            
            # Employment indicators
            fig.add_trace(
                go.Scatter(x=aggregated_data['rok'], y=aggregated_data['employment_rate'],
                          mode='lines+markers', name='Wskaźnik zatrudnienia',
                          line=dict(color='green', width=3)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=aggregated_data['rok'], y=aggregated_data['unemployment_rate'],
                          mode='lines+markers', name='Stopa bezrobocia',
                          line=dict(color='red', width=3)),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=aggregated_data['rok'], y=aggregated_data['activity_rate'],
                          mode='lines+markers', name='Aktywność zawodowa',
                          line=dict(color='blue', width=3)),
                row=1, col=1
            )
            
            # Wages
            fig.add_trace(
                go.Scatter(x=aggregated_data['rok'], y=aggregated_data['avg_wage'],
                          mode='lines+markers', name='Przeciętne wynagrodzenie',
                          line=dict(color='purple', width=3)),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f'Trendy na rynku pracy{title_suffix}',
                height=600
            )
            
            fig.update_xaxes(title_text="Rok", row=2, col=1)
            fig.update_yaxes(title_text="Wskaźniki (%)", row=1, col=1)
            fig.update_yaxes(title_text="Wynagrodzenie (zł)", row=2, col=1)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating employment trends: {str(e)}")
            return go.Figure()
    
    def create_wage_inequality_analysis(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create wage inequality analysis."""
        try:
            year_data = df[df['rok'] == year].copy()
            
            # Calculate wage statistics
            median_wage = year_data['avg_wage'].median()
            wage_std = year_data['avg_wage'].std()
            
            year_data['wage_category'] = year_data['avg_wage'].apply(
                lambda x: 'Wysokie' if x > median_wage + wage_std else 
                         ('Niskie' if x < median_wage - wage_std else 'Średnie')
            )
            
            fig = px.scatter(
                year_data,
                x='unemployment_rate',
                y='avg_wage',
                size='employment_rate',
                color='wage_category',
                hover_name='wojewodztwo',
                title=f'Analiza nierówności płacowych ({year})',
                labels={
                    'unemployment_rate': 'Stopa bezrobocia (%)',
                    'avg_wage': 'Przeciętne wynagrodzenie (zł)',
                    'employment_rate': 'Wskaźnik zatrudnienia (%)',
                    'wage_category': 'Kategoria płacowa'
                }
            )
            
            # Add median wage line
            fig.add_hline(y=median_wage, line_dash="dash", line_color="gray",
                         annotation_text=f"Mediana: {median_wage:.0f} zł")
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating wage inequality analysis: {str(e)}")
            return go.Figure()
    
    def create_job_market_dynamics(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create job market supply-demand dynamics."""
        try:
            year_data = df[df['rok'] == year].copy()
            
            # Calculate job market pressure
            year_data['job_pressure'] = year_data['job_seekers'] / year_data['job_vacancies']
            
            fig = px.scatter(
                year_data,
                x='job_vacancies',
                y='job_seekers',
                size='unemployment_rate',
                color='job_pressure',
                hover_name='wojewodztwo',
                title=f'Dynamika rynku pracy - podaż vs popyt ({year})',
                labels={
                    'job_vacancies': 'Wolne miejsca pracy (tys.)',
                    'job_seekers': 'Poszukujący pracy (tys.)',
                    'unemployment_rate': 'Stopa bezrobocia (%)',
                    'job_pressure': 'Presja na rynku pracy (współczynnik)'
                },
                color_continuous_scale='RdYlGn_r'
            )
            
            # Add equilibrium line
            max_val = max(year_data['job_vacancies'].max(), year_data['job_seekers'].max())
            fig.add_line(x=[0, max_val], y=[0, max_val], line_dash="dash", line_color="gray",
                        annotation_text="Równowaga podaży i popytu")
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating job market dynamics: {str(e)}")
            return go.Figure()
    
    def create_flexible_work_analysis(self, df: pd.DataFrame, selected_voivodeships: List[str] = None, year: int = 2022) -> go.Figure:
        """Create flexible work arrangements analysis."""
        try:
            if selected_voivodeships:
                data = df[df['wojewodztwo'].isin(selected_voivodeships)]
                title_suffix = f" - wybrane województwa: {', '.join(selected_voivodeships)}"
            else:
                data = df
                title_suffix = " - cała Polska"
                
            # Focus on recent years to show trends
            recent_data = data[data['rok'].isin([2020, 2021, 2022])]
            
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=('Praca zdalna (%)', 'Praca w niepełnym wymiarze (%)', 'Zatrudnienie tymczasowe (%)')
            )
            
            for i, (year, year_data) in enumerate(recent_data.groupby('rok')):
                # Remote work
                fig.add_trace(
                    go.Box(y=year_data['remote_work'], name=str(year), showlegend=False),
                    row=1, col=1
                )
                
                # Part-time employment
                fig.add_trace(
                    go.Box(y=year_data['part_time_employment'], name=str(year), showlegend=False),
                    row=1, col=2
                )
                
                # Temporary employment
                fig.add_trace(
                    go.Box(y=year_data['temporary_employment'], name=str(year), showlegend=False),
                    row=1, col=3
                )
            
            fig.update_layout(
                title=f'Elastyczne formy zatrudnienia - trendy 2020-2022{title_suffix}',
                height=400
            )
            
            fig.update_yaxes(title_text="Udział (%)", row=1, col=1)
            fig.update_yaxes(title_text="Udział (%)", row=1, col=2)
            fig.update_yaxes(title_text="Udział (%)", row=1, col=3)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating flexible work analysis: {str(e)}")
            return go.Figure()
    
    def create_employment_map(self, df: pd.DataFrame, year: int, metric: str = 'employment_rate') -> go.Figure:
        """Create employment indicators map."""
        try:
            from map_visualizations import MapVisualizations
            
            map_viz = MapVisualizations()
            
            metric_names = {
                'employment_rate': 'Wskaźnik zatrudnienia',
                'unemployment_rate': 'Stopa bezrobocia',
                'avg_wage': 'Przeciętne wynagrodzenie'
            }
            
            fig = map_viz.create_scatter_map(
                df=df,
                metric=metric,
                year=year,
                title=f'{metric_names.get(metric, metric)} ({year})'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating employment map: {str(e)}")
            return go.Figure()
    
    def get_labor_market_summary(self, df: pd.DataFrame, voivodeship: str, year: int) -> Dict:
        """Get labor market summary for a voivodeship."""
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                return {}
            
            row = data.iloc[0]
            
            # Calculate labor market health score (0-100)
            unemployment_score = max(0, 100 - row['unemployment_rate'] * 10)  # Lower unemployment = higher score
            wage_score = min(100, (row['avg_wage'] / 6000) * 100)  # Relative to high wage level
            employment_score = row['employment_rate']
            
            health_score = (unemployment_score + wage_score + employment_score) / 3
            
            return {
                'voivodeship': voivodeship,
                'year': year,
                'employment_rate': row['employment_rate'],
                'unemployment_rate': row['unemployment_rate'],
                'activity_rate': row['activity_rate'],
                'avg_wage': row['avg_wage'],
                'wage_growth': row['wage_growth'],
                'job_vacancies': row['job_vacancies'],
                'job_seekers': row['job_seekers'],
                'job_market_tension': row['job_seekers'] / row['job_vacancies'] if row['job_vacancies'] > 0 else 0,
                'remote_work': row['remote_work'],
                'labor_market_health': health_score
            }
            
        except Exception as e:
            st.error(f"Error getting labor market summary: {str(e)}")
            return {}
    
    def analyze_labor_market_resilience(self, df: pd.DataFrame, voivodeship: str) -> Dict:
        """Analyze labor market resilience during crises."""
        try:
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            
            if len(voiv_data) < 4:  # Need all years
                return {}
            
            # Compare pre-COVID (2019) vs COVID peak (2020) vs recovery (2022)
            pre_covid = voiv_data[voiv_data['rok'] == 2019].iloc[0]
            covid_peak = voiv_data[voiv_data['rok'] == 2020].iloc[0]
            recovery = voiv_data[voiv_data['rok'] == 2022].iloc[0]
            
            # Calculate resilience metrics
            unemployment_shock = covid_peak['unemployment_rate'] - pre_covid['unemployment_rate']
            unemployment_recovery = recovery['unemployment_rate'] - pre_covid['unemployment_rate']
            
            wage_shock = ((covid_peak['avg_wage'] - pre_covid['avg_wage']) / pre_covid['avg_wage']) * 100
            wage_recovery = ((recovery['avg_wage'] - pre_covid['avg_wage']) / pre_covid['avg_wage']) * 100
            
            # Remote work adaptation
            remote_work_growth = recovery['remote_work'] - pre_covid['remote_work']
            
            return {
                'unemployment_shock': unemployment_shock,
                'unemployment_recovery': unemployment_recovery,
                'wage_shock_pct': wage_shock,
                'wage_recovery_pct': wage_recovery,
                'remote_work_adaptation': remote_work_growth,
                'resilience_score': max(0, 100 - abs(unemployment_recovery) * 10 - abs(wage_shock))
            }
            
        except Exception as e:
            st.error(f"Error analyzing labor market resilience: {str(e)}")
            return {}
    
    def create_market_dynamics(self, df: pd.DataFrame, selected_voivodeships: List[str] = None, year: int = 2022) -> go.Figure:
        """Create labor market dynamics analysis."""
        try:
            if selected_voivodeships:
                data = df[df['wojewodztwo'].isin(selected_voivodeships)]
                title_suffix = f" - wybrane województwa: {', '.join(selected_voivodeships)}"
            else:
                data = df
                title_suffix = " - cała Polska"
            
            year_data = data[data['rok'] == year]
            
            if year_data.empty:
                return go.Figure()
            
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Wskaźnik zatrudnienia vs Bezrobocie',
                    'Wynagrodzenia vs Bezrobocie', 
                    'Wolne miejsca vs Poszukujący pracy',
                    'Wzrost wynagrodzeń (%)'
                ),
                specs=[[{"type": "scatter"}, {"type": "scatter"}],
                       [{"type": "scatter"}, {"type": "bar"}]]
            )
            
            # Employment vs unemployment
            fig.add_trace(
                go.Scatter(
                    x=year_data['unemployment_rate'],
                    y=year_data['employment_rate'],
                    mode='markers+text',
                    text=year_data['wojewodztwo'],
                    textposition='top center',
                    marker=dict(size=12, color='blue'),
                    name='Wskaźniki zatrudnienia'
                ),
                row=1, col=1
            )
            
            # Wages vs unemployment
            fig.add_trace(
                go.Scatter(
                    x=year_data['unemployment_rate'],
                    y=year_data['avg_wage'],
                    mode='markers+text',
                    text=year_data['wojewodztwo'],
                    textposition='top center',
                    marker=dict(size=12, color='green'),
                    name='Wynagrodzenia'
                ),
                row=1, col=2
            )
            
            # Job market balance
            fig.add_trace(
                go.Scatter(
                    x=year_data['job_seekers'],
                    y=year_data['job_vacancies'],
                    mode='markers+text',
                    text=year_data['wojewodztwo'],
                    textposition='top center',
                    marker=dict(size=12, color='red'),
                    name='Rynek pracy'
                ),
                row=2, col=1
            )
            
            # Wage growth
            top_growth = year_data.nlargest(8, 'wage_growth')
            fig.add_trace(
                go.Bar(
                    x=top_growth['wojewodztwo'],
                    y=top_growth['wage_growth'],
                    marker_color='orange',
                    name='Wzrost wynagrodzeń'
                ),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'Dynamika rynku pracy ({year}){title_suffix}',
                height=700,
                showlegend=False
            )
            
            # Update axis labels
            fig.update_xaxes(title_text="Stopa bezrobocia (%)", row=1, col=1)
            fig.update_yaxes(title_text="Wskaźnik zatrudnienia (%)", row=1, col=1)
            fig.update_xaxes(title_text="Stopa bezrobocia (%)", row=1, col=2)
            fig.update_yaxes(title_text="Średnie wynagrodzenie (zł)", row=1, col=2)
            fig.update_xaxes(title_text="Poszukujący pracy (tys.)", row=2, col=1)
            fig.update_yaxes(title_text="Wolne miejsca pracy (tys.)", row=2, col=1)
            fig.update_xaxes(title_text="Województwo", row=2, col=2, tickangle=45)
            fig.update_yaxes(title_text="Wzrost wynagrodzeń (%)", row=2, col=2)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating market dynamics: {str(e)}")
            return go.Figure()
