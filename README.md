# Finding Top Users on StackOverflow

## Description
Identify the top users associated to particular tags or search queries based on accepted answers and reputation

## Project Overview
There are two main functions for this application:

1. Topics: Identify users by providing a list of topics (tags in StackOverflow).  The function returns the top users for that topic.
2. Search: Identify users by providing a list of keywords that searches through posted questions.  The function returns the users who provided the accepted answer for the 

## System Requirements
Python 2.7

## Libraries
- StackAPI
- pprint
- requests
- argparse

## Usage Instructions

### Topics

##### Prepare the CSV

1. Make a list of topics that conform to the tagging convention on StackOverflow topics.csv
2. Save the file to the same directory as this script

See existing [topics.csv](topics.csv) as a reference

##### Run the Script
1. Open Terminal / Command Line and navigate to the directory
2. Run the command

```
$ python main.py topics
```

##### Additional arguments:
- --file: specify an alternate filename for the list of topics
- --all_time: set to True to look at all historical data (default is the last month)
- --max: choose the max results up to 100 (default is 10)

```
$ python main.py topics --file=my_topics.csv --all_time=true --max=20 
```

### Search

1. Make a list of search terms to query in StackOverflow.  Make sure to maintain the columns in keywords.csv
2. Save the file to the same directory as this script

See existing [keywords.csv](keywords.csv) as a reference

##### Column Definitions
- keyword: the search term
- topic: limit search results to a specific topic
- title: this term must appear in the title of the question
- body: this term must appear in the body of the question

##### Run the Script
1. Open Terminal / Command Line and navigate to the directory
2. Run the command with the file flag

```
$ python main.py search --file=keywords.csv
```

##### Additional arguments:
- --file: specify an alternate filename for the list of keywords
- --from_date: start date for questions (default is 01/01/2017)
- --to_date: end date for questions (default is current date)
- --max: choose the max results up to 100 (default is 10)

```
$ python main.py topics --file=my_keywords.csv --from_date=07/01/2017 --to_date=07/31/2017 --max=25
```
