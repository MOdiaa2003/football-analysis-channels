#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


#function is used to create service objects for interacting with Google APIs.
from googleapiclient.discovery import build
import numpy as np
import pandas as pd
from dateutil import parser
import isodate
# Data visualization libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
sns.set(style="darkgrid", color_codes=True)


# In[2]:


api_key='AIzaSyBUNicTGDknr5Y0wwWfC4XPKgxsnusfuk0'


# In[3]:


channel_ids=['UC9c89meMU-ES5hb3CVAgIjQ'
             ,'UCyzSRvqm6AVuNtYOMNYEA0Q'
             ,'UCAIxr4DpLZH-Iih4mlbLjiA'
             ,'UC0j1bJUOS_utB8q618YJ5Bw'
             ,'UCxUPU7lI249SW_j5WgByJRA'
             ,'UCKrzNQINh6mc03WbgMA5EGA'
             ,'UC_j8JjshK56_Ds5FCfsin8A'
             ,'UCrMd6lrIFEniqb_J1_p_Q7g'
             ,'UCvRbdoDaIeiY6umPJg1L0KA']


# In[4]:


# Set the name of the API service we want to use to "youtube"
api_service_name = "youtube"

# Set the version of the API we want to use to "v3"
api_version = "v3"

# Use the build function to create a client for interacting with the YouTube Data API
# - developerKey: The API key used for authentication and authorization
# The resulting 'youtube' object can be used to make requests to the YouTube Data API
youtube = build(api_service_name, api_version, developerKey=api_key)


# #### Bring some info for channels (channelName,#_subscribers,#_views,totalVideos,playlistId)

# In[5]:


def get_channel_stats(youtube, channel_ids):
    """
    Get channel statistics
    Params:
    ------
    youtube: build object of Youtube API
    channel_ids: list of channel IDs
     ------
    Returns:
    dataframe with all channel stats for each channel ID
    """
    all_data = []  # Initialize an empty list to store channel statistics
    
    try:  # Start a try-except block to handle potential exceptions
        request = youtube.channels().list(  # Create a request object for the YouTube API
            part="snippet,contentDetails,statistics",  # Specify the parts of the channel data to retrieve
            id=','.join(channel_ids)  # Combine the channel IDs into a single string separated by commas
        )
        response = request.execute()  # Execute the API request and get the response

        # Check if 'items' key exists in the response
        if 'items' in response:  # If the 'items' key exists in the response dictionary(check if channels exists)
            # Loop through each item in the 'items' list
            for item in response['items']:
                data = {  # Create a dictionary to store channel statistics
                    'channelName': item['snippet']['title'],  # Get the channel name from the 'snippet' part
                    'subscribers': item['statistics']['subscriberCount'],  # Get the subscriber count
                    'views': item['statistics']['viewCount'],  # Get the total views count
                    'totalVideos': item['statistics']['videoCount'],  # Get the total videos count
                    'playlistId': item['contentDetails']['relatedPlaylists']['uploads']  # Get the upload playlist ID
                }
                all_data.append(data)  # Append the channel statistics dictionary to the list
        else:
            print("No channels found for the given IDs.")  # Print a message if no channels are found in the response
    except Exception as e:  # Catch any exceptions that occur during the API request or response processing
        print(f"An error occurred: {str(e)}")  # Print the error message
        return None  # Return None to indicate that the operation was unsuccessful
    
    return pd.DataFrame(all_data)  # Convert the list of channel statistics dictionaries into a DataFrame and return it


# In[6]:


ch_stats=get_channel_stats(youtube,channel_ids)


# In[7]:


