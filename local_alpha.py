from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import string


def load_data(file_path, num_rows=500):
    df = pd.read_csv(file_path, nrows=num_rows)
    return df[['id', 'article', 'highlights']].to_dict('records')

# Preprocess data (tokenization, stop-word removal, and stemming)
def preprocess_data(data):

    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    processed_data = []
    for document in data:
        tokens = word_tokenize(document.lower())
        # make sure there are no numbers
        filtered_tokens = [ps.stem(token) for token in tokens if token.isalnum() and token not in stop_words and not token.isdigit()]
        processed_data.append(" ".join(filtered_tokens))

    return processed_data

# Indexing
def create_index(processed_data):
    index = {}
    for i, document in enumerate(processed_data):
        for term in document.split():
            if term not in index:
                index[term] = set()
            index[term].add(i)

    return index

# Boolean Retrieval
def boolean_retrieval(query, index, processed_data):
    query_terms = set(word_tokenize(query.lower()))
    result_set = set(range(len(processed_data)))

    for term in query_terms:
        if term in index:
            result_set = result_set.intersection(index[term])

    return result_set

# Vector-based Retrieval using TF-IDF
def tfidf_retrieval(query, processed_data):

    vectorizer = TfidfVectorizer(max_df=1.0,min_df=0.0)
    vectors = vectorizer.fit_transform(processed_data)

    feature_names = vectorizer.get_feature_names_out()

    query_index = feature_names.tolist().index(query)

    # Get the TF-IDF scores for the query in all documents
    query_scores = vectors[:, query_index].toarray().flatten()


    ### -----     code below is to see what is the document processed by tf-idf vectorization      ----- ###

    # dense = vectors.todense()
    # dense_list = dense.tolist()

    # all_keywords = []

    # for description in dense_list:
    #     x=0
    #     keywords = []
    #     for word in description:
    #         if word > 0:
    #             keywords.append((feature_names[x]))
    #         x+=1
    #     all_keywords.append(keywords)

    return query_scores

def vector_based_retrieval(query, processed_data):

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_data)
    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
    return similarity_scores
    

def search():
    data_path = os.path.dirname(os.path.realpath(__file__)) + "/dataset/"
    file_path = data_path + "data.csv"
    num_rows = 500

    # Load data
    data = load_data(file_path, num_rows)

    # Preprocess data
    processed_data = preprocess_data([d['article'] for d in data])

    # Indexing with document numbers
    index = create_index(processed_data)

    # Get query from the URL parameter
    #user_query = request.args.get('query')
    user_query = "jesus"

    # Stemming on the query
    user_query = " ".join([PorterStemmer().stem(word) for word in word_tokenize(user_query.lower())])

    # Boolean Retrieval
    boolean_results = list(boolean_retrieval(user_query, index, processed_data))

    #tfidf retrieval function calling here.
    tfidf_scores = tfidf_retrieval(user_query, processed_data)

    #vsm retrieval function calling here.
    vsm_scores = vector_based_retrieval(user_query, processed_data)

    # Combine results, scores, and document count
    results = [
        {
            "id": data[i]['id'],
            "document_number": i + 1,  # Add 1 to start counting from 1
            "highlights": data[i]['highlights'],
            "tfidf_score": tfidf_scores[i],
            "vsm_score": vsm_scores[i],
            "article": data[i]['article']
        }
        for i in boolean_results
    ]
    return results
    
if __name__ == '__main__':
    search()