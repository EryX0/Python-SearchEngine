import requests
import json

def get_data():
    url = 'http://127.0.0.1:5000/search'
    #send query to server with post, header = json and data = query

    post = requests.get(url, headers={'Content-Type': 'application/json'}, data=json.dumps({'query': 'jesus'}))
    print(post.text)
    data = post.json()
    return data

if __name__ == '__main__':
    data = get_data()
    print(data)