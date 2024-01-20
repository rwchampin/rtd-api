import requests
from bs4 import BeautifulSoup
from .models import BlogTopic

class BlogTopicScraper:
    def __init__(self, base_url="https://css-tricks.com/archives/page/", start_page=1):
        self.base_url = base_url
        self.page_number = start_page

    def get_articles_from_page(self, page_url):
        try:
            response = requests.get(page_url)
            response.raise_for_status()  # Raise an error for bad status codes
            return BeautifulSoup(response.text, 'html.parser').find_all('article')
        except requests.RequestException as e:
            print(f"Error fetching page {page_url}: {e}")
            return None

    def get_next_page(self):
        page_url = f"{self.base_url}{self.page_number}"
        articles = self.get_articles_from_page(page_url)

        if not articles:
            print(f"No articles found on page {self.page_number}. Stopping.")
            return None

        print(f"Page {self.page_number} - Found {len(articles)} articles")

        for article in articles:
            h2_tag = article.find('h2')
            if h2_tag and h2_tag.find('a'):
                title = h2_tag.get_text().strip()
                url = h2_tag.find('a')['href']
                topic = BlogTopic(url=url)
                topic.save()
                print(f"Title: {title}, URL: {url}")
            else:
                print("No title or URL found for an article.")

        self.page_number += 1

        return page_url

    def get_all_pages(self):
        while True:
            page_url = self.get_next_page()
            if not page_url:
                break
            
            
            
     