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
