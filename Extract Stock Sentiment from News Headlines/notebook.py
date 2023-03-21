# Import libraries
from bs4 import BeautifulSoup
import os

html_tables = {}

# For every table in the datasets folder...
for table_name in os.listdir('datasets'):
    #this is the path to the file. Don't touch!
    table_path = f'datasets/{table_name}'
    # Open as a python file in read-only mode
    table_file = open(table_path, 'r')
    # Read the contents of the file into 'html'
    html = BeautifulSoup(table_file)
    # Find 'news-table' in the Soup and load it into 'html_table'
    html_table = html.find(id='news-table')
    # Add the table to our dictionary
    html_tables[table_name] = html_table


get_ipython().run_cell_magic('nose', '', "import bs4 \n\ndef test_load_html():\n    assert type(html) == bs4.BeautifulSoup, \\\n    'You should load the BeautifulSoup objects in variable named html.'\n    \ndef test_load_html_table():\n    assert type(html_table) == bs4.element.Tag, \\\n    'You should load the news-table tags in the variable named html_table.' \n    \ndef test_load_html_tables():\n    assert len(html_tables) == 5, \\\n    'You should load all five tables in the html tables dictionary.'\n    \ndef test_html_tables_has_data():\n    assert type(html_tables['tsla_26nov.html'])  == bs4.element.Tag, \\\n    'You should load the news-table elements into the html_tables dictionary.'")



# Read one single day of headlines 
tsla = html_tables['tsla_22sep.html']
# Get all the table rows tagged in HTML with <tr> into 'tesla_tr'
tsla_tr = tsla.findAll('tr')

# For each row...
for i, table_row in enumerate(tsla_tr):
    # Read the text of the element 'a' into 'link_text'
    link_text = table_row.a.get_text()
    # Read the text of the element 'td' into 'data_text'
    data_text = table_row.td.get_text()
    # Print the count
    print(f'File number {i+1}:')
    # Print the contents of 'link_text' and 'data_text' 
    print(link_text)
    print(data_text)
    # The following exits the loop after four rows to prevent spamming the notebook, do not touch
    if i == 3:
        break


get_ipython().run_cell_magic('nose', '', '\ndef test_link_ok():\n    assert link_text == "Tesla\'s People Problem and the Inscrutable Musk: 2 Things That Make You Go Hmmm", \\\n    "Iterate through table_row and load link_text exactly 3 times."\n    \ndef test_data_ok():\n    assert data_text == \'05:30PM\\xa0\\xa0\', \\\n    "Iterate through table_row and load data_text exactly 3 times."')



# Hold the parsed news into a list
parsed_news = []
# Iterate through the news
for file_name, news_table in html_tables.items():
    # Iterate through all tr tags in 'news_table'
    for x in news_table.findAll('tr'):
        # Read the text from the tr tag into text
        text = x.get_text() 
        # Split the text in the td tag into a list 
        date_scrape = x.td.text.split()
        # If the length of 'date_scrape' is 1, load 'time' with the only element
        # If not, load 'date' with the 1st element and 'time' with the second
        if len(date_scrape) == 1:
            time = date_scrape[0]
        else:
            date = date_scrape[0]
            time = date_scrape[1]

        # Extract the ticker from the file name, get the string up to the 1st '_'  
        ticker = file_name.split("_")[0]
        # Append ticker, date, time and headline as a list to the 'parsed_news' list
        parsed_news.append([ticker, date, time, x.a.text])



