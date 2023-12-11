import requests
from datetime import datetime, timedelta, timezone
import os

class NewsObject:
    def __init__(self):
        self.news_api_key = os.environ.get('NEWS_API_KEY')
        self.news_api_url = 'https://newsapi.org/v2/top-headlines'

    def call_news(self, category):  # string -> {headlines: urls}
        headers = {
            'X-Api-Key': self.news_api_key
        }
        params = {
            'country': 'us',
            'category': category,
            'pageSize': 20,
            'page': 1
        }

        response = requests.get(self.news_api_url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"News API Error: {response.status_code} - {response.text}")

        data = response.json()

        # build ret list of titles and urls
        articles_ordered = []
        for article in data['articles']:
            # check if the article was published in the last 36 hours
            published_time = datetime.fromisoformat(article['publishedAt'].replace('Z', '-04:00'))
            if datetime.now(timezone.utc) - published_time > timedelta(hours=36): continue  # Skip

            # Check if the URL is likely an article and not a homepage
            if 'youtube' in article['url'] or 'google' in article['url']: continue  # Skip
            if article['url'].endswith('.com'): continue

            articles_ordered.append({'headline':article['title'], 'url':article['url']})

        # flip it
        articles_ordered.reverse()

        return articles_ordered
