# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import django

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'NOTASECRET'


if django.VERSION[:2] == (1, 8):
    # Use a wrapper that includes Django commit 4f6a7663bcddffb114f2647f9928cbf1fdd8e4b5
    # so that full SQL queries from sqlite come through
    engine = 'django18_sqlite3_backend'
else:
    engine = 'django.db.backends.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': engine,
        'NAME': ':memory:',
    },
    'replica': {
        'ENGINE': engine,
        'NAME': ':memory:',
        'TEST': {
            'MIRROR': 'default',
        }
    },
    'second': {
        'ENGINE': engine,
        'NAME': ':memory:',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'second': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'testapp',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