get_ipython().run_cell_magic('nose', '', '\nimport pandas as pd\n\ndef test_date():\n    assert pd.DataFrame(parsed_news)[1].sort_values().unique()[4] == \'Jan-01-19\', \\\n    \'All dates should be loaded in the 2nd column, with format like in "Jan-01-19"\'\n    \ndef test_time():\n    assert pd.DataFrame(parsed_news)[2].sort_values().unique()[4] == \'01:06PM\', \\\n    \'All dates should be loaded in the 2nd column, with format like in "01:06PM"\'\n    \ndef test_ticker():\n    assert list(pd.DataFrame(parsed_news)[0].sort_values().unique()) == [\'fb\', \'tsla\'], \\\n    \'The tickers loaded in parsed_news should be "tsla" and "fb". They should be the 1st column.\'\n\ndef test_num_headlines():\n    assert len(parsed_news) == 500, \\\n    \'The parsed_news list of lists should contain exactly 500 elements.\'\n\ndef test_len_data():\n    assert len(parsed_news[9]) == 4, \\\n    \'You should have exactly 4 elements inside each sub-list.\'')



# NLTK VADER for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# New words and values
new_words = {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
}
# Instantiate the sentiment intensity analyzer with the existing lexicon
vader = SentimentIntensityAnalyzer()
# Update the lexicon
vader.lexicon.update(new_words)


get_ipython().run_cell_magic('nose', '', '\nimport nltk\n\ndef test_vader():\n    assert type(vader) == nltk.sentiment.vader.SentimentIntensityAnalyzer, \\\n    \'The vader object should be a SentimentIntensityAnalyzer instance.\'\n    \ndef test_lexicon_len():\n    assert len(vader.lexicon) >= 7504, "The lexicon should have been enriched with at least 5 words."')


# REAKING NEWS: NLTK Crushes Sentiment Estimates

import pandas as pd
# Use these column names
columns = ['ticker', 'date', 'time', 'headline']
# Convert the list of lists into a DataFrame
scored_news = pd.DataFrame(parsed_news, columns=columns)
# Iterate through the headlines and get the polarity scores
scores = [vader.polarity_scores(headline) for headline in scored_news.headline]
# Convert the list of dicts into a DataFrame
scores_df = pd.DataFrame(scores)
# Join the DataFrames
scored_news = scored_news.join(scores_df)
# Convert the date column from string to datetime
scored_news['date'] = pd.to_datetime(scored_news.date).dt.date


get_ipython().run_cell_magic('nose', '', '\nimport datetime\n\ndef test_scored_news_columns():\n    assert list(scored_news.columns[:4]) == [\'ticker\', \'date\', \'time\', \'headline\'], \\\n    "Don\'t forget to add the column names to the DataFrame. They first 4 should be [\'ticker\', \'date\', \'time\', \'headline\']. The rest are set automatically."\n\ndef test_shape_scored_news():\n    assert scored_news.shape == (500, 8), \\\n    \'The DataFrame scored_news should have exactly 500 rows and 8 columns.\'\n    \ndef test_shape_scores_df():\n    assert scores_df.shape == (500, 4), \\\n    \'The DataFrame scores_df should have exactly 500 rows and 4 columns.\' \n    \ndef test_first_date():\n    assert scored_news.date.min() == datetime.date(2018, 9, 18), "Convert the column date to a *date* (not a datetime)."\n    \ndef test_min_score():\n    assert scored_news[["neg", "pos", "neu"]].min().min() >= 0 , "neg, pos and neu cannot be smaller than 0."\n \ndef test_max_score():\n    assert scored_news[["neg", "pos", "neu"]].max().max() <= 1, "neg, pos and neu cannot be bigger than 1."\n\ndef test_min_comp():\n    assert scored_news["compound"].min() >= -1, "The compounded score cannot be bigger than -1."')


# Plot all the sentiment in subplots

import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
get_ipython().run_line_magic('matplotlib', 'inline')

# Group by date and ticker columns from scored_news and calculate the mean
mean_c = scored_news.groupby(['date','ticker']).mean()
# Unstack the column ticker
mean_c = mean_c.unstack('ticker')
# Get the cross-section of compound in the 'columns' axis
mean_c = mean_c.xs("compound", axis="columns")
# Plot a bar chart with pandas
mean_c.plot.bar(figsize = (10, 6));


