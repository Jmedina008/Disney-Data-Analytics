#!/usr/bin/env python
# coding: utf-8

# # Disney Movie Analysis
# 
# Analysis of Disney movie performance across various metrics.
# 
# ## Table of Contents
# 1. [Setup and Data Loading](#Setup-and-Data-Loading)
# 2. [Box Office Analysis](#Box-Office-Analysis)
#    - Revenue Distribution
#    - Budget vs Revenue
#    - ROI Analysis
# 3. [Genre Analysis](#Genre-Analysis)
#    - Genre Distribution
#    - Genre Performance
#    - Genre Trends
# 4. [Temporal Analysis](#Temporal-Analysis)
#    - Release Patterns
#    - Seasonal Performance
#    - Year-over-Year Growth
# 5. [Audience Analysis](#Audience-Analysis)
#    - Rating Distribution
#    - Popularity Metrics
#    - Demographic Insights
# 6. [Statistical Tests](#Statistical-Tests)
#    - Hypothesis Testing
#    - Regression Analysis
#    - Time Series Analysis
# 7. [Conclusions](#Conclusions)

# ## Setup and Data Loading

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
import os

# Import statistical libraries
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Set plotting style
plt.style.use('seaborn')
sns.set_palette('deep')

# Configure display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 50)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# Helper functions
def load_data(filepath):
    """Load and validate data from specified path."""
    try:
        df = pd.read_parquet(filepath)
        print(f'Successfully loaded data from {filepath}')
        return df
    except Exception as e:
        print(f'Error loading data: {e}')
        return None

def format_currency(value):
    """Format numbers as currency."""
    return f'${value:,.2f}' if pd.notnull(value) else 'N/A'

def calculate_growth(series):
    """Calculate year-over-year growth rate."""
    return (series - series.shift(1)) / series.shift(1) * 100

# Load processed movie data
movies_df = load_data('../../../data/processed/disney_plus/disney_movies_processed_20250309.parquet')

# Load box office data
with open('../../../data/raw/box_office/box_office_data_20250309_231818.json', 'r') as f:
    box_office_df = pd.DataFrame(json.load(f))

# Merge datasets
df = pd.merge(movies_df, box_office_df, on='id', how='left')

# Display basic information about the dataset
print("Dataset Overview:")
print(f"Number of movies: {len(df)}")
print("\nMissing values:")
print(df.isnull().sum())

# Display first few rows
print(df.head())

# ## Box Office Analysis

# Calculate basic financial statistics
financial_stats = pd.DataFrame({
    'Budget': [df['budget'].min(), df['budget'].median(), df['budget'].mean(), df['budget'].max()],
    'Revenue': [df['revenue'].min(), df['revenue'].median(), df['revenue'].mean(), df['revenue'].max()]
}, index=['Min', 'Median', 'Mean', 'Max'])

print("Financial Statistics (in USD):")
print(financial_stats.applymap(format_currency))

