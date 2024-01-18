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
import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from WebCrawler.WebCrawler.spiders.web_crawler import MyCrawler
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


app = Flask(__name__)
CORS(app)

nltk.download('stopwords')
nltk.download('punkt')

def crawler():
    parser = argparse.ArgumentParser(
        description='Python Search Engine - Crawler'
    )
    parser.add_argument('--limit','-l', type=int, default=500, help='Crawl limit')
    parser.add_argument('--log','-g', action='store_true' , default=False, help='Enable logging')
    parser.add_argument('--crawl','-c', action='store_true' ,  default=False, help='getting new data')
    args = parser.parse_args()

    custom_settings = {
        'FEED_FORMAT': 'csv',  # Replace with the desired data format
        'FEED_URI': './dataset/data.csv',  # Replace with the desired data file
        'LOG_ENABLED': args.log,  # Disable logging
        'CLOSESPIDER_ITEMCOUNT': args.limit  # Crawl limit
    }
    settings = get_project_settings()
    settings.update(custom_settings)
    process = CrawlerProcess(settings)
    process.crawl(MyCrawler)
    if args.crawl:
        if os.path.isfile('./dataset/data.csv'):
            os.remove('./dataset/data.csv')
            print("getting new data...")
            process.start()
        else:
            print("getting new data...")
            process.start()
        print("Crawling complete!")

def summarizer(documents, num_sentences=1):
    parser = PlaintextParser.from_string(documents, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    summary =  " ".join(str(sentence) for sentence in summary)
    return summary


# Load data from CSV file
def load_data(file_path, num_rows=500):
    df = pd.read_csv(file_path, nrows=num_rows)
    return df[['link', 'article', 'title']].to_dict('records')

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
    query_terms = set(query.split())
    result_set = set()

    # at least one query term should be in the returned document
    flag = False
    for term in query_terms:

        if term in index:
            flag = True
            result_set = result_set.union(index[term])

    if flag == False:
        result_set = set()

    return result_set

def tfidf_retrieval(query, processed_data):

    vectorizer = TfidfVectorizer(max_df=1.0,min_df=0.0)
    vectors = vectorizer.fit_transform(processed_data)

    feature_names = vectorizer.get_feature_names_out()

    # get the index of the query terms in the feature names
    query_indexes = []
    for query_term in query.split():
        try:
            query_indexes.append(feature_names.tolist().index(query_term))
        except:
            continue
    #return all zero if query indexes is empty
    if len(query_indexes) == 0:
        return [0] * len(processed_data)

    # sum query indexes scores of each document, and store in query_scores
    query_scores = []
    for document in vectors:
        score = 0
        for index in query_indexes:
            score += document[0, index]
        query_scores.append(score)

    return query_scores

# Vector-based Retrieval using TF-IDF
def vector_based_retrieval(query, processed_data):
    vectorizer = TfidfVectorizer(max_df=1.0,min_df=0.0)
    vectors = vectorizer.fit_transform(processed_data)
    query_vector = vectorizer.transform([query])
    #vsm retrieval with cosine similarity
    similarity_score = cosine_similarity(query_vector, vectors)

    return similarity_score

@app.route('/search', methods=['GET'])
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
    user_query = request.args.get('query')
    # Stemming on the query
    user_query = " ".join([PorterStemmer().stem(word) for word in word_tokenize(user_query.lower())])

    # Boolean Retrieval
    boolean_results = list(boolean_retrieval(user_query, index, processed_data))

    #tfidf retrieval function calling here.
    tfidf_scores = tfidf_retrieval(user_query, processed_data)

    #vsm retrieval function calling here.
    vsm_scores = vector_based_retrieval(user_query, processed_data)

    # Combine results, scores, and document count
    results = []
    for i in boolean_results:
        if tfidf_scores[i] > 0 or vsm_scores[0][i] > 0:
            results.append({
                "link": data[i]['link'],
                "document_number": i + 1,  # Add 1 to start counting from 1
                "tfidf_score": tfidf_scores[i],
                "vsm_score": vsm_scores[0][i],
                "title": data[i]['title'],
                "article": data[i]['article'],
                "highlight": summarizer(data[i]['article'], num_sentences=1)
            })

    return jsonify(results)

if __name__ == '__main__':
    crawler()
    app.run(host='0.0.0.0', port=5000, debug=False)