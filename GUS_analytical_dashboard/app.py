"""
Główna aplikacja Dashboard Danych Publicznych (GUS)
Interaktywny dashboard do analizy danych ekonomicznych Polski.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import DataLoader, get_sample_data_info
from visualizations import Visualizations
import os

# Konfiguracja strony
st.set_page_config(
    page_title="Dashboard Danych Publicznych (GUS)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS
st.markdown("""
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
""", unsafe_allow_html=True)

# Inicjalizacja sesji
if 'data_loader' not in st.session_state:
    st.session_state.data_loader = DataLoader()
    st.session_state.visualizations = Visualizations()
    st.session_state.data_loaded = False

def main():
    """Główna funkcja aplikacji."""
    
    # Nagłówek
    st.markdown('<div class="main-header">📊 Dashboard Danych Publicznych (GUS)</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Ustawienia")
        
        # Sekcja wczytywania danych
        st.markdown("### 📁 Źródło danych")
        
        data_source = st.radio(
            "Wybierz źródło danych:",
            ["Dane przykładowe", "Prześlij własny plik"],
            help="Wybierz między danymi przykładowymi a przesłaniem własnego pliku"
        )
        
        if data_source == "Prześlij własny plik":
            uploaded_file = st.file_uploader(
                "Prześlij plik CSV lub Excel",
                type=['csv', 'xlsx', 'xls'],
                help="Plik powinien zawierać kolumny: rok, wojewodztwo, pkb_mld_zl, bezrobocie_proc"
            )
            
            if uploaded_file is not None:
                with st.spinner("Wczytywanie danych..."):
                    df = st.session_state.data_loader.load_uploaded_file(uploaded_file)
                    if not df.empty:
                        st.session_state.data_loader.data = df
                        st.session_state.data_loaded = True
                        st.success("✅ Dane zostały wczytane!")
                    else:
                        st.error("❌ Nie udało się wczytać danych")
        else:
            # Wczytaj dane przykładowe
            if not st.session_state.data_loaded:
                with st.spinner("Wczytywanie danych przykładowych..."):
                    df = st.session_state.data_loader.load_data()
                    if not df.empty:
                        st.session_state.data_loaded = True
                        st.success("✅ Dane przykładowe wczytane!")
                    else:
                        st.error("❌ Nie udało się wczytać danych przykładowych")
        
        # Jeśli dane są wczytane, pokaż filtry
        if st.session_state.data_loaded:
            st.markdown("### 🔍 Filtry")
            
            # Filtry
            years = st.session_state.data_loader.get_available_years()
            voivodeships = st.session_state.data_loader.get_available_voivodeships()
            
            if years and voivodeships:
                # Zakres lat
                year_range = st.slider(
                    "Zakres lat:",
                    min_value=min(years),
                    max_value=max(years),
                    value=(min(years), max(years)),
                    help="Wybierz zakres lat do analizy"
                )
                
                # Wybór województw
                selected_voivodeships = st.multiselect(
                    "Wybierz województwa:",
                    options=voivodeships,
                    default=voivodeships[:5],  # Domyślnie pierwsze 5
                    help="Wybierz województwa do analizy"
                )
                
                # Typ analizy
                st.markdown("### 📊 Typ analizy")
                analysis_type = st.selectbox(
                    "Wybierz typ analizy:",
                    [
                        "Przegląd główny",
                        "Analiza PKB",
                        "Analiza bezrobocia",
                        "Porównanie województw",
                        "Korelacje",
                        "Tempo wzrostu"
                    ]
                )
        
        # Informacje o danych
        with st.expander("ℹ️ Informacje o danych"):
            info = get_sample_data_info()
            st.markdown("**Wymagane kolumny:**")
            for col in info["required_columns"]:
                st.markdown(f"• `{col}`")
            
            st.markdown("**Opcjonalne kolumny:**")
            for col in info["optional_columns"]:
                st.markdown(f"• `{col}`")
            
            st.markdown(f"**Opis:** {info['description']}")
    
    # Główna zawartość
    if not st.session_state.data_loaded:
        st.info("👆 Wybierz źródło danych w panelu bocznym, aby rozpocząć analizę.")
        
        # Pokaż przykład struktury danych
        st.markdown("## 📋 Przykładowa struktura danych")
        sample_df = pd.DataFrame({
            'rok': [2019, 2019, 2020, 2020],
            'wojewodztwo': ['Mazowieckie', 'Śląskie', 'Mazowieckie', 'Śląskie'],
            'pkb_mld_zl': [298.5, 158.2, 285.3, 148.7],
            'bezrobocie_proc': [3.8, 4.2, 4.5, 5.1]
        })
        st.dataframe(sample_df, use_container_width=True)
        
    else:
        # Filtruj dane
        filtered_data = st.session_state.data_loader.filter_data(
            voivodeships=selected_voivodeships,
            year_range=year_range
        )
        
        if filtered_data.empty:
            st.warning("⚠️ Brak danych dla wybranych filtrów.")
            return
        
        # Wyświetl analizę na podstawie wybranego typu
        if analysis_type == "Przegląd główny":
            show_overview(filtered_data)
        elif analysis_type == "Analiza PKB":
            show_gdp_analysis(filtered_data)
        elif analysis_type == "Analiza bezrobocia":
            show_unemployment_analysis(filtered_data)
        elif analysis_type == "Porównanie województw":
            show_voivodeship_comparison(filtered_data, selected_voivodeships)
        elif analysis_type == "Korelacje":
            show_correlation_analysis(filtered_data)
        elif analysis_type == "Tempo wzrostu":
            show_growth_analysis(filtered_data)


def show_overview(df: pd.DataFrame):
    """Wyświetla przegląd główny danych."""
    st.markdown("## 📈 Przegląd główny")
    
    # Metryki główne
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Liczba województw",
            len(df['wojewodztwo'].unique()),
            help="Liczba województw w analizie"
        )
    
    with col2:
        st.metric(
            "Zakres lat",
            f"{df['rok'].min()} - {df['rok'].max()}",
            help="Zakres czasowy danych"
        )
    
    with col3:
        avg_gdp = df.groupby('rok')['pkb_mld_zl'].sum().mean()
        st.metric(
            "Średnie PKB (mld zł)",
            f"{avg_gdp:.1f}",
            help="Średnie całkowite PKB we wszystkich latach"
        )
    
    with col4:
        avg_unemployment = df['bezrobocie_proc'].mean()
        st.metric(
            "Średnie bezrobocie (%)",
            f"{avg_unemployment:.1f}",
            help="Średni poziom bezrobocia"
        )
    
    # Wykresy główne
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gdp = st.session_state.visualizations.create_line_chart(
            df, 'pkb_mld_zl', 'PKB według województw', 'PKB (mld zł)'
        )
        st.plotly_chart(fig_gdp, use_container_width=True)
    
    with col2:
        fig_unemployment = st.session_state.visualizations.create_line_chart(
            df, 'bezrobocie_proc', 'Bezrobocie według województw', 'Bezrobocie (%)'
        )
        st.plotly_chart(fig_unemployment, use_container_width=True)
    
    # Tabela rankingowa
    st.markdown("### 🏆 Ranking województw (najnowsze dane)")
    latest_year = df['rok'].max()
    summary_table = st.session_state.visualizations.create_summary_table(df, latest_year)
    if not summary_table.empty:
        st.dataframe(summary_table, use_container_width=True)


def show_gdp_analysis(df: pd.DataFrame):
    """Wyświetla szczegółową analizę PKB."""
    st.markdown("## 💰 Analiza PKB")
    
    # Wykres liniowy PKB
    fig_line = st.session_state.visualizations.create_line_chart(
        df, 'pkb_mld_zl', 'Dynamika PKB w czasie', 'PKB (mld zł)'
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Wykres słupkowy dla wybranego roku
        selected_year = st.selectbox(
            "Wybierz rok dla porównania:",
            sorted(df['rok'].unique(), reverse=True)
        )
        
        fig_bar = st.session_state.visualizations.create_bar_chart(
            df, 'pkb_mld_zl', selected_year, 'PKB według województw', 'PKB (mld zł)'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # PKB per capita jeśli dostępne
        if 'pkb_per_capita' in df.columns:
            fig_per_capita = st.session_state.visualizations.create_line_chart(
                df, 'pkb_per_capita', 'PKB per capita', 'PKB per capita (zł)'
            )
            st.plotly_chart(fig_per_capita, use_container_width=True)
        else:
            st.info("Dane o PKB per capita nie są dostępne (brak danych o ludności)")


def show_unemployment_analysis(df: pd.DataFrame):
    """Wyświetla szczegółową analizę bezrobocia."""
    st.markdown("## 👥 Analiza bezrobocia")
    
    # Wykres liniowy bezrobocia
    fig_line = st.session_state.visualizations.create_line_chart(
        df, 'bezrobocie_proc', 'Dynamika bezrobocia w czasie', 'Bezrobocie (%)'
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Wykres słupkowy dla wybranego roku (od najwyższego)
        selected_year = st.selectbox(
            "Wybierz rok dla porównania:",
            sorted(df['rok'].unique(), reverse=True),
            key="unemployment_year"
        )
        
        # Modyfikuj funkcję żeby pokazać najwyższe bezrobocie
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
        # Statystyki bezrobocia
        st.markdown("### 📊 Statystyki")
        
        unemployment_stats = df.groupby('rok')['bezrobocie_proc'].agg(['mean', 'min', 'max']).round(1)
        unemployment_stats.columns = ['Średnie', 'Minimum', 'Maksimum']
        unemployment_stats.index.name = 'Rok'
        
        st.dataframe(unemployment_stats, use_container_width=True)


def show_voivodeship_comparison(df: pd.DataFrame, selected_voivodeships: list):
    """Wyświetla porównanie województw."""
    st.markdown("## 🔄 Porównanie województw")
    
    if not selected_voivodeships:
        st.warning("Wybierz województwa do porównania w panelu bocznym.")
        return
    
    # Porównanie obu metryk
    fig_comparison = st.session_state.visualizations.create_comparison_chart(
        df, 
        selected_voivodeships,
        ['pkb_mld_zl', 'bezrobocie_proc'],
        ['PKB (mld zł)', 'Bezrobocie (%)']
    )
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Tabela porównawcza
    st.markdown("### 📋 Tabela porównawcza")
    
    comparison_data = df[df['wojewodztwo'].isin(selected_voivodeships)]
    pivot_gdp = comparison_data.pivot(index='rok', columns='wojewodztwo', values='pkb_mld_zl')
    
    st.markdown("**PKB (mld zł)**")
    st.dataframe(pivot_gdp.round(1), use_container_width=True)


def show_correlation_analysis(df: pd.DataFrame):
    """Wyświetla analizę korelacji."""
    st.markdown("## 🔗 Analiza korelacji")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Korelacja PKB vs Bezrobocie
        fig_corr = st.session_state.visualizations.create_correlation_chart(
            df, 'pkb_mld_zl', 'bezrobocie_proc',
            'PKB (mld zł)', 'Bezrobocie (%)'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Korelacja dla wybranego roku
        selected_year = st.selectbox(
            "Wybierz rok:",
            sorted(df['rok'].unique(), reverse=True),
            key="corr_year"
        )
        
        fig_corr_year = st.session_state.visualizations.create_correlation_chart(
            df, 'pkb_mld_zl', 'bezrobocie_proc',
            'PKB (mld zł)', 'Bezrobocie (%)',
            year=selected_year
        )
        st.plotly_chart(fig_corr_year, use_container_width=True)
    
    # Macierz korelacji
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


def show_growth_analysis(df: pd.DataFrame):
    """Wyświetla analizę tempa wzrostu."""
    st.markdown("## 📈 Analiza tempa wzrostu")
    
    # Wybór województwa i metryki
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
    
    # Wykres tempa wzrostu
    fig_growth = st.session_state.visualizations.create_growth_chart(
        df, selected_metric, selected_voivodeship, selected_metric_label
    )
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Tabela z tempem wzrostu dla wszystkich województw
    st.markdown("### 📊 Tempo wzrostu - wszystkie województwa")
    
    growth_data = []
    for voivodeship in df['wojewodztwo'].unique():
        voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
        if len(voiv_data) > 1:
            # Oblicz średnie tempo wzrostu
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


if __name__ == "__main__":
    main()
