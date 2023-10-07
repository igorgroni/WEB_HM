import json
from bs4 import BeautifulSoup
import requests

base_url = 'http://quotes.toscrape.com'

quotes_data = []
authors_data = []


def get_page_urls(base_url: str):
    urls = []
    page_number = 1
    page_exists = True

    while page_exists:
        url = f'{base_url}/page/{page_number}/'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                next_button = soup.find('li', class_='next')
                record = soup.find('div', class_='quote')
                if not next_button and not record:
                    break
                urls.append(url)
                page_number += 1
                continue
        except Exception:
            print('Page processing error')
            page_exists = False
    return urls


def get_author_urls(page_urls: list, base_url: str):
    author_urls = []

    for url in page_urls:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        links = soup.select("div[class=quote] span a")
        for link in links:
            author_urls.append(base_url + link["href"] + '/')
    return set(author_urls)


def get_author_info(author_urls: list):
    authors = []

    for url in author_urls:
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        fullname = soup.find('h3', class_='author-title').get_text()
        born_date = soup.find('span', class_='author-born-date').get_text()
        born_location = soup.find(
            'span', class_='author-born-location').get_text()[3:]
        description = soup.find(
            'div', class_='author-description').get_text().replace('\n', '').strip().replace('\\', '')
        author = {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description
        }
        authors.append(author)
    return authors
    

def save_to_json(data_list, filename):
    indent = len(data_list[0]) - 1
    with open(filename, 'w', encoding='utf-8') as fd:
        json.dump(data_list, fd, ensure_ascii=False, indent=indent)
    

def get_quotes(urls: list):
    quote_list = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')

        for i in range(len(quotes)):
            tagsforquote = tags[i].find_all('a', class_='tag')

            quote = {
                'tags': [tagforquote.text for tagforquote in tagsforquote],
                'author': authors[i].text,
                'quote': quotes[i].text
            }
            quote_list.append(quote)
    return quote_list

def main():
    base_url = 'http://quotes.toscrape.com'

    author_file_name = 'authors.json'
    quotes_file_name = 'quotes.json'

    
    page_urls = get_page_urls(base_url)

    
    author_urls = get_author_urls(page_urls, base_url)

   
    authors = get_author_info(author_urls)
    save_to_json(authors, author_file_name)

    
    quotes = get_quotes(page_urls)
    save_to_json(quotes, quotes_file_name)


if __name__ == '__main__':
    main()
