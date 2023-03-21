

# The first step is to come up with a list of words that users might use to express their desire in buying low-cost sofas.</p>
# List of words to pair with products
words = ["buy", "price", "discount", "promotion", "promo", "shop"]

# Print list of words
print(words)


get_ipython().run_cell_magic('nose', '', '\ndef test_words_in_long_word_list_task_1():\n    correct_words = [\'buy\', \'price\', \'discount\', \'promotion\', \'promo\', \'shop\', \n                     \'buying\', \'prices\', \'pricing\', \'shopping\', \'discounts\', \n                     \'promos\', \'ecommerce\', \'e commerce\', \'buy online\', \n                     \'shop online\', \'cheap\', \'best price\', \'lowest price\', \n                     \'cheapest\', \'best value\', \'offer\', \'offers\', \'promotions\',\n                     \'purchase\', \'sale\', \'bargain\', \'affordable\',\n                     \'cheap\', \'low cost\', \'low price\', \'budget\', \'inexpensive\', \'economical\',]\n    assert all([word in correct_words for word in words]), \\\n    \'The variable `words` should contain relevant words to the products in the brief.\'\n\ndef test_len_words_task_1():\n    assert 6 <= len(set(words)) <= 10, \\\n    "There should be six to ten brief-related words in the list `words`."')


# Combine the words with the product names
products = ['sofas', 'convertible sofas', 'love seats', 'recliners', 'sofa beds']

# Create an empty list
keywords_list = []

# Loop through products
for product in products:
    # Loop through words
    for word in words:
        # Append combinations
        keywords_list.append([product, product + ' ' + word])
        keywords_list.append([product, word + ' ' + product])
        
# Inspect keyword list
from pprint import pprint
pprint(keywords_list)

get_ipython().run_cell_magic('nose', '', "\ndef test_list_task_2():\n    assert isinstance(keywords_list, list), 'The variable `keywords_list` is not a Python list.'\n\ndef test_keywords_list_created_correctly_task_2():\n    test_keywords_list = []\n\n    for product in products:\n        for word in words:\n            test_keywords_list.append([product, word + ' ' + product])\n            test_keywords_list.append([product, product + ' ' + word])\n\n    assert all([kl in test_keywords_list for kl in keywords_list]), \\\n     'Make sure you have \\'product word\\' or \\'word product\\' as the second element in each sublist.'")


# Convert the list of lists into a DataFrame

# Load library
import pandas as pd

# Create a DataFrame from list
keywords_df = pd.DataFrame(keywords_list)

# Print the keywords DataFrame to explore it
print(keywords_df.head())
get_ipython().run_cell_magic('nose', '', '\ndef test_pandas_loaded_task_3():\n    assert \'pd\' in globals(), \\\n    \'Did you forget to import pandas aliased as pd?\'\n\ndef test_keywords_df_created_correctly_task_3():\n    import pandas as pd\n    correct_keywords_df = pd.DataFrame.from_records(keywords_list)\n    assert correct_keywords_df.equals(keywords_df), "The contents of `keywords_df` doesn\'t appear to be correct. Don\'t specify column names yet!"\n    \n#     correct_keywords_df = pd.DataFrame.from_records(keywords_list)\n    \n#     assert (correct_keywords_df\n#             .sort_values(list(sorted(correct_keywords_df.columns.values)))\n#             .reset_index(drop=True)\n#             .equals(keywords_df\n#                     .sort_values(list(sorted(keywords_df.columns.values)))\n#                     .reset_index(drop=True))) , \\\n#     \'The DataFrame you created doesn\\\'t seem to be the right one.\'')



# Rename the columns of the DataFrame
keywords_df = keywords_df.rename(columns={0: "Ad Group", 1: "Keyword"})
get_ipython().run_cell_magic('nose', '', "\ndef test_df_columns_renamed_correctly_task_4():\n    assert 'Ad Group' in keywords_df.columns.values and 'Keyword' in keywords_df.columns.values , \\\n    'Make sure you are using the proper names for the columns. Capitalization matters!'")



# Add a campaign column
keywords_df["Campaign"] = "SEM_Sofas"
keywords_df.head()

get_ipython().run_cell_magic('nose', '', '\ndef test_campaign_column_created_task_5():\n    assert \'Campaign\' in keywords_df.columns.values, \\\n    "`Campaign` needs to be the name of the new column. Capitalization matters!"\n    \ndef test_campaign_name_task_5():\n    assert len(set(keywords_df[\'Campaign\'])) == 1 and set(keywords_df[\'Campaign\']).pop() == \'SEM_Sofas\', \\\n    "Is \'SEM_Sofas\' the campaign name in every row of the `Campaign` column?"')



# Add a criterion type column
keywords_df["Criterion Type"] = "Exact"
keywords_df.head()

get_ipython().run_cell_magic('nose', '', '\ndef test_criterion_type_column_created_task_6():\n    assert \'Criterion Type\' in keywords_df.columns.values, \\\n    "`Criterion Type` needs to be the name of the new column. Capitalization matters!"\n    \ndef test_criterion_type_task_6():\n    assert len(set(keywords_df[\'Criterion Type\'])) == 1 and set(keywords_df[\'Criterion Type\']).pop() == \'Exact\', \\\n    "Is \'Exact\' the campaign name in every row of the `Criterion Type` column?"')



# Make a copy of the keywords DataFrame
keywords_phrase = keywords_df.copy()

# Change criterion type match to phrase
keywords_phrase["Criterion Type"] = "Phrase"

# Append the DataFrames
keywords_df_final = keywords_df.append(keywords_phrase)


get_ipython().run_cell_magic('nose', '', '\ndef test_criterion_type_task_7():\n    assert len(set(keywords_phrase[\'Criterion Type\'])) == 1 and set(keywords_phrase[\'Criterion Type\']).pop() == \'Phrase\', \\\n    "Is \'Phrase\' the campaign name in every row of the `Criterion Type` column in `keyword_phrase`?"\n\ndef test_phrase_df_created_task_7():\n    test_keywords_df_final = keywords_df.append(keywords_phrase)\n    assert test_keywords_df_final.equals(keywords_df_final), \\\n    \'The final DataFrame does not seem to be created correctly.\'')


# Save the final keywords to a CSV file
keywords_df_final.to_csv('keywords.csv', index=False)

# View a summary of our campaign work
summary = keywords_df_final.groupby(['Ad Group', 'Criterion Type'])['Keyword'].count()
print(summary)

get_ipython().run_cell_magic('nose', '', 'import os\n\n# def test_df_saved_to_csv_task_8():\n#     test_keywords_df = pd.read_csv(\'keywords.csv\')\n#     assert keywords_df_final.equals(test_keywords_df), \\\n#     \'The \\\'keywords.csv\\\' file isn\\\'t saved correctly.\'\n\ndef test_file_exists_task_8():\n    assert os.path.exists("keywords.csv"), \\\n    \'Did you save the `keywords_df_final` DataFrame to \\\'keywords.csv\\\'?\'\n    \ndef test_index_excluded_task_8():\n    test_keywords_csv = pd.read_csv(\'keywords.csv\')\n    assert len(pd.read_csv(\'keywords.csv\').columns) == 4, \\\n    \'Did you exclude the DataFrame index in \\\'keywords.csv\\\' using `index=False`?\'')

