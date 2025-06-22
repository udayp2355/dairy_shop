import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load the dataset
df = pd.read_csv('dairy_products_large.csv')

# Combine 'Description' and 'Ingredients' for feature extraction
df['Combined_Features'] = df['Description'] + ' ' + df['Ingredients']

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the 'Combined_Features' column
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Combined_Features'])

# Compute similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Save the TF-IDF Vectorizer and similarity matrix
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)

with open('cosine_sim.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)

# Save the dataset
df.to_csv('dairy_products_large.csv', index=False)
