import functools

from flask import (
    Blueprint, 
    flash, 
    g, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

''' If the user is logged in (user id stored in session) their information 
    should be loaded
'''
# Register function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    # Check if user id is stored in session and stores it in g.user for length of request
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif (
            db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone()
            is not None
        ):
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # The user is queried first and stored in a variable for later use
        user = db.execute(
            'Select * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
            # Hash the submitted password and securely compare
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            # session is a dict that stores data across requests. Data is stored in a cookie
            # that is sent to the browser
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

''' Remove the user id from the session and redirect to index. '''
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

''' Decorator to return a new view function that wraps the original to check if a user
    is loaded and redirects to the login page otherwise. If a user is loaded, the orginal
    view is called and continues. '''
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view