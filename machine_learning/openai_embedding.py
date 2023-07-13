import openai
openai.api_key = "YOUR_API_KEY"
embedding = openai.Embedding.create(
    input="Your text goes here", model="text-embedding-ada-002"
)["data"][0]["embedding"]
import tiktoken

from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
# search through the reviews for a specific product
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
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002

filter_sent = "Politics"
titles = ["Whose Really Supporting Russia","The Perfect Hillary Clinton Analogy","The Evolution of Alex Jones",\
                "Patrick Bet David on The Breakfast Club","The Truth About The 2020 Election","Kobe Bryant's Last Great Interview"]
#df = pd.DataFrame(titles, columns=['embedding'])


#encoding = tiktoken.get_encoding(embedding_encoding)
#df["embedding"] = df.embedding.apply(lambda x: get_embedding(x, engine=embedding_model))
#df["embedding"] = df.embedding.apply(eval).apply(np.array)

results = search_titles(titles, filter_sent, n=3)