# Convert count columns to numeric columns
numeric_cols = ['subscribers', 'views', 'totalVideos']
ch_stats[numeric_cols] = ch_stats[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Sort the DataFrame 'ch' by the 'views' column in descending order,
# and modify 'ch' in place (inplace=True)
ch_stats.sort_values(by='subscribers', ascending=False, inplace=True)

# Display the sorted DataFrame 'ch'
ch_stats


# #### bring video's_id of each channel to get statistics 

# In[8]:


def get_video_ids(youtube, playlist_id):
    """
    Get list of video IDs of all videos in the given playlist
    
    Params:
    ------
    youtube: The build object from googleapiclient.discovery
             This object allows making requests to the YouTube Data API.
    
    playlist_id: Playlist ID of the channel
    
    Returns:
    -------
    List of video IDs of all videos in the playlist
    """
    
    # Create a request to retrieve playlist items from the specified playlist
    request = youtube.playlistItems().list(
                part='contentDetails',           # Request the 'contentDetails' part of each playlist item
                playlistId=playlist_id,          # Specify the playlist ID to retrieve items from
                maxResults=50)                   # Set the maximum number of results per page to 50
    
    # Execute the request and store the response
    response = request.execute()
    
    # Initialize an empty list to store the video IDs
    video_ids = []
    
    # Extract video IDs from the response and append them to the video_ids list
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    # Get the 'nextPageToken' from the response (if it exists)
    next_page_token = response.get('nextPageToken')
    
    # Initialize a flag to indicate whether there are more pages of results
    more_pages = True
    
    # Continue retrieving additional pages of results until there are no more pages
    while more_pages:
        # If there is no 'nextPageToken', there are no more pages
        if next_page_token is None:
            more_pages = False
        else:
            # Create a new request for the next page of results using the 'nextPageToken'
            request = youtube.playlistItems().list(
                        part='contentDetails',     # Request the 'contentDetails' part of each playlist item
                        playlistId=playlist_id,    # Specify the playlist ID
                        maxResults=50,             # Set the maximum number of results per page to 50
                        pageToken=next_page_token) # Specify the 'nextPageToken' to retrieve the next page
            
            # Execute the request and store the response
            response = request.execute()
    
            # Extract video IDs from the response and append them to the video_ids list
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            # Get the 'nextPageToken' from the response for the next iteration
            next_page_token = response.get('nextPageToken')
        
    # Return the list of video IDs
    return video_ids


# In[9]:


playlist_id='UUxUPU7lI249SW_j5WgByJRA'
v_ids=get_video_ids(youtube, playlist_id)


# In[10]:


len(v_ids)


# #### bring some details from each  channel by get video's ids of each channel by get_video_ids func

# In[11]:


def get_video_details(youtube, video_ids):
    """
    Get video statistics of all videos with given IDs
    
    Params:
    ------
    youtube: The build object from googleapiclient.discovery
             This object allows making requests to the YouTube Data API.
    
    video_ids: List of video IDs
    
    Returns:
    -------
    DataFrame with statistics of videos, i.e.:
        'channelTitle', 'title', 'description', 'tags', 'publishedAt'
        'viewCount', 'likeCount', 'favoriteCount', 'commentCount'
        'duration', 'definition', 'caption'
    """
    
    # Initialize an empty list to store information about all videos
    all_video_info = []
    
    # Iterate over the list of video IDs in chunks of 50 (YouTube API's maximum limit)
    # increasing by 50 at each step until it reaches the length of the video_ids
    for i in range(0, len(video_ids), 50):
        # Create a request to retrieve details for multiple videos at once
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",  # Request the 'snippet', 'contentDetails', and 'statistics' parts
            id=','.join(video_ids[i:i+50])             # Specify the IDs of the videos to retrieve details for
            #it will handle case when i reach become close to i+50>len(video_ids) to reset i+50 into len(video_ids) without any errors
        )
        # Execute the request and store the response
        response = request.execute() 

        # Iterate over each video in the response
        for video in response['items']:
            # Define the keys and values to keep from the response
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            # Create a dictionary to store information about the current video
            video_info = {}
            # Store the video ID in the dictionary
            video_info['video_id'] = video['id']

            # Iterate over each key (snippet, statistics, contentDetails) and its corresponding values
            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    # Try to extract the specified value from the response and store it in the dictionary
                    # If the value does not exist or an error occurs, set it to None
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            # Append the dictionary containing information about the current video to the list
            all_video_info.append(video_info)
            
    # Convert the list of dictionaries into a DataFrame and return it
    return pd.DataFrame(all_video_info)


# In[12]:


v_details=get_video_details(youtube, v_ids)
len(v_details)


# #### bring some comments from each  video by get video's ids of each channel by get_video_ids func

# In[13]:


def get_comments_in_videos(youtube, video_ids):
    """
    Get top level comments as text from all videos with given IDs (only the first 10 comments due to quote limit of Youtube API)
    
    Params:
    ------
    youtube: The build object from googleapiclient.discovery.
             This object allows making requests to the YouTube Data API.
    
    video_ids: List of video IDs.
    
    Returns:
    -------
    DataFrame with video IDs and associated top level comment in text.
    """
    
    # Initialize an empty list to store information about all comments
    all_comments = []
    
    # Iterate over each video ID in the list of video IDs
    for video_id in video_ids:
        try:   
            # Create a request to retrieve comment threads for the specified video
            request = youtube.commentThreads().list(
                part="snippet,replies",  # Request the 'snippet' and 'replies' parts of each comment thread
                videoId=video_id         # Specify the video ID to retrieve comment threads for
            )
            # Execute the request and store the response
            response = request.execute()
        
            # Extract the text of the top-level comments from the response (only the first 10 comments)
            comments_in_video = [comment['snippet']['topLevelComment']['snippet']['textOriginal'] for comment in response['items'][0:10]]
            
            # Create a dictionary to store information about the comments in the current video
            comments_in_video_info = {'video_id': video_id, 'comments': comments_in_video}

            # Append the dictionary containing information about the comments to the list
            all_comments.append(comments_in_video_info)
            
        except: 
            # Catch any errors that occur (most likely because comments are disabled on a video)
            print('Could not get comments for video ' + video_id)
        
    # Convert the list of dictionaries into a DataFrame and return it
    return pd.DataFrame(all_comments)   


