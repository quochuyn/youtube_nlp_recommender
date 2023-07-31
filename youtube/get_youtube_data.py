# get_youtube_data.py

# data science
import numpy as np
import pandas as pd

# youtube api
import googleapiclient.discovery

# utils
import tomli
from typing import Union
from .youtube_utils import convert_isodate_to_seconds, get_value_from_key
from .transcripts import get_video_transcript, get_video_transcripts



def get_youtube_api_key() -> str:
    r"""
    Returns
    -------
    api_key : str
        The Youtube API key created in Google Cloud by following the instructions on
        the API overview page: https://developers.google.com/youtube/v3/getting-started
    """

    with open('./youtube/secrets.toml', 'rb') as read_file:
        secrets = tomli.load(read_file)
    
    return secrets['api']['key1']



def make_client(api_key: str) -> googleapiclient.discovery.Resource:
    r"""
    Create a Youtube API client for making API requests.

    Parameters
    ----------
    api_key : str
        The Youtube API key created in Google Cloud by following the instructions on 
        the API overview page: https://developers.google.com/youtube/v3/getting-started

    Returns
    -------
    youtube : googleapiclient.discovery.Resource
        The Youtube API client which calls methods for requesting API content.
    """

    # Creates a YouTube API client for use in subsequent requests
    # User's API key is only needed once to create the client

    youtube = googleapiclient.discovery.build(
        serviceName='youtube', 
        version='v3', 
        developerKey = api_key
    )

    return youtube



def search_youtube(
        youtube : googleapiclient.discovery.Resource, 
        query : str,
        max_vids : int = 50,
        order : str = 'relevance',
        comments : bool = False,
        max_comments : int = 20,
        transcripts : bool = False,
        verbose : bool = True,
    ) -> pd.DataFrame:

    r"""
    Perform a Youtube `search` on a string query. The quota cost of this 
    method depends on the `max_vids` and `comments` parameters. 
    
    Each Youtube search call only return 50 results at a single time. Thus, a call 
    to this method has a quota cost of (100 + 1) * ceil(`max_vids` / 50) units. 
    The 100 and 1 costs refer to the `search` and `videos` methods, respectively.
    (e.g., max_vids==40 && comments==False -> (100 + 1) * ceil(40 / 50) = 101 units
           max_vids==80 && comments==False -> (100 + 1) * ceil(80 / 50) = 202 units)

    If `comments`==True, then we incur an additional quota cost equal to the number
    of videos being pulled.
    (e.g., max_vids==40 && comments==True -> 101 + 40 = 141 units
           max_vids==80 && comments==True -> 202 + 80 = 282 units)

    Parameters
    ----------
    youtube : googleapiclient.discovery.Resource
        The Youtube API client which calls methods for requesting API content.
    query : str
        The Youtube search query.
    max_vids : int, default=50
        The max number of videos to return from search.
    order : str, default='relevance'
        The metric to order the search results. Acceptable values are
        ['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'].
    comments : bool, default=False
        Boolean value whether to grab the video comments (if available).
    max_comments : int, default=100
        The max number of comments to return from each video. Requires
        `comments`==True.
    transcripts : bool, default=False
        Boolean value whether to grab the video transcripts (if available).
    verbose : bool, default=True
        Boolean value that controls the verbosity, the messages displayed.
        
    Returns
    -------
    df : pd.DataFrame
        The pandas DataFrame of video data returned by search.
    """

    if order not in ['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount']:
        raise ValueError(f"Value for order ({order}) is not one of the acceptable values.")

    if verbose:
        print(f"Searching for: {query}")

    # list for each row
    video_list = [] 

    # counter for number of videos searched so far 
    num_vids_searched = 0 
    while num_vids_searched < max_vids:

        # list for video ids (need to obtain extra info not present in search)
        video_ids = []  

        # one search page can at most return 50 results
        num_results = min(max_vids, 50)

        # if first page of search
        if num_vids_searched == 0:
            # search by query
            search_response = youtube.search().list(
                part='snippet',
                q=query,
                maxResults=num_results,
                order=order,
                type='video',           # restrict to videos only (instead of also channels and playlists)
                relevanceLanguage='en', # english only
            ).execute()
        else:
            # search by query, but specify the page token
            search_response = youtube.search().list(
                part='snippet',
                q=query,
                pageToken=next_page_token,
                maxResults=num_results,
                order=order,
                type='video',           # restrict to videos only (instead of also channels and playlists)
                relevanceLanguage='en', # english only
            ).execute()

        # loop through search results
        for video in search_response['items']:
            video_snippet = video['snippet']
            video_values = {
                'video_id' : get_value_from_key(video, ['id', 'videoId']),
                'published_at' : get_value_from_key(video_snippet, 'publishedAt'),
                'channel_id' : get_value_from_key(video_snippet, 'channelId'),
                'title' : get_value_from_key(video_snippet, 'title'),
                'description' : get_value_from_key(video_snippet, 'description'),
                'channel_title' : get_value_from_key(video_snippet, 'channelTitle'),
                'live_broadcast_content' : get_value_from_key(video_snippet, 'liveBroadcastContent'),
                'thumbnail_default_url' : get_value_from_key(video_snippet, ['thumbnails', 'default', 'url']),
                'thumbnail_medium_url' : get_value_from_key(video_snippet, ['thumbnails', 'medium', 'url']),
                'thumbnail_high_url' : get_value_from_key(video_snippet, ['thumbnails', 'high', 'url']),
            }

            if comments == True:
                # TODO: Handle grabbing more than 100 comments
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_values['video_id'],
                    maxResults=max_comments, # grab at most 100 to reduce quota usage
                    order='relevance',       # default is 'time'
                ).execute()

                comments_list = []
                for comment in comments_response['items']:
                    comment_text = get_value_from_key(comment, ['snippet', 'topLevelComment', 'snippet', 'textOriginal'])
                    if comment_text is not np.NaN:
                        comments_list.append(comment_text)
                
                video_values['comments'] = comments_list

            video_list.append(video_values)
            video_ids.append(video_values['video_id'])

        # grab list of videos
        # NOTE: We execute 1 call to youtube.videos() by passing the entire list of video ids.
        #       This lowers our quota usage if we were to do a call for each video id.
        videos_response = youtube.videos().list(
            part=['snippet', 'contentDetails', 'statistics'],
            id=video_ids,
        ).execute()

        # loop through list of videos
        for index, video in enumerate(videos_response['items']):
            video_snippet = video['snippet']
            video_content_details = video['contentDetails']
            video_statistics = video['statistics']

            # update video values to include extra info
            extra_video_values = {
                'thumbnail_standard_url' : get_value_from_key(video_snippet, ['thumbnails', 'standard', 'url']),
                'thumbnail_maxres_url' : get_value_from_key(video_snippet, ['thumbnails', 'maxres', 'url']),
                'tags' : get_value_from_key(video_snippet, 'tags'),
                'video_category_id' : get_value_from_key(video_snippet, 'categoryId'),
                'video_duration' : get_value_from_key(video_content_details, 'duration'),
                'video_caption' : get_value_from_key(video_content_details, 'caption'),
                'video_view_count' : get_value_from_key(video_statistics, 'viewCount'),
                'video_like_count' : get_value_from_key(video_statistics, 'likeCount'),
                'video_comment_count' : get_value_from_key(video_statistics, 'commentCount'),
            }
            video_list[index+num_vids_searched].update(extra_video_values)
        
        next_page_token = search_response['nextPageToken']
        num_vids_searched += num_results

    df = pd.DataFrame(video_list)

    df = _clean_youtube_df(df)

    # getting transcripts takes a while
    if transcripts == True:
        df.loc[:,'transcript'] = df['video_id'].apply(get_video_transcript)

    if verbose:
        print(f"Returning {df.shape[0]} results")

    return df



