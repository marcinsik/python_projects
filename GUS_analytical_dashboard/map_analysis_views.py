"""
Map analysis views for the GUS Analytical Dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import Config
from session_manager import SessionManager

class MapAnalysisViews:
    """Handles map analysis view rendering."""
    
    @staticmethod
    def show_map_analysis(df: pd.DataFrame):
        """Display interactive map analysis."""
        st.markdown("## 🗺️ Mapa Polski - Wizualizacja Choropleth")
        
        session_manager = SessionManager()
        map_viz = session_manager.get_map_visualizations()
        
        # Map configuration controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Metric selection
            metric_options = Config.METRIC_OPTIONS.copy()
            
            # Add GDP per capita if population data is available
            if 'ludnosc_tys' in df.columns:
                # Calculate GDP per capita
                df = df.copy()
                df['pkb_per_capita'] = (df['pkb_mld_zl'] * 1000000) / (df['ludnosc_tys'] * 1000)
            else:
                # Remove GDP per capita option if no population data
                if 'PKB per capita (zł)' in metric_options:
                    del metric_options['PKB per capita (zł)']
            
            selected_metric_label = st.selectbox(
                "Wybierz wskaźnik:",
                list(metric_options.keys())
            )
            selected_metric = metric_options[selected_metric_label]
        
        with col2:
            # Year selection
            available_years = sorted(df['rok'].unique())
            selected_year = st.selectbox(
                "Wybierz rok:",
                available_years,
                index=len(available_years)-1  # Default to latest year
            )
        
        with col3:
            # Color scale selection
            selected_color_scale = st.selectbox(
                "Skala kolorów:",
                Config.COLOR_SCALES
            )
        
        # Map type selection
        st.markdown("### Typ mapy")
        map_type = st.radio(
            "Wybierz typ wizualizacji:",
            ["Mapa punktowa", "Animowana mapa czasowa"],
            horizontal=True,
            help="Mapa punktowa pokazuje dane dla wybranego roku, animowana mapa pokazuje zmiany w czasie"
        )
        
        # Debug information
        MapAnalysisViews._render_debug_info(df)
        
        if map_type == "Mapa punktowa":
            MapAnalysisViews._render_scatter_map(
                df, map_viz, selected_metric, selected_metric_label, selected_year
            )
        else:
            MapAnalysisViews._render_animated_map(
                df, map_viz, selected_metric, selected_metric_label, selected_color_scale
            )
        
        # Voivodeship details
        MapAnalysisViews._render_voivodeship_details(df, selected_metric, selected_metric_label)
    
    @staticmethod
    def _render_debug_info(df: pd.DataFrame):
        """Render debug information about the data."""
        with st.expander("🔍 Informacje o danych"):
            st.write(f"Liczba rekordów: {len(df)}")
            st.write(f"Dostępne lata: {sorted(df['rok'].unique())}")
            st.write(f"Dostępne województwa: {len(df['wojewodztwo'].unique())}")
            st.write(f"Dostępne kolumny: {list(df.columns)}")
    
    @staticmethod
    def _render_scatter_map(df, map_viz, selected_metric, selected_metric_label, selected_year):
        """Render scatter map for selected year."""
        st.markdown(f"### {selected_metric_label} - {selected_year}")
        
        try:
            # Create the scatter map
            fig = map_viz.create_scatter_map(
                df=df,
                metric=selected_metric,
                year=selected_year,
                title=f"{selected_metric_label} według województw"
            )
            
            if fig.data:  # Check if figure has data
                st.plotly_chart(fig, use_container_width=True)
                
                # Show summary statistics
                MapAnalysisViews._render_year_statistics(df, selected_metric, selected_year)
                
                # Show rankings
                MapAnalysisViews._render_rankings(df, selected_metric, selected_metric_label, selected_year)
            else:
                st.warning("Brak danych do wyświetlenia na mapie dla wybranych parametrów.")
        
        except Exception as e:
            st.error(f"Błąd podczas tworzenia mapy: {str(e)}")
    
    @staticmethod
    def _render_animated_map(df, map_viz, selected_metric, selected_metric_label, selected_color_scale):
        """Render animated map."""
        st.markdown(f"### {selected_metric_label} - Animacja czasowa")
        
        # Check if we have multiple years for animation
        available_years = sorted(df['rok'].unique())
        if len(available_years) < 2:
            st.warning("⚠️ Animacja wymaga danych z co najmniej dwóch różnych lat.")
            st.info(f"Dostępne lata w danych: {available_years}")
            return
        
        # Animation type selection
        animation_type = st.radio(
            "Wybierz typ animacji:",
            ["Mapa punktowa animowana", "Wykres słupkowy animowany"],
            horizontal=True
        )
        
        try:
            if animation_type == "Mapa punktowa animowana":
                fig = map_viz.create_animated_scatter_map(
                    df=df,
                    metric=selected_metric,
                    title=f"{selected_metric_label} - zmiany w czasie",
                    color_scale=selected_color_scale
                )
            else:
                fig = map_viz.create_animated_bar_chart_map(
                    df=df,
                    metric=selected_metric,
                    title=f"{selected_metric_label} - ranking województw w czasie"
                )
            
            if fig.data:  # Check if figure has data
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("💡 **Wskazówka:** Użyj przycisków odtwarzania poniżej mapy, aby zobaczyć zmiany w czasie.")
                
                # Show trend analysis
                MapAnalysisViews._render_trend_analysis(df, selected_metric)
            else:
                st.warning("Brak danych do wyświetlenia animowanej mapy.")
        
        except Exception as e:
            st.error(f"Błąd podczas tworzenia animowanej mapy: {str(e)}")
    
    @staticmethod
    def _render_year_statistics(df, selected_metric, selected_year):
        """Render statistics for selected year."""
        st.markdown("### 📊 Statystyki dla wybranego roku")
        year_data = df[df['rok'] == selected_year]
        
        if not year_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            metric_values = year_data[selected_metric].dropna()
            
            with col1:
                st.metric("Minimum", f"{metric_values.min():.2f}")
            with col2:
                st.metric("Maksimum", f"{metric_values.max():.2f}")
            with col3:
                st.metric("Średnia", f"{metric_values.mean():.2f}")
            with col4:
                st.metric("Mediana", f"{metric_values.median():.2f}")
    
    @staticmethod
    def _render_rankings(df, selected_metric, selected_metric_label, selected_year):
        """Render top/bottom rankings."""
        year_data = df[df['rok'] == selected_year]
        
        if not year_data.empty:
            st.markdown("### 🏆 Ranking województw")
            col1, col2 = st.columns(2)
            
            sorted_data = year_data.sort_values(selected_metric, ascending=False)
            
            with col1:
                st.markdown("**Najwyższe wartości:**")
                top_5 = sorted_data.head(5)[['wojewodztwo', selected_metric]]
                for idx, row in top_5.iterrows():
                    st.markdown(f"🥇 **{row['wojewodztwo']}**: {row[selected_metric]:.2f}")
            
            with col2:
                st.markdown("**Najniższe wartości:**")
                bottom_5 = sorted_data.tail(5)[['wojewodztwo', selected_metric]]
                for idx, row in bottom_5.iterrows():
                    st.markdown(f"📊 **{row['wojewodztwo']}**: {row[selected_metric]:.2f}")
    
    @staticmethod
    def _render_trend_analysis(df, selected_metric):
        """Render trend analysis for animated maps."""
        st.markdown("### 📈 Analiza trendów")
        
        # Calculate year-over-year changes
        trend_data = []
        for voivodeship in df['wojewodztwo'].unique():
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            if len(voiv_data) > 1:
                first_value = voiv_data[selected_metric].iloc[0]
                last_value = voiv_data[selected_metric].iloc[-1]
                change = last_value - first_value
                pct_change = (change / first_value * 100) if first_value != 0 else 0
                trend_data.append({
                    'wojewodztwo': voivodeship,
                    'zmiana_bezwzględna': change,
                    'zmiana_procentowa': pct_change
                })
        
        if trend_data:
            trend_df = pd.DataFrame(trend_data)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Największy wzrost:**")
                top_growth = trend_df.nlargest(3, 'zmiana_procentowa')
                for _, row in top_growth.iterrows():
                    st.markdown(f"📈 **{row['wojewodztwo']}**: +{row['zmiana_procentowa']:.1f}%")
            
            with col2:
                st.markdown("**Największy spadek:**")
                top_decline = trend_df.nsmallest(3, 'zmiana_procentowa')
                for _, row in top_decline.iterrows():
                    st.markdown(f"📉 **{row['wojewodztwo']}**: {row['zmiana_procentowa']:.1f}%")
    
    @staticmethod
    def _render_voivodeship_details(df, selected_metric, selected_metric_label):
        """Render detailed voivodeship analysis."""
        st.markdown("### 🔍 Szczegóły województwa")
        
        selected_voivodeship = st.selectbox(
            "Wybierz województwo do szczegółowej analizy:",
            sorted(df['wojewodztwo'].unique())
        )
        
        if selected_voivodeship:
            voiv_data = df[df['wojewodztwo'] == selected_voivodeship].sort_values('rok')
            
            if not voiv_data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Show basic info
                    latest_data = voiv_data.iloc[-1]
                    st.markdown(f"**Województwo:** {selected_voivodeship}")
                    st.markdown(f"**Najnowsze dane ({int(latest_data['rok'])}):**")
                    if 'pkb_mld_zl' in voiv_data.columns:
                        st.markdown(f"• PKB: {latest_data['pkb_mld_zl']:.1f} mld zł")
                    if 'bezrobocie_proc' in voiv_data.columns:
                        st.markdown(f"• Bezrobocie: {latest_data['bezrobocie_proc']:.1f}%")
                    if 'ludnosc_tys' in voiv_data.columns:
                        st.markdown(f"• Ludność: {latest_data['ludnosc_tys']:.0f} tys.")
                
                with col2:
                    # Create trend chart for selected voivodeship
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=voiv_data['rok'],
                        y=voiv_data[selected_metric],
                        mode='lines+markers',
                        name=selected_metric_label,
                        line=dict(width=3),
                        marker=dict(size=8)
                    ))
                    
                    fig.update_layout(
                        title=f"{selected_metric_label} - {selected_voivodeship}",
                        xaxis_title="Rok",
                        yaxis_title=selected_metric_label,
                        height=300
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
