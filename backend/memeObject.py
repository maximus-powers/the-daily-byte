import requests

class MemeObject:
    def __init__(self):
        self.API_KEY = 'zcBrBdJyTPrKomZF9BMZ3wevHHZVI2jt'
        self.suggestion_endpoint = 'https://api.giphy.com/v1/tags/related/'
        self.search_endpoint = 'https://api.giphy.com/v1/gifs/search'

    # search suggestions
    # not using this anymore. Didn't work well
    def find_search_suggestions(self, headline):
        # API url encoding and params
        url = f'{self.suggestion_endpoint}{headline}'
        params = {
            'api_key': self.API_KEY
        }

        # make request
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # print(response.json()['data'])
            print('Meme Suggested Term: ' + response.json()['data'][0]['name'])
            data = response.json()['data']

            list_of_suggestions = []
            for item in data:
                list_of_suggestions.append(item['name'])

            return list_of_suggestions
        else:
            print(response.status_code)
            return None

    # search memes
    def find_meme(self, search_term):
        params = {
            'api_key': self.API_KEY,
            'q': search_term,
            'limit': 25,
            'lang': 'en'
        }
        
        # handle if no square gif is found

        # make request
        response = requests.get(self.search_endpoint, params=params)
        data = response.json()['data']
        if response.status_code == 200:
            for gif in data:
                width = int(gif['images']['original']['width'])
                height = int(gif['images']['original']['height'])
                if width == height:
                    gif_url = gif['images']['original']['url']
                    break

            print('Meme Found, URL: ' + gif_url + '\n')
            return gif_url
        else:
            print(response.status_code)
            return None



        
        