def _clean_youtube_df(youtube_df : pd.DataFrame) -> pd.DataFrame:
    r"""
    Clean the Youtube data frame.
    """

    # convert the `video_duration` (ISO 8601 duration string) into seconds.
    youtube_df.loc[:,'video_duration'] = youtube_df['video_duration'].apply(
        lambda x: convert_isodate_to_seconds(x) if isinstance(x, str) else x
    )

    # remove videos with missing `video_id`
    youtube_df = youtube_df.dropna(subset=['video_id'], ignore_index=True)

    # fix `video_caption` into actual boolean type
    youtube_df.loc[:,'video_caption'] = youtube_df['video_caption'].apply(
        lambda x: (x == 'true') if x is not np.NaN else False
    )

    # define `is_comments_enabled`, `is_live_content`, and `NoCommentsBinary`
    youtube_df.loc[:,'is_comments_enabled'] = youtube_df['video_comment_count'].apply(
        lambda x: ((int(x) > 0) * 1) if x is not np.NaN else 0
    )
    youtube_df.loc[:,'is_live_content'] = youtube_df['live_broadcast_content'].apply(
        # `live_broadcast_content` takes on only 3 values: 'live', 'upcoming', or 'none'
        lambda x: 1 if x in ['live', 'upcoming'] else 0
    )
    youtube_df.loc[:,'NoCommentsBinary'] = youtube_df['is_comments_enabled'].apply(
        lambda x: ((not x) * 1) if x is not np.NaN else x
    )

    # fix dtypes
    youtube_df = youtube_df.astype({
        'video_caption' : 'bool',
        'video_category_id' : 'int64',
        'video_duration' : float,
        'video_view_count' : float,
        'video_like_count' : float,
        'video_comment_count' : float,
    })

    return youtube_df