get_ipython().run_cell_magic('nose', '', '\ndef test_mean_shape():\n    assert mean_c.shape == (23, 2), \'"mean_c" should have exactly 23 rows and 2 columns.\'\n    \ndef test_ticker():\n    assert mean_c.columns.name == \'ticker\', \'you should group by and unstack the column ticker.\'\n\ndef test_cols():\n    assert list(mean_c.columns) == [\'fb\', \'tsla\'], \'Columns should be "fb" and "tsla".\'')


# Weekends and duplicates
# Count the number of headlines in scored_news (store as integer)
num_news_before = scored_news.headline.count()
# Drop duplicates based on ticker and headline
scored_news_clean = scored_news.drop_duplicates(subset=['headline', 'ticker'])
# Count number of headlines after dropping duplicates
num_news_after = scored_news_clean.headline.count()
# Print before and after numbers to get an idea of how we did 
f"Before we had {num_news_before} headlines, now we have {num_news_after}"


get_ipython().run_cell_magic('nose', '', '\ndef test_df_shape():\n    assert scored_news_clean.shape == (476, 8), \'"scored_news_clean" should have 476 rows and 8 columns.\'\n    \ndef test_df_cols():\n    l = list(scored_news.columns)\n    l.sort()\n    assert l == [\'compound\', \'date\', \'headline\', \'neg\', \'neu\', \'pos\', \'ticker\', \'time\'], \\\n           \'"scored_news_clean" should still have the same column names as scored_news.\'\n\ndef test_scored_news_counts():\n    assert (num_news_before, num_news_after) == (500, 476), \\\n    \'"num_news_before" should be 500 and "num_news_after" should be 476.\'')


# Sentiment on one single trading day and stock
# Set the index to ticker and date
single_day = scored_news_clean.set_index(['ticker', 'date'])
# Cross-section the fb row
single_day = single_day.xs('fb')
# Select the 3rd of January of 2019
single_day = single_day.loc['2019-01-03']
# Convert the datetime string to just the time
single_day['time'] = pd.to_datetime(single_day['time']).dt.time
# Set the index to time and 
single_day = single_day.set_index('time')
# Sort it
single_day = single_day.sort_index()


get_ipython().run_cell_magic('nose', '', '\nimport datetime\n\ndef test_shape():\n    assert single_day.shape == (19, 5), \'single_day should have 19 rows and 5 columns\'\n    \ndef test_cols():\n    assert list(single_day.columns) == [\'headline\', \'compound\', \'neg\', \'neu\', \'pos\'], \\\n    \'single_day column names should be "headline", "compound", "neg", "neu" and "pos"\'\n\ndef test_index_type():\n    assert type(single_day.index[1]) == datetime.time, \'The index should be of type "datetime.type"\'\n    \ndef test_index_val():\n    assert single_day.index[1] == datetime.time(8, 4), \'The 2nd index value should be exactly "08:04:00"\'')


# Visualize the single day
TITLE = "Negative, neutral, and positive sentiment for FB on 2019-01-03"
COLORS = ["red","orange", "green"]
# Drop the columns that aren't useful for the plot
plot_day = single_day.drop(['compound', 'headline'], 1)
# Change the column names to 'negative', 'positive', and 'neutral'
plot_day.columns = ['negative', 'neutral', 'positive']
# Plot a stacked bar chart
plot_day.plot.bar(stacked = True, figsize=(10, 6), title = TITLE, color = COLORS).legend(bbox_to_anchor=(1.2, 0.5))
plt.ylabel("scores");


get_ipython().run_cell_magic('nose', '', '\nimport datetime\n\ndef test_shape():\n    assert plot_day.shape == (19, 3), \'plot_day should have 19 rows and 3 columns.\'\n    \ndef test_cols():\n    assert list(plot_day.columns) == [\'negative\', \'neutral\', \'positive\'], \\\n    \'plot_day column names should be "negative", "neutral" and "positive".\'\n\ndef test_index_type():\n    assert plot_day.index.name == \'time\', \'The index should be named "time".\'\n    ')

