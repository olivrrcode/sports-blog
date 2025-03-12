from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from markdown import markdown

from sports_blog.auth import login_required
from sports_blog.db import get_db


bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, c.id AS category_id, c.name AS category_name'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' LEFT JOIN category c ON p.category_id = c.id'
        ' ORDER BY created DESC'
    ).fetchall()

    new_posts = []
    for post in posts:
        post = dict(post)
        post["body"] = markdown(post["body"])

        new_posts.append(post)
    return render_template('blog/index.html', posts=new_posts)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    db = get_db()
    categories = db.execute('SELECT id, name FROM category ORDER BY name').fetchall()
    
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        category_id = request.form['category_id']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Content is required.'
        elif not category_id:
            error = 'Category is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO post (title, body, author_id, category_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], category_id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html', categories=categories)

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))