import openai
import tiktoken
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np

openai.api_key = ""
embedding = openai.Embedding.create(
    input="Your text goes here", model="text-embedding-ada-002"
)["data"][0]["embedding"]

def search_titles(df, query, n=3, pprint=True):
    product_embedding = get_embedding(
        query,
        engine="text-embedding-ada-002"
    )
    for x in df:
        result = cosine_similarity(get_embedding(
            x,
            engine="text-embedding-ada-002"
        ), product_embedding)
        print(result,x)

            
titles = []
#embedding_model = "text-embedding-ada-002"
#åembedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002

#filter_sent = "Politics (from Ancient Greek πολιτικά (politiká) 'affairs of the cities') is the set of activities that are associated with making decisions in groups, or other forms of power relations among individuals, such as the distribution of resources or status. The branch of social science that studies politics and government is referred to as political science."
#titles = ["Whose Really Supporting Russia","The Perfect Hillary Clinton Analogy","The Evolution of Alex Jones",\
        # #      "Patrick Bet David on The Breakfast Club","The Truth About The 2020 Election","Kobe Bryant's Last Great Interview","Curry hour","The thing that's great about this job is the time sourcing the items involves no traveling. I just look online to buy it. It's really as simple as that. While everyone else is searching for what they can sell, I sit in front of my computer and buy better stuff for less money and spend a fraction of the time doing it.","Meanwhile, on the other side of the planet, a bustling metropolis thrived with energy and creativity. Skyscrapers reached for the heavens, their glass facades reflecting a tapestry of cultures and traditions. In the heart of the city, a vibrant street festival brought people together from all walks of life. Colorful parades meandered through the streets, accompanied by the infectious beats of drums and the melodies of diverse instruments. Food stalls lined the pavements, tantalizing passersby with an array of exotic cuisines, from sizzling kebabs to delicate sushi rolls."]
#df = pd.DataFrame(titles, columns=['embedding'])
filter_sent = "political"
titles = ["ok test","quality","here","ok test"]

#results = search_titles(titles, filter_sent, n=3,model='ada002')
#results = search_titles(titles, filter_sent, n=3,model='gpt4')
def search_gpt4():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model="gpt-4",
        messages=[
            {
            "role": "system",
            ##"content": f"You will be provided with statements,and you will answer as a python list of true and false ie: [True, False, True]. Which of these are {filter_sent} and which are not"

            "content": f"Which of these can be characterized as {filter_sent} and which are not \
              Answer as a python list of true and false ie: [True, False, True...etc]"
            },
            {
            "role": "user",
            "content": "The Truth About The 2020 Election\n"
        "Who's Really Supporting Russia\n"
        "The Evolution of Alex Jones\n"
        "The Perfect Hillary Clinton Analogy\n"
        "Kobe Bryant's Last Great Interview\n"
        "Patrick Bet David on The Breakfast Club"
            }
        ],
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    return response.choices[0]["message"]["content"]


print(search_gpt4())
