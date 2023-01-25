import requests
from bs4 import BeautifulSoup
import re
import datetime
import os

# Веб-скрейпинг

KEYWORDS = ['python', 'игр', 'IT', 'разработк']
html_page = requests.get('https://habr.com/ru/all/').text


def logger(old_function):

    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as f:
            # Если есть строки в аргументах, укоротить их до 20 символов
            args_list = []
            for arg in args:
                if isinstance(arg, str) and len(arg) > 20:
                    args_list.append(arg[:20])
            kwargs_list = []
            for kwarg in kwargs:
                if isinstance(kwarg, str) and len(kwarg) > 20:
                    kwargs_list.append(kwarg[:20])
            f.write(
                f'{datetime.datetime.now()}: {old_function.__name__}, args: {args_list}, kwargs: {kwargs_list}, '
                f'result: {result}\n')
        return result

    return new_function


# Найдены ли ключевые слова в тексте
@logger
def keywords_found(text):
    for keyword in KEYWORDS:
        s = re.search(keyword, text, re.IGNORECASE)
        if s is not None:
            return True
        else:
            return False


soup = BeautifulSoup(html_page, 'html.parser')
articles = soup.find_all('article')

if __name__ == '__main__':
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)
    for article in articles:
        # Получить полный адрес статьи, затем всю статью в отдельный обьект
        article_href = 'https://habr.com' + article.find(class_='tm-article-snippet__title-link')['href']
        full_article = BeautifulSoup(requests.get(article_href).text, 'html.parser')
        full_article = full_article.find('article')
        # Ищем в превью и тексте статьи
        if keywords_found(article.text) or keywords_found(full_article.text):
            date_string = article.find('time')['title']
            title_string = article.find('h2').a.span.text
            print(date_string, ' - ', title_string, ' - ', article_href)
