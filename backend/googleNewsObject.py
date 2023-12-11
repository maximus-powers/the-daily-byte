import requests

class NewsObject:
    def __init__(self):
        self.google_api_key = 'AIzaSyDNoJgBOgy1J7q2g5zRybrIx2DaFmN_Tqk'  # Replace with your Google API key
        self.cx = 'd6004758d147448d0'  # Replace with your Search Engine ID (cx parameter)
        self.custom_search_url = 'https://www.googleapis.com/customsearch/v1'

    def call_news(self, query):
        params = {
            'key': self.google_api_key,
            'cx': self.cx,
            'q': query,
            'num': 10,
            'dateRestrict': 'd1'
        }

        response = requests.get(self.custom_search_url, params=params)

        # Check if the response was successful
        if not response.ok:
            print(f"Error {response.status_code}: {response.text}")
            return {}

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON response.")
            return {}

        # Check if there are any errors in the response
        if 'error' in data:
            print(data['error']['message'])
            return {}

        print(f"News articles for query '{query}':")

        # Build a dictionary of titles and urls
        titles = {}
        for item in data.get('items', []):
            titles[item['title']] = item['link']

        return titles