# In[14]:


c_details= get_comments_in_videos(youtube, v_ids)
c_details


# ##### let's take a look at # of subscribers per channel to see distribution of values across channels

# In[15]:



# Set the figure size
plt.figure(figsize=(10, 8))

# Create the bar plot x-axis for channel name,y-axis for # subscribers both come from ch_stats dataframe 
#but sorting dataframe by # of subscribers in desc order
ax = sns.barplot(x='channelName', y='subscribers', data=ch_stats.sort_values('subscribers', ascending=False))

# Rotate the x-axis labels to easily read channel name instead of words overlapping
plot = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# Specify an Arabic font for the x-axis labels
plt.rcParams['font.family'] = 'Traditional Arabic'  

# Show the plot
plt.show()
#we face problem which is arabic words doesn't seem correct the order of letters reversed
# so we search and bring solution from stackoverflow 
#https://stackoverflow.com/questions/54064646/arabic-letters-arent-showing-correctly-in-the-plot/60279813#60279813?newreg=14ca23e9e8d848689f2ed754d0e4997d


# In[16]:


import arabic_reshaper  # Importing the arabic_reshaper module for reshaping Arabic text
from bidi.algorithm import get_display  # Importing the get_display function from the bidi.algorithm module for bidirectional text handling

reshaped = []  # Creating an empty list to store reshaped Arabic text

for item in ch_stats['channelName']:  # Iterating over each item (channel name) in the 'channelName' column of the DataFrame ch_stats
    reshaped_text = arabic_reshaper.reshape(item)  # Reshaping the Arabic text using the arabic_reshaper module
    bidi_text = get_display(reshaped_text)  # Converting the reshaped text into a format suitable for display using the get_display function
    reshaped.append(bidi_text)  # Appending the bidi_text to the list l


# Set the figure size
plt.figure(figsize=(10, 8))

# Create the bar plot x-axis for channel name,y-axis for # subscribers both come from ch_stats dataframe 
#but sorting dataframe by # of subscribers in desc order
ax = sns.barplot(x=reshaped, y='subscribers', data=ch_stats.sort_values('subscribers', ascending=False))

# Rotate the x-axis labels to easily read channel name instead of words overlapping
plot = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
#This line sets the y-axis tick labels to display values in millions (M) using a custom formatter.
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000000) + 'M'))
# Specify an Arabic font for the x-axis labels
plt.rcParams['font.family'] = 'Arial'  

# Show the plot
plt.show()    


# In[17]:


# we will look at  the total number of views of each channel
#The views is fairly similar to the subscriber count , mohamed adnan and saba7o korah remain
#the two most popular channels considering both subscribers and views.


# In[18]:


# Set the figure size
plt.figure(figsize=(10, 8))

# Create the bar plot x-axis for channel name,y-axis for # subscribers both come from ch_stats dataframe 
#but sorting dataframe by # of subscribers in desc order
ax = sns.barplot(x=reshaped, y='views', data=ch_stats.sort_values('views', ascending=False))

# Rotate the x-axis labels to easily read channel name instead of words overlapping
plot = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
#This line sets the y-axis tick labels to display values in millions (M) using a custom formatter.
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x/1000000) + 'M'))
# Specify an Arabic font for the x-axis labels
plt.rcParams['font.family'] = 'Arial'  

# Show the plot
plt.show()    


# In[19]:


# so we can say that when you uplod more videos you get more views and subscribers,we will check correlation


# ### Get video statistics for all the channels

# In[20]:


# Create a dataframe with video statistics  from all channels

video_df = pd.DataFrame()
comments_df = pd.DataFrame()

for c in ch_stats['channelName'].unique():
    print("Getting video information from channel: " + c)
    playlist_id = ch_stats.loc[ch_stats['channelName']== c, 'playlistId'].iloc[0]
    video_ids = get_video_ids(youtube, playlist_id)
    
    # get video data
    video_data = get_video_details(youtube, video_ids)
 

    #append video data together and comment data toghether
    video_df = video_df.append(video_data, ignore_index=True)
    


