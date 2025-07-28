"""
Indicators View Module
Main interface for all indicator categories in the dashboard.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Optional

from indicators.demographics import DemographicsIndicators
from indicators.industry import IndustryIndicators
from indicators.construction import ConstructionIndicators
from indicators.education import EducationIndicators
from indicators.labor_market import LaborMarketIndicators


class IndicatorsManager:
    """Manager class for all indicator categories."""
    
    def __init__(self):
        """Initialize all indicator classes."""
        self.demographics = DemographicsIndicators()
        self.industry = IndustryIndicators()
        self.construction = ConstructionIndicators()
        self.education = EducationIndicators()
        self.labor_market = LaborMarketIndicators()
        
        self.categories = {
            'demographics': {
                'name': '👥 Demografia',
                'description': 'Populacja, migracje, struktura wiekowa',
                'class': self.demographics
            },
            'industry': {
                'name': '🏭 Przemysł',
                'description': 'Produkcja przemysłowa, eksport/import',
                'class': self.industry
            },
            'construction': {
                'name': '🏠 Budownictwo',
                'description': 'Pozwolenia na budowę, ceny nieruchomości',
                'class': self.construction
            },
            'education': {
                'name': '🎓 Edukacja',
                'description': 'Liczba studentów, absolwentów',
                'class': self.education
            },
            'labor_market': {
                'name': '💼 Rynek pracy',
                'description': 'Aktywność zawodowa, płace średnie',
                'class': self.labor_market
            }
        }
    
    def get_combined_sample_data(self) -> Dict[str, pd.DataFrame]:
        """Get sample data for all indicator categories."""
        try:
            data = {}
            
            with st.spinner("Generowanie danych przykładowych..."):
                data['demographics'] = self.demographics.get_sample_data()
                data['industry'] = self.industry.get_sample_data()
                data['construction'] = self.construction.get_sample_data()
                data['education'] = self.education.get_sample_data()
                data['labor_market'] = self.labor_market.get_sample_data()
            
            return data
            
        except Exception as e:
            st.error(f"Błąd podczas generowania danych: {str(e)}")
            return {}
    
    def show_indicators_overview(self, year: int = 2022):
        """Show overview of all indicator categories."""
        st.markdown("## 📊 Przegląd wszystkich wskaźników")
        
        # Get sample data for all categories
        all_data = self.get_combined_sample_data()
        
        if not all_data:
            st.warning("Nie udało się wczytać danych wskaźników.")
            return
        
        # Create tabs for each category
        tab_names = [cat['name'] for cat in self.categories.values()]
        tabs = st.tabs(tab_names)
        
        for i, (cat_key, cat_info) in enumerate(self.categories.items()):
            with tabs[i]:
                self._show_category_overview(cat_key, cat_info, all_data.get(cat_key), year)
    
    def _show_category_overview(self, category_key: str, category_info: Dict, data: pd.DataFrame, year: int):
        """Show overview for a specific category."""
        if data is None or data.empty:
            st.warning(f"Brak danych dla kategorii {category_info['name']}")
            return
        
        st.markdown(f"### {category_info['name']}")
        st.markdown(f"*{category_info['description']}*")
        
        # Show basic statistics
        year_data = data[data['rok'] == year] if 'rok' in data.columns else data
        
        if year_data.empty:
            st.warning(f"Brak danych dla roku {year}")
            return
        
        # Create overview based on category
        if category_key == 'demographics':
            self._show_demographics_overview(year_data, year)
        elif category_key == 'industry':
            self._show_industry_overview(year_data, year)
        elif category_key == 'construction':
            self._show_construction_overview(year_data, year)
        elif category_key == 'education':
            self._show_education_overview(year_data, year)
        elif category_key == 'labor_market':
            self._show_labor_market_overview(year_data, year)
    
    def _show_demographics_overview(self, data: pd.DataFrame, year: int):
        """Show demographics overview."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pop = data['population_total'].sum()
            st.metric("Populacja całkowita", f"{total_pop:.1f} mln")
        
        with col2:
            avg_birth_rate = data['birth_rate'].mean()
            st.metric("Średnia urodzeń", f"{avg_birth_rate:.1f}‰")
        
        with col3:
            avg_aging = (data['age_65_plus'] / data['age_0_14']).mean() * 100
            st.metric("Indeks starzenia", f"{avg_aging:.0f}")
        
        with col4:
            migration_balance = data['migration_balance'].sum()
            st.metric("Saldo migracji", f"{migration_balance:.1f} tys.")
        
        # Show population pyramid for largest voivodeship
        largest_voiv = data.loc[data['population_total'].idxmax(), 'wojewodztwo']
        fig = self.demographics.create_population_pyramid(data, largest_voiv, year)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_industry_overview(self, data: pd.DataFrame, year: int):
        """Show industry overview."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_production = data['industrial_production'].sum()
            st.metric("Produkcja przemysłowa", f"{total_production:.1f} mld zł")
        
        with col2:
            total_export = data['export_value'].sum()
            st.metric("Eksport", f"{total_export:.1f} mld EUR")
        
        with col3:
            total_import = data['import_value'].sum()
            st.metric("Import", f"{total_import:.1f} mld EUR")
        
        with col4:
            trade_balance = data['trade_balance'].sum()
            st.metric("Bilans handlowy", f"{trade_balance:.1f} mld EUR")
        
        # Show production overview
        fig = self.industry.create_production_overview(data, year)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_construction_overview(self, data: pd.DataFrame, year: int):
        """Show construction overview."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_permits = data['building_permits'].sum()
            st.metric("Pozwolenia na budowę", f"{total_permits:,.0f}")
        
        with col2:
            avg_price = data['housing_price_m2'].mean()
            st.metric("Średnia cena m²", f"{avg_price:.0f} zł")
        
        with col3:
            completed_dwellings = data['dwellings_completed'].sum()
            st.metric("Mieszkania oddane", f"{completed_dwellings:,.0f}")
        
        with col4:
            total_investment = data['infrastructure_investment'].sum()
            st.metric("Inwestycje infrastr.", f"{total_investment:.1f} mln zł")
        
        # Show housing market overview
        fig = self.construction.create_housing_market_overview(data, year)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_education_overview(self, data: pd.DataFrame, year: int):
        """Show education overview."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_students = data['students_total'].sum()
            st.metric("Studenci łącznie", f"{total_students:.1f} tys.")
        
        with col2:
            total_graduates = data['graduates_total'].sum()
            st.metric("Absolwenci", f"{total_graduates:.1f} tys.")
        
        with col3:
            stem_share = (data['graduates_stem'].sum() / data['graduates_total'].sum()) * 100
            st.metric("Udział STEM", f"{stem_share:.1f}%")
        
        with col4:
            total_universities = data['universities_count'].sum()
            st.metric("Liczba uczelni", f"{total_universities:.0f}")
        
        # Show education overview
        fig = self.education.create_education_overview(data, year)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_labor_market_overview(self, data: pd.DataFrame, year: int):
        """Show labor market overview."""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_employment = data['employment_rate'].mean()
            st.metric("Średnie zatrudnienie", f"{avg_employment:.1f}%")
        
        with col2:
            avg_unemployment = data['unemployment_rate'].mean()
            st.metric("Średnie bezrobocie", f"{avg_unemployment:.1f}%")
        
        with col3:
            avg_wage = data['avg_wage'].mean()
            st.metric("Średnia płaca", f"{avg_wage:.0f} zł")
        
        with col4:
            total_vacancies = data['job_vacancies'].sum()
            st.metric("Wolne miejsca", f"{total_vacancies:.1f} tys.")
        
        # Show labor market overview
        fig = self.labor_market.create_labor_market_overview(data, year)
        if fig.data:
            st.plotly_chart(fig, use_container_width=True)
    
    def show_detailed_analysis(self, category: str, data: Dict[str, pd.DataFrame]):
        """Show detailed analysis for a specific category."""
        if category not in self.categories:
            st.error(f"Nieznana kategoria: {category}")
            return
        
        cat_info = self.categories[category]
        cat_data = data.get(category)
        
        if cat_data is None or cat_data.empty:
            st.warning(f"Brak danych dla kategorii {cat_info['name']}")
            return
        
        st.markdown(f"## {cat_info['name']} - Analiza szczegółowa")
        
        # Control panel
        col1, col2 = st.columns(2)
        
        with col1:
            available_years = sorted(cat_data['rok'].unique()) if 'rok' in cat_data.columns else [2022]
            selected_year = st.selectbox("Wybierz rok:", available_years, 
                                       index=len(available_years)-1)
        
        with col2:
            analysis_types = self._get_analysis_types(category)
            selected_analysis = st.selectbox("Typ analizy:", analysis_types)
        
        # Voivodeship selection section
        st.markdown("### 🗺️ Wybór województw")
        available_voivodeships = sorted(cat_data['wojewodztwo'].unique()) if 'wojewodztwo' in cat_data.columns else []
        
        col_select1, col_select2 = st.columns(2)
        
        with col_select1:
            select_all = st.checkbox("Wszystkie województwa", value=True)
            if select_all:
                selected_voivodeships = available_voivodeships
            else:
                selected_voivodeships = st.multiselect(
                    "Wybierz województwa:",
                    available_voivodeships,
                    default=available_voivodeships[:5] if len(available_voivodeships) > 5 else available_voivodeships
                )
        
        with col_select2:
            # Quick selection buttons
            st.markdown("**Szybki wybór:**")
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🏙️ Największe"):
                    # Select top 5 most populous voivodeships
                    top_voivodeships = ['Mazowieckie', 'Śląskie', 'Wielkopolskie', 'Małopolskie', 'Dolnośląskie']
                    selected_voivodeships = [v for v in top_voivodeships if v in available_voivodeships]
                    select_all = False
            
            with col_btn2:
                if st.button("🌊 Nadmorskie"):
                    # Select coastal voivodeships
                    coastal_voivodeships = ['Pomorskie', 'Zachodniopomorskie', 'Warmińsko-Mazurskie']
                    selected_voivodeships = [v for v in coastal_voivodeships if v in available_voivodeships]
                    select_all = False
        
        if not selected_voivodeships:
            st.warning("Wybierz przynajmniej jedno województwo.")
            return
        
        # Show analysis based on selection
        self._show_category_analysis(category, cat_data, selected_year, 
                                   selected_voivodeships, selected_analysis)
    
    def _get_analysis_types(self, category: str) -> List[str]:
        """Get available analysis types for a category."""
        analysis_map = {
            'demographics': [
                'Piramida wieku', 'Trendy migracyjne', 'Indeks starzenia', 
                'Mapa urbanizacji', 'Analiza trendów'
            ],
            'industry': [
                'Przegląd produkcji', 'Bilans handlowy', 'Mapa produktywności',
                'Analiza sektorów', 'Przepływ inwestycji'
            ],
            'construction': [
                'Rynek mieszkaniowy', 'Trendy cen', 'Mapa aktywności',
                'Analiza podaży-popytu', 'Struktura budownictwa'
            ],
            'education': [
                'Przegląd edukacji', 'Trendy studentów', 'Analiza STEM',
                'Efektywność edukacji', 'Mapa ośrodków akademickich'
            ],
            'labor_market': [
                'Przegląd rynku pracy', 'Trendy zatrudnienia', 'Nierówności płacowe',
                'Dynamika rynku', 'Elastyczne formy pracy'
            ]
        }
        return analysis_map.get(category, ['Analiza podstawowa'])
    
    def _show_category_analysis(self, category: str, data: pd.DataFrame, year: int, 
                               selected_voivodeships: List[str], analysis_type: str):
        """Show specific analysis for a category."""
        # Filter data by selected voivodeships
        if selected_voivodeships and len(selected_voivodeships) < len(data['wojewodztwo'].unique()):
            data = data[data['wojewodztwo'].isin(selected_voivodeships)]
        
        # Show number of selected voivodeships
        st.info(f"📊 Analiza dla {len(selected_voivodeships)} województw: {', '.join(selected_voivodeships)}")
        
        try:
            if category == 'demographics':
                self._show_demographics_analysis(data, year, selected_voivodeships, analysis_type)
            elif category == 'industry':
                self._show_industry_analysis(data, year, selected_voivodeships, analysis_type)
            elif category == 'construction':
                self._show_construction_analysis(data, year, selected_voivodeships, analysis_type)
            elif category == 'education':
                self._show_education_analysis(data, year, selected_voivodeships, analysis_type)
            elif category == 'labor_market':
                self._show_labor_market_analysis(data, year, selected_voivodeships, analysis_type)
                
        except Exception as e:
            st.error(f"Błąd podczas tworzenia analizy: {str(e)}")
    
    def _show_demographics_analysis(self, data: pd.DataFrame, year: int, selected_voivodeships: List[str], analysis_type: str):
        """Show demographics analysis."""
        if analysis_type == 'Piramida wieku' and len(selected_voivodeships) == 1:
            fig = self.demographics.create_population_pyramid(data, selected_voivodeships[0], year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Piramida wieku' and len(selected_voivodeships) > 1:
            st.warning("Piramida wieku jest dostępna tylko dla jednego województwa. Wybierz jedno województwo.")
        elif analysis_type == 'Trendy migracyjne':
            fig = self.demographics.create_migration_flow(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Indeks starzenia':
            fig = self.demographics.create_aging_index(data)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Mapa urbanizacji':
            fig = self.demographics.create_urbanization_map(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Analiza trendów':
            fig = self.demographics.create_population_trends(data, selected_voivodeships)
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_industry_analysis(self, data: pd.DataFrame, year: int, selected_voivodeships: List[str], analysis_type: str):
        """Show industry analysis.""" 
        if analysis_type == 'Przegląd produkcji':
            fig = self.industry.create_production_overview(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Bilans handlowy':
            fig = self.industry.create_trade_balance_analysis(data)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Mapa produktywności':
            fig = self.industry.create_productivity_heatmap(data)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Analiza sektorów':
            fig = self.industry.create_sector_comparison(data, selected_voivodeships, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Przepływ inwestycji':
            fig = self.industry.create_investment_trends(data, selected_voivodeships)
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_construction_analysis(self, data: pd.DataFrame, year: int, selected_voivodeships: List[str], analysis_type: str):
        """Show construction analysis."""
        if analysis_type == 'Rynek mieszkaniowy':
            fig = self.construction.create_housing_market_overview(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Trendy cen':
            fig = self.construction.create_price_trends(data, selected_voivodeships)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Mapa aktywności':
            fig = self.construction.create_construction_activity_map(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Analiza podaży-popytu' and len(selected_voivodeships) == 1:
            fig = self.construction.create_supply_demand_analysis(data, selected_voivodeships[0])
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Analiza podaży-popytu' and len(selected_voivodeships) > 1:
            st.warning("Analiza podaży-popytu jest dostępna tylko dla jednego województwa.")
        elif analysis_type == 'Struktura budownictwa':
            fig = self.construction.create_building_types_breakdown(data, year)
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_education_analysis(self, data: pd.DataFrame, year: int, selected_voivodeships: List[str], analysis_type: str):
        """Show education analysis."""
        if analysis_type == 'Przegląd edukacji':
            fig = self.education.create_education_overview(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Trendy studentów':
            fig = self.education.create_student_trends(data, selected_voivodeships)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Analiza STEM':
            fig = self.education.create_stem_analysis(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Efektywność edukacji':
            fig = self.education.create_education_efficiency(data, selected_voivodeships, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Mapa ośrodków akademickich':
            fig = self.education.create_academic_centers_map(data, year)
            st.plotly_chart(fig, use_container_width=True)
    
    def _show_labor_market_analysis(self, data: pd.DataFrame, year: int, selected_voivodeships: List[str], analysis_type: str):
        """Show labor market analysis."""
        if analysis_type == 'Przegląd rynku pracy':
            fig = self.labor_market.create_labor_market_overview(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Trendy zatrudnienia':
            fig = self.labor_market.create_employment_trends(data, selected_voivodeships)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Nierówności płacowe':
            fig = self.labor_market.create_wage_inequality_analysis(data, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Dynamika rynku':
            fig = self.labor_market.create_market_dynamics(data, selected_voivodeships, year)
            st.plotly_chart(fig, use_container_width=True)
        elif analysis_type == 'Elastyczne formy pracy':
            fig = self.labor_market.create_flexible_work_analysis(data, selected_voivodeships, year)
            st.plotly_chart(fig, use_container_width=True)
