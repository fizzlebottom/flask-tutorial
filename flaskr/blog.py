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