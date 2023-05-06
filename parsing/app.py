import os

import requests

from parserController import app, execute_data
from parserController import add_image
from parserController.Parsers import parser_newsdataio
import threading
import time


def parsing_news():
    while True:
        add_pars()
        time.sleep(60)


def add_pars():
    list_articles = parser_newsdataio.start_pars_news('', 'us', 'en', 'top')

    for art in list_articles:
        title = art[0]
        intro = art[1]
        text = art[2]
        image_url = art[3]
        response = "https://error"
        print(title)

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


if __name__ == '__main__':
    t = threading.Thread(target=parsing_news)
    t.start()