# In[21]:


video_df


# In[22]:


# Write video data to CSV file for future references
video_df.to_csv('video_data_top10_channels.csv')


# # Preprocessing & Transformation

# ##### To be able to make use of the data for analysis, we need to perform a few pre-processing steps. Firstly, I would like reformat some columns, especially the date and time columns such as "pushlishedAt" and "duration". In addition, I also think it is necessary to enrich the data with some new features that might be useful for understanding the videos' characteristics.

# ### Check for empty values

# In[23]:


video_df.isnull().any()


# ### Next, we need to check if the data type of the columns are correct. I have checked the data types and indeed some count columns such as view count and comment count are currently not in correct data type. In this step, we convert these count columns into integer.

# In[24]:


cols = ['viewCount', 'likeCount', 'favoriteCount', 'commentCount']
video_df[cols] = video_df[cols].apply(pd.to_numeric, errors='coerce', axis=1)


# #### go depeer  
# I want to go  for further analyses, for example:
# 
# create published date column with another column showing the day in the week the video was published, which will be useful for later analysis.
# 
# convert video duration to seconds instead of the current default string format
# 
# calculate number of tags for each video
# 
# calculate comments and likes per 1000 view ratio
# 
# calculate title character length

# In[25]:



# Assuming you have imported parser and video_df is your DataFrame

# Convert the 'publishedAt' column to datetime objects
video_df['publishedAt'] = pd.to_datetime(video_df['publishedAt'])

# Extract the day name and store it in a new column
video_df['pushblishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime("%A"))




# In[26]:


# convert duration to seconds
video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]')


# In[27]:


# Add number of tags
video_df['tagsCount'] = video_df['tags'].apply(lambda x: 0 if x is None else len(x))


# In[28]:


# Comments and likes per 1000 view ratio
video_df['likeRatio'] = video_df['likeCount']/ video_df['viewCount'] * 1000
video_df['commentRatio'] = video_df['commentCount']/ video_df['viewCount'] * 1000


# In[29]:


# Title character length
video_df['titleLength'] = video_df['title'].apply(lambda x: len(x))


# In[45]:


video_df['hour_published'] = video_df['publishedAt'].dt.hour


# ##### Let's look at the video dataset at this point to see if everything went well

# In[46]:


video_df


# # Exploratory analysis

# ### Views distribution per channel

# #####  now we can see how the views are distributed per channel. Some channels might have a lot of views on one of their videos and the rest do not receive many views. Other channels might have more evenly distribution views per video. It can be observed that first four plots from left  have quite large variance in their views, which indicates having higher views in few videos . the rest have less views overall but the views have constant rate  across videos.

# In[31]:


# Reshape Arabic text
reshaped_channel_titles = video_df['channelTitle'].apply(lambda x: arabic_reshaper.reshape(x))
# Convert reshaped text to displayable form
display_channel_titles = reshaped_channel_titles.apply(lambda x: get_display(x))


# In[32]:


plt.rcParams['figure.figsize'] = (18, 10)
sns.violinplot(display_channel_titles, video_df['viewCount'], palette='pastel')
plt.title('Views per channel', fontsize=7)

# Rotate x-axis labels by 45 degrees
plt.xticks(rotation=45)

plt.show()


# ### Does the number of likes and comments matter for a video to get more views?
# 

# ##### Firstly, I would like to check if comments and likes do correlate with how many views a video would get. In the plots below, it can be observed that the number of views and number of comments/ likes strongly correlated with each other. The number of likes seems to suggest stronger correlation than the number of comments. However, this is expected as the more people watching a video, the more likely this video will get comments and likes. To correct for this factor, we will plot these relationships again using the comments per 1000 view and likes per 1000 view ratios.

# In[41]:



# Create subplots
fig, ax = plt.subplots(1, 2)

# Plot the scatterplots
sns.scatterplot(data=video_df, x="commentCount", y="viewCount", ax=ax[0])
sns.scatterplot(data=video_df, x="likeCount", y="viewCount", ax=ax[1])

# Function to format y-axis labels
def format_yticks_millions(value, _):
    return '{:.0f}M'.format(value / 1000000)

# Apply the formatter to the y-axis of both subplots
for axis in ax:
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(format_yticks_millions))

# Show the plot
plt.show()


# ##### Now we will take a look at the correlation if we look at the comment ratio and like ratio instead of the absolute number.

# In[42]:


# Create subplots
fig, ax = plt.subplots(1, 2)

