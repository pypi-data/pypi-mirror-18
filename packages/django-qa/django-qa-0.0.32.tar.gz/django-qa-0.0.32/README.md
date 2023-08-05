**WELCOME TO DJANGO-QA**
=========================
[![Build Status](https://travis-ci.org/swappsco/django-qa.svg?branch=master)](https://travis-ci.org/swappsco/django-qa)
[![Coverage Status](https://coveralls.io/repos/github/swappsco/django-qa/badge.svg?branch=master)](https://coveralls.io/github/swappsco/django-qa?branch=master)

## A Simple Q&A App using Python Django

[django-qa](http://swappsco.github.io/django-qa/) is a fork from [Simple-Q-A-App-using-Python-Django](http://arjunkomath.github.io/Simple-Q-A-App-using-Python-Django) aimed to create a pluggable package than allows to implement a StackOverflow-like forum site for your Django web project.
The development of this package is kindly supported by [SWAPPS](https://www.swapps.co/) and constantly developed by it's colaborators. Feel free to use it, add some issues if you find bugs or think of a really cool feature, even clone it and generate a pull requests to incorporate those cool features made by yourself; If you have special requirements, [drop us a few lines](https://www.swapps.co/) and perhaps we can help you out too.

This application is still under active development and we cannot guarantee that nothing will break between versions. Most of the core features are already there, so we expect to release a beta version soon.

## Features

* Assumes nothing about the rest of your application.
* Create questions and answers.
* Comment on questions and answers.
* Upvote/Downvote questions and answers.
* Users have a reputation and a profile.
* Support for tagging questions with django-taggit.
* Questions are categorized by latest, popular and most voted.

## Installation
Django-QA aims at keeping things simple. To install it you have to do what you would do with most django apps.

Install with pip:
```
pip install django-qa`
```

Add to INSTALLED_APPS in your project settings.
```python
INSTALLED_APPS = (
...
qa,
...
)
```

Add our urls to the project:
```python
urlpatterns = [
    ...,
    url(r'^', include('qa.urls')),
    ...
    ]
```

Run migrations:
```
python manage.py migrate
```

And that's it!

## About the functionality

* The package is integrated with the framework authentication process, right now the package defines an user profile linked to Django's user model, this models was created to contain information related to the user's activities inside the package functionalities.
* It has comments on questions and answers.
* It has no support for anonymous questions nor answers or comments.
* It has tagging support through django-taggit.
* It has a basic implementation for score and reputation records.

## Next steps
With this setup you will have a functional questions and answers section inside of your project. Probably you will need to work on changing the default templates to fit the look and feel of your site.

If your project has an user profile already, you may want to merge it with the data provided by this app (questions, answers, comments, reputation, etc). That requires some extra work, but can be done without using ugly hacks.

The template structure serves as a foundation for your project, but you can (and should) override the defaults to better suit your needs. For example we load bootstrap3 from a CDN, but if your application already has bootstrap in a package you can just extend from your main base template.

The package has no moderation options on none of the models yet and still lacks REST support.

If you think that something essential for this kind of application is missing, you can request a feature by adding an issue to our repository.
