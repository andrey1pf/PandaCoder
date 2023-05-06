import mysql.connector
from datetime import datetime


def execute_data(article_title, article_intro, article_text, article_image):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="blog"
    )
    print(3)

    cursor = mydb.cursor()

    now = datetime.now()
    title = article_title
    intro = article_intro
    text = article_text
    date_article = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    image = article_image

    print("start insert")
    print(article_title)

    sql = "INSERT IGNORE INTO article (title, intro, text, date, ImageID) VALUES (%s, %s, %s, %s, %s)"
    val = (title, intro, text, date_article, image)

    print("end insert")
    cursor.execute(sql, val)
    mydb.commit()
