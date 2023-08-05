# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import pytest
import six
from django.core.cache import caches
from django.db.models import Q
from django.db.models.functions import Upper
from django.test import TestCase

from django_perf_rec import TestCaseMixin, record
from testapp.models import Author

from .utils import temporary_path, run_query

FILE_DIR = os.path.dirname(__file__)


class RecordTests(TestCase):

    def test_single_db_query(self):
        with record():
            run_query('default', 'SELECT 1337')

    def test_multiple_db_queries(self):
        with record():
            run_query('default', 'SELECT 1337')
            run_query('default', 'SELECT 4949')

    def test_non_deterministic_QuerySet_annotate(self):
        with record():
            list(Author.objects.annotate(
                x=Upper('name'),
                y=Upper('name'),
            ))

    def test_non_deterministic_QuerySet_extra(self):
        with record():
            list(Author.objects.extra(select={
                'x': '1',
                'y': '1',
            }))

    def test_non_deterministic_Q_query(self):
        with record():
            list(Author.objects.filter(Q(name='foo', age=1)))

    def test_single_cache_op(self):
        with record():
            caches['default'].get('foo')

    def test_multiple_cache_ops(self):
        with record():
            caches['default'].set('foo', 'bar')
            caches['second'].get_many(['foo', 'bar'])
            caches['default'].delete('foo')

    def test_multiple_calls_in_same_function_are_different_records(self):
        with record():
            caches['default'].get('foo')

        with record():
            caches['default'].get('bar')

    def test_custom_name(self):
        with record(record_name='custom'):
            caches['default'].get('foo')

    def test_custom_name_multiple_calls(self):
        with record(record_name='custom'):
            caches['default'].get('foo')

        with pytest.raises(AssertionError) as excinfo:
            with record(record_name='custom'):
                caches['default'].get('bar')

        assert 'Performance record did not match' in six.text_type(excinfo.value)

    def test_path_pointing_to_filename(self):
        with temporary_path('custom.perf.yml'):

            with record(path='custom.perf.yml'):
                caches['default'].get('foo')

            assert os.path.exists('custom.perf.yml')

    def test_path_pointing_to_filename_record_twice(self):
        with temporary_path('custom.perf.yml'):

            with record(path='custom.perf.yml'):
                caches['default'].get('foo')

            with record(path='custom.perf.yml'):
                caches['default'].get('foo')

    def test_path_pointing_to_dir(self):
        temp_dir = os.path.join(FILE_DIR, 'perf_files/')
        with temporary_path(temp_dir):

            with record(path='perf_files/'):
                caches['default'].get('foo')

            full_path = os.path.join(
                FILE_DIR,
                'perf_files',
                'test_api.perf.yml',
            )
            assert os.path.exists(full_path)

    def test_custom_nested_path(self):
        temp_dir = os.path.join(FILE_DIR, 'perf_files/')
        with temporary_path(temp_dir):

            with record(path='perf_files/api/'):
                caches['default'].get('foo')

            full_path = os.path.join(
                FILE_DIR,
                'perf_files',
                'api',
                'test_api.perf.yml',
            )
            assert os.path.exists(full_path)

    def test_file_name_is_deprecated(self):
        full_path = os.path.join(FILE_DIR, 'test_api.perf.yml')

        with pytest.warns(DeprecationWarning) as warnings:
            with record(file_name=full_path):
                caches['default'].get('foo')

        assert len(warnings) == 1
        assert (
            "The 'file_name' argument of record is deprecated" in
            warnings[0].message.args[0]
        )


class TestCaseMixinTests(TestCaseMixin, TestCase):

    def test_record_performance(self):
        with self.record_performance():
            caches['default'].get('foo')

    def test_record_performance_record_name(self):
        with self.record_performance(record_name='other'):
            caches['default'].get('foo')

    def test_record_performance_file_name(self):
        perf_name = __file__.replace('.py', '.file_name.perf.yml')
        with self.record_performance(path=perf_name):
            caches['default'].get('foo')
