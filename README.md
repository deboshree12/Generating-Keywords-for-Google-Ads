# Generating-Keywords-for-Google-Ads

The Python code provided in this project creates a list of keywords to use in a SEM (Search Engine Marketing) campaign for selling low-cost sofas. The project is divided into the following steps:

The first step is to come up with a list of words that users might use to express their desire in buying low-cost sofas. This is achieved by creating a list of relevant words such as "buy", "price", "discount", etc.

The list of words is then combined with the names of different types of sofas such as "convertible sofas", "love seats", etc. to create a list of potential keywords.

The list of potential keywords is converted into a Pandas DataFrame, which allows for easy manipulation and analysis of the data.

The column names of the DataFrame are then changed to "Ad Group" and "Keyword".

A new column called "Campaign" is added to the DataFrame with the value "SEM_Sofas".

Another new column called "Criterion Type" is added to the DataFrame with the value "Exact".

A copy of the original DataFrame is made and the value of the "Criterion Type" column in the new DataFrame is changed to "Phrase". The two DataFrames are then concatenated to create the final DataFrame.

The final DataFrame is then saved to a CSV file called "keywords.csv".

Finally, a summary of the campaign work is displayed by grouping the data in the final DataFrame by "Ad Group" and "Criterion Type" and counting the number of keywords in each group.

Overall, this Python code provides a useful framework for creating a list of SEM keywords for selling low-cost sofas, which can be adapted and modified for other products or industries.





