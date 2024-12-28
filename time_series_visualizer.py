import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean the data
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

def draw_line_plot():
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['value'], color='blue', linewidth=1)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('line_plot.png')
    return plt.gcf()  # Return the current figure

def draw_bar_plot():
    # Prepare data for bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Group by year and month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Create a list of full month names in order
    month_names = ['January', 'February', 'March', 'April', 'May', 
                   'June', 'July', 'August', 'September', 'October', 
                   'November', 'December']

    # Draw bar plot
    plt.figure(figsize=(12, 6))
    df_bar.columns = month_names  # Set the column names to full month names
    df_bar.plot(kind='bar', ax=plt.gca())
    plt.title('Average Daily Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=month_names)  # Ensure full month names are used
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('bar_plot.png')
    return plt.gcf()  # Return the current figure

def draw_box_plot():
    # Prepare data for box plot
    df_box = df.copy()
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.month

    # Ensure month is treated as a categorical variable with the correct order
    df_box['month'] = pd.Categorical(df_box['month'], 
                                      categories=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 
                                      ordered=True)

    # Draw box plots
    plt.figure(figsize=(12, 6))

    # Year-wise box plot
    plt.subplot(1, 2, 1)
    sns.boxplot(x='year', y='value', data=df_box)
    plt.title('Year-wise Box Plot (Trend)')
    plt.xlabel('Year')
    plt.ylabel('Page Views')

    # Month-wise box plot
    plt.subplot(1, 2, 2)
    sns.boxplot(x='month', y='value', data=df_box, 
                order=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])  # Use month numbers for ordering
    plt.title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')

    # Set x-ticks to abbreviated month names
    plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 
                                          'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 
                                          'Nov', 'Dec'])

    plt.tight_layout()
    plt.savefig('box_plot.png')
    return plt.gcf()  # Return the current figure

# Main function to call the plotting functions
if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()