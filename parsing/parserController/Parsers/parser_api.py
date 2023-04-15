import requests

from parserController.ChatGPT import gpt


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

    if data['status'] == 'ok':
        articles = data['articles']
        list_article = []
        for article in articles:
            title = article['title']
            description = article['description']
            url = article['url']
            image_url = article['urlToImage']
            content = article['content']
            article_info = [title, description, content, image_url, url]
            if check_article(article_info):
                print(article_info[2])
                if article_info[2].find("… [+") != -1:
                    index = article_info[2].find("… [")
                    text = article_info[2][:index]
                    text += gpt.continue_text(text, title, description)
                    article_info[2] = text
                else:
                    article_info[2] += gpt.continue_text(article_info[2], title, description)
                list_article.append(article_info)

        return list_article
    else:
        print('Error while getting data:', data['message'])


def check_article(article):
    if article[2] is None:
        return False
    return True
