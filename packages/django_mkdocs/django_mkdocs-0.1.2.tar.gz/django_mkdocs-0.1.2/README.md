# django-mkdocs

Django-mkdocs is built on the premise that there is a need for simple, beautiful, maintainable documentation which can be user-permissioned. The app is *heavily inspired* by [django-documentation](https://github.com/Narsil/django-documentation) with updated compatibility for Django 1.10, and uses [MkDocs](http://www.mkdocs.org/) to generate a static-site served by Django.

To be clear, django-mkdocs was not intended for large-scale access. It was originally created to serve documentation internally and to select partners. If your documents are intended to be public, using MkDocs alone with github-pages or Amazon S3 may be a better solution.


## Installation

Django-mkdocs can be installed directly from pip:
```
$ pip install django-mkdocs
```

### Plugging django-mkdocs into your Django project

In your Django project, add 'django_mkdocs' to your settings.py:
```
project/settings.py



INSTALLED_APPS = (
...
'django_mkdocs',
)
```

Add a reference to your projects urls.py:

```
project/urls.py



from django.conf.urls import url, include

...
...

urlpatterns = [
...
url(r'^docs/', include('django_mkdocs.urls', namespace='documentation')),
]
```

### Setting up the MkDocs documentation

MkDocs is included with django-mkdocs. The project naturally has excellent documentation and is linked [here](http://www.mkdocs.org/).

We recommend making a directory for your documentation in the root of your Django project, and starting a MkDocs project in there.

```
$ mkdocs new project_docs
```

Your directory structure should now look something like this:

```
├── manage.py
├── project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── project_docs
    ├── docs
    │   └── index.md
    └── mkdocs.yml
```

The main configuration file for MkDocs is mkdocs.yml. Let's move it into the Django project root for easier builds later on:
```
$ mv project_docs/mkdocs.yml ./mkdocs.yml
```

Now we'll need to change a couple of references in this file.
- **site_name** is the title of your HTML page
- **pages** tells MkDocs your desired site-structure and which markdown files should be used to generate it
- **docs_dir** refers to the markdown your documentation will be generated from, while
- **site_dir** refers to the location where the static site will be generated.
- Lastly, **use_directory_urls** should be set to false for Django's routing to work correctly.

```
mkdocs.yml



site_name: My Docs
pages:
    - Home: index.md
use_directory_urls: false
docs_dir: project_docs/docs
site_dir: project_docs/site

```

To build the documentation, run the following command from the directory containing mkdocs.yml. We include the optional *--clean* flag here to signify that site_dir should be cleansed of page references that have been removed from our mkdocs.yml.
```
$ mkdocs build --clean
```

It's also recommended that you add this command to your post-deployment script for fresh document builds each time you deploy.

### Options for serving the documentation

In order to serve your docs, django-mkdocs needs to know where to look for them. These settings must be configured in your project's settings.py. Set the DOCUMENTATION_ROOT to the directory which contains both your **docs_dir** and **site_dir** folders. In this snippet, 'PROJECT_DIR' is the absolute path to our Django project.

```
project/settings.py



# django-mkdocs demo parameters!
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DOCUMENTATION_ROOT = PROJECT_DIR + '/project_docs'
```

DOCUMENTATION_HTML_ROOT points to the root of our statically generated site. This should correspond to the same directory as our mkdocs.yml site_dir.
```
DOCUMENTATION_HTML_ROOT = DOCUMENTATION_ROOT + '/site'
```

DOCUMENTATION_ACCESS_FUNCTION is used in the views that attempt to access the documentation. Django-mkdocs calls DOCUMENTATION_ACCESS_FUNCTION with request.user as an argument. This flag determines who has access to view the docs.
```
DOCUMENTATION_ACCESS_FUNCTION = lambda user: user.is_staff
```

Django-mkdocs assumes an Nginx server is used by default to serve the documentation. DOCUMENTATION_XSENDFILE is set to true by default. If you are not using Nginx, expect a very small number of users, and understand the consequences of using django.views.static.serve, set the following flag:
```
DOCUMENTATION_XSENDFILE = False
```

## Viewing your documentation
With the above steps completed, you should now be able to view your static site at the endpoint defined in your project's urlconf. Let's test this out locally. First, run Django's development server from the project root:

```
$ python manage.py runserver
```

Point your browser to localhost:8000/docs (or the url you referenced). You should now see your generated docs!

NOTE: If following along in the demo project, you may need to run migrations and create a superuser. You will also need to authenticate at the django admin console at localhost:8000/admin after performing the following commands.

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

## Deploying to Heroku

You may also wish to have your documentation build automatically every time you deploy. One way to accomplish this with Heroku is to add a post deployment hook. From the root of your django project, create a directory named bin/, and in that directory, a script named *post_compile*.

```
$ mkdir bin
$ touch bin/post_compile
```

You can add any other shell commands you like, but let's add our build command.

```
bin/post_compile


echo "-----> Building MkDocs documentation"
mkdocs build --clean
```

And your final directory tree should look like this:

```
├── bin
│   └── post_compile
├── manage.py
├── mkdocs.yml
├── project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── project_docs
    ├── docs
    │   └── index.md
    └── site
```
