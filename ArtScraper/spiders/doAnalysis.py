"""
Author: Stephen W. Thomas
Perform sentiment analysis using the MPQA lexicon.
Note, in this simple approach, we don't do anything to handle negations
or any of the other hard problems.
"""

# For reading input files in CSV format
import csv

# For doing cool regular expressions
import re

# For sorting dictionaries
import operator

# Intialize an empty list to hold all of our tweets
tweets = []


# A helper function that removes all the non ASCII characters
# from the given string. Retuns a string with only ASCII characters.
def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)



# LOAD AND CLEAN DATA

# Load in the input file and process each row at a time.
# We assume that the file has three columns:
# 0. The tweet text.
# 1. The tweet ID.
# 2. The tweet publish date
#
# Create a data structure for each tweet:
#
# id:       The ID of the tweet
# pubdate:  The publication date of the tweet
# orig:     The original, unpreprocessed string of characters
# clean:    The preprocessed string of characters
x="  احب  احب احب"
def getScore(X):


    # Create a data structure to hold the lexicon.
    # We will use a Python diction. The key of the dictionary will be the word
    # and the value will be the word's score.
    lexicon = dict()

    # Read in the lexicon.
    with open('/Users/georgesrbeiz/Downloads/Latest_News (1)/News-3-4/ArtScraper/ArtScraper/spiders/ALL_lex.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            lexicon[row[0]] = int(row[1])

    # Use lexicon to score tweets
    score = 0
    for word in X.split(" "):
        if word in lexicon:
            score = score + lexicon[word]
        #
        # with open('scores.txt', 'w') as file:
        #     file.write(str(score))
    return score




print (getScore(x))
# connection = pymongo.MongoClient("ds040309.mlab.com", 40309)
#
# db = connection["newsaggregartor"]
#
# db.authenticate("gnr011", "Kalash1")
#
#
# arr = db.articles.distinct('art_content')
