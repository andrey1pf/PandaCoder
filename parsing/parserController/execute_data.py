import mysql.connector
from datetime import datetime
import os

from parserController import pars_cred


def execute_data(article_title, article_intro, article_text, article_image):
    print(3)
    host_mysql = os.environ.get('MYSQL_HOST')
    mydb = mysql.connector.connect(
        host=host_mysql,
        user=pars_cred.get_db[0],
        password=pars_cred.get_db[1],
        database="blog"
    )

    cursor = mydb.cursor()

    now = datetime.now()
    title = article_title
    intro = article_intro
    text = article_text
    date_article = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    image = article_image

    q = "SELECT COUNT(*) as count FROM article WHERE title = %s"
    cursor.execute(q, (title,))
    result = cursor.fetchall()
    print(result[0][0])
    if len(result[0][0]) == 0:
        print(4)
        sql = "INSERT IGNORE INTO article (title, intro, text, date, ImageID) VALUES (%s, %s, %s, %s, %s)"
        val = (title, intro, text, date_article, image)
        cursor.execute(sql, val)
        mydb.commit()

    cursor.close()
    mydb.close()
