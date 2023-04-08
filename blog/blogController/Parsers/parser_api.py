import requests


def do_pars():
    api_key = ''
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': api_key,
        'pageSize': 5
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Обработка данных
    if data['status'] == 'ok':
        articles = data['articles']
        list_article = []
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            image_url = article['urlToImage']
            content = article['content']
            # Основной текст статьи
            article_info = [title, description, content, image_url, url]
            if check_article(article_info):
                list_article.append(article_info)

        return list_article
    else:
        print('Ошибка получения данных:', data['message'])


def check_article(article):
    for i in article:
        if i == 'None':
            return False

    return True
