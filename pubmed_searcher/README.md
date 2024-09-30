# Pubmed Searcher

## Description

The **Pubmed Searcher** component allows users to search for article information from Pubmed using specified keywords. This component retrieves relevant articles and outputs the search results as a record-formatted pandas dataframe.

## Inputs

- **Keywords** (str): Enter the keywords to search for articles in the Pubmed database. Multiple keywords can be separated by spaces.
- **From year** (str): Specify the starting year for the search. Articles published from this year onward will be included in the results.
- **To year** (str): Specify the ending year for the search. Articles published up to this year will be included in the results.
- **Max pages** (str): Define the maximum number of pages of search results to retrieve. Each page contains a set number of articles.

## Output

- **Output** (List[Dict]): The output is a list of dictionaries where each dictionary represents a record of an article found in the search. This list is formatted into a pandas dataframe for easy analysis and manipulation.

## Configuration Parameters

This component does not require any additional configuration parameters.

## Input Types

```json
{
    "Keywords": "TEXT",
    "From year": "TEXT",
    "To year": "TEXT",
    "Max pages": "TEXT"
}
```

## Output Type

- **Output Type**: LIST