from bs4 import BeautifulSoup
from datetime import datetime
import requests
import base64

from blogController import db
from blogController.models import Article


def check_new_news(date_time, article):
    date = article.date
    if date_time > str(date):
        return True
    return False


def check_work_timer():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def parsing_news_BBC():
    article = Article.query.order_by(Article.date.desc()).first()

    url = "https://www.bbc.com/news/technology"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    stat = soup.find_all("div", class_="gel-layout__item gs-u-pb+@m gel-1/3@m gel0-1/4@xl gel-1/3@xxl nw-o-keyline "
                                       "nw-o-no-keyline@m")
    list_news = []

    for stats in stat:
        theme = stats.find("h3", {'class': 'gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text'}).text
        description = stats.find("p", {'class': 'gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary '
                                                'gs-u-display-none gs-u-display-block@m'}).text
        sub_link = stats.find("a", class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold "
                                          "nw-o-link-split__anchor").get('href')
        date_time = stats.find("time", class_="gs-o-bullet__text date qa-status-date").get('datetime')

        if check_new_news(date_time, article) and sub_link[:17] == "/news/technology-":
            y = {'theme': theme, 'description': description, 'sub_link': sub_link, 'main_text': ""}
            list_news.append(y)

    for element in list_news:
        url_link = "https://www.bbc.com/" + element.get('sub_link')
        request_main = requests.get(url_link)
        soup_main = BeautifulSoup(request_main.text, "html.parser")
        main_text = soup_main.find_all("div", class_="ssrcss-rgov1k-MainColumn e1sbfw0p0")

        for texts in main_text:
            texts = texts.find("article", {'class': 'ssrcss-pv1rh6-ArticleWrapper e1nh2i2l6'})
            result_text_with_attribute = texts.select("p")
            result_text = ""

            for i in range(len(result_text_with_attribute) - 1):
                result_text += result_text_with_attribute[i].text + "<br>"
            element.update({'main_text': result_text})

        image = texts.fins("span", {'class': 'ssrcss-11kpz0x-Placeholder e16icw910'})
        article = Article(title=element.get('theme'), intro=element.get('description'), text=element.get('main_text'))

        try:
            db.session.add(article)
            db.session.commit()
        except:
            pass
