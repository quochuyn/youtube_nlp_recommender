#Goal: Take in a user's input on what to filter and list of videos from the YouTube API
# that match the primary query and then return the remaining video URLS that match the filter


#Example Here a user wants to filter out political videos
#Query: Patrick Bet David

#Filter Out: Politics

#https://huggingface.co/sentence-transformers

from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity



def filter_out_embed(model, filter_sent : str, list_of_videos : list, threshold : int = 0.19):
    r"""
    Takes in a filter sentence and a list of video string titles and returns
    video titles that are less than 0.19 cosine similarity.
    
    Parameters
    ----------
    model : sentence_transformers.SentenceTransformer.SentenceTransformer
        The HuggingFace Senctence Transformer language model to perform
        encoding of the text.
    filter_sent : str
        The filter sentence written in natural language to remove from the youtube
        search query.
    list_of_videos : list
        The list of titles to be encoded by the `model`.
    threshold : int, default=0.19
        The threshold to filter videos by cosine similarity comparison.

    Returns
    -------
    results : list
        The list of titles left after the filter pass.
    """

    results = []
    #Compute embedding for both lists
    embedding_filter= model.encode(filter_sent, convert_to_tensor=True)
    for i in list_of_videos:
        embedding_uniq_vid = model.encode(i, convert_to_tensor=True)
        result = util.pytorch_cos_sim(embedding_filter, embedding_uniq_vid)
       # print(result,i)
        if result.item()<threshold:
            results.append(i)
    # print(results,"yea")##
    return results

"""
#A threshold of 0.19 would be perfect here

Are the following similar to "politics"

Cosine Similarity ----- Title to Compare to --- Label

tensor([[0.3055]]) The Truth About The 2020 Election  --- Should be Politics
tensor([[0.2883]]) Who'se Really Supporting Russia --- Should be Politics
tensor([[0.2119]]) The Evolution of Alex Jones  --- Should be Politics
tensor([[0.1958]]) The Perfect Hillary Clinton Analogy  --- Should be Politics
tensor([[0.1542]]) Kobe Bryant's Last Great Interview
tensor([[0.0648]]) Patrick Bet David on The Breakfast Club

"""



if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    import os
    import sys
    import youtube.get_youtube_data as get_youtube_data

    sys.path.insert(0, os.getcwd())


    #these sentences have no words in common yet they are semantically similar
    #they should have a higher cosine similarity than a noisy pair of sentences

    #based on these basic examples, we can start with a min threshold of 0.3
    filter_sent = "Politics"
    list_of_videos = ["Who'se Really Supporting Russia","The Perfect Hillary Clinton Analogy","The Evolution of Alex Jones",\
                    "Patrick Bet David on The Breakfast Club","The Truth About The 2020 Election","Kobe Bryant's Last Great Interview"]
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    #for this example will return ['Patrick Bet David on The Breakfast Club', 'Kobe Bryant’s Last Great Interview']
    print(filter_out_embed(model,filter_sent,list_of_videos))

    YOUTUBE_API_KEY = get_youtube_data.get_youtube_api_key()
    youtube = get_youtube_data.make_client(YOUTUBE_API_KEY)
    youtube_df = get_youtube_data.search_youtube(
        youtube,
        query='Patrick Bet David',
        max_vids=15,        # youtube accepts 50 as the max value
        order='relevance'   # default is relevance
    )

    titles = youtube_df['title'].tolist()
    print("titles:",titles)
    print("api test")
    print(filter_out_embed(model,filter_sent,titles))

    print(type(model))
