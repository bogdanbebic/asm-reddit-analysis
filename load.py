from functools import reduce
import pandas as pd
import numpy as np
import os

# Data path initial location
submission_dataPath = "ASM_PZ2_podaci_2122/reddit2008/submissions_2008_asm/"
comments_dataPath = "ASM_PZ2_podaci_2122/reddit2008/comments_2008_asm_v1.1/comments_2008/"

# Read data file names
submission_FileNames = os.listdir(submission_dataPath)
comments_FileNames= os.listdir(comments_dataPath)

# Func: Read data from Comment datasets
def loadDataSet(filePath, fileNames):
    
    # Array of all Subreddit Ids
    allSubredditId = []

    # Array with authors and their subreddit_ids
    totalAuthorsWitjSubredditId = pd.DataFrame([])

    for fileName in fileNames:
        # Read file
        commentData = pd.read_csv(filePath + fileName)
        # Only uniqe subreddit_id 
        subredditId = commentData["subreddit_id"].unique()
        # Author with subreddit_id 
        subreddit_comment_author = commentData[["author", "subreddit_id"]]

        # Merege all subredditIds
        allSubredditId = np.union1d(allSubredditId, subredditId)

        # Concatenate all authors and subreddit_ids
        totalAuthorsWitjSubredditId = pd.concat([totalAuthorsWitjSubredditId, subreddit_comment_author ])

    # It is possible to have "[deleted]" as authir name
    # Remove all deleted author data
    filter = totalAuthorsWitjSubredditId['author']!="[deleted]"
    allAuthorsWithSubredditId = totalAuthorsWitjSubredditId[filter]
   
    return [allSubredditId, allAuthorsWithSubredditId]

def loadData():
    
    submissionData = loadDataSet(submission_dataPath, submission_FileNames)
    commentsData = loadDataSet(comments_dataPath, comments_FileNames)

    allSubredditId = np.union1d(submissionData[0], commentsData[0])
    allAuthorsWithSubredditId =  pd.concat([submissionData[1], commentsData[1]])
    allAuthorsWithSubredditId = allAuthorsWithSubredditId.groupby(["author", "subreddit_id"])
    
    print(f"Number of different subreddit Ids is {len(allSubredditId)}")
    print(f"Number of authors with subreddit Ids from Comments dataset is {len(allAuthorsWithSubredditId)}")

    return [allSubredditId, allAuthorsWithSubredditId]
    

