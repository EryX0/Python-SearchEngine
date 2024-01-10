import requests

def get_data():
    url = 'http://127.0.0.1:5000/search'
    #send query to server with post, header = json and data = query

    get = requests.get(url, headers={'Content-Type': 'application/json'}, params={'query': 'police'})
    print(get.text)
    data = get.json()
    return data

if __name__ == '__main__':
    data = get_data()
    print(data)