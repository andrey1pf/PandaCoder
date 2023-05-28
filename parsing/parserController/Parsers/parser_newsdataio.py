import json
from newsdataapi import NewsDataApiClient
from parserController.ChatGPT import gpt
import time
import requests
from parserController import pars_cred


api = NewsDataApiClient(apikey=pars_cred.get_data()[1])


def start_pars_news(query, country, language, category):
    print('tut')
    response = api.news_api(q=query, country=country, language=language, category=category)
    print(response['status'])
    if response['status'] == 'success':
        results = response['results']
        result_articles = []
        start_time = time.time()
        count_request_ph = 0
        count_articles = 0
        for result in results:
            count_articles += 1
            title = result['title']
            description = result['description']
            url = result['link']
            image_url = result['image_url']
            content = result['content']
            content = check_content(content)
            
            try:
                content_ = gpt.refactor_text(content)
                article_info = [title, description, content_, image_url, url]

                if check_article(article_info):
                    print("yes image")
                    result_articles.append(article_info)
                else:
                    print("no image")

                    image_url_new = search_image(title)
                    article_info[3] = image_url_new

                    result_articles.append(article_info)

                count_request_ph += 1

                if count_request_ph == 3:
                    count_request_ph = 0
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 61:
                        time.sleep(61 - elapsed_time)
                    start_time = time.time()

                if count_articles == 5:
                    break
            except:
                print('to many requests...')

        return result_articles
    else:
        print("Error: " + str(response.status_code))


def check_article(article):
    if article[3] is None:
        return False
    return True


def search_image(query):
    access_key = pars_cred.get_data()[0]
    url = 'https://api.unsplash.com/search/photos?query=' + query

    headers = {
        'Authorization': 'Client-ID ' + access_key
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    image_url = data['results'][0]['urls']['regular']
    return image_url


def check_content(content):
    substring1 = "Show key events only"
    substring2 = "Please turn on JavaScript to use this feature"

    if substring1 in content:
        content = content.replace(substring1, "")

    if substring2 in content:
        content = content.replace(substring2, "")

    return content
