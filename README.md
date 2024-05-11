# football-analysis-channels
# introduction| business problem:
YouTube has evolved into the world's largest video-sharing platform, with over 2 billion logged-in monthly users who collectively watch more than 1 billion hours of video every day.
In today's data-driven world, businesses face a challenge on YouTube: figuring out what really makes videos successful. There are lots of ideas out there, like longer videos being better or posting more often. But what's the truth? A data analyst can help by looking at the numbers, separating fact from fiction, and showing creators how to make videos that people really want to watch.

# Data Acquisition:
By get benefit from  the power of YouTube's API with advanced data retrieval techniques, I extracted valuable insights from the platform's vast repository of user interactions and video metrics. By querying the API endpoints for specific data points such as view counts, likes, comments, and subscriber data, I curated a comprehensive dataset to fuel informed decision-making and strategic content optimization.

# Questions:
1-Does the number of likes and comments matter for a video to get more views?

2-Does the video duration matter for views and interaction (likes/ comments)?

3-Does title length matter for views?

4-How many tags do good performing videos have? What are the common tags among these videos?

5-Across all the creators I take into consideration, how often do they upload new videos? On which days in the week?, on which hours in the day?

# Data preparation:
1-checking null values in columns

2-adding published Day column by extracting day name from date column

3-adding duration in second by converting unknown duration column like(PT16M37S) to second

4-adding tag count and title length columns for more analysis

5-adding two kpis column for viewers engagement likes ratio and comment ratio per 1k views  

# tools used:

1. Pandas: The go-to tool for data wrangling, making tasks like data cleaning, manipulation, and analysis seamless and efficient.

2. Seaborn and Matplotlib: These libraries provide powerful visualization capabilities, enabling the creation of insightful plots and charts for data exploration and presentation.

3. YouTube API: A gateway for accessing YouTube's vast data resources programmatically, allowing for the extraction and analysis of video, channel, and user data.

4. Git and GitHub: Essential for version control and collaboration in software development projects.


# insights(conclusions):

1. More likes and comments usually mean more views, though it's not always a direct cause-and-effect relationship. Getting lots of likes can boost your video's appeal ("social proof").

2. Make sure to tag your videos well—around 5 to 30 tags usually hits the sweet spot between visibility and relevance.

3. Keep your video titles neither too short nor too long. Aim for titles with 30 to 70 characters to attract the most views.

4. Surprisingly, there's no magic formula for the best days to upload videos. So, focus on consistency rather than specific upload days, but we can see that the best time is in 9 and 10 pm to get more views .