# Plot the scatterplots
sns.scatterplot(data=video_df, x="commentRatio", y="viewCount", ax=ax[0])
sns.scatterplot(data=video_df, x="likeRatio", y="viewCount", ax=ax[1])

# Function to format y-axis labels
def format_yticks_millions(value, _):
    return '{:.0f}M'.format(value / 1000000)

# Apply the formatter to the y-axis of both subplots
for axis in ax:
    axis.yaxis.set_major_formatter(ticker.FuncFormatter(format_yticks_millions))

# Show the plot
plt.show()


# ###### After correcting for the absolute number of views, it turns out that the correlation is much less clear. The comment-view relationship seems to completely disappear: a lot of videos have millions of views and very few comments, while some vides have very few views have better interaction. However, it is understandable that comments take more effort than views and likes, and normally comments would die off when the video gets older.As for like-view relatioship, we can still see some positive correlation between views and like ratio (though very subtle), which means that the more views a video has, the more people would hit the like button! This seems to support the idea of social proof, which means that people tend to like better the products that are already liked by many other people.

# ### Does the video duration matter for views and interaction (likes/ comments)?

# ##### As can be seen in the histogram below, most videos are between 300 to 1200 seconds, which is about 5 to 20 minutes. Here I have to limit the duration to 7,000 because of some really long videos (potentially streaming videos).
# so from this if we are content creator in this field i will do my videos between 7.5 to 20 min 
# 

# In[36]:


sns.histplot(data=video_df[video_df['durationSecs'] < 7000], x="durationSecs", bins=40)


# ##### Now we plot the duration against comment count and like count. It can be seen that actually shorter videos tend to get more likes and comments than very long videos.

# In[37]:


fig, ax =plt.subplots(1,2)
sns.scatterplot(data = video_df, x = "durationSecs", y = "commentCount", ax=ax[0])
sns.scatterplot(data = video_df, x = "durationSecs", y = "likeCount", ax=ax[1])


# ### Does title length matter for views?

# ##### There is no clear relationship between title length and views as seen the scatterplot below, but most-viewed videos tend to have average title length of 30-70 characters

# In[38]:


sns.scatterplot(data = video_df, x = "titleLength", y = "viewCount")


# ## Number of tags vs views

# ##### It seems that most videos have between 30 to 50 . The relationship between number of tags and view count is not clearly seen, but too few tags or too many tags do seem to correlate with fewer views

# In[39]:


sns.scatterplot(data = video_df, x = "tagsCount", y = "viewCount")


# ## Which day in the week are most videos uploaded?

# ##### It's interesting to see that more videos are uploaded on saturday , sunday,tuesday and wensday as pl ,la liga and champions league in this days .but it seems that Sunday,Monday and Tuesday is right and the rest were soo close to each other and not vary from others
# so we can say that there isn't any pattern for #_videos in each day

# In[44]:


day_df = pd.DataFrame(video_df['pushblishDayName'].value_counts())
weekdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_df = day_df.reindex(weekdays)
ax = day_df.reset_index().plot.bar(x='index', y='pushblishDayName', rot=0)


# In[51]:


day_df = pd.DataFrame(video_df['hour_published'].value_counts())
hours = [str(hour) for hour in range(24)]
# Plotting the bar plot
plt.bar(day_df.index.astype(str), day_df['hour_published'])

# Setting labels and title
plt.xlabel('Hour')
plt.ylabel('Count of Videos Published')
plt.title('Videos Published by Hour')

# Rotating x-axis labels for better readability
plt.xticks(rotation=45)

# Show plot
plt.show()


# ### Conclusions and future research ideas

# In this project, we have explored the video data of the 9 most popular football analysis channels in middle east and revealed many interesting findings for anyone who are starting out with a Youtube channel in football :
# 
# The more likes and comments a video has, the more views the video gets (it is not guaranteed that this is a causal relationship, it is simply a correlation and can work both way). Likes seem to be a better indicator for interaction than comments and the number of likes seem to follow the "social proof", which means the more views the video has, the more people will like it.
# 
# Most videos have between 5 and 30 tags.
# 
# Most-viewed videos tend to have average title length of 30-70 characters. Too short or too long titles seem to harm viewership.
# 
# there isn't any pattern or particular days  for uploding videos as the variance between the all days are 
# very low. 
# 
# Ideas for future research:
# 
# To expand and build on this research project, one can:
# 
# Expand the dataset to include more channels 
# 
# Do sentiment analysis on the comments and find out which videos get more positive comments and which videos get less positive comments
# 
# Do market research by analyzing questions in the comment threads and identifying common questions/ market gaps which could potentially filled
# 
