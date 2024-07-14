"""
Author: Napol Thanarangkaun
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from collections import deque

class Spinnex:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited = set()
        self.queue = deque([start_url])

    def fetch(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def parse_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            if not bool(urlparse(href).netloc):  # relative link
                href = urljoin(base_url, href)
            if urlparse(href).scheme in ['http', 'https']:
                links.add(href)
        return links

    def crawl(self):
        pages_crawled = 0
        while self.queue and pages_crawled < self.max_pages:
            current_url = self.queue.popleft()
            if current_url in self.visited:
                continue
            print(f"Crawling: {current_url}")
            html = self.fetch(current_url)
            if html is None:
                continue
            self.visited.add(current_url)
            pages_crawled += 1
            for link in self.parse_links(html, current_url):
                if link not in self.visited:
                    self.queue.append(link)

if __name__ == "__main__":
    start_url = "https://webug.xyz"
    spider = Spinnex(start_url)
    spider.crawl()
