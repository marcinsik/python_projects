# Public Data Dashboard (Statistics Poland - GUS)

Interactive dashboard for analyzing public data from Statistics Poland (Główny Urząd Statystyczny).

## Features

- 📊 Interactive GDP and unemployment charts
- 🗺️ Filtering by voivodeships
- 📅 Time trend analysis
- 📈 Regional comparisons
- 🔄 Import custom data
- 🗺️ **Interactive Map of Poland** - choropleth visualization with value gradients
- 📊 **Comprehensive Socio-Economic Indicators** - demographics, industry, construction, education, labor market

## Technologies

The application is built using the following technologies:

### Backend & Data Analysis
- **Python** - main programming language
- **Pandas** - data manipulation and analysis
- **NumPy** - numerical computations

### Frontend & Visualizations
- **Streamlit** - framework for creating interactive web applications
- **Plotly** - library for creating interactive charts and visualizations

### Data Import/Export
- **OpenPyXL** - Excel file handling (.xlsx, .xls)
- **Requests** - HTTP communication (for future API integrations)

### Architecture
- **Modular structure** - separate modules for data loading and visualizations
- **Responsive design** - adapts to different screen sizes
- **Data caching** - performance optimization through Streamlit

## Installation

```bash
pip install -r requirements.txt
```

## Running

### Method 1: Direct execution
```bash
streamlit run app.py
```

### Method 2: Using script (recommended)
```bash
./run_app.sh
```

### Method 3: With activated virtual environment
```bash
source .venv/bin/activate
streamlit run app.py --server.port 8501
```

After launching, the application will be available at: **http://localhost:8501**

```
analytical_dashboard/
├── app.py                    # 🎯 Main application entry point (restructured)
├── main.py                   # 🚀 Application controller and orchestrator
├── config.py                 # ⚙️ Configuration settings and constants
├── session_manager.py        # 💾 Session state management
├── ui_components.py          # 🎨 UI component rendering functions
├── analysis_views.py         # 📊 Standard analysis view implementations
├── map_analysis_views.py     # 🗺️ Map-specific analysis views
├── indicators_view.py        # 📈 Comprehensive socio-economic indicators manager
├── data_loader.py            # 📁 Module for loading and processing data
├── visualizations.py         # 📊 Functions for creating Plotly charts
├── map_visualizations.py     # 🗺️ Interactive maps and choropleth visualizations
├── indicators/               # 📂 Indicators modules folder
│   ├── __init__.py           #     Package initialization
│   ├── demographics.py      # 👥 Demographics indicators and analysis
│   ├── industry.py          # 🏭 Industry indicators and analysis
│   ├── construction.py      # 🏠 Construction indicators and analysis
│   ├── education.py         # 🎓 Education indicators and analysis
│   └── labor_market.py      # 💼 Labor market indicators and analysis
├── data/                     # 📂 Data folder
│   └── sample_data.csv       #     Sample GUS data (GDP, unemployment)
├── .venv/                    # 🐍 Python virtual environment
├── requirements.txt          # 📦 Python dependencies list
├── run_app.sh               # 🚀 Script for easy application launch
└── README.md                # 📖 This file
```

### Module Description

#### Core Application Files

#### `main.py` - Application Controller
- **Main orchestrator**: Coordinates all application components
- **Routing logic**: Directs user selections to appropriate analysis views
- **Error handling**: Centralized error management and user feedback
- **Clean architecture**: Separates concerns and improves maintainability

#### `config.py` - Configuration Management
- **Settings centralization**: All configuration in one place
- **UI constants**: Color schemes, layout settings, analysis types
- **Page setup**: Streamlit configuration and CSS styling
- **Easy customization**: Modify behavior without touching core logic

#### `session_manager.py` - State Management
- **Session state**: Centralized session state management
- **Object initialization**: Manages DataLoader, Visualizations, and MapVisualizations
- **Data access**: Provides clean interface to session data
- **State persistence**: Maintains application state across interactions

#### `ui_components.py` - User Interface
- **Reusable components**: Modular UI element creation
- **Sidebar management**: Complete sidebar rendering and logic
- **Filter controls**: Dynamic filter generation and handling
- **Responsive design**: Components that adapt to different screen sizes

#### Analysis View Files

#### `analysis_views.py` - Standard Analysis Views
- **Core analyses**: Overview, GDP, unemployment, correlations, growth
- **Chart integration**: Uses visualization classes for consistent styling
- **Data presentation**: Clean data display with tables and metrics
- **Interactive elements**: User controls for customizing analysis views

#### `map_analysis_views.py` - Map Analysis Views
- **Interactive maps**: Specialized map visualization handling
- **Geographic data**: Polish voivodeship mapping and coordinates
- **Animation controls**: Time-series and animated visualizations
- **Map interactions**: Zoom, hover, selection functionality

#### Data and Visualization Files

#### `data_loader.py` - Data Management
- **DataLoader class**: Central data management
- **Data import**: CSV, Excel (.xlsx, .xls) support
- **Validation**: Data completeness and correctness checking
- **Transformations**: GDP per capita calculations, growth rate
- **Caching**: Performance optimization through Streamlit

#### `visualizations.py` - Charts and Visualizations
- **Visualizations class**: Ready-to-use chart creation functions
- **Chart types**: Line, bar, correlation, scatter plots
- **Plotly Integration**: Interactive charts with hover, zoom, pan
- **Styling**: Consistent design, color palette, responsiveness

