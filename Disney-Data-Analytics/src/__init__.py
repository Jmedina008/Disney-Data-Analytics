"""
Disney Data Analytics - A comprehensive data science portfolio
showcasing Disney entertainment analytics across movies, streaming, and theme parks.

Author: Josh Medina
"""

__version__ = "1.0.0"
__author__ = "Josh Medina"
__email__ = "your.email@example.com"

# Package imports
from . import data_collection
from . import data_processing  
from . import analysis
from . import models
from . import visualization
from . import utils

__all__ = [
    'data_collection',
    'data_processing', 
    'analysis',
    'models',
    'visualization',
    'utils'
]