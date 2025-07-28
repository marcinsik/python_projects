"""
Industry Indicators Module
Handles industrial production, export/import data.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Optional


class IndustryIndicators:
    """Class for industry-related indicators and visualizations."""
    
    def __init__(self):
        """Initialize industry indicators."""
        self.indicators = {
            'industrial_production': 'Produkcja przemysłowa (mld zł)',
            'manufacturing_output': 'Produkcja wytwórcza (mld zł)',
            'mining_output': 'Produkcja wydobywcza (mln zł)',
            'energy_production': 'Produkcja energii (GWh)',
            'export_value': 'Eksport (mld EUR)',
            'import_value': 'Import (mld EUR)',
            'trade_balance': 'Bilans handlowy (mld EUR)',
            'foreign_investment': 'Inwestycje zagraniczne (mld zł)',
            'employment_industry': 'Zatrudnienie w przemyśle (tys.)',
            'productivity_index': 'Indeks produktywności (2015=100)'
        }
        
        # Unit labels for charts
        self.unit_labels = {
            'industrial_production': 'Produkcja (mld zł)',
            'manufacturing_output': 'Produkcja (mld zł)',
            'mining_output': 'Produkcja (mln zł)',
            'energy_production': 'Produkcja (GWh)',
            'export_value': 'Eksport (mld EUR)',
            'import_value': 'Import (mld EUR)',
            'trade_balance': 'Bilans (mld EUR)',
            'foreign_investment': 'Inwestycje (mld zł)',
            'employment_industry': 'Zatrudnienie (tys.)',
            'productivity_index': 'Indeks (2015=100)'
        }
        
        self.sectors = {
            'automotive': 'Motoryzacyjny',
            'machinery': 'Maszynowy',
            'food': 'Spożywczy',
            'chemicals': 'Chemiczny',
            'textiles': 'Tekstylny',
            'electronics': 'Elektroniczny',
            'steel': 'Stalowy',
            'energy': 'Energetyczny'
        }
    
    def get_sample_data(self) -> pd.DataFrame:
        """Generate sample industry data for Polish voivodeships."""
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
                # Base industrial strength by voivodeship
                industrial_base = {
                    'Mazowieckie': 85.5, 'Śląskie': 78.2, 'Wielkopolskie': 45.8,
                    'Małopolskie': 38.9, 'Dolnośląskie': 41.4, 'Łódzkie': 29.7,
                    'Pomorskie': 32.2, 'Zachodniopomorskie': 22.1, 
                    'Kujawsko-Pomorskie': 21.8, 'Lubelskie': 17.9,
                    'Podkarpackie': 27.4, 'Warmińsko-Mazurskie': 15.8,
                    'Świętokrzyskie': 12.3, 'Podlaskie': 10.1,
                    'Lubuskie': 19.2, 'Opolskie': 15.8
                }
                
                # COVID impact and recovery
                covid_factor = 0.92 if year == 2020 else (0.98 if year == 2021 else 1.05 if year == 2022 else 1.0)
                base_prod = industrial_base[voiv] * covid_factor
                
                # Random variations
                import random
                random.seed(hash(f"{voiv}_{year}"))
                
                data.append({
                    'rok': year,
                    'wojewodztwo': voiv,
                    'industrial_production': round(base_prod * (0.95 + random.random() * 0.1), 1),
                    'manufacturing_output': round(base_prod * 0.75 * (0.95 + random.random() * 0.1), 1),
                    'mining_output': round(base_prod * 0.15 * 1000 * (0.9 + random.random() * 0.2), 0),
                    'energy_production': round(base_prod * 150 * (0.95 + random.random() * 0.1), 0),
                    'export_value': round(base_prod * 0.8 * (0.9 + random.random() * 0.2), 1),
                    'import_value': round(base_prod * 0.9 * (0.9 + random.random() * 0.2), 1),
                    'trade_balance': round((base_prod * 0.8 - base_prod * 0.9) * (0.8 + random.random() * 0.4), 1),
                    'foreign_investment': round(base_prod * 0.3 * (0.8 + random.random() * 0.4), 1),
                    'employment_industry': round(base_prod * 8 * (0.98 + random.random() * 0.04), 1),
                    'productivity_index': round(100 + (year - 2019) * 2.5 + random.random() * 5, 1)
                })
        
        return pd.DataFrame(data)
    
    def create_production_overview(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create industrial production overview."""
        try:
            year_data = df[df['rok'] == year]
            
            if year_data.empty:
                return go.Figure()
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Produkcja przemysłowa', 'Produkcja wytwórcza', 
                               'Eksport', 'Import'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            top_5_prod = year_data.nlargest(5, 'industrial_production')
            top_5_manuf = year_data.nlargest(5, 'manufacturing_output')
            top_5_export = year_data.nlargest(5, 'export_value')
            top_5_import = year_data.nlargest(5, 'import_value')
            
            # Industrial production
            fig.add_trace(
                go.Bar(x=top_5_prod['wojewodztwo'], y=top_5_prod['industrial_production'],
                       name='Produkcja przemysłowa', marker_color='steelblue'),
                row=1, col=1
            )
            
            # Manufacturing output
            fig.add_trace(
                go.Bar(x=top_5_manuf['wojewodztwo'], y=top_5_manuf['manufacturing_output'],
                       name='Produkcja wytwórcza', marker_color='darkgreen'),
                row=1, col=2
            )
            
            # Export
            fig.add_trace(
                go.Bar(x=top_5_export['wojewodztwo'], y=top_5_export['export_value'],
                       name='Eksport', marker_color='orange'),
                row=2, col=1
            )
            
            # Import
            fig.add_trace(
                go.Bar(x=top_5_import['wojewodztwo'], y=top_5_import['import_value'],
                       name='Import', marker_color='red'),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'Przegląd przemysłu - TOP 5 województw ({year})',
                showlegend=False,
                height=600
            )
            
            # Update axis labels with units
            fig.update_yaxes(title_text=self.unit_labels['industrial_production'], row=1, col=1)
            fig.update_yaxes(title_text=self.unit_labels['manufacturing_output'], row=1, col=2)
            fig.update_yaxes(title_text=self.unit_labels['export_value'], row=2, col=1)
            fig.update_yaxes(title_text=self.unit_labels['import_value'], row=2, col=2)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating production overview: {str(e)}")
            return go.Figure()
    
    def create_trade_balance_analysis(self, df: pd.DataFrame) -> go.Figure:
        """Create trade balance analysis over time."""
        try:
            # Calculate national totals by year
            national_trade = df.groupby('rok').agg({
                'export_value': 'sum',
                'import_value': 'sum',
                'trade_balance': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=national_trade['rok'],
                y=national_trade['export_value'],
                mode='lines+markers',
                name='Eksport',
                line=dict(color='green', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=national_trade['rok'],
                y=national_trade['import_value'],
                mode='lines+markers',
                name='Import',
                line=dict(color='red', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=national_trade['rok'],
                y=national_trade['trade_balance'],
                mode='lines+markers',
                name='Bilans handlowy',
                line=dict(color='blue', width=3),
                marker=dict(size=8)
            ))
            
            # Add zero line for trade balance
            fig.add_hline(y=0, line_dash="dash", line_color="gray",
                         annotation_text="Równowaga handlowa")
            
            fig.update_layout(
                title='Bilans handlowy Polski - trendy czasowe',
                xaxis_title='Rok',
                yaxis_title='Wartość (mld EUR)',
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating trade balance analysis: {str(e)}")
            return go.Figure()
    
    def create_productivity_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create productivity heatmap by voivodeship and year."""
        try:
            # Create pivot table for heatmap
            pivot_data = df.pivot(index='wojewodztwo', columns='rok', values='productivity_index')
            
            fig = px.imshow(
                pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                color_continuous_scale='RdYlGn',
                title='Indeks produktywności przemysłowej',
                labels={'color': 'Indeks produktywności'}
            )
            
            fig.update_layout(height=600)
            return fig
            
        except Exception as e:
            st.error(f"Error creating productivity heatmap: {str(e)}")
            return go.Figure()
    
    def create_sector_composition(self, voivodeship: str) -> go.Figure:
        """Create sector composition pie chart for a voivodeship."""
        try:
            # Sample sector data (in practice, this would come from real data)
            import random
            random.seed(hash(voivodeship))
            
            sectors_data = {}
            for sector_key, sector_name in self.sectors.items():
                sectors_data[sector_name] = random.randint(5, 25)
            
            fig = px.pie(
                values=list(sectors_data.values()),
                names=list(sectors_data.keys()),
                title=f'Struktura sektorowa przemysłu - {voivodeship}'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating sector composition: {str(e)}")
            return go.Figure()
    
    def create_investment_flow(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create foreign investment flow visualization."""
        try:
            year_data = df[df['rok'] == year].sort_values('foreign_investment', ascending=True)
            
            fig = px.bar(
                year_data,
                x='foreign_investment',
                y='wojewodztwo',
                orientation='h',
                title=f'Inwestycje zagraniczne według województw ({year})',
                labels={'foreign_investment': 'Inwestycje (mld zł)', 'wojewodztwo': 'Województwo'},
                color='foreign_investment',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(height=600)
            return fig
            
        except Exception as e:
            st.error(f"Error creating investment flow: {str(e)}")
            return go.Figure()
    
    def get_industry_summary(self, df: pd.DataFrame, voivodeship: str, year: int) -> Dict:
        """Get industry summary for a voivodeship."""
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                return {}
            
            row = data.iloc[0]
            
            return {
                'voivodeship': voivodeship,
                'year': year,
                'industrial_production': row['industrial_production'],
                'manufacturing_share': (row['manufacturing_output'] / row['industrial_production']) * 100,
                'export_value': row['export_value'],
                'import_value': row['import_value'],
                'trade_balance': row['trade_balance'],
                'export_import_ratio': row['export_value'] / row['import_value'] if row['import_value'] > 0 else 0,
                'foreign_investment': row['foreign_investment'],
                'employment_industry': row['employment_industry'],
                'productivity_index': row['productivity_index']
            }
            
        except Exception as e:
            st.error(f"Error getting industry summary: {str(e)}")
            return {}
    
    def analyze_competitiveness(self, df: pd.DataFrame, voivodeship: str) -> Dict:
        """Analyze industrial competitiveness indicators."""
        try:
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            
            if len(voiv_data) < 2:
                return {}
            
            latest = voiv_data.iloc[-1]
            first = voiv_data.iloc[0]
            
            # Calculate competitiveness metrics
            productivity_growth = (latest['productivity_index'] - first['productivity_index']) / len(voiv_data)
            export_growth = ((latest['export_value'] - first['export_value']) / first['export_value']) * 100
            investment_growth = ((latest['foreign_investment'] - first['foreign_investment']) / first['foreign_investment']) * 100
            
            # Ranking against other voivodeships in latest year
            latest_year_data = df[df['rok'] == latest['rok']]
            prod_rank = (latest_year_data['industrial_production'] > latest['industrial_production']).sum() + 1
            export_rank = (latest_year_data['export_value'] > latest['export_value']).sum() + 1
            
            return {
                'productivity_growth_annual': productivity_growth,
                'export_growth_total': export_growth,
                'investment_growth_total': investment_growth,
                'production_rank': prod_rank,
                'export_rank': export_rank,
                'trade_balance_trend': 'positive' if latest['trade_balance'] > 0 else 'negative'
            }
            
        except Exception as e:
            st.error(f"Error analyzing competitiveness: {str(e)}")
            return {}
    
    def create_sector_comparison(self, df: pd.DataFrame, selected_voivodeships: List[str], year: int) -> go.Figure:
        """Create sector comparison for selected voivodeships."""
        try:
            year_data = df[(df['rok'] == year) & (df['wojewodztwo'].isin(selected_voivodeships))]
            
            if year_data.empty:
                return go.Figure()
            
            # Create grouped bar chart for different sectors
            fig = go.Figure()
            
            metrics = ['industrial_production', 'export_value', 'import_value']
            metric_names = ['Produkcja przemysłowa (mld zł)', 'Eksport (mld EUR)', 'Import (mld EUR)']
            colors = ['steelblue', 'green', 'orange']
            
            x_pos = list(range(len(selected_voivodeships)))
            bar_width = 0.25
            
            for i, (metric, name, color) in enumerate(zip(metrics, metric_names, colors)):
                y_values = [year_data[year_data['wojewodztwo'] == voiv][metric].iloc[0] 
                           if not year_data[year_data['wojewodztwo'] == voiv].empty else 0 
                           for voiv in selected_voivodeships]
                
                fig.add_trace(go.Bar(
                    x=[x + i * bar_width for x in x_pos],
                    y=y_values,
                    name=name,
                    marker_color=color,
                    width=bar_width
                ))
            
            fig.update_layout(
                title=f'Porównanie sektorów przemysłowych ({year})',
                xaxis=dict(
                    title='Województwo',
                    tickmode='array',
                    tickvals=[x + bar_width for x in x_pos],
                    ticktext=selected_voivodeships,
                    tickangle=45
                ),
                yaxis_title='Wartość',
                barmode='group',
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating sector comparison: {str(e)}")
            return go.Figure()
    
    def create_investment_trends(self, df: pd.DataFrame, selected_voivodeships: List[str]) -> go.Figure:
        """Create investment trends for selected voivodeships."""
        try:
            filtered_data = df[df['wojewodztwo'].isin(selected_voivodeships)]
            
            fig = go.Figure()
            
            colors = px.colors.qualitative.Set2
            
            for i, voiv in enumerate(selected_voivodeships):
                voiv_data = filtered_data[filtered_data['wojewodztwo'] == voiv].sort_values('rok')
                
                if not voiv_data.empty:
                    fig.add_trace(go.Scatter(
                        x=voiv_data['rok'],
                        y=voiv_data['foreign_investment'],
                        mode='lines+markers',
                        name=voiv,
                        line=dict(color=colors[i % len(colors)], width=3),
                        marker=dict(size=8),
                        hovertemplate=f'<b>{voiv}</b><br>' +
                                    'Rok: %{x}<br>' +
                                    'Inwestycje: %{y:.1f} mld EUR<br>' +
                                    '<extra></extra>'
                    ))
            
            fig.update_layout(
                title=f'Trendy inwestycji zagranicznych w wybranych województwach',
                xaxis_title='Rok',
                yaxis_title='Inwestycje zagraniczne (mld EUR)',
                hovermode='x unified',
                height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating investment trends: {str(e)}")
            return go.Figure()
