from functools import reduce
from unicodedata import name
import pandas as pd
import numpy as np
import os

# Data path initial location
submission_dataPath = "ASM_PZ2_podaci_2122/reddit2008/submissions_2008_asm/"
comments_dataPath = (
    "ASM_PZ2_podaci_2122/reddit2008/comments_2008_asm_v1.1/comments_2008/"
)

# Read data file names
submission_FileNames = os.listdir(submission_dataPath)
comments_FileNames = os.listdir(comments_dataPath)

# Func: Read data from Comment datasets
def loadDataSet(filePath, fileNames):
    # Array with authors and their subreddit_ids
    allFileData = pd.DataFrame([])
    for fileName in fileNames:
        # Read file
        singleFileData = pd.read_csv(filePath + fileName)
        allFileData = pd.concat([allFileData, singleFileData])

    return allFileData

submissionData = loadDataSet(submission_dataPath, submission_FileNames)
commentsData = loadDataSet(comments_dataPath, comments_FileNames)

allSubredditId = np.union1d(submissionData['subreddit_id'], commentsData['subreddit_id'])
print(f"Number of different subreddit Ids is {len(allSubredditId)}")

# count comments per subreddit ID
group = commentsData.groupby(["subreddit_id"])
counts = group.size().reset_index(name="counts")
sorted_counts = counts.sort_values("counts", ascending=False)
print(sorted_counts[:10])

# count users per subreddit ID
allAuthorsWithSubredditId = pd.concat([submissionData, commentsData])
# It is possible to have "[deleted]" as author name
# Remove all deleted author data
filtered = allAuthorsWithSubredditId["author"] != "[deleted]"
groupSubredditAuthor = allAuthorsWithSubredditId[filtered].groupby(
    ["subreddit_id", "author"]
)
countsSubredditAuthor = groupSubredditAuthor.size().reset_index(name="counts")
# subredditId - author - countInteractions
# subredditId - countAuthors
authorsPerSubreddit = countsSubredditAuthor.groupby(["subreddit_id"]).size().reset_index(name="counts")
print(authorsPerSubreddit.sort_values("counts", ascending=False)[:10])

print("AVG number users per subreddit:")
print(authorsPerSubreddit['counts'].sum() / len(allSubredditId))

# sorted_countsSubredditAuthor = countsSubredditAuthor.sort_values("counts", ascending=False)
# print(sorted_countsSubredditAuthor[:10])


print(f"Max submissions per author {submissionData.groupby(['author']).size().reset_index(name='counts').sort_values('counts', ascending=False)[:10]}")
print(f"Max comments per author {commentsData.groupby(['author']).size().reset_index(name='counts').sort_values('counts', ascending=False)[:10]}")

countsAuthorSubreddit = allAuthorsWithSubredditId[filtered].groupby(['author', 'subreddit_id']).size().reset_index(name='counts')
# author - subreddit - count interactions
# author - count subreddits
subredditsPerAuthor = countsAuthorSubreddit.groupby(['author']).size().reset_index(name='counts')
print(subredditsPerAuthor.sort_values('counts', ascending=False)[:10])

