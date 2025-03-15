import json
import os

def get_movie_analysis_cells():
    return [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Disney Movie Analysis\n\n",
                "Analysis of Disney movie performance across various metrics.\n\n",
                "## Table of Contents\n",
                "1. [Setup and Data Loading](#Setup-and-Data-Loading)\n",
                "2. [Box Office Analysis](#Box-Office-Analysis)\n",
                "   - Revenue Distribution\n",
                "   - Budget vs Revenue\n",
                "   - ROI Analysis\n",
                "3. [Genre Analysis](#Genre-Analysis)\n",
                "   - Genre Distribution\n",
                "   - Genre Performance\n",
                "   - Genre Trends\n",
                "4. [Temporal Analysis](#Temporal-Analysis)\n",
                "   - Release Patterns\n",
                "   - Seasonal Performance\n",
                "   - Year-over-Year Growth\n",
                "5. [Audience Analysis](#Audience-Analysis)\n",
                "   - Rating Distribution\n",
                "   - Popularity Metrics\n",
                "   - Demographic Insights\n",
                "6. [Conclusions](#Conclusions)"
            ]
        }
    ]

def get_theme_park_cells():
    return [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Theme Park Analysis\n\n",
                "Analysis of Disney theme park operations and visitor patterns.\n\n",
                "## Table of Contents\n",
                "1. [Setup and Data Loading](#Setup-and-Data-Loading)\n",
                "2. [Wait Time Analysis](#Wait-Time-Analysis)\n",
                "   - Wait Time Distribution\n",
                "   - Peak Hours\n",
                "   - Attraction-specific Patterns\n",
                "3. [Crowd Analysis](#Crowd-Analysis)\n",
                "   - Daily Patterns\n",
                "   - Weekly Trends\n",
                "   - Seasonal Variations\n",
                "4. [Attraction Analysis](#Attraction-Analysis)\n",
                "   - Popular Attractions\n",
                "   - Capacity Utilization\n",
                "   - Maintenance Patterns\n",
                "5. [Guest Experience](#Guest-Experience)\n",
                "   - FASTPASS Usage\n",
                "   - Guest Flow\n",
                "   - Service Metrics\n",
                "6. [Conclusions](#Conclusions)"
            ]
        }
    ]

def get_streaming_cells():
    return [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Disney+ Streaming Analytics\n\n",
                "Analysis of Disney+ streaming platform performance and content engagement.\n\n",
                "## Table of Contents\n",
                "1. [Setup and Data Loading](#Setup-and-Data-Loading)\n",
                "2. [Content Analysis](#Content-Analysis)\n",
                "   - Content Distribution\n",
                "   - Release Strategy\n",
                "   - Content Lifecycle\n",
                "3. [Viewer Engagement](#Viewer-Engagement)\n",
                "   - Watch Time\n",
                "   - Completion Rates\n",
                "   - User Behavior\n",
                "4. [Platform Performance](#Platform-Performance)\n",
                "   - User Growth\n",
                "   - Retention Metrics\n",
                "   - Technical Performance\n",
                "5. [Content Strategy](#Content-Strategy)\n",
                "   - Popular Categories\n",
                "   - Recommendation Effectiveness\n",
                "   - Content Gaps\n",
                "6. [Conclusions](#Conclusions)"
            ]
        }
    ]

def get_industry_cells():
    return [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Entertainment Industry Analysis\n\n",
                "Analysis of the entertainment industry landscape and Disney's position.\n\n",
                "## Table of Contents\n",
                "1. [Setup and Data Loading](#Setup-and-Data-Loading)\n",
                "2. [Market Analysis](#Market-Analysis)\n",
                "   - Market Share\n",
                "   - Competition\n",
                "   - Industry Size\n",
                "3. [Financial Analysis](#Financial-Analysis)\n",
                "   - Revenue Trends\n",
                "   - Profitability\n",
                "   - Investment Patterns\n",
                "4. [Competitive Analysis](#Competitive-Analysis)\n",
                "   - Competitor Comparison\n",
                "   - Competitive Advantages\n",
                "   - Market Positioning\n",
                "5. [Future Outlook](#Future-Outlook)\n",
                "   - Growth Opportunities\n",
                "   - Industry Trends\n",
                "   - Risk Analysis\n",
                "6. [Conclusions](#Conclusions)"
            ]
        }
    ]