#### `map_visualizations.py` - Interactive Maps
- **MapVisualizations class**: Ready-to-use map creation functions
- **Map types**: Scatter maps, choropleth maps, animated time series maps
- **Interactivity**: Hover details, zoom, pan, time animation
- **Polish geography**: Voivodeship boundaries and coordinates integration

#### Entry Point

#### `app.py` - Application Entry Point
- **Simple launcher**: Imports and runs the main application
- **Backward compatibility**: Maintains existing run commands
- **Clean interface**: Single point of entry for the entire application

## Sample Data

The application contains sample data from 2019-2022 for all 16 Polish voivodeships:

- **GDP** (billion PLN) - Gross Domestic Product by voivodeships
- **Unemployment** (%) - Registered unemployment rate
- **Population** (thousands) - Number of inhabitants (optional for GDP per capita)

## Extension Possibilities

### Planned Features
- 🌐 **GUS API Integration** - automatic downloading of latest data
-  **More indicators** - inflation, investments, export/import
- 🔄 **Real-time updates** - automatic data refresh
- 📊 **Custom dashboard** - layout configuration options
- 🗺️ **Enhanced mapping** - detailed GeoJSON boundaries and additional map styles

## Map Visualization Features

The application now includes interactive map visualizations of Poland:

### 🗺️ Available Map Types

1. **Scatter Map** - Shows voivodeships as circles sized and colored by the selected metric
2. **Animated Time Series Map** - Shows changes over time with play/pause controls

### 📍 Current Implementation

- **Coordinate-based mapping**: Uses approximate coordinates of voivodeship capitals
- **Interactive controls**: Select metrics (GDP, unemployment, population), years, and color scales
- **Detailed analytics**: Rankings, statistics, and trend analysis for each voivodeship
- **Responsive design**: Maps adapt to different screen sizes

### 🔧 Technical Notes

The current implementation uses scatter plots with coordinates for Polish voivodeship capitals. For production use with precise choropleth boundaries, you would need:

- Detailed GeoJSON files with Polish voivodeship boundaries
- Integration with services like Natural Earth Data or OpenStreetMap
- Custom geographic projection optimization for Poland

## Architecture Benefits

### 🏗️ **Modular Design**
The application has been restructured into smaller, focused modules that each handle specific responsibilities:

- **Separation of Concerns**: Each file has a single, clear purpose
- **Easier Maintenance**: Changes to one feature don't affect others
- **Better Testing**: Individual components can be tested independently
- **Code Reusability**: Components can be reused across different parts of the application

### 🔧 **Improved Structure**
- **Configuration Management**: All settings centralized in `config.py`
- **Session State**: Clean session management through `session_manager.py`
- **UI Components**: Reusable interface elements in `ui_components.py`
- **View Separation**: Analysis logic separated from UI rendering

### 📈 **Scalability**
- **Easy Extension**: New analysis types can be added without modifying existing code
- **Plugin Architecture**: New visualization types can be easily integrated
- **Performance**: Better caching and state management
- **Maintainability**: Clear code organization makes updates easier

### 🚀 **Development Benefits**
- **Faster Development**: Modular structure speeds up feature development
- **Debugging**: Easier to isolate and fix issues
- **Team Collaboration**: Multiple developers can work on different modules
- **Documentation**: Clear module purposes improve code understanding

## 📊 Socio-Economic Indicators

The application now includes comprehensive socio-economic indicators across five major categories:

### 👥 Demographics Indicators
- **Population Analysis**: Total population, density, migration patterns
- **Age Structure**: Population pyramids, aging index, dependency ratios
- **Migration Flows**: Migration balance, urbanization rates
- **Visualizations**: Population pyramids, migration flow maps, aging trends

### 🏭 Industry Indicators  
- **Production Metrics**: Industrial output, manufacturing, mining, energy
- **Trade Analysis**: Export/import values, trade balance, competitiveness
- **Investment Flows**: Foreign investment, productivity indices
- **Visualizations**: Production overviews, trade balance trends, productivity heatmaps

### 🏠 Construction Indicators
- **Building Activity**: Construction permits, dwellings completed/started
- **Real Estate Market**: Housing prices per m², market dynamics
- **Infrastructure**: Public construction, renovation permits
- **Visualizations**: Housing market overviews, price trends, construction activity maps

### 🎓 Education Indicators
- **Student Population**: Total students, public vs private institutions
- **Graduate Analysis**: Total graduates, STEM specializations
- **Academic Infrastructure**: Universities count, PhD students
- **Visualizations**: Education overviews, STEM analysis, academic center maps

### 💼 Labor Market Indicators
- **Employment Metrics**: Employment rate, unemployment rate, activity rate
- **Wage Analysis**: Average wages, wage growth, inequality analysis
- **Job Market Dynamics**: Job vacancies, job seekers, market pressure
- **Flexible Work**: Remote work, part-time, temporary employment
- **Visualizations**: Labor market overviews, wage trends, employment maps

### 📈 Analysis Features
- **Overview Mode**: Quick comparison across all indicator categories
- **Detailed Analysis**: In-depth exploration of specific categories
- **Interactive Visualizations**: Charts, maps, and trend analysis
- **Comparative Analysis**: Regional and temporal comparisons
- **Sample Data**: Realistic synthetic data for all Polish voivodeships (2019-2022)

