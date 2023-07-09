#Goal: Take in a user's input on what to filter and list of videos from the YouTube API
# that match the primary query and then return the remaining video URLS that match the filter


#Example
#Query: Patrick Bet David

#Filter Out: Politics

from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


#these sentences have no words in common yet they are semantically similar
#they should have a higher cosine similarity than a noisy pair of sentences

#based on these basic examples, we can start with a min threshold of 0.3
filter_sent = "Politics"
list_of_videos = ["Who'se Really Supporting Russia","The Perfect Hillary Clinton Analogy","The Evolution of Alex Jones",\
                  "Patrick Bet David on The Breakfast Club","The Truth About The 2020 Election","Kobe Bryant’s Last Great Interview"]
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
def filter_out(filter_sent,list_of_videos):
    #Compute embedding for both lists
    embedding_filter= model.encode(filter_sent, convert_to_tensor=True)
    for i in list_of_videos:
        embedding_uniq_vid = model.encode(i, convert_to_tensor=True)
        result = util.pytorch_cos_sim(embedding_filter, embedding_uniq_vid)
        print(result,i)
filter_out(filter_sent,list_of_videos)
"""
#A threshold of 0.19 would be perfect here
tensor([[0.2883]]) Who'se Really Supporting Russia --- Should be Politics
tensor([[0.1958]]) The Perfect Hillary Clinton Analogy  --- Should be Politics
tensor([[0.2119]]) The Evolution of Alex Jones  --- Should be Politics
tensor([[0.0648]]) Patrick Bet David on The Breakfast Club
tensor([[0.3055]]) The Truth About The 2020 Election  --- Should be Politics
tensor([[0.1542]]) Kobe Bryant’s Last Great Interview
"""