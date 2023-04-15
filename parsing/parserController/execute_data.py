import sqlite3
from datetime import datetime


def execute_data(article_title, article_intro, article_text, article_image):
    conn = sqlite3.connect('../blog/blogController/blog.db')
    cursor = conn.cursor()

    now = datetime.now()
    title = article_title
    intro = article_intro
    text = article_text
    date_article = now.strftime('%Y-%m-%d %H:%M:%S.%f')
    image = article_image

    print("start insert")
    print(article_title)
    cursor.execute("SELECT * FROM article WHERE title = ?", (article_title,))
    row = cursor.fetchone()

    if row:
        print("Attention: this article is not unique")
    else:
        cursor.execute("INSERT INTO article (title, intro, text, date, ImageID) "
                       "VALUES (?, ?, ?, ?, ?)",
                       (title, intro, text, date_article, image))
        print("end insert")

    conn.commit()
    conn.close()
