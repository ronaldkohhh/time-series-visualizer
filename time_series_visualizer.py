import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=True, index_col='date')
# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025))
            & (df['value'] <= df['value'].quantile(0.975))].sort_values(
                by='date')


def draw_line_plot():
  # Draw line plot
  fig = plt.figure(figsize=(12, 5))
  ax = sns.lineplot(x='date', y='value', data=df)
  ax.set(xlabel='Date',
         ylabel='Page Views',
         title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.set_xticks(df.index[::130])

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_avg = df.copy()
  df_avg['year'] = df_avg.index.year
  df_avg['month'] = df_avg.index.month_name()
  df_avg['month'] = pd.Categorical(df_avg['month'],
                                   categories=[
                                       'January', 'February', 'March', 'April',
                                       'May', 'June', 'July', 'August',
                                       'September', 'October', 'November',
                                       'December'
                                   ],
                                   ordered=True)
  df_avg = df_avg.groupby(['year', 'month'],
                          sort=False)['value'].mean().unstack()

  # Draw bar plot
  ax = df_avg.plot(kind='bar', figsize=(12, 5))
  ax.set_xlabel('Years')
  ax.set_ylabel('Average Page Views')
  ax.legend(title='Months')
  fig = ax.get_figure()

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]
  df_box['month'] = pd.Categorical(df_box['month'],
                                   categories=[
                                       'Jan', 'Feb', 'Mar', 'Apr', 'May',
                                       'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
                                       'Nov', 'Dec'
                                   ],
                                   ordered=True)

  # Draw box plots (using Seaborn)
  fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))
  sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
  ax1.set_title('Year-wise Box Plot (Trend)')
  ax1.set_xlabel('Year')
  ax1.set_ylabel('Page Views')
  sns.boxplot(x='month', y='value', data=df_box, ax=ax2)
  ax2.set_title('Month-wise Box Plot (Seasonality)')
  ax2.set_xlabel('Month')
  ax2.set_ylabel('Page Views')

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