def get_franchise_cells():
    return [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Disney Franchise Analysis\n\n",
                "Analysis of Disney's major franchises and their performance.\n\n",
                "## Table of Contents\n",
                "1. [Setup and Data Loading](#Setup-and-Data-Loading)\n",
                "2. [Revenue Analysis](#Revenue-Analysis)\n",
                "   - Box Office Revenue\n",
                "   - Merchandise Sales\n",
                "   - Licensing Income\n",
                "3. [Cross-platform Performance](#Cross-platform-Performance)\n",
                "   - Movies\n",
                "   - Theme Parks\n",
                "   - Streaming\n",
                "4. [Audience Demographics](#Audience-Demographics)\n",
                "   - Age Distribution\n",
                "   - Geographic Reach\n",
                "   - Consumer Segments\n",
                "5. [Growth Analysis](#Growth-Analysis)\n",
                "   - Historical Growth\n",
                "   - Market Expansion\n",
                "   - Future Potential\n",
                "6. [Conclusions](#Conclusions)"
            ]
        }
    ]

def get_setup_cells():
    return [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Import required libraries\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from datetime import datetime\n",
                "\n",
                "# Set plotting style\n",
                "plt.style.use('seaborn')\n",
                "sns.set_palette('deep')\n",
                "%matplotlib inline\n",
                "\n",
                "# Configure display options\n",
                "pd.set_option('display.max_columns', None)\n",
                "pd.set_option('display.max_rows', 50)\n",
                "pd.set_option('display.float_format', lambda x: '%.2f' % x)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Helper functions for data processing\n",
                "def load_data(filepath):\n",
                "    \"\"\"Load and validate data from specified path.\"\"\"\n",
                "    try:\n",
                "        df = pd.read_parquet(filepath)\n",
                "        print(f'Successfully loaded data from {filepath}')\n",
                "        return df\n",
                "    except Exception as e:\n",
                "        print(f'Error loading data: {e}')\n",
                "        return None\n",
                "\n",
                "def format_currency(value):\n",
                "    \"\"\"Format numbers as currency.\"\"\"\n",
                "    return f'${value:,.2f}'\n",
                "\n",
                "def calculate_growth(series):\n",
                "    \"\"\"Calculate year-over-year growth rate.\"\"\"\n",
                "    return (series - series.shift(1)) / series.shift(1) * 100"
            ]
        }
    ]

def create_notebook(filepath, title, description, content_cells):
    """Create a Jupyter notebook with specific content cells."""
    notebook = {
        "cells": content_cells + get_setup_cells(),
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Write notebook to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

def main():
    # Define notebooks with their specific content cells
    notebooks = [
        {
            "path": "notebooks/disney_plus/analysis/movie_analysis.ipynb",
            "title": "Disney Movie Analysis",
            "description": "Analysis of Disney movie performance, including box office revenue, genres, and ratings.",
            "cells": get_movie_analysis_cells()
        },
        {
            "path": "notebooks/theme_parks/analysis/theme_park_analysis.ipynb",
            "title": "Theme Park Analysis",
            "description": "Analysis of Disney theme park operations, including wait times, crowd patterns, and attraction popularity.",
            "cells": get_theme_park_cells()
        },
        {
            "path": "notebooks/disney_plus/analysis/streaming_analytics.ipynb",
            "title": "Disney+ Streaming Analytics",
            "description": "Analysis of Disney+ streaming platform, including content performance and viewer engagement.",
            "cells": get_streaming_cells()
        },
        {
            "path": "notebooks/entertainment/analysis/industry_analysis.ipynb",
            "title": "Entertainment Industry Analysis",
            "description": "Analysis of the broader entertainment industry and Disney's market position.",
            "cells": get_industry_cells()
        },
        {
            "path": "notebooks/entertainment/analysis/franchise_analysis.ipynb",
            "title": "Disney Franchise Analysis",
            "description": "Analysis of Disney's major franchises across movies, merchandise, and theme parks.",
            "cells": get_franchise_cells()
        }
    ]
    
    for notebook in notebooks:
        create_notebook(
            notebook["path"],
            notebook["title"],
            notebook["description"],
            notebook["cells"]
        )
        print(f"Created notebook: {notebook['path']}")

if __name__ == "__main__":
    main() 