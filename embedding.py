from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity


#these sentences have no words in common yet they are semantically similar
#they should have a higher cosine similarity than a noisy pair of sentences
sentences = ["Part Time Helper", "Temporary Secretary"]

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

#Compute embedding for both lists
embedding_1= model.encode(sentences[0], convert_to_tensor=True)
embedding_2 = model.encode(sentences[1], convert_to_tensor=True)

result = util.pytorch_cos_sim(embedding_1, embedding_2)
print(result)


