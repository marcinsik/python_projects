#!/usr/bin/env python3
"""
Test script for the map visualizations functionality.
"""

import pandas as pd
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from map_visualizations import MapVisualizations
    
    # Create sample data
    sample_data = {
        'rok': [2019, 2019, 2020, 2020, 2021, 2021],
        'wojewodztwo': ['Mazowieckie', 'Śląskie', 'Mazowieckie', 'Śląskie', 'Mazowieckie', 'Śląskie'],
        'pkb_mld_zl': [298.5, 158.2, 285.3, 148.7, 295.1, 152.3],
        'bezrobocie_proc': [3.8, 4.2, 4.5, 5.1, 4.1, 4.8],
        'ludnosc_tys': [5423, 4517, 5423, 4517, 5423, 4517]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Initialize map visualizations
    map_viz = MapVisualizations()
    
    print("✅ MapVisualizations imported successfully")
    print(f"✅ Sample data created: {len(df)} rows")
    print(f"✅ Available years: {sorted(df['rok'].unique())}")
    print(f"✅ Available voivodeships: {df['wojewodztwo'].unique().tolist()}")
    
    # Test scatter map creation
    fig1 = map_viz.create_scatter_map(df, 'pkb_mld_zl', 2020, 'Test PKB Map')
    print(f"✅ Scatter map created: {len(fig1.data)} traces")
    
    # Test animated scatter map creation
    fig2 = map_viz.create_animated_scatter_map(df, 'pkb_mld_zl', 'Test Animated PKB Map')
    print(f"✅ Animated scatter map created: {len(fig2.data)} traces")
    
    # Test animated bar chart creation
    fig3 = map_viz.create_animated_bar_chart_map(df, 'pkb_mld_zl', 'Test Animated Bar Chart')
    print(f"✅ Animated bar chart created: {len(fig3.data)} traces")
    
    print("\n🎉 All map visualization tests passed!")
    print("\nTeraz możesz uruchomić aplikację:")
    print("streamlit run app.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Sprawdź czy wszystkie wymagane pakiety są zainstalowane.")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
