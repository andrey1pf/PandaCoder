import base64
import os
import requests

from flask import render_template, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, redirect
from urllib.parse import urlparse, urljoin

from blogController import app, db
from blogController.models import Article, User
from blogController import add_image, search_article
import io
import threading
import time


@app.route('/', methods=['GET'])
def index():
    articles = Article.query.order_by(Article.date.desc()).all()
    imgs_src = []
    for article in articles:
        blob_reader = io.BytesIO(article.ImageID)
        base64_content = base64.b64encode(blob_reader.read()).decode('utf-8')
        img_src = f"data:image/jpeg;base64,{base64_content}"
        imgs_src.append(img_src)
    return render_template("index.html", articles=articles[:9], image_data=imgs_src[:9])


@app.route('/about', methods=['GET'])
def about():
    return render_template("about.html")


@app.route('/posts', methods=['GET'])
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>', methods=['GET'])
def posts_detail(id):
    article = Article.query.get(id)
    blob_reader = io.BytesIO(article.ImageID)
    base64_content = base64.b64encode(blob_reader.read()).decode('utf-8')
    img_src = f"data:image/jpeg;base64,{base64_content}"

    return render_template("posts_detail.html", article=article, image_data=img_src)


@app.route('/posts/<int:id>/delete', methods=['GET'])
@login_required
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "An error occurred while deleting the article."


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "An error occurred while edit the article."
    else:
        return render_template('post_update.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])
@login_required
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        image = request.files['image']

        image.save(f'{title[:10]}.jpg')

        image_blob = add_image.convert_to_binary_data(f'{title[:10]}.jpg')

        article = Article(title=title, intro=intro, text=text, ImageID=image_blob)

        try:
            db.session.add(article)
            db.session.commit()
            os.remove(f'{title[:10]}.jpg')
            return redirect('/posts')
        except:
            return "An error occurred while adding the article."
    else:
        return render_template('create-article.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if not (login or password or password2):
            flash('Please, fill all fields!')
        elif password != password2:
            flash("Passwords doesn't match!")
            return render_template("register.html")
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login_page'))
            except:
                return "An error occurred while adding user."
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if login and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Login success")
                next_page = request.args.get('next') or "/"
                return redirect(get_safe_redirect(next_page))
            else:
                flash('Login or password is not correct')
        else:
            flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        article = Article.query.order_by(Article.id.desc()).first()
        blob_reader = io.BytesIO(article.ImageID)
        base64_content = base64.b64encode(blob_reader.read()).decode('utf-8')
        img_src = f"data:image/jpeg;base64,{base64_content}"
        return render_template("search_article.html", article=article, image_data=img_src)

    if request.method == 'POST':
        query = request.form['find_article']
        id_article = search_article.search_article(query)
        if id_article != null:
            article = Article.query.get(id_article)
            blob_reader = io.BytesIO(article.ImageID)
            base64_content = base64.b64encode(blob_reader.read()).decode('utf-8')
            img_src = f"data:image/jpeg;base64,{base64_content}"

            return render_template("search_article.html", article=article, image_data=img_src)


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


def is_safe_redirect_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return (
            redirect_url.scheme in ("http", "https")
            and host_url.netloc == redirect_url.netloc
    )


def get_safe_redirect(url):
    if url and is_safe_redirect_url(url):
        return url

    url = request.referrer
    if url and is_safe_redirect_url(url):
        return url

    return "index"
