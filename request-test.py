import requests

def get_data():
    url = 'http://185.81.97.49:5000/search'
    #send query to server with post, header = json and data = query

    get = requests.get(url, headers={'Content-Type': 'application/json'}, params={'query': 'jesus'})
    print(get.text)
    data = get.json()
    return data

if __name__ == '__main__':
    data = get_data()
    print(data)