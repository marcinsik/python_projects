"""
Moduł do tworzenia wizualizacji dla dashboard'u.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
from typing import List, Optional


class Visualizations:
    """Klasa odpowiedzialna za tworzenie wykresów i wizualizacji."""
    
    def __init__(self):
        """Inicjalizacja klasy wizualizacji."""
        self.color_palette = px.colors.qualitative.Set3
        
    def create_line_chart(self, 
                         df: pd.DataFrame,
                         metric: str,
                         title: str,
                         y_label: str,
                         voivodeships: Optional[List[str]] = None) -> go.Figure:
        """
        Tworzy wykres liniowy dla wybranej metryki.
        
        Args:
            df: DataFrame z danymi
            metric: Nazwa kolumny z metryką
            title: Tytuł wykresu
            y_label: Etykieta osi Y
            voivodeships: Lista województw do wyświetlenia
            
        Returns:
            Wykres Plotly
        """
        if df.empty:
            return self._create_empty_chart("Brak danych do wyświetlenia")
        
        # Filtruj dane jeśli wybrano konkretne województwa
        if voivodeships:
            df = df[df['wojewodztwo'].isin(voivodeships)]
        
        fig = px.line(
            df, 
            x='rok', 
            y=metric,
            color='wojewodztwo',
            title=title,
            labels={
                'rok': 'Rok',
                metric: y_label,
                'wojewodztwo': 'Województwo'
            },
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            xaxis_title="Rok",
            yaxis_title=y_label,
            legend_title="Województwo",
            hovermode='x unified',
            template="plotly_white"
        )
        
        fig.update_traces(
            line=dict(width=2),
            marker=dict(size=6)
        )
        
        return fig
    
    def create_bar_chart(self, 
                        df: pd.DataFrame,
                        metric: str,
                        year: int,
                        title: str,
                        y_label: str,
                        top_n: int = 10) -> go.Figure:
        """
        Tworzy wykres słupkowy dla wybranego roku.
        
        Args:
            df: DataFrame z danymi
            metric: Nazwa kolumny z metryką
            year: Rok do analizy
            title: Tytuł wykresu
            y_label: Etykieta osi Y
            top_n: Liczba województw do wyświetlenia
            
        Returns:
            Wykres Plotly
        """
        if df.empty:
            return self._create_empty_chart("Brak danych do wyświetlenia")
        
        # Filtruj dane dla wybranego roku
        year_data = df[df['rok'] == year].copy()
        
        if year_data.empty:
            return self._create_empty_chart(f"Brak danych dla roku {year}")
        
        # Sortuj i weź top N
        year_data = year_data.nlargest(top_n, metric)
        
        fig = px.bar(
            year_data,
            x='wojewodztwo',
            y=metric,
            title=f"{title} - {year}",
            labels={
                'wojewodztwo': 'Województwo',
                metric: y_label
            },
            color=metric,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            xaxis_title="Województwo",
            yaxis_title=y_label,
            xaxis_tickangle=-45,
            template="plotly_white"
        )
        
        return fig
    
    def create_comparison_chart(self, 
                              df: pd.DataFrame,
                              voivodeships: List[str],
                              metrics: List[str],
                              metric_labels: List[str]) -> go.Figure:
        """
        Tworzy wykres porównujący różne metryki dla wybranych województw.
        
        Args:
            df: DataFrame z danymi
            voivodeships: Lista województw do porównania
            metrics: Lista metryk do porównania
            metric_labels: Lista etykiet dla metryk
            
        Returns:
            Wykres Plotly z podwykresami
        """
        if df.empty or not voivodeships:
            return self._create_empty_chart("Brak danych do wyświetlenia")
        
        # Filtruj dane dla wybranych województw
        filtered_df = df[df['wojewodztwo'].isin(voivodeships)]
        
        if filtered_df.empty:
            return self._create_empty_chart("Brak danych dla wybranych województw")
        
        # Utwórz podwykresy
        fig = make_subplots(
            rows=len(metrics), 
            cols=1,
            subplot_titles=metric_labels,
            vertical_spacing=0.08
        )
        
        colors = px.colors.qualitative.Set1[:len(voivodeships)]
        
        for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
            for j, voivodeship in enumerate(voivodeships):
                voiv_data = filtered_df[filtered_df['wojewodztwo'] == voivodeship]
                
                fig.add_trace(
                    go.Scatter(
                        x=voiv_data['rok'],
                        y=voiv_data[metric],
                        name=voivodeship if i == 0 else None,
                        showlegend=(i == 0),
                        line=dict(color=colors[j], width=2),
                        marker=dict(size=6)
                    ),
                    row=i+1, col=1
                )
        
        fig.update_layout(
            height=300 * len(metrics),
            title="Porównanie województw",
            template="plotly_white"
        )
        
        # Aktualizuj etykiety osi
        for i in range(len(metrics)):
            fig.update_xaxes(title_text="Rok", row=i+1, col=1)
            fig.update_yaxes(title_text=metric_labels[i], row=i+1, col=1)
        
        return fig
    
    def create_correlation_chart(self, 
                               df: pd.DataFrame,
                               x_metric: str,
                               y_metric: str,
                               x_label: str,
                               y_label: str,
                               year: Optional[int] = None) -> go.Figure:
        """
        Tworzy wykres korelacji między dwiema metrykami.
        
        Args:
            df: DataFrame z danymi
            x_metric: Metryka dla osi X
            y_metric: Metryka dla osi Y
            x_label: Etykieta osi X
            y_label: Etykieta osi Y
            year: Rok do analizy (opcjonalnie)
            
        Returns:
            Wykres rozrzutu Plotly
        """
        if df.empty:
            return self._create_empty_chart("Brak danych do wyświetlenia")
        
        plot_data = df.copy()
        
        # Filtruj po roku jeśli podano
        if year:
            plot_data = plot_data[plot_data['rok'] == year]
            title_suffix = f" - {year}"
        else:
            title_suffix = " - wszystkie lata"
        
        if plot_data.empty:
            return self._create_empty_chart("Brak danych dla wybranego okresu")
        
        fig = px.scatter(
            plot_data,
            x=x_metric,
            y=y_metric,
            color='wojewodztwo' if year else 'rok',
            title=f"Korelacja: {x_label} vs {y_label}{title_suffix}",
            labels={
                x_metric: x_label,
                y_metric: y_label,
                'wojewodztwo': 'Województwo',
                'rok': 'Rok'
            },
            hover_data=['wojewodztwo', 'rok']
        )
        
        # Dodaj linię trendu
        fig.add_trace(
            go.Scatter(
                x=plot_data[x_metric],
                y=px.scatter(plot_data, x=x_metric, y=y_metric, trendline="ols").data[1].y,
                mode='lines',
                name='Trend',
                line=dict(dash='dash', color='red', width=2)
            )
        )
        
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white"
        )
        
        return fig
    
    def create_growth_chart(self, 
                          df: pd.DataFrame,
                          metric: str,
                          voivodeship: str,
                          metric_label: str) -> go.Figure:
        """
        Tworzy wykres tempa wzrostu dla wybranej metryki i województwa.
        
        Args:
            df: DataFrame z danymi
            metric: Nazwa kolumny z metryką
            voivodeship: Nazwa województwa
            metric_label: Etykieta metryki
            
        Returns:
            Wykres Plotly
        """
        if df.empty:
            return self._create_empty_chart("Brak danych do wyświetlenia")
        
        # Filtruj dane dla województwa
        voiv_data = df[df['wojewodztwo'] == voivodeship].copy()
        voiv_data = voiv_data.sort_values('rok')
        
        if len(voiv_data) < 2:
            return self._create_empty_chart(f"Za mało danych dla województwa {voivodeship}")
        
        # Oblicz tempo wzrostu
        voiv_data['wzrost_proc'] = voiv_data[metric].pct_change() * 100
        
        fig = go.Figure()
        
        # Wykres słupkowy tempa wzrostu
        colors = ['green' if x > 0 else 'red' for x in voiv_data['wzrost_proc'].fillna(0)]
        
        fig.add_trace(
            go.Bar(
                x=voiv_data['rok'],
                y=voiv_data['wzrost_proc'],
                name='Tempo wzrostu (%)',
                marker_color=colors,
                text=[f"{x:.1f}%" if not pd.isna(x) else "" for x in voiv_data['wzrost_proc']],
                textposition='outside'
            )
        )
        
        fig.update_layout(
            title=f"Tempo wzrostu {metric_label} - {voivodeship}",
            xaxis_title="Rok",
            yaxis_title="Tempo wzrostu (%)",
            template="plotly_white"
        )
        
        # Dodaj linię na poziomie 0
        fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
        
        return fig
    
    def create_summary_table(self, df: pd.DataFrame, year: int) -> pd.DataFrame:
        """
        Tworzy tabelę podsumowującą dla wybranego roku.
        
        Args:
            df: DataFrame z danymi
            year: Rok do analizy
            
        Returns:
            DataFrame z podsumowaniem
        """
        if df.empty:
            return pd.DataFrame()
        
        year_data = df[df['rok'] == year].copy()
        
        if year_data.empty:
            return pd.DataFrame()
        
        # Sortuj po PKB
        summary = year_data.sort_values('pkb_mld_zl', ascending=False).copy()
        
        # Formatuj kolumny
        summary['PKB (mld zł)'] = summary['pkb_mld_zl'].round(1)
        summary['Bezrobocie (%)'] = summary['bezrobocie_proc'].round(1)
        
        if 'pkb_per_capita' in summary.columns:
            summary['PKB per capita (tys zł)'] = (summary['pkb_per_capita'] / 1000).round(1)
        
        # Wybierz kolumny do wyświetlenia
        columns_to_show = ['wojewodztwo', 'PKB (mld zł)', 'Bezrobocie (%)']
        if 'PKB per capita (tys zł)' in summary.columns:
            columns_to_show.append('PKB per capita (tys zł)')
        
        return summary[columns_to_show].reset_index(drop=True)
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """
        Tworzy pusty wykres z komunikatem.
        
        Args:
            message: Komunikat do wyświetlenia
            
        Returns:
            Pusty wykres Plotly
        """
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            template="plotly_white"
        )
        return fig
