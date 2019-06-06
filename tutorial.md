# Create a Flask Single Page Application - Flaskr
## Basic blog app built in the Flask [tutorial](http://flask.pocoo.org/docs/tutorial/)

## -- Add a section about git??

## Virtual Environments
Use a virtual environment to manage dependencies for your project, in dev and prod.

The more Python projects you have, the more likely you'll need to work with different versions of libraries or Python. This can break compatibility.

Virtual environments are independent groups of libraries, one for each project.

Python 3 comes bundled with the **[venv](https://docs.python.org/3/library/venv.html#module-venv)** module to create virtual environments.

### Create an environment
Create a project folder and a `venv` folder within:
>mkdir myProject <br>
>cd myProject <br>
>py -3 -m venv venv

### Activate the environment
Before you work on your project, activate the corresponding environment:

On Windows:
>venv\Scripts\activate

Your shell prompt will change to show the name of the activated venv.

## Install Flask
Within the activated venv, use the following command to install Flask:
>pip install Flask

Flask is now installed. Check out 
[Quickstart](http://flask.pocoo.org/docs/1.0/quickstart/) or the 
[Docs](http://flask.pocoo.org/docs/1.0/)

### Flask Dependencies
This distributions will be installed automagically with Flask.
* [Werkzeug](http://werkzeug.pocoo.org/)
implements WSGI, the standard Python interface between applications and servers.
* [Jinja](http://jinja.pocoo.org/)
is a template language that renders the pages your application serves.
* [MarkupSafe](https://pypi.org/project/MarkupSafe/)
comes with Jinja. It escapes untrsusted input when rendering templates to avoid injection attacks.
* [ItsDangerous](https://pythonhosted.org/itsdangerous/)
securely signs data to ensure its integrity. This is used to protect Flask's session cookie.
* [Click](http://click.pocoo.org/)
is a framework for writing command line applications. It provides the `flask` command and allows adding custom management commands.

### Optional Dependencies
This distributions will not be installed automatically. Flask will detect and use them if you install them.
* [Blinker](https://pythonhosted.org/blinker/)
provides support for [Signals](http://flask.pocoo.org/docs/1.0/signals/#signals)
* [SimpleJSON](https://simplejson.readthedocs.io/)
is a fast JSON implementation that is compatible with Python's `json` module. It is preferred for JSON operations if it is installed.
* [python-dotenv](https://github.com/theskumar/python-dotenv#readme)
enables support for 
[Environment Variables from dotenv](http://flask.pocoo.org/docs/1.0/cli/#dotenv)
when running `flask` commands.
* [Watchdog](https://pythonhosted.org/watchdog/) 
provides a faster, more efficient reloader for the dev server.

## Project Layout
The tutorial assumes you're working from the `flask-tutorial` directory. The filenames at the top of each code block are relative to this directory.

A Flask application can be as simple as a single file.

`hello.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
```

As a project gets bigger, it will be overwhelming to keep all the code in one file. Python projects use *packages* to organize code into multiple modules that can be imported when needed, and the tutorial does this as well.

The project directory will contain:
* `flaskr/`, a Python package containing your application code and files.
* `tests/`, a directory containing test modules.
* `venv/`, a Python virtual environment where Flask and other dependencies are installed.
* Installation files telling Python how to install your project.
* Version control config, such as [git](https://git-scm.com/).
You should make a habit of using some type of version control for all your projects, no matter the size.
Any other project files you might add in the future.

By the end, your project layout will look like this:
```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
```

If you're using version control, the following files that are generated while running your project should be ignored. There may be other files based on the editor you use. In general, ignore files that you didn't write. For example, with git:

`.gitignore`
```
venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/
```
## Application Setup
A Flask application is an instance of the [Flask](http://flask.pocoo.org/docs/1.0/api/#flask.Flask) class. Everything about the application, such as configuration and URLs, will be registered by this class.

The most straightforward way to create a Flask applicaton is to create a global **Flask** instance directly at the top of your code, like how the "Hello, World!" example did above. While this is simple and useful in some cases, it can cause some tricky issues as the project grows.

Instead of creating a **Flask** instance globally, you will create it inside a function. This function is known as the *application factory*. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.

### The Application Factory
Create `flaskr` directory and add the `__init__.py` file. The `__init__.py` servers double duty: it will contain the application factory, and  it tells Python that the `flaskr` directory should be treated as a package.

>mkdir flaskr

`flaskr/__init__.py`
```python
import os
from flask import Flask

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
```

`create_app` is the application factory function. You'll add to it later in the tutorial, but it already does a lot.

1. `app = Flask(__name__, instance_relative_config=True)` creates the Flask instance.
    * `__name__` is the name of the current Python module. The app needs to know where it's located to set up some paths, and `__name__` is a convenient way to tell it that.
    * `instance_relative_config=True` tells the app that configuration files are relative to the 
    [instance folder](http://flask.pocoo.org/docs/1.0/config/#instance-folders). The instance folder is located outside the `flaskr` package and can hold local data that shouldn't be committed to version control, such as configuration secrets and the database file.
2. [app.config.from_mapping()](http://flask.pocoo.org/docs/1.0/api/#flask.Config.from_mapping) sets some default configuration that the app will use:
    * [SECRET_KEY](http://flask.pocoo.org/docs/1.0/config/#SECRET_KEY) is used by Flask and extensions to keep data safe. It’s set to `'dev'` to provide a convenient value during development, but it should be overridden with a random value when deploying.
    * `DATABASE` is the path where the SQLite db file will be saved. It's under [app.instance_path](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.instance_path), which is the path that Flask has chosen for the instance folder. You'll learn more about the database.
3. [app.config.from_pyfile()](http://flask.pocoo.org/docs/1.0/api/#flask.Config.from_pyfile) overrides the default configuration with values taken from the `config.py` file in the instance folder if it exists. For example, when deploying, this can be used to set a real `SECRET_KEY`.
    * `test_config` can also be passed to the factory, and will be used instead of the instance configuration. This is so the tests you'll write later can be configured independently of any development values you have configured.
4. [os.markdirs()](https://docs.python.org/3/library/os.html#os.makedirs) ensures that
[app.instance_path](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.instance_path) exists. Flask doesn't create the instance folder automatically, but it needs to bre created because your project will create the SQLite db file there.
5. [@app.route()](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.route) creates a simple route so you can see the application working before getting into the rest of the tutorial. It creates a connections between the URL `/hello` and a function that returns a response, the string `Hello, World!` in this case.

### Run the Application

Now we can run the application using the `flask` command. From terminal, tell Flask where to find your application, then run it in development mode.

Dev mode shows an interactive debugger whenever a page raises an exception, and restarts the server whenever you make changes to the code. You can leave it running and just reload the browser page as you follow the tutorial.

For Linux and Mac:
>export FLASK_APP=flaskr <br />
>export FLASK_ENV=development <br />
>flask run

For Windows cmd, use `set` instead of `export`:
>set FLASK_APP=flaskr <br />
>set FLASK_ENV=development <br />
>flask run

For Windows Powershell, use `$env:` instead of `export`:
>$env:FLASK_APP = "flaskr" <br />
>$env:FLASK_ENV = "development" <br />
>flask run

You'll see output similar to this:
>\* Serving Flask app "flaskr" <br />
>\* Environment: development <br />
>\* Debug mode: on <br />
>\* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) <br />
>\* Restarting with stat <br />
>\* Debugger is active! <br />
>\* Debugger PIN: 855-212-761

Visit [http://127.0.0.1:5000/hello](http://127.0.0.1:5000/hello) in a web browser and you should see the "Hello, World!" message. Congrats! You're now running your Flask web application!

## Define and Access the Database

The application will use a [SQLite](https://sqlite.org/about.html) database to store users and posts. Python comes with built-in support for SQLite in the **[sqlite3](https://docs.python.org/3/library/sqlite3.html#module-sqlite3)** module.

SQLite is convenient because it doesn't require setting up a separate database server and is built-in to Python. However, if concurrent requests try to write to the db at the same time, they will slow down as each write happens sequentially. Small applications won't notice this. Once you become big, you may want to switch to a different db.

The tutorial doesn't go into details about SQL. If you are not familiar with it, the SQLite docs describe the [language](https://sqlite.org/lang.html).

### Connect to the Database

The first thing to do when working with a SQLite db (and most other Python db libraries) is to create a connection to it. Any queries and operations are performed using the connection, which is closed after the work is finished.

In web applications this connection is typically tied to the request. It is created at some point when handling a request, and closed before the response is sent.

`flaskr/db.py`
```python
import sqlite 3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
```

[g](http://flask.pocoo.org/docs/1.0/api/#flask.g) is a special object that is unique for each request. It is used to store data that might be accessed by multiple functions during the request. The connection is stored and reused instead of creating a new connection if `get_db` is called a second time in the same request.

[current_app](http://flask.pocoo.org/docs/1.0/api/#flask.current_app) is another special object that points to the Flask application handling the request. Since you used an application factory, there is no application object when writing the rest of your code. `get_db` will be called when the application has been created and is handling a request, so `current_app` can be used.

[sqlite3.connect()](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect) establishes a connection to the file point at by the `DATABASE` configuration key. This file doesn't have to exist yet, and won't until you initialize the db later.

[sqlite3.Row](https://docs.python.org/3/library/sqlite3.html#sqlite3.Row) tells the connection to return rows that behave like dicts. This allows accessing the columns by name.

`close_db` checks if a connection was created by checking if `g.db` was set. If the connection exists, it is closed. Further down you will tell your application about the `close_db` function in the application factory so that it is called after each request.

### Create the Tables

In SQLite, data is stored in *tables* and *columns*. These need to be created before you can store and retrieve data. Flaskr will store users in the `user` table, and posts in the `post` table. Create a file with the SQL commands needed to create empty tables:

`flaskr/schema.sql`
```sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user (id)
);
```

Add the Python functions that will run these SQL commands to the `db.py` file:

`flaskr/db.py`
```python
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db()
    click.echo('Initialized the database.')
```

[open_resource()](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.open_resource) opens a file relative to the `flaskr` package, which is userful since you won't necessarily know where that location is when deploying the application later. `get_db` returns a database connection, which is used to execute the commands read from the file.

[click.command()](http://click.pocoo.org/api/#click.command) defines a command line command called `init-db` that calls the `init-db` function and shows a success message to the user. You can read [Command Line Interface](http://flask.pocoo.org/docs/1.0/cli/#cli) to learn more about writing commands.

### Register with the Application

The `close_db` and `init_db_command` functions need to be registered with the application instance, otherwise they won't be used by the application. However, since you're using a factory function, that instance isn't available when writing the functions. Instead, write a function that takes an application and does the registration.

`flaskr/db.py`
```python
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
```

[app.teardown_appcontext()](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.teardown_appcontext) tells Flask to call that function when cleaning up after returning the response.

[app.cli.add_command()](http://click.pocoo.org/api/#click.Group.add_command) adds a new command that can be called with the `flask` command.

Import and call this function from the factory. Place the new code at the end of the factory function before return the app.

`flaskr/__init__.py`
```python
def create_app():
    app = ...
    # existing code omitted

    from . import db
    db.init_app(app)

    return app
```

### Initialize the Database File

Now that `init-db` has been registered with the app, it can be called using the `flask` command, similar to the `run` command from the previous page.

**Note:**

If you’re still running the server from the previous page, you can either stop the server, or run this command in a new terminal. If you use a new terminal, remember to change to your project directory and activate the env as described in [Activate the environment](http://flask.pocoo.org/docs/1.0/installation/#install-activate-env). You’ll also need to set FLASK_APP and FLASK_ENV as shown on the previous page.

Run the `init-db` command:
```cmd
flask init-db
Initialized the database.
```

There will now be a `flaskr.sqlite` file in the `instance` folder in your project.

### Blueprints and Views

A view function is the code you write to respond to requests to your application. Flask uses patterns to match the incoming request URL to the view that should handle it. The view returns data that Flask turns into an outgoing response. Flask can also go the other direction and generate a URL to a view based on its name and arguments.

#### Create a Blueprint

A [Blueprint](http://flask.pocoo.org/docs/1.0/api/#flask.Blueprint) is a way to organize a group of related views and other code. Rather than registering views and other code directly with an application, they are registered with a blueprint. Then the blueprint is registered with the application when it is available in the factory function.

Flaskr will have two blueprints, one for authentication functions and one for the blog posts functions. The code for each blueprint will go in a separate module. Since the blog needs to know about authentication, you'll write the authentication one first.

`flaskr/auth.py`
```python
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

```

This creates a [Blueprint](http://flask.pocoo.org/docs/1.0/api/#flask.Blueprint) named `auth`. Like the application object, the blueprint needs to know where it's defined, so `__name__` is passed as the second argument. The `url_prefix` will be prepended to all the URLs associated with the blueprint.

Import and register the blueprint from the factory using [app.register_blueprint()](http://flask.pocoo.org/docs/1.0/api/#flask.Flask.register_blueprint). Place the new code at the end of the factory function before returning the app.

`flaskr/__init__.py`
```python
def create_app():
    app = ...
    # existing code omitted

    from . import auth
    app.register_blueprint(auth.bp)

    return app
```

The authentication blueprint will have views to register new users and to log in and log out.

### The First View: Register

When the user visits the `/auth/register` URL, the `register` view will return HTML with a form for them to fill out. When they submit the form, it will validate their input and either show the form again with an error message or create the new user and go to the login page.

For now you will just write the view code. Later, you'll write templates to generate the HTML form.

`flaskr/auth.py`
```python
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
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
```

Here's what the `register` view function is doing:

1. [@bp.route](http://flask.pocoo.org/docs/1.0/api/#flask.Blueprint.route) associates the URL `/register` with the `register` view function. When Flask receives a request to `/auth/register` it will call the `register` view and use the return value as the response.

2. If the user submitted the form, [request.method](http://flask.pocoo.org/docs/1.0/api/#flask.Request.method) will be `POST`. In this case, start validating the input.

3. [request.form](http://flask.pocoo.org/docs/1.0/api/#flask.Request.form) is a special type of [dict](https://docs.python.org/3/library/stdtypes.html#dict) mapping submitted form keys and values. The user will input their `username` and `password`.

4. Validate that `username` and `password` are not empty.

5. Valdate that `username` is not already registered by querying the database and checking if a result is returned. [db.execute](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.execute) takes a SQL query with `?` placeholders for any user input, and a tuple of values to replace the placeholders with. The database library will take care of escaping the values so you are not vulnerable to a *SQL injection attack*.

    [fetchone()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchone) returns one row from the query. If the query returned no results, it returns `None`. Later, [fetchall()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.fetchall) is used, which returns a list of all results.

6. If validation succeeds, insert the new user data into the database. For security, passwords should never be stored in the db directly. Instead, [generate_password_hash()](http://werkzeug.pocoo.org/docs/utils/#werkzeug.security.generate_password_hash) is used to securely has the password, and that hash is stored. Since this query modifies the data, [db.commit()](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.commit) needs to be called afterwards to save the changes.

7. After storing the user, they are redirected to the login page. [url_for()](http://flask.pocoo.org/docs/1.0/api/#flask.url_for) generates the URL for the login view based on its name. This is preferable to writing the URL directly as it allows you to change the URL later without changing all code that links to it. [redirect()](http://flask.pocoo.org/docs/1.0/api/#flask.redirect) generates a redirect response to the generated URL.

8. If validation fails, the error is shown to the user. [flash()](http://flask.pocoo.org/docs/1.0/api/#flask.flash) stores messages that can be retrieved when rendering the template.

9. When the user initially navigates to `auth/register`, or there was a validation error, an HTML page with the registration form should be shown. [render_template()](http://flask.pocoo.org/docs/1.0/api/#flask.render_template) will render a template containing the HTML, which you'll write in the next step of the tutorial

### Login

This view follows the same pattern as the `register` view above.

`flaskr/auth.py`

```python
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')
```

There are a few differences from the `register` view:

1. The user is queried first and stored in a variable for later use.

2. [check_password_hash()](http://werkzeug.pocoo.org/docs/utils/#werkzeug.security.check_password_hash) hashes the submitted password in the same way as the stored hash and securely compares them. If they match, the password is valid.

3. [session](http://flask.pocoo.org/docs/1.0/api/#flask.session) is a [dict](https://docs.python.org/3/library/stdtypes.html#dict) that stores data across requests. When validation succeeds, the user's `id` is stored in a new session. The data is stored in a *cookie* that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely *signs* the data so that it can't be tampered with.

Now that the user's `id` is stored in the [session](http://flask.pocoo.org/docs/1.0/api/#flask.session), it will be available on subsequent requests. At the beginning of each request, if a user is logged in their information should be loaded and made available to other views.

`flaskr/auth.py`

```python
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
```

[bp.before_app_request()](http://flask.pocoo.org/docs/1.0/api/#flask.Blueprint.before_app_request) registers a function that runs before the view function, no matter what URL is requested. `load_logged_in_user` checks if a user id is stored in the [session](http://flask.pocoo.org/docs/1.0/api/#flask.session) and gets that user's data from the database, storing it on [g.user](http://flask.pocoo.org/docs/1.0/api/#flask.g), which lasts for the length of the request. If there is no user id, or if the id doesn't exist, `g.user` will be `None`.

### Logout

To log out, you need to remove the user id from the [session](http://flask.pocoo.org/docs/1.0/api/#flask.session). Then `load_logged_in_user` won't load a user on subsequent requests.

`flaskr/auth.py`

```python
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
```

### Require Authentication in Other Views

Creating, editing, and deleting blog posts will require a user to be logged in. A *decorator* can be used to check this for each view it's applied to.

`flaskr/auth.py`

```python
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
```

This decorator returns a new view function that wraps the original view it's appied to. The new function checks if a user is loaded and redirects to the login page otherwise. If a user is loaded the original view is called and continues normally. You'll use this decorator when writing the blog views.

### Endpoints and URLs

The [url_for()](http://flask.pocoo.org/docs/1.0/api/#flask.url_for) function generates the URL to a view based on a name and arguments. The name associated with a view is also called the *endpoint*, and by default it's the same as the name of the view function.

For example, the `hello()` view that was added to the app factory earlier in the tutorial has the name `'hello'` and can be linked to with `url_for('hello')`. If it took an argument, which you'll see later, it would be linked to using `url_for('hello'), who='World'`.

When using a blueprint, the name of the blueprint is prepended to the name of the functions, so the endpoint for the `login` function you wrote above is `'auth.login'` because you added it to the `'auth'` blueprint.

## Templates

You've written the authentication views for your application, but if you're running the server and try to go to any of the URLs, you'll see a `TemplateNotFound` error. That's because the views are calling [render_template()](http://flask.pocoo.org/docs/1.0/api/#flask.render_template), but you haven't written the templates yet. The template files will be stored in the `templates` directory inside the `flaskr` package.

Templates are files that contain static data as well as placeholders for dynamic ata. A template is rendered with specific data to produce a final document. Flask uses the [Jinja](http://jinja.pocoo.org/docs/templates/) template library to render templates.

In you application, you will use templates to render [HTML](https://developer.mozilla.org/docs/Web/HTML) which will display in the user's browser. In Flask, Jinja is configured to *autoescape* any data that is rendered in HTML templates. This means that it's safe to render user input; any characters they've entered the could mess with the HTML, such as `<` and `>` will be *escaped* with *safe* values that look the same in the browser but don't cause unwanted effects.

Jinja looks and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. Anything between `{{` and `}}` is an expression that will be output to the final document. `{%` and `%}` denotes a control flow statement like `if` and `for`. Unlike Python, blocks are denoted by start and end tags rather than indentation since static text within a block could change indentation.

### The Base Layout

Each page in the application will have the same basic layout around a different body. Instead of writing the entire HTML structure in each template, each template will *extend* a base template and override specific sections.

`flaskr/templates/base.html`

```html
<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
    <h1>Flaskr</h1>
    <ul>
        {% if g.user $}
            <li><span>{{ g.user['username'] }}</span>
            <li><a href="{{ url_for('auth.logout') }}">Log out</a>
        {% else %}
            <li><a href="{{ url_for('auth.register') }}">Register</a>
            <li><a href="{{ url_for('auth.login') }}">Log In</a>
        {% endif %}
    </ul>
</nav>
<section class="content">
    <header>
        {% block header %}{% endblock %}
    </header>
    {% for message in get_flashed_messages() %}
        <div class="flash">{{ message }}</div>
    {% endfor %}
    {% block content %}{% endblock %}
</section>
```

[g](http://flask.pocoo.org/docs/1.0/api/#flask.g) is automatically available in templates. Based on if `g.user` is set (from `load_logged_in_user`), either the username and a logout link are displayed, otherwise links to register and log in are displayed. [url_for()](http://flask.pocoo.org/docs/1.0/api/#flask.url_for) is also automagically available, and is used to generate URLs to views instead of writing them out manually.

AFter the page title, and before the content, the template loops over each message returned by [get_flashed_messages()](http://flask.pocoo.org/docs/1.0/api/#flask.get_flashed_messages) is also automatically available, and is used to generate URLs to views instead of writing them out manually.

After the page title, and before the content, the template loops over each message returned by [get_flashed_messages()](http://flask.pocoo.org/docs/1.0/api/#flask.get_flashed_messages). You used [flash()](http://flask.pocoo.org/docs/1.0/api/#flask.flash) in the views to show error messages, and this is the code that will display them.

There are three blocks defined here that will be overridden in the other templates:

1. `{% block title %}` will change the title displayed in the browser's tab and window title.

2. `{% block header %}`is similar to `title` but will change the title displayed on the page.

3. `{% block content %}` is where the content of each page goes, such as the login form or a blog post.

The base template is directly in the `templates` directory. To keep the others organized, the templates for a blueprint will be placed in a directory with the same name as the blueprint.

### Register

`flaskr/templates/auth/register.html`

```html
{% extends 'base.html' %}

{% block header %}
    <h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}

{% block content %}
    <form method="post">
        <label for="username">Username</label>
        <input name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <input type="submit" value="Register">
    </form>
{% endblock %}
```

`{% extends 'base.html' %}` tells Jinja that this template should replace the blocks from the base template. All the rendered content must appear inside `{% block %}` tags that override blocks from the base template.

A useful pattern used here is to place `{% block title %}` inside `{% block header %}`. This will set the title block and then output the value of it into the header block, so that both the window and page share the same title without writing it twice.

The `input` tags are using the `required` attribute here. This tells the browser not to submit the form until those fields are filled in. If the user is using an older browser that doesn't support that attribute, or if they are using something besides a browser to make requests, you still want to validate the data in the Flask view. It's important to always fully validate the data on the server, even if the client does some validation as well.

### Log In

This is identical to the register template except for the title and submit button.

`flaskr/templates/auth/login.html`

```html
{% extends 'base.html %}

{% block header %}
    <h1>{% block title %}Log In{% endblock %}</h1>
{% endblock %}

{% block content %}
    <form method="post">
        <label for="username">Username</label>
        <input name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <input type="submit" value="Log In">
    </form>
{% endblock %}
```

### Register A User

Now that the authentication templates are written, you can register a user. Make sure the server is still running (`flask run` if it's not), then go to [http://127.0.0.1:5000/auth/register](http://127.0.0.1:5000/auth/register).

Try click the "Register" button without filling out the form and see that the browser shows an error message. Try removing the `required` attributes from the `register.html` template and click "Register" again. Instead of the browser showing an error, the page will reload and the error from [flash()](http://flask.pocoo.org/docs/1.0/api/#flask.flash) in the view will be shown.

Fill out a username and password and you'll be redirected to the login page. Try entering an incorrect username, or the correct username and incorrect password. If you log in you'll get an error because there's no `index` view to redirect to yet.

## Static Files

The authentication views and templates work but they look very plain right now. Some [CSS](https://developer.mozilla.org/docs/Web/CSS) can be added to add style to the HTML layout you constructed. The style won't change, so it's a *static* file rather than a template.

Flask automagically adds a `static` view that takes a path relative to the `flaskr/static` directory and serves it. The `base.html` template already has a link to the `style.css` file:

```html
{{ url_for('static', filename='style.css') }}
```

Besides CSS, other types of static files might be files with JavaScript functions, or a logo image. They are all placed under the `flaskr/static` directory and referenced with `url_for('static', filename='...')`.

This tutorial isn't focused on how to write CSS, so you can just copy the following in the `flaskr/static/style.css` file:

`flaskr/static/style.css`

```css
html { font-family: sans-serif; background: #eee; padding: 1rem; }
body { max-width: 960px; margin: 0 auto; background: white; }
h1 { font-family: serif; color: #377ba8; margin: 1rem 0; }
a { color: #377ba8; }
hr { border: none; border-top: 1px solid lightgray; }
nav { background: lightgray; display: flex; align-items: center; padding: 0 0.5rem; }
nav h1 { flex: auto; margin: 0; }
nav h1 a { text-decoration: none; padding: 0.25rem 0.5rem; }
nav ul  { display: flex; list-style: none; margin: 0; padding: 0; }
nav ul li a, nav ul li span, header .action { display: block; padding: 0.5rem; }
.content { padding: 0 1rem 1rem; }
.content > header { border-bottom: 1px solid lightgray; display: flex; align-items: flex-end; }
.content > header h1 { flex: auto; margin: 1rem 0 0.25rem 0; }
.flash { margin: 1em 0; padding: 1em; background: #cae6f6; border: 1px solid #377ba8; }
.post > header { display: flex; align-items: flex-end; font-size: 0.85em; }
.post > header > div:first-of-type { flex: auto; }
.post > header h1 { font-size: 1.5em; margin-bottom: 0; }
.post .about { color: slategray; font-style: italic; }
.post .body { white-space: pre-line; }
.content:last-child { margin-bottom: 0; }
.content form { margin: 1em 0; display: flex; flex-direction: column; }
.content label { font-weight: bold; margin-bottom: 0.5em; }
.content input, .content textarea { margin-bottom: 1em; }
.content textarea { min-height: 12em; resize: vertical; }
input.danger { color: #cc2f2e; }
input[type=submit] { align-self: start; min-width: 10em; }
```

You can find a less compact version of `style.css` in the [example code](https://github.com/pallets/flask/tree/1.0.2/examples/tutorial/flaskr/static/style.css).

Go to [http://127.0.0.1:5000/auth/login](http://127.0.0.1:5000/auth/login) and the page should look like the screenshot below:

![flaskr register image](http://flask.pocoo.org/docs/1.0/_images/flaskr_login.png)

You can read more about CSS from [Mozilla's documentation](https://developer.mozilla.org/docs/Web/CSS). If you change a static file, refresh the browser page. If the change doesn't show up, try clearing your browser's cache.