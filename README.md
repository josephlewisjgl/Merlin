# Merlin

Merlin will be a Chatbot that can take requests from users to search for and retrieve data and information from StatsWales. For now Merlin operates solely as a rule-based bot using strings of text and conditionals but eventually the bot will be generative and use regular expressions.

## At the moment Merlin can:

### 1. Search for a dataset based on one or more keywords.

To access this function use:

*search school ethnicity*

Merlin will curate a list of all the cubes that match the key terms searched for and return their title and cube number.

### 2. Give you a brief description of a specific data cube from StatsWales metadata.

*describe econ0074*

Will return a brief message from Merlin who will describe the cube for you using the metadata provided on StatsWales.

### 3. Download your data for you.

*download econ0074*

Merlin will begin a download process for you on the dataset with the ID provided, there will then be a prompt from Merlin for the file path you would like to store the data under and Merlin will use it to store your data as a .csv file.

## Extra keywords:

### To close Merlin:

*exit*

### For more help:

*help*
