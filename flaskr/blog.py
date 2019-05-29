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
