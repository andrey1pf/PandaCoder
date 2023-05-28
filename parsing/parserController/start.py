import os

import requests

from parserController import add_image, execute_data
from parserController.Parsers import parser_newsdataio
import threading
import time


def parsing_news():
    while True:
        print(1)
        add_pars()
        time.sleep(60)


def add_pars():
    list_articles = parser_newsdataio.start_pars_news('', 'us', 'en', 'top')
    print(00)
    for art in list_articles:
        title = art[0]
        intro = art[1]
        text = art[2]
        image_url = art[3]
        response = "https://error"

        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(f'{title[:10]}.jpg', 'wb') as f:
                    f.write(response.content)
            image_blob = add_image.convert_to_binary_data(f'{art[0][:10]}.jpg')
            os.remove(f'{title[:10]}.jpg')

            if response != "https://error":
                execute_data.execute_data(title, intro, text, image_blob)
        except:
            pass


def start():
    print(1234)
    t = threading.Thread(target=parsing_news)
    t.start()
