# get_youtube_data.py

# data science
import numpy as np
import pandas as pd

# youtube api
import googleapiclient.discovery

# utils
import tomli
import utils



def get_youtube_api_key() -> str:
    r"""
    Returns
    -------
    api_key : str
        The Youtube API key created in Google Cloud by following the instructions on
        the API overview page: https://developers.google.com/youtube/v3/getting-started
    """


    with open('./secrets.toml', 'rb') as read_file:
        secrets = tomli.load(read_file)
    
    return secrets['api']['key1']



def get_youtube_api_key_list() -> list[str]:
    r"""
    Returns
    -------
    api_key_list : list[str]
        A list of Youtube API keys to be cycled through to not hit 10,000 credit daily 
        quota. Instructions for creating a key in Google Cloud can be found on the API
        overview page: https://developers.google.com/youtube/v3/getting-started
    """

    with open('./secrets.toml', 'rb') as read_file:
        secrets = tomli.load(read_file)
    
    # return only key values
    return [v for k,v in secrets['api'].items() if 'key' in k.lower()]



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
    ) -> pd.DataFrame:

    r"""
    Perform a youtube search on a string query. A call to this method has a quota
    cost of 100 + 1 = 101 units (search + videos).

    Parameters
    ----------
    youtube : googleapiclient.discovery.Resource
        The Youtube API client which calls methods for requesting API content.
    query : str
        The youtube search query.
    max_vids : int, default=50
        The max number of videos to return from search.
    order : str, default='relevance'
        The metric to order the search results. Acceptable values are
        ['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'].
        
    Returns
    -------
    df : pd.DataFrame
        The pandas DataFrame of video data returned by search.
    """

    assert 0 < max_vids <= 50, f"Value for max_vids ({max_vids}) is not within range of acceptable values."
    assert order in ['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'], f"Value for order ({order}) is not one of the acceptable values."

    # search by query
    search_response = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=max_vids,
        order=order,
        relevanceLanguage='en' # english only
    ).execute()

    # loop through search results
    video_ids = []  # list for video ids (need to obtain extra info not present in search)
    video_list = [] # list for each row
    for video in search_response['items']:
        video_snippet = video['snippet']
        video_values = {
            'video_id' : video['id']['videoId'],
            'published_at' : video_snippet['publishedAt'],
            'channel_id' : video_snippet['channelId'],
            'title' : video_snippet['title'],
            'description' : video_snippet['description'],
            'channel_title' : video_snippet['channelTitle'],
            'thumbnail_default_url' : video_snippet['thumbnails']['default']['url'],
            'thumbnail_medium_url' : video_snippet['thumbnails']['medium']['url'],
            'thumbnail_high_url' : video_snippet['thumbnails']['high']['url'],
        }
        video_list.append(video_values)
        video_ids.append(video['id']['videoId'])

    # grab list of videos
    # NOTE: We execute 1 call to youtube.videos() by passing the entire list of video ids.
    #       This lowers our quota usage if we were to do a call for each video id.
    videos_response = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_ids,
    ).execute()

    # loop through list of videos
    for index, video in enumerate(videos_response['items']):
        video_snippet = video['snippet']
        video_content_details = video['contentDetails']
        video_statistics = video['statistics']

        # update video values to include extra info
        extra_video_values = {
            'thumbnail_standard_url' : video_snippet['thumbnails']['standard']['url'],
            'thumbnail_maxres_url' : video_snippet['thumbnails']['maxres']['url'],
            'tags' : video_snippet['tags'] if 'tags' in video_snippet.keys() else '[]',
            'video_duration' : video_content_details['duration'],
            'video_caption' : video_content_details['caption'],
            'video_view_count' : video_statistics['viewCount'],
            'video_like_count' : video_statistics['likeCount'],
            'video_comment_count' : video_statistics['commentCount']
        }
        video_list[index].update(extra_video_values)

    # TODO: get video transcripts if video_caption == True
    
    df = pd.DataFrame(video_list)

    df = _clean_youtube_df(df)

    return df



def _clean_youtube_df(youtube_df):
    r"""
    Clean the youtube data frame.
    """

    # convert the video_duration (ISO 8601 duration string) into seconds.
    youtube_df.loc[:,'video_duration'] = youtube_df['video_duration'].apply(utils.convert_isodate_to_seconds)

    return youtube_df


