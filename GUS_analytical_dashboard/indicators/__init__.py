"""
Indicators package for GUS Analytical Dashboard
Contains modules for different economic and social indicators.
"""

from .demographics import DemographicsIndicators
from .industry import IndustryIndicators  
from .construction import ConstructionIndicators
from .education import EducationIndicators
from .labor_market import LaborMarketIndicators

__all__ = [
    'DemographicsIndicators',
    'IndustryIndicators', 
    'ConstructionIndicators',
    'EducationIndicators',
    'LaborMarketIndicators'
]
