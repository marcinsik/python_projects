"""
Education Indicators Module
Handles student numbers, graduates, and education statistics.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Optional


class EducationIndicators:
    """Class for education-related indicators and visualizations."""
    
    def __init__(self):
        """Initialize education indicators."""
        self.indicators = {
            'students_total': 'Studenci łącznie (tys.)',
            'students_public': 'Studenci uczelni publicznych (tys.)',
            'students_private': 'Studenci uczelni prywatnych (tys.)',
            'graduates_total': 'Absolwenci łącznie (tys.)',
            'graduates_stem': 'Absolwenci STEM (tys.)',
            'graduates_humanities': 'Absolwenci humanistyki (tys.)',
            'phd_students': 'Doktoranci (tys.)',
            'universities_count': 'Liczba uczelni',
            'education_spending': 'Wydatki na edukację (mln zł)',
            'student_teacher_ratio': 'Stosunek student/wykładowca'
        }
        
        self.study_fields = {
            'engineering': 'Inżynierskie',
            'business': 'Ekonomiczne',
            'medicine': 'Medyczne',
            'humanities': 'Humanistyczne',
            'science': 'Przyrodnicze',
            'social': 'Społeczne',
            'arts': 'Artystyczne',
            'agriculture': 'Rolnicze'
        }
        
        self.education_levels = {
            'bachelor': 'Licencjat',
            'master': 'Magister',
            'phd': 'Doktorat',
            'postgrad': 'Studia podyplomowe'
        }
    
    def get_sample_data(self) -> pd.DataFrame:
        """Generate sample education data for Polish voivodeships."""
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
                # Base student numbers (major academic centers)
                student_base = {
                    'Mazowieckie': 310.5, 'Małopolskie': 185.2, 'Śląskie': 128.8,
                    'Wielkopolskie': 115.4, 'Dolnośląskie': 98.1, 'Łódzkie': 89.7,
                    'Pomorskie': 78.2, 'Lubelskie': 65.1, 'Podkarpackie': 58.4,
                    'Kujawsko-Pomorskie': 52.8, 'Zachodniopomorskie': 48.2, 
                    'Warmińsko-Mazurskie': 42.8, 'Świętokrzyskie': 38.1,
                    'Podlaskie': 35.9, 'Lubuskie': 28.4, 'Opolskie': 25.8
                }
                
                # Demographic decline trend
                decline_factor = 0.98 ** (year - 2019)  # 2% annual decline
                base_students = student_base[voiv] * decline_factor
                
                import random
                random.seed(hash(f"{voiv}_{year}_education"))
                
                # University count based on voivodeship size
                uni_count = max(2, int(base_students / 15)) + random.randint(-1, 2)
                
                data.append({
                    'rok': year,
                    'wojewodztwo': voiv,
                    'students_total': round(base_students * (0.95 + random.random() * 0.1), 1),
                    'students_public': round(base_students * 0.65 * (0.95 + random.random() * 0.1), 1),
                    'students_private': round(base_students * 0.35 * (0.95 + random.random() * 0.1), 1),
                    'graduates_total': round(base_students * 0.22 * (0.9 + random.random() * 0.2), 1),
                    'graduates_stem': round(base_students * 0.08 * (0.9 + random.random() * 0.2), 1),
                    'graduates_humanities': round(base_students * 0.06 * (0.9 + random.random() * 0.2), 1),
                    'phd_students': round(base_students * 0.025 * (0.9 + random.random() * 0.2), 1),
                    'universities_count': uni_count,
                    'education_spending': round(base_students * 12 * (0.9 + random.random() * 0.2), 1),
                    'student_teacher_ratio': round(15 + random.random() * 10, 1)
                })
        
        return pd.DataFrame(data)
    
    def create_education_overview(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create education system overview."""
        try:
            year_data = df[df['rok'] == year]
            
            if year_data.empty:
                return go.Figure()
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Studenci łącznie (tys.)', 'Absolwenci (tys.)', 
                               'Doktoranci (tys.)', 'Liczba uczelni (szt.)'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Top voivodeships for each metric
            top_students = year_data.nlargest(8, 'students_total')
            top_graduates = year_data.nlargest(8, 'graduates_total')
            top_phd = year_data.nlargest(8, 'phd_students')
            top_unis = year_data.nlargest(8, 'universities_count')
            
            # Students
            fig.add_trace(
                go.Bar(x=top_students['wojewodztwo'], y=top_students['students_total'],
                       name='Studenci', marker_color='steelblue'),
                row=1, col=1
            )
            
            # Graduates
            fig.add_trace(
                go.Bar(x=top_graduates['wojewodztwo'], y=top_graduates['graduates_total'],
                       name='Absolwenci', marker_color='green'),
                row=1, col=2
            )
            
            # PhD students
            fig.add_trace(
                go.Bar(x=top_phd['wojewodztwo'], y=top_phd['phd_students'],
                       name='Doktoranci', marker_color='orange'),
                row=2, col=1
            )
            
            # Universities
            fig.add_trace(
                go.Bar(x=top_unis['wojewodztwo'], y=top_unis['universities_count'],
                       name='Uczelnie', marker_color='red'),
                row=2, col=2
            )
            
            fig.update_layout(
                title=f'System edukacji wyższej - przegląd ({year})',
                showlegend=False,
                height=600
            )
            
            # Update axis labels with units
            fig.update_yaxes(title_text="Liczba studentów (tys.)", row=1, col=1)
            fig.update_yaxes(title_text="Liczba absolwentów (tys.)", row=1, col=2)
            fig.update_yaxes(title_text="Liczba doktorantów (tys.)", row=2, col=1)
            fig.update_yaxes(title_text="Liczba uczelni (szt.)", row=2, col=2)
            
            fig.update_xaxes(tickangle=45)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating education overview: {str(e)}")
            return go.Figure()
    
    def create_student_trends(self, df: pd.DataFrame) -> go.Figure:
        """Create student population trends."""
        try:
            # National totals by year
            national_data = df.groupby('rok').agg({
                'students_total': 'sum',
                'students_public': 'sum',
                'students_private': 'sum',
                'graduates_total': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=national_data['rok'],
                y=national_data['students_total'],
                mode='lines+markers',
                name='Studenci łącznie',
                line=dict(color='blue', width=3),
                marker=dict(size=10)
            ))
            
            fig.add_trace(go.Scatter(
                x=national_data['rok'],
                y=national_data['students_public'],
                mode='lines+markers',
                name='Uczelnie publiczne',
                line=dict(color='green', width=2),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=national_data['rok'],
                y=national_data['students_private'],
                mode='lines+markers',
                name='Uczelnie prywatne',
                line=dict(color='red', width=2),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=national_data['rok'],
                y=national_data['graduates_total'],
                mode='lines+markers',
                name='Absolwenci',
                line=dict(color='orange', width=2),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title='Trendy w szkolnictwie wyższym - dane krajowe',
                xaxis_title='Rok',
                yaxis_title='Liczba osób (tys.)',
                hovermode='x unified',
                height=500
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating student trends: {str(e)}")
            return go.Figure()
    
    def create_stem_analysis(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create STEM education analysis."""
        try:
            year_data = df[df['rok'] == year]
            
            # Calculate STEM percentage
            year_data = year_data.copy()
            year_data['stem_percentage'] = (year_data['graduates_stem'] / year_data['graduates_total']) * 100
            
            fig = px.scatter(
                year_data,
                x='graduates_total',
                y='graduates_stem',
                size='students_total',
                color='stem_percentage',
                hover_name='wojewodztwo',
                title=f'Analiza absolwentów STEM ({year})',
                labels={
                    'graduates_total': 'Absolwenci łącznie (tys.)',
                    'graduates_stem': 'Absolwenci STEM (tys.)',
                    'stem_percentage': 'Udział STEM (%)'
                },
                color_continuous_scale='Viridis'
            )
            
            fig.update_layout(height=500)
            return fig
            
        except Exception as e:
            st.error(f"Error creating STEM analysis: {str(e)}")
            return go.Figure()
    
    def create_education_efficiency(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create education efficiency analysis."""
        try:
            year_data = df[df['rok'] == year].copy()
            
            # Calculate efficiency metrics
            year_data['graduation_rate'] = (year_data['graduates_total'] / year_data['students_total']) * 100
            year_data['spending_per_student'] = year_data['education_spending'] / year_data['students_total']
            
            fig = px.scatter(
                year_data,
                x='student_teacher_ratio',
                y='graduation_rate',
                size='spending_per_student',
                color='universities_count',
                hover_name='wojewodztwo',
                title=f'Efektywność systemu edukacji ({year})',
                labels={
                    'student_teacher_ratio': 'Stosunek student/wykładowca',
                    'graduation_rate': 'Wskaźnik ukończenia (%)',
                    'spending_per_student': 'Wydatki na studenta (tys. zł)',
                    'universities_count': 'Liczba uczelni (szt.)'
                }
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating education efficiency: {str(e)}")
            return go.Figure()
    
    def create_field_distribution(self, voivodeship: str) -> go.Figure:
        """Create study field distribution for a voivodeship."""
        try:
            # Sample field distribution (in practice, this would come from real data)
            import random
            random.seed(hash(voivodeship))
            
            fields_data = {}
            for field_key, field_name in self.study_fields.items():
                fields_data[field_name] = random.randint(8, 25)
            
            fig = px.pie(
                values=list(fields_data.values()),
                names=list(fields_data.keys()),
                title=f'Rozkład kierunków studiów - {voivodeship} (% studentów)'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating field distribution: {str(e)}")
            return go.Figure()
    
    def create_academic_centers_map(self, df: pd.DataFrame, year: int) -> go.Figure:
        """Create academic centers map."""
        try:
            from map_visualizations import MapVisualizations
            
            map_viz = MapVisualizations()
            
            fig = map_viz.create_scatter_map(
                df=df,
                metric='students_total',
                year=year,
                title=f'Ośrodki akademickie - liczba studentów ({year})'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating academic centers map: {str(e)}")
            return go.Figure()
    
    def get_education_summary(self, df: pd.DataFrame, voivodeship: str, year: int) -> Dict:
        """Get education summary for a voivodeship."""
        try:
            data = df[(df['wojewodztwo'] == voivodeship) & (df['rok'] == year)]
            
            if data.empty:
                return {}
            
            row = data.iloc[0]
            
            # Calculate derived metrics
            graduation_rate = (row['graduates_total'] / row['students_total']) * 100
            public_share = (row['students_public'] / row['students_total']) * 100
            stem_share = (row['graduates_stem'] / row['graduates_total']) * 100
            
            return {
                'voivodeship': voivodeship,
                'year': year,
                'students_total': row['students_total'],
                'graduates_total': row['graduates_total'],
                'universities_count': row['universities_count'],
                'graduation_rate': graduation_rate,
                'public_share': public_share,
                'stem_share': stem_share,
                'phd_students': row['phd_students'],
                'education_spending': row['education_spending'],
                'spending_per_student': row['education_spending'] / row['students_total'],
                'student_teacher_ratio': row['student_teacher_ratio']
            }
            
        except Exception as e:
            st.error(f"Error getting education summary: {str(e)}")
            return {}
    
    def analyze_education_competitiveness(self, df: pd.DataFrame, voivodeship: str) -> Dict:
        """Analyze education competitiveness indicators."""
        try:
            voiv_data = df[df['wojewodztwo'] == voivodeship].sort_values('rok')
            
            if len(voiv_data) < 2:
                return {}
            
            latest = voiv_data.iloc[-1]
            first = voiv_data.iloc[0]
            
            # Calculate trends
            student_growth = ((latest['students_total'] - first['students_total']) / first['students_total']) * 100
            stem_growth = ((latest['graduates_stem'] - first['graduates_stem']) / first['graduates_stem']) * 100
            efficiency_trend = (latest['graduation_rate'] - first['graduation_rate']) if 'graduation_rate' in latest else 0
            
            # Ranking against other voivodeships
            latest_year_data = df[df['rok'] == latest['rok']]
            student_rank = (latest_year_data['students_total'] > latest['students_total']).sum() + 1
            stem_rank = (latest_year_data['graduates_stem'] > latest['graduates_stem']).sum() + 1
            
            return {
                'student_growth_total': student_growth,
                'stem_growth_total': stem_growth,
                'efficiency_trend': efficiency_trend,
                'student_rank_national': student_rank,
                'stem_rank_national': stem_rank,
                'academic_strength': 'high' if student_rank <= 5 and stem_rank <= 5 else 'moderate'
            }
            
        except Exception as e:
            st.error(f"Error analyzing education competitiveness: {str(e)}")
            return {}
