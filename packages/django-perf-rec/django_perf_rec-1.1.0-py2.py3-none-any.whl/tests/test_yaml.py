# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import shutil
from tempfile import mkdtemp

import pytest
import six
import yaml
from django.test import SimpleTestCase

from django_perf_rec.yaml import KVFile


class KVFileTests(SimpleTestCase):

    def setUp(self):
        super(KVFileTests, self).setUp()
        KVFile._clear_load_cache()
        self.temp_dir = mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        super(KVFileTests, self).tearDown()

    def test_load_no_permissions(self):
        with pytest.raises(IOError):
            KVFile('/')

    def test_load_non_existent_is_empty(self):
        kvf = KVFile(self.temp_dir + '/foo.yml')
        default = object()
        assert kvf.get('foo', default) is default

    def test_load_existent(self):
        file_name = self.temp_dir + '/foo.yml'
        with open(file_name, 'w') as fp:
            fp.write('foo: bar')

        assert KVFile(file_name).get('foo', '') == 'bar'

    def test_load_non_dictionary(self):
        file_name = self.temp_dir + '/foo.yml'
        with open(file_name, 'w') as fp:
            fp.write('[not, a, dictionary]')

        with pytest.raises(TypeError) as excinfo:
            KVFile(file_name)
        assert 'not a dictionary' in six.text_type(excinfo.value)

    def test_get_after_set_same(self):
        kvf = KVFile(self.temp_dir + '/foo.yml')
        kvf.set_and_save('foo', 'bar')

        assert kvf.get('foo', '') == 'bar'

    def test_load_second_same(self):
        kvf = KVFile(self.temp_dir + '/foo.yml')
        kvf.set_and_save('foo', 'bar')
        kvf2 = KVFile(self.temp_dir + '/foo.yml')

        assert kvf2.get('foo', '') == 'bar'

    def test_sets_dont_cause_append_duplication(self):
        file_name = self.temp_dir + '/foo.yml'
        kvf = KVFile(file_name)
        kvf.set_and_save('foo', 'bar')
        kvf.set_and_save('foo2', 'bar')

        with open(file_name, 'r') as fp:
            lines = fp.readlines()
            fp.seek(0)
            data = yaml.safe_load(fp)

        assert len(lines) == 2
        assert data == {'foo': 'bar', 'foo2': 'bar'}
