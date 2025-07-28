"""
Analysis views for the GUS Analytical Dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from session_manager import SessionManager
from ui_components import UIComponents

class AnalysisViews:
    """Handles different analysis view rendering."""
    
    @staticmethod
    def show_overview(df: pd.DataFrame):
        """Display main overview analysis."""
        st.markdown("## 📈 Przegląd główny")
        
        # Render overview metrics
        UIComponents.render_metrics(df)
        
        # Main charts
        col1, col2 = st.columns(2)
        
        session_manager = SessionManager()
        viz = session_manager.get_visualizations()
        
        with col1:
            fig_gdp = viz.create_line_chart(
                df, 'pkb_mld_zl', 'PKB według województw', 'PKB (mld zł)'
            )
            st.plotly_chart(fig_gdp, use_container_width=True)
        
        with col2:
            fig_unemployment = viz.create_line_chart(
                df, 'bezrobocie_proc', 'Bezrobocie według województw', 'Bezrobocie (%)'
            )
            st.plotly_chart(fig_unemployment, use_container_width=True)
        
        # Summary table
        st.markdown("### 🏆 Ranking województw (najnowsze dane)")
        latest_year = df['rok'].max()
        summary_table = viz.create_summary_table(df, latest_year)
        if not summary_table.empty:
            st.dataframe(summary_table, use_container_width=True)
    
    @staticmethod
    def show_gdp_analysis(df: pd.DataFrame):
        """Display detailed GDP analysis."""
        st.markdown("## 💰 Analiza PKB")
        
        session_manager = SessionManager()
        viz = session_manager.get_visualizations()
        
        # Line chart for GDP
        fig_line = viz.create_line_chart(
            df, 'pkb_mld_zl', 'Dynamika PKB w czasie', 'PKB (mld zł)'
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart for selected year
            selected_year = st.selectbox(
                "Wybierz rok dla porównania:",
                sorted(df['rok'].unique(), reverse=True)
            )
            
            fig_bar = viz.create_bar_chart(
                df, 'pkb_mld_zl', selected_year, 'PKB według województw', 'PKB (mld zł)'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # GDP per capita if available
            if 'pkb_per_capita' in df.columns:
                fig_per_capita = viz.create_line_chart(
                    df, 'pkb_per_capita', 'PKB per capita', 'PKB per capita (zł)'
                )
                st.plotly_chart(fig_per_capita, use_container_width=True)
            else:
                st.info("Dane o PKB per capita nie są dostępne (brak danych o ludności)")
    
    @staticmethod
    def show_unemployment_analysis(df: pd.DataFrame):
        """Display detailed unemployment analysis."""
        st.markdown("## 👥 Analiza bezrobocia")
        
        session_manager = SessionManager()
        viz = session_manager.get_visualizations()
        
        # Line chart for unemployment
        fig_line = viz.create_line_chart(
            df, 'bezrobocie_proc', 'Dynamika bezrobocia w czasie', 'Bezrobocie (%)'
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart for selected year (highest unemployment)
            selected_year = st.selectbox(
                "Wybierz rok dla porównania:",
                sorted(df['rok'].unique(), reverse=True),
                key="unemployment_year"
            )
            
            # Show highest unemployment
            year_data = df[df['rok'] == selected_year].copy()
            if not year_data.empty:
                year_data = year_data.nlargest(10, 'bezrobocie_proc')
                
                fig_bar = px.bar(
                    year_data,
                    x='wojewodztwo',
                    y='bezrobocie_proc',
                    title=f"Najwyższe bezrobocie - {selected_year}",
                    labels={'wojewodztwo': 'Województwo', 'bezrobocie_proc': 'Bezrobocie (%)'},
                    color='bezrobocie_proc',
                    color_continuous_scale='reds'
                )
                fig_bar.update_layout(
                    xaxis_tickangle=-45,
                    template="plotly_white"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Unemployment statistics
            st.markdown("### 📊 Statystyki")
            
            unemployment_stats = df.groupby('rok')['bezrobocie_proc'].agg(['mean', 'min', 'max']).round(1)
            unemployment_stats.columns = ['Średnie', 'Minimum', 'Maksimum']
            unemployment_stats.index.name = 'Rok'
            
            st.dataframe(unemployment_stats, use_container_width=True)
    
    @staticmethod
    def show_voivodeship_comparison(df: pd.DataFrame, selected_voivodeships: list):
        """Display voivodeship comparison."""
        st.markdown("## 🔄 Porównanie województw")
        
        if not selected_voivodeships:
            st.warning("Wybierz województwa do porównania w panelu bocznym.")
            return
        
        session_manager = SessionManager()
        viz = session_manager.get_visualizations()
        
        # Comparison chart for both metrics
        fig_comparison = viz.create_comparison_chart(
            df, 
            selected_voivodeships,
            ['pkb_mld_zl', 'bezrobocie_proc'],
            ['PKB (mld zł)', 'Bezrobocie (%)']
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Comparison table
        st.markdown("### 📋 Tabela porównawcza")
        
        comparison_data = df[df['wojewodztwo'].isin(selected_voivodeships)]
        pivot_gdp = comparison_data.pivot(index='rok', columns='wojewodztwo', values='pkb_mld_zl')
        
        st.markdown("**PKB (mld zł)**")
        st.dataframe(pivot_gdp.round(1), use_container_width=True)
    
    @staticmethod
    def show_correlation_analysis(df: pd.DataFrame):
        """Display correlation analysis."""
        st.markdown("## 🔗 Analiza korelacji")
        
        session_manager = SessionManager()
        viz = session_manager.get_visualizations()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # GDP vs Unemployment correlation
            fig_corr = viz.create_correlation_chart(
                df, 'pkb_mld_zl', 'bezrobocie_proc',
                'PKB (mld zł)', 'Bezrobocie (%)'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            # Correlation for selected year
            selected_year = st.selectbox(
                "Wybierz rok:",
                sorted(df['rok'].unique(), reverse=True),
                key="corr_year"
            )
            
            fig_corr_year = viz.create_correlation_chart(
                df, 'pkb_mld_zl', 'bezrobocie_proc',
                'PKB (mld zł)', 'Bezrobocie (%)',
                year=selected_year
            )
            st.plotly_chart(fig_corr_year, use_container_width=True)
        
        # Correlation matrix
        st.markdown("### 📊 Macierz korelacji")
        numeric_cols = ['pkb_mld_zl', 'bezrobocie_proc']
        if 'pkb_per_capita' in df.columns:
            numeric_cols.append('pkb_per_capita')
        
        corr_matrix = df[numeric_cols].corr()
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Macierz korelacji",
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    @staticmethod
    def show_growth_analysis(df: pd.DataFrame):
        """Display growth rate analysis."""
        st.markdown("## 📈 Analiza tempa wzrostu")
        
        # Voivodeship and metric selection
        col1, col2 = st.columns(2)
        
        with col1:
            selected_voivodeship = st.selectbox(
                "Wybierz województwo:",
                sorted(df['wojewodztwo'].unique())
            )
        
        with col2:
            metric_options = {
                'PKB': 'pkb_mld_zl',
                'Bezrobocie': 'bezrobocie_proc'
            }
            if 'pkb_per_capita' in df.columns:
                metric_options['PKB per capita'] = 'pkb_per_capita'
            
            selected_metric_label = st.selectbox(
                "Wybierz metrykę:",
                list(metric_options.keys())
            )
            selected_metric = metric_options[selected_metric_label]
        
        # Growth chart
        session_manager = SessionManager()
        viz = session_manager.get_visualizations()
        
        fig_growth = viz.create_growth_chart(
            df, selected_metric, selected_voivodeship, selected_metric_label
        )
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Growth table for all voivodeships
        st.markdown("### 📊 Tempo wzrostu - wszystkie województwa")
        
        growth_data = []
        for voivodeship in df['wojewodztwo'].unique():
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            if len(voiv_data) > 1:
                # Calculate average growth rate
                voiv_data_copy = voiv_data.copy()
                voiv_data_copy['growth'] = voiv_data_copy[selected_metric].pct_change() * 100
                avg_growth = voiv_data_copy['growth'].mean()
                
                growth_data.append({
                    'Województwo': voivodeship,
                    f'Średnie tempo wzrostu {selected_metric_label} (%)': round(avg_growth, 2)
                })
        
        if growth_data:
            growth_df = pd.DataFrame(growth_data)
            growth_df = growth_df.sort_values(f'Średnie tempo wzrostu {selected_metric_label} (%)', ascending=False)
            st.dataframe(growth_df, use_container_width=True)