# Create revenue distribution plot
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='revenue', bins=30)
plt.title('Distribution of Movie Revenue')
plt.xlabel('Revenue (USD)')
plt.ylabel('Count')
plt.ticklabel_format(style='plain', axis='x')
plt.xticks(rotation=45)
plt.savefig('../../../reports/figures/revenue_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate and display top 10 highest-grossing movies
top_10_revenue = df.nlargest(10, 'revenue')[['title', 'release_date', 'revenue', 'budget']]
print("\nTop 10 Highest-Grossing Disney Movies:")
print(top_10_revenue.to_string(index=False))

# Create budget vs revenue scatter plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='budget', y='revenue', alpha=0.6)
plt.title('Budget vs Revenue Relationship')
plt.xlabel('Budget (USD)')
plt.ylabel('Revenue (USD)')

# Add diagonal line representing break-even point
max_val = max(df['budget'].max(), df['revenue'].max())
plt.plot([0, max_val], [0, max_val], 'r--', label='Break-even line')
plt.legend()

# Add annotations for notable outliers
for idx, row in df.nlargest(3, 'revenue').iterrows():
    plt.annotate(row['title'], 
                 (row['budget'], row['revenue']),
                 xytext=(10, 10), 
                 textcoords='offset points')

plt.ticklabel_format(style='plain')
plt.tight_layout()
plt.savefig('../../../reports/figures/budget_vs_revenue.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate and analyze ROI
df['roi'] = (df['revenue'] - df['budget']) / df['budget'] * 100

# Create ROI distribution plot
plt.figure(figsize=(12, 6))
sns.boxplot(y=df['roi'])
plt.title('Return on Investment (ROI) Distribution')
plt.ylabel('ROI (%)')
plt.savefig('../../../reports/figures/roi_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Display top 10 movies by ROI
top_10_roi = df.nlargest(10, 'roi')[['title', 'release_date', 'budget', 'revenue', 'roi']]
print("\nTop 10 Movies by ROI:")
print(top_10_roi.to_string(index=False))

# ## Genre Analysis

# Extract genres from the genre_ids column
def extract_genres(row):
    """Extract genre names from genre_ids."""
    if pd.isna(row['genre_ids']):
        return []
    
    genres = []
    for genre_id in row['genre_ids']:
        if pd.notnull(genre_id):
            genres.append(str(genre_id))
    return genres

# Apply the function to create a list of genres for each movie
df['genres_list'] = df.apply(extract_genres, axis=1)

# Create a new dataframe with one row per movie-genre combination
genre_df = df.explode('genres_list')

# Count the number of movies in each genre
genre_counts = genre_df['genres_list'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Create a bar chart of genre distribution
plt.figure(figsize=(14, 8))
sns.barplot(data=genre_counts.head(15), x='genre', y='count')
plt.title('Distribution of Disney Movies by Genre')
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('../../../reports/figures/genre_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate average revenue by genre
genre_performance = genre_df.groupby('genres_list').agg({
    'revenue': 'mean',
    'budget': 'mean',
    'roi': 'mean',
    'id': 'count'
}).reset_index()
genre_performance.columns = ['genre', 'avg_revenue', 'avg_budget', 'avg_roi', 'movie_count']
genre_performance = genre_performance.sort_values('avg_revenue', ascending=False)

# Create a bar chart of average revenue by genre
plt.figure(figsize=(14, 8))
sns.barplot(data=genre_performance.head(10), x='genre', y='avg_revenue')
plt.title('Average Revenue by Genre')
plt.xlabel('Genre')
plt.ylabel('Average Revenue (USD)')
plt.xticks(rotation=45, ha='right')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('../../../reports/figures/genre_revenue.png', dpi=300, bbox_inches='tight')
plt.show()

# Create a bar chart of average ROI by genre
plt.figure(figsize=(14, 8))
sns.barplot(data=genre_performance.head(10), x='genre', y='avg_roi')
plt.title('Average ROI by Genre')
plt.xlabel('Genre')
plt.ylabel('Average ROI (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('../../../reports/figures/genre_roi.png', dpi=300, bbox_inches='tight')
plt.show()

# Analyze genre trends over time
df['release_year'] = pd.to_datetime(df['release_date']).dt.year

# Create a pivot table of genre counts by year
genre_trends = genre_df.groupby(['release_year', 'genres_list']).size().reset_index()
genre_trends.columns = ['year', 'genre', 'count']

# Filter for the top 5 genres
top_genres = genre_counts.head(5)['genre'].tolist()
genre_trends_filtered = genre_trends[genre_trends['genre'].isin(top_genres)]

# Create a line chart of genre trends
plt.figure(figsize=(14, 8))
sns.lineplot(data=genre_trends_filtered, x='year', y='count', hue='genre')
plt.title('Genre Trends Over Time')
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.legend(title='Genre')
plt.tight_layout()
plt.savefig('../../../reports/figures/genre_trends.png', dpi=300, bbox_inches='tight')
plt.show()

# ## Temporal Analysis

# Convert release_date to datetime
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_year'] = df['release_date'].dt.year
df['release_month'] = df['release_date'].dt.month
df['release_quarter'] = df['release_date'].dt.quarter

# Create a line chart of movie releases by year
yearly_releases = df.groupby('release_year').size().reset_index()
yearly_releases.columns = ['year', 'count']

plt.figure(figsize=(14, 8))
sns.lineplot(data=yearly_releases, x='year', y='count')
plt.title('Number of Disney Movie Releases by Year')
plt.xlabel('Release Year')
plt.ylabel('Number of Movies')
plt.tight_layout()
plt.savefig('../../../reports/figures/yearly_releases.png', dpi=300, bbox_inches='tight')
plt.show()

# Create a bar chart of movie releases by month
monthly_releases = df.groupby('release_month').size().reset_index()
monthly_releases.columns = ['month', 'count']

plt.figure(figsize=(14, 8))
sns.barplot(data=monthly_releases, x='month', y='count')
plt.title('Number of Disney Movie Releases by Month')
plt.xlabel('Release Month')
plt.ylabel('Number of Movies')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.savefig('../../../reports/figures/monthly_releases.png', dpi=300, bbox_inches='tight')
plt.show()

# Analyze seasonal performance
seasonal_performance = df.groupby('release_quarter').agg({
    'revenue': 'mean',
    'budget': 'mean',
    'roi': 'mean',
    'id': 'count'
}).reset_index()
seasonal_performance.columns = ['quarter', 'avg_revenue', 'avg_budget', 'avg_roi', 'movie_count']

plt.figure(figsize=(14, 8))
sns.barplot(data=seasonal_performance, x='quarter', y='avg_revenue')
plt.title('Average Revenue by Release Quarter')
plt.xlabel('Release Quarter')
plt.ylabel('Average Revenue (USD)')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('../../../reports/figures/quarterly_revenue.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate year-over-year growth in revenue
yearly_revenue = df.groupby('release_year')['revenue'].sum().reset_index()
yearly_revenue['yoy_growth'] = calculate_growth(yearly_revenue['revenue'])

plt.figure(figsize=(14, 8))
sns.lineplot(data=yearly_revenue, x='release_year', y='yoy_growth')
plt.title('Year-over-Year Growth in Disney Movie Revenue')
plt.xlabel('Release Year')
plt.ylabel('YoY Growth (%)')
plt.axhline(y=0, color='r', linestyle='--')
plt.tight_layout()
plt.savefig('../../../reports/figures/yoy_growth.png', dpi=300, bbox_inches='tight')
plt.show()

# ## Audience Analysis

# Analyze rating distribution
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='vote_average', bins=20)
plt.title('Distribution of Movie Ratings')
plt.xlabel('Rating (0-10)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('../../../reports/figures/rating_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# Create a scatter plot of rating vs popularity
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='vote_average', y='popularity', alpha=0.6)
plt.title('Rating vs Popularity')
plt.xlabel('Rating (0-10)')
plt.ylabel('Popularity')

# Add annotations for notable outliers
for idx, row in df.nlargest(5, 'popularity').iterrows():
    plt.annotate(row['title'], 
                 (row['vote_average'], row['popularity']),
                 xytext=(10, 10), 
                 textcoords='offset points')

plt.tight_layout()
plt.savefig('../../../reports/figures/rating_vs_popularity.png', dpi=300, bbox_inches='tight')
plt.show()

# Analyze the relationship between rating and revenue
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='vote_average', y='revenue', alpha=0.6)
plt.title('Rating vs Revenue')
plt.xlabel('Rating (0-10)')
plt.ylabel('Revenue (USD)')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('../../../reports/figures/rating_vs_revenue.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate correlation between rating and revenue
rating_revenue_corr = df['vote_average'].corr(df['revenue'])
print(f"Correlation between rating and revenue: {rating_revenue_corr:.2f}")

# Analyze the relationship between vote count and revenue
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='vote_count', y='revenue', alpha=0.6)
plt.title('Vote Count vs Revenue')
plt.xlabel('Vote Count')
plt.ylabel('Revenue (USD)')
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('../../../reports/figures/vote_count_vs_revenue.png', dpi=300, bbox_inches='tight')
plt.show()

# Calculate correlation between vote count and revenue
vote_count_revenue_corr = df['vote_count'].corr(df['revenue'])
print(f"Correlation between vote count and revenue: {vote_count_revenue_corr:.2f}")

# ## Statistical Tests

print("\n\n## Advanced Statistical Analysis")
print("Performing statistical tests to validate observations and identify significant patterns.")

# 1. Hypothesis Testing: Do high-budget movies have significantly higher revenue?
print("\n### Hypothesis Testing: Budget Impact on Revenue")
print("H0: High-budget and low-budget movies have the same average revenue")
print("H1: High-budget movies have higher average revenue than low-budget movies")

# Define high and low budget movies (using median as threshold)
median_budget = df['budget'].median()
high_budget = df[df['budget'] > median_budget]['revenue']
low_budget = df[df['budget'] <= median_budget]['revenue']

# Perform t-test
t_stat, p_value = stats.ttest_ind(high_budget, low_budget, equal_var=False)
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Conclusion: {'Reject' if p_value < 0.05 else 'Fail to reject'} the null hypothesis")
print(f"Interpretation: {'High-budget movies do have significantly higher revenue' if p_value < 0.05 else 'There is no significant difference in revenue between high and low budget movies'}")

# 2. ANOVA: Is there a significant difference in revenue across different release quarters?
print("\n### ANOVA: Revenue Differences Across Release Quarters")
print("H0: All quarters have the same average revenue")
print("H1: At least one quarter has a different average revenue")

# Perform one-way ANOVA
quarters = []
revenues = []
for quarter in df['release_quarter'].unique():
    quarters.append(f"Q{quarter}")
    revenues.append(df[df['release_quarter'] == quarter]['revenue'])

f_stat, p_value = stats.f_oneway(*revenues)
print(f"F-statistic: {f_stat:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Conclusion: {'Reject' if p_value < 0.05 else 'Fail to reject'} the null hypothesis")
print(f"Interpretation: {'There are significant differences in revenue across quarters' if p_value < 0.05 else 'There is no significant difference in revenue across quarters'}")

# 3. Regression Analysis: Predicting movie revenue
print("\n### Multiple Regression Analysis: Predicting Movie Revenue")

# Prepare data for regression
features = ['budget', 'vote_average', 'vote_count', 'popularity', 'release_year']
X = df[features].dropna()
y = df.loc[X.index, 'revenue']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Fit linear regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.4f}")
print("Feature Importance:")
for feature, coef in zip(features, model.coef_):
    print(f"  - {feature}: {coef:.4f}")

# Create a more detailed regression model using statsmodels
print("\n### Detailed Regression Analysis with statsmodels")
X_with_const = sm.add_constant(X)
model = sm.OLS(y, X_with_const).fit()
print(model.summary().tables[1])  # Print coefficient table

# 4. Time Series Analysis: Analyzing revenue trends over time
print("\n### Time Series Analysis: Revenue Trends")

# Prepare time series data
yearly_revenue = df.groupby('release_year')['revenue'].sum().reset_index()
yearly_revenue = yearly_revenue.set_index('release_year')
yearly_revenue = yearly_revenue.sort_index()

# Check for stationarity using Augmented Dickey-Fuller test
print("Augmented Dickey-Fuller Test for Stationarity:")
result = adfuller(yearly_revenue['revenue'].dropna())
print(f"ADF Statistic: {result[0]:.4f}")
print(f"P-value: {result[1]:.4f}")
print(f"Conclusion: {'Revenue time series is stationary' if result[1] < 0.05 else 'Revenue time series is non-stationary'}")

# Perform seasonal decomposition if we have enough data points
if len(yearly_revenue) >= 6:
    try:
        # Decompose time series into trend, seasonal, and residual components
        decomposition = seasonal_decompose(yearly_revenue['revenue'], model='additive', period=4)
        
        # Plot decomposition
        plt.figure(figsize=(14, 10))
        plt.subplot(411)
        plt.plot(decomposition.observed)
        plt.title('Observed')
        plt.subplot(412)
        plt.plot(decomposition.trend)
        plt.title('Trend')
        plt.subplot(413)
        plt.plot(decomposition.seasonal)
        plt.title('Seasonal')
        plt.subplot(414)
        plt.plot(decomposition.resid)
        plt.title('Residual')
        plt.tight_layout()
        plt.savefig('../../../reports/figures/time_series_decomposition.png', dpi=300, bbox_inches='tight')
        plt.show()
    except:
        print("Not enough data points for seasonal decomposition with the specified period.")

# 5. Chi-Square Test: Is there an association between genre and high/low revenue?
print("\n### Chi-Square Test: Genre and Revenue Association")
print("H0: There is no association between genre and revenue level")
print("H1: There is an association between genre and revenue level")

# Create a contingency table
# First, identify the top 5 genres
top_genres = genre_counts.head(5)['genre'].tolist()

# Create a new column for revenue level (high/low)
median_revenue = df['revenue'].median()
genre_df['revenue_level'] = genre_df['revenue'].apply(lambda x: 'High' if x > median_revenue else 'Low')

# Filter for top genres
filtered_df = genre_df[genre_df['genres_list'].isin(top_genres)]

# Create contingency table
contingency = pd.crosstab(filtered_df['genres_list'], filtered_df['revenue_level'])
print("Contingency Table (Genre vs Revenue Level):")
print(contingency)

# Perform chi-square test
chi2, p, dof, expected = stats.chi2_contingency(contingency)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"Conclusion: {'Reject' if p < 0.05 else 'Fail to reject'} the null hypothesis")
print(f"Interpretation: {'There is a significant association between genre and revenue level' if p < 0.05 else 'There is no significant association between genre and revenue level'}")

# Save statistical test results
plt.figure(figsize=(10, 6))
coefficients = pd.Series(model.coef_, index=features)
coefficients.plot(kind='bar')
plt.title('Regression Coefficients for Revenue Prediction')
plt.xlabel('Features')
plt.ylabel('Coefficient Value')
plt.tight_layout()
plt.savefig('../../../reports/figures/regression_coefficients.png', dpi=300, bbox_inches='tight')
plt.show()

# ## Conclusions

# Calculate overall statistics
total_movies = len(df)
total_revenue = df['revenue'].sum()
avg_revenue = df['revenue'].mean()
avg_roi = df['roi'].mean()
highest_grossing = df.loc[df['revenue'].idxmax()]['title']
highest_roi = df.loc[df['roi'].idxmax()]['title']
most_popular_genre = genre_counts.iloc[0]['genre']
best_performing_genre = genre_performance.iloc[0]['genre']
best_release_quarter = seasonal_performance.loc[seasonal_performance['avg_revenue'].idxmax()]['quarter']

print("## Disney Movie Analysis Conclusions")
print(f"Total Movies Analyzed: {total_movies}")
print(f"Total Revenue Generated: {format_currency(total_revenue)}")
print(f"Average Revenue per Movie: {format_currency(avg_revenue)}")
print(f"Average ROI: {avg_roi:.2f}%")
print(f"Highest Grossing Movie: {highest_grossing}")
print(f"Highest ROI Movie: {highest_roi}")
print(f"Most Common Genre: {most_popular_genre}")
print(f"Best Performing Genre (by Revenue): {best_performing_genre}")
print(f"Best Release Quarter (by Revenue): Q{best_release_quarter}")

# Save the analysis results to a CSV file
results = {
    'Metric': [
        'Total Movies Analyzed',
        'Total Revenue Generated',
        'Average Revenue per Movie',
        'Average ROI',
        'Highest Grossing Movie',
        'Highest ROI Movie',
        'Most Common Genre',
        'Best Performing Genre (by Revenue)',
        'Best Release Quarter (by Revenue)'
    ],
    'Value': [
        total_movies,
        total_revenue,
        avg_revenue,
        avg_roi,
        highest_grossing,
        highest_roi,
        most_popular_genre,
        best_performing_genre,
        f"Q{best_release_quarter}"
    ]
}

results_df = pd.DataFrame(results)
results_df.to_csv('../../../reports/disney_movie_analysis_results.csv', index=False)
print("Analysis results saved to '../../../reports/disney_movie_analysis_results.csv'") 