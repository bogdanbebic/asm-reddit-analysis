import pandas as pd
import numpy as np
import os

# Data path initial location
reddit_data_path = "ASM_PZ2_podaci_2122/reddit2008"
submission_dataPath = f"{reddit_data_path}/submissions_2008_asm/"
comments_dataPath = f"{reddit_data_path}/comments_2008_asm_v1.1/comments_2008/"


def loadDataSet(folderPath):
    allFileData = pd.DataFrame([])
    for fileName in os.listdir(folderPath):
        singleFileData = pd.read_csv(folderPath + fileName)
        allFileData = pd.concat([allFileData, singleFileData])

    return allFileData


submissionData = loadDataSet(submission_dataPath)
commentsData = loadDataSet(comments_dataPath)

allSubredditIds = np.union1d(submissionData['subreddit_id'], commentsData['subreddit_id'])
print(f"Number of different subreddits: {len(allSubredditIds)}")

# It is possible to have "[deleted]" as author name
submissionFilter = submissionData["author"] != "[deleted]"
commentsFilter = commentsData["author"] != "[deleted]"

filteredSubmissions = submissionData[submissionFilter]
filteredComments = commentsData[commentsFilter]

allData = pd.concat([filteredSubmissions, filteredComments])

commentsPerSubreddit = commentsData.groupby(["subreddit_id"]).size().reset_index(name="counts")
print(commentsPerSubreddit.sort_values("counts", ascending=False)[:10])

# count users per subreddit ID
# subredditId - author - countInteractions
interactionsPerAuthorPerSubreddit = allData.groupby(["subreddit_id", "author"]).size().reset_index(name="counts")
# subredditId - countAuthors
authorsPerSubreddit = interactionsPerAuthorPerSubreddit.groupby(["subreddit_id"]).size().reset_index(name="counts")
print(authorsPerSubreddit.sort_values("counts", ascending=False)[:10])

print(f"AVG number users per subreddit:\n{authorsPerSubreddit['counts'].sum() / len(allSubredditIds)}")

submissionsPerAuthor = filteredSubmissions.groupby(['author']).size().reset_index(name='counts')
commentsPerAuthor = filteredComments.groupby(['author']).size().reset_index(name='counts')
print(f"Max submissions per author:\n{submissionsPerAuthor.sort_values('counts', ascending=False)[:10]}")
print(f"Max comments per author:\n{commentsPerAuthor.sort_values('counts', ascending=False)[:10]}")

# author - subreddit - count interactions
interactionsPerSubredditPerAuthor = allData.groupby(['author', 'subreddit_id']).size().reset_index(name='counts')
# author - count subreddits
subredditsPerAuthor = interactionsPerSubredditPerAuthor.groupby(['author']).size().reset_index(name='counts')
print(f"Subreddits per author:\n{subredditsPerAuthor.sort_values('counts', ascending=False)[:10]}")
