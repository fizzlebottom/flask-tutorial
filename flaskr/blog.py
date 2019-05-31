from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """ Index will show all posts, most recent first.
    """
    db = get_db()
    posts = db.execute( 
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id' # JOIN is used to pull author info from user table
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required # User must be logged in to see the "Create" view
def create():
    """ Either the form is displayed or the posted data is validated and the post added to the db, or an error is shown.
    """
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title: # If no title, set relevant error message
            error = 'Title is required'

        if error is not None:
            flash(error) # Display the error message
        else:
            db = get_db() # Grab database
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit() # Insert the new post data into db
            return redirect(url_for('blog.index')) # Go back to blog index

    return render_template('blog/create.html')

def get_post(id, check_author=True): # check_author argument defined to allow function to get a post without checking author
    """ Function to get the blog post to allow to call from each view as needed
    """
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id)) # abort raises special exception that returns HTTP status code.

    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    return post

@bp.route('/<int:id>/update', methods=('GET','POST'))
@login_required
def update(id): # Function takes arguement (id) that corresponds to post number ie. /1/update
    """ Function to update/edit an existing post.

    Flask will capture the 1, ensure it’s an int, and pass it as the id argument.
    If you don’t specify int: and instead do <id>, it will be a string.
    To generate a URL to the update page, url_for() needs to be passed the id so it 
    knows what to fill in: url_for('blog.update', id=post['id']).
    """
    post = get_post(id) # update view uses a post object and an UPDATE query. You could do this in one view/template

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