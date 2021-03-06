![](http://pinaxproject.com/pinax-design/patches/pinax-messages.svg)

# Pinax Messages

[![](https://img.shields.io/pypi/v/pinax-messages.svg)](https://pypi.python.org/pypi/pinax-messages/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://pypi.python.org/pypi/pinax-messages/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-messages.svg)](https://circleci.com/gh/pinax/pinax-messages)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-messages.svg)](https://codecov.io/gh/pinax/pinax-messages)
[![](https://img.shields.io/github/contributors/pinax/pinax-messages.svg)](https://github.com/pinax/pinax-messages/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-messages.svg)](https://github.com/pinax/pinax-messages/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-messages.svg)](https://github.com/pinax/pinax-messages/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)

`pinax-messages` is an app for providing private user-to-user threaded messaging.


### Supported Django and Python Versions

* Django 1.8, 1.10, 1.11, and 2.0
* Python 2.7, 3.4, 3.5, and 3.6

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Template Tags](#template-tags-and-filters)
* [Reference Guide](#reference-guide)
* [Change Log](#change-log)
* [Project History](#project-history)
* [About Pinax](#about-pinax)


## Installation

### Install `pinax-messages`

* Add `"pinax-messages"` to your `requirements.txt` file or install pinax-messages manually:

```
$ pip install pinax-messages
```

* Add `"pinax.messages"` to your `INSTALLED_APPS` setting:


    INSTALLED_APPS = (
        ...
        "pinax.messages"
        ...
    )

### Run Migrations

* Run Django migrations to create `pinax-messages` database tables:

```
$ python manage.py migrate
```

### Hook Up URLs

Add `pinax.messages.urls` to your project urlpatterns:

    urlpatterns = [
        ...
        url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
        ...
    ]


## Usage

`pinax-messages` handles user-to-user private threaded messaging primarily by the inclusion of template snippets.
These snippets fall into three categories: view message inbox (all threads), view message thread, and create (or respond to) a message.

### Access Inbox

Place this snippet wherever a "Message Inbox" link is needed for viewing user message inbox:

```html
<a href="{% url 'pinax_messages:inbox' %}"><i class="fa fa-envelope"></i> {% trans "Message Inbox" %}</a>
```

### View Message Thread

Place this snippet wherever you have need to view a specific message thread:

```html
<a href="{% url 'pinax_messages:thread_detail' thread.pk %}"><i class="fa fa-envelope"></i> {% trans "View Message Thread" %}</a>
```

### Create Message - Template

Add the following line to an object template in order to provide a button for messaging a user associated with `object`:

```html
<a href="{% url "pinax_messages:message_user_create" user_id=object.user.id %}" class="btn btn-default">Message this user</a>
```

### Create Message - Code

Use the following code to create a new message programmatically. Note that `to_users` (message recipients) is a list, allowing messages sent to multiple users.

```python
from pinax.messages.models import Message

Message.new_message(from_user=self.request.user, to_users=[user], subject=subject, content=content)
```

### Template Context Variables

`pinax-messages` provides two context variables using a template context processor. In order to access these in your templates, add `user_messages` to your `TEMPLATES` settings:

```python
TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            # ...
            "context_processors": [
                # ...
                "pinax.messages.context_processors.user_messages"
            ],
        },
    },
]
```

The following context variables are available, and work with the current authenticated user:

* `inbox_threads` — all message threads for current user
* `unread_threads` — unread message threads for current user

#### Templates

[Example templates](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap/templates/pinax/messages) are available in the `pinax-theme-bootstrap` [project](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap).


## Template Tags and Filters

### unread

Determines if a message thread has unread messages for a user.

**Argument**: `user`

For instance if there are unread messages in a thread, change the CSS class accordingly:

```html
{% load pinax_messages_tags %}

    <div class="thread {% if thread|unread:user %}unread{% endif %}">
    ...
    </div>
```

### unread_thread_count

Returns the number of unread threads for the user. Use for notifying a user of new messages, for example in _account_bar.html

**Argument**: `user`

For instance if there are unread messages in a thread, change the CSS class accordingly:

```html
{% load pinax_messages_tags %}

    {% with user|unread_thread_count as user_unread %}
    <li class="{% if user_unread %}unread{% endif %}">
        <a href="{% url 'pinax_messages:inbox' %}"><i class="fa fa-envelope"></i> {% trans "Messages" %}
            {% if user_unread %}<sup>{{ user_unread }}</sup>{% endif %}
        </a>
    </li>        
    {% endwith %}
```

## Reference Guide

### URL–View–Template Matrix

| URL Name                             | View                  | Template              |
| ------------------------------------ | --------------------- | --------------------- |
| `pinax-messages:inbox`               | `InboxView()`         | `inbox.html`          |
| `pinax-messages:message_create`      | `MessageCreateView()` | `message_create.html` |
| `pinax-messages:message_user_create` | `MessageCreateView()` | `message_create.html` |
| `pinax-messages:thread_detail`       | `ThreadView()`        | `thread_detail.html`  |
| `pinax-messages:thread_delete`       | `ThreadDeleteView()`  | N/A                   |

### URL Names

These URL names are available when using pinax-messages urls.py:

`pinax-messages:inbox` — Inbox view

`pinax-messages:message_create` — Create new message

`pinax-messages:message_user_create` — Create new message to specific user

`pinax-messages:thread_detail` — View message thread, requires thread PK

`pinax-messages:thread_delete` — Delete message thread, requires thread PK

### Views

`InboxView` - Display all message threads

`MessageCreateView` — Create a new message thread

`ThreadView` — View specific message thread

`ThreadDeleteView` — Delete specific message thread

### Forms

`NewMessageForm` — creates a new message thread to a single user

`NewMessageFormMultiple` — creates a new message thread to multiple users

`MessageReplyForm` - creates a reply to a message thread

### Templates

[Example templates](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap/templates/pinax/messages) are found in the `pinax-theme-bootstrap` [project](https://github.com/pinax/pinax-theme-bootstrap/tree/master/pinax_theme_bootstrap).

`pinax/messages/inbox.html` — Displays inbox message threads

`pinax/messages/thread_detail.html` — Show message thread and allow response

`pinax/messages/message_create.html` — New message form

### Signals

`message_sent` — `providing_args = ["message", "thread", "reply"]`


## Change Log

### 1.2.0

* Add `unread_thread_count` template filter

### 1.1.0

* Add Django 2.0 compatibility testing
* Drop Django 1.9 and Python 3.3 support
* Move documentation into README
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description

### 1.0.1

- Fix thread delete view with correct template path and success URL

### 1.0.0

- add documentation

### 0.3

- convert to Django generic CBVs
- various fixes and cleanup

### 0.1

- initial release


## Project History

This app was formerly named `user-messages` but was renamed after being donated to Pinax from Eldarion.


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.

The Pinax documentation is available at http://pinaxproject.com/pinax/. If you would like to help us improve our documentation or write more documentation, please join our Pinax Project Slack team and let us know!

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out our blog http://blog.pinaxproject.com.
