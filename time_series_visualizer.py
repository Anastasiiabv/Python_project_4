import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)
df = df[(df['value'] > lower_bound) & (df['value'] < upper_bound)]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='blue', linestyle='-', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=16)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Page Views', fontsize=14)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.index = pd.to_datetime(df_bar.index)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()

    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                     'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    monthly_avg = monthly_avg.reindex(columns=months_order)
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw bar plot
    monthly_avg.plot(kind='bar', ax=ax, colormap='tab20')
    ax.set_title('Average Monthly Page Views by Year', fontsize=16)
    ax.set_xlabel('Years', fontsize=14)
    ax.set_ylabel('Average Page Views', fontsize=14)
    ax.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.index = pd.to_datetime(df_box.index)
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Draw box plots (using Seaborn)
    sns.boxplot(x='year', y='value', hue='year', data=df_box, ax=axes[0], legend=False, palette='Set3')
    axes[0].set_title('Year-wise Box Plot (Trend)', fontsize=16)
    axes[0].set_xlabel('Year', fontsize=14)
    axes[0].set_ylabel('Page Views', fontsize=14)
    axes[0].tick_params(axis='both', labelsize=12)

    sns.boxplot(x='month', y='value',hue='month', data=df_box, order=months_order, ax=axes[1], palette='Set3',legend=False)
    axes[1].set_title('Month-wise Box Plot (Seasonality)', fontsize=16)
    axes[1].set_xlabel('Month', fontsize=14)
    axes[1].set_ylabel('Page Views', fontsize=14)
    axes[1].tick_params(axis='x', labelsize=12)
    axes[1].tick_params(axis='y', labelsize=12)
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
