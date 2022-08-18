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


def groupby_count(data_frame, groupby_list):
    return data_frame.groupby(groupby_list).size().reset_index(name="counts")


def groupby_count_sorted(data_frame, groupby_list):
    return groupby_count(data_frame, groupby_list).sort_values('counts', ascending=False)


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

commentsPerSubreddit = groupby_count_sorted(commentsData, ["subreddit_id"])
print(f"Comments per subreddit:\n{commentsPerSubreddit[:10]}")

# count users per subreddit ID
# subredditId - author - countInteractions
interactionsPerAuthorPerSubreddit = groupby_count(allData, ["subreddit_id", "author"])
# subredditId - countAuthors
authorsPerSubreddit = groupby_count_sorted(interactionsPerAuthorPerSubreddit, ["subreddit_id"])
print(f"Authors per subreddit:\n{authorsPerSubreddit[:10]}")

print(f"AVG number users per subreddit:\n{authorsPerSubreddit['counts'].sum() / len(allSubredditIds)}")

submissionsPerAuthor = groupby_count_sorted(filteredSubmissions, ['author'])
commentsPerAuthor = groupby_count_sorted(filteredComments, ['author'])
print(f"Max submissions per author:\n{submissionsPerAuthor[:10]}")
print(f"Max comments per author:\n{commentsPerAuthor[:10]}")

# author - subreddit - count interactions
interactionsPerSubredditPerAuthor = groupby_count(allData, ['author', 'subreddit_id'])
# author - count subreddits
subredditsPerAuthor = groupby_count_sorted(interactionsPerSubredditPerAuthor, ['author'])
print(f"Subreddits per author:\n{subredditsPerAuthor[:10]}")
