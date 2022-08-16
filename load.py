import pandas as pd
import numpy as np
import os

# Data path initial location
submission_dataPath = "ASM_PZ2_podaci_2122/reddit2008/submissions_2008_asm/"
comments_dataPath = "ASM_PZ2_podaci_2122/reddit2008/comments_2008_asm_v1.1/comments_2008/"

# Read data file names
submission_FileNames = os.listdir(submission_dataPath)
comments_FileNames= os.listdir(comments_dataPath)

def loadCommentDataSet():
    
    # Array of all Subreddit Ids
    allSubredditId = []

    # Array with authors and their subreddit_ids
    totalAuthorsWitjSubredditId = pd.DataFrame([])

    for fileName in comments_FileNames:
        # Read file
        commentData = pd.read_csv(comments_dataPath + fileName)
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
    allAuthorsWitjSubredditId = totalAuthorsWitjSubredditId[filter]

    print(f"Number of different subreddit Ids from Comments dataset is {len(allSubredditId)}")
    print(f"Is the subbredit id set unique? {len(set(allSubredditId)) == len(allSubredditId)}")
    print(f"Number of authors with subreddit Ids from Comments dataset is {len(allAuthorsWitjSubredditId)}")

    return [allSubredditId, allAuthorsWitjSubredditId]

rsl = loadCommentDataSet()
