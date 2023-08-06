"""
Tests for nearby.config module
"""

import configparser
import os
import unittest

from nearby import config


TEST_CONF = os.path.join(os.path.dirname(__file__), 'data', 'test.conf')


class HostBasedConfigParserTestCase(unittest.TestCase):

    def setUp(self):
        self.simple = config.HostBasedConfigParser({
            'host': str,
            'remote_path': config._path_type,
            'local_path': config._path_type,
            'user': config._path_type,
        })
        self.simple.read(config._BASE_CONFIG)
        self.simple.add_section('__user_args__')

        self.complex = config.HostBasedConfigParser({
            'host': str,
            'remote_path': config._path_type,
            'local_path': config._path_type,
            'user': config._path_type,
        })
        self.complex.read([config._BASE_CONFIG, TEST_CONF])
        self.complex.add_section('__user_args__')

    def test_that_test_conf_exists(self):
        self.assertTrue(os.path.exists(TEST_CONF))

    def test_is_valid_ipv4_wildcard(self):
        good_ipv4_wildcards = [
            '127.0.0.1',
            '127.0.0.*',
            '127.0.*.0',
            '127.0.*.*',
            '127.*.*.*',
            '*.*.*.*',
        ]
        bad_ipv4_wildcards = [
            '*',
            'anything',
            '',
            '*.*.*',  # bad octet value
            '127.0.*',  # not enough octets
            '256.*.*.*',  # bad octet value
        ]
        for wildcard in good_ipv4_wildcards:
            self.assertTrue(
                self.simple._is_valid_ipv4_wildcard(wildcard))
        for wildcard in bad_ipv4_wildcards:
            self.assertFalse(
                self.simple._is_valid_ipv4_wildcard(wildcard))

    def test_transform_with_specificity(self):
        test_strs_to_expected = {
            '127.0.0.1': (r'^127\.0\.0\.1$', 4),
            '127.0.0.*': (r'^127\.0\.0\.\d{1,3}$', 3),
            '127.0.*.*': (r'^127\.0\.\d{1,3}\.\d{1,3}$', 2),
            '127.*.*.*': (r'^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$', 1),
            '*.*.*.*': (r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', 0),
            '*': (r'^.*$', 0),
            'bitbucket.org': (r'^bitbucket\.org$', 0),
            '*.bitbucket.org': (r'^.*\.bitbucket\.org$', 0),
            '*.*.bitbucket.org': (r'^.*\..*\.bitbucket\.org$', 0),
        }
        for test_str, expected in test_strs_to_expected.items():
            actual = self.simple._transform_with_specificity(test_str)
            self.assertEqual(actual, expected)

    def test_get_ipv4_specificity(self):
        test_strs_to_expected = {
            '127.0.0.1': 4,
            '127.0.0.*': 3,
            '127.0.*.1': 3,
            '127.0.*.*': 2,
            '127.*.*.*': 1,
            '*.*.*.*': 0,
        }
        for test_str, expected in test_strs_to_expected.items():
            actual = self.simple._get_ipv4_specificity(test_str)
            self.assertEqual(actual, expected)

    def test_get_hostname_specificity(self):
        test_strs_to_expected = {
            'anything': 0,
            '*': 0,
            '*anything*': 0,
            '*.bitbucket.org': 0,
            'bitbucket.org': 0,
        }
        for test_str, expected in test_strs_to_expected.items():
            actual = self.simple._get_hostname_specificity(test_str)
            self.assertEqual(actual, expected)

    def test_transform_ipv4_pattern(self):
        test_strs_to_expected = {
            '127.0.0.1': r'^127\.0\.0\.1$',
            '127.0.0.*': r'^127\.0\.0\.\d{1,3}$',
            '127.0.*.*': r'^127\.0\.\d{1,3}\.\d{1,3}$',
            '127.*.*.*': r'^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
            '*.*.0.*': r'^\d{1,3}\.\d{1,3}\.0\.\d{1,3}$',
            '*.*.*.*': r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
        }
        for test_str, expected in test_strs_to_expected.items():
            actual = self.simple._transform_ipv4_pattern(test_str)
            self.assertEqual(actual, expected)

    def test_transform_hostname_pattern(self):
        test_strs_to_expected = {
            'nativedev': '^nativedev$',
            '*nativedev*': '^.*nativedev.*$',
            '*': '^.*$',
            '*.bitbucket.org': '^.*\.bitbucket\.org$',
        }
        for test_str, expected in test_strs_to_expected.items():
            actual = self.simple._transform_hostname_pattern(test_str)
            self.assertEqual(actual, expected)

    def test_simple_get_specificity_list(self):
        test_strs_to_expected = {
            'nativedev': ['__user_args__'],
            '10.0.3.123': ['__user_args__']
        }
        for test_str, expected in test_strs_to_expected.items():
            actual = self.simple._get_specificity_list(test_str)
            self.assertEqual(actual, expected)

    def test_complex_get_specificity_list(self):
        test_strs_to_expected = {
            'nativedev': [
                # TODO: add specificity logic for hostnames
                '__user_args__',
                'host *',
                'host nativedev 10.0.3.123',
            ],
            '10.0.3.123': [
                '__user_args__',
                'host nativedev 10.0.3.123',
                'host 10.0.3.*',
                'host 10.0.*.*',
                'host 10.*.*.*',
                # TODO: make all ipv4 wildcards more specific
                #       than non-ipv4 wildcards
                'host *',
                'host *.*.*.*',
            ],
            '10.0.3.255': [
                '__user_args__',
                'host 10.0.3.*',
                'host 10.0.*.*',
                'host 10.*.*.*',
                'host *',
                'host *.*.*.*',
            ],
            '10.0.255.255': [
                '__user_args__',
                'host 10.0.*.*',
                'host 10.*.*.*',
                'host *',
                'host *.*.*.*',
            ],
            '10.255.255.255': [
                '__user_args__',
                'host 10.*.*.*',
                'host *',
                'host *.*.*.*',
            ],
            '255.255.255.255': [
                '__user_args__',
                'host *',
                'host *.*.*.*',
            ],
            'github.bitbucket.org': [
                '__user_args__',
                'host *',
            ],
            'bitbucket.org': [
                '__user_args__',
                'host bitbucket.org',
                'host *',
            ]
        }
        for test_str, expected in test_strs_to_expected.items():
            # TODO: returning specificity list in increasing order
            #       is leading to kludgy code in a couple of places. fix it
            actual = list(
                reversed(self.complex._get_specificity_list(test_str)))
            self.assertEqual(actual, expected)

    def test_has_own_option(self):
        with self.assertRaises(configparser.NoSectionError):
            self.simple.has_own_option('fictional', 'irrelevant')
        with self.assertRaises(configparser.NoSectionError):
            self.complex.has_own_option('fictional', 'irrelevant')
        self.assertTrue(self.complex.has_own_option('host 10.0.3.*', 'user'))
        self.assertFalse(self.complex.has_own_option('host 10.*.*.*', 'user'))

    def test_simple_get_option(self):
        self.assertEqual(
            self.simple.get_option('10.0.3.123', 'remote_path'), '/')
        # failure modes
        with self.assertRaises(configparser.NoOptionError):
            self.simple.get_option('10.0.3.123', 'fictional')
        with self.assertRaises(configparser.NoOptionError):
            self.simple.get_option('10.0.3.123', 'random_setting')

    def test_complex_get_option(self):
        # if these don't error out then cascading works properly
        self.complex.get_option('10.0.3.123', 'random_setting')
        self.complex.get_option('10.0.3.123', 'another_setting')
        self.complex.get_option('10.0.3.123', 'yet_another_setting')
        self.complex.get_option('10.0.3.123', 'still_yet_another_setting')

        self.assertEqual(
            self.complex.get_option('10.0.3.123', 'random_setting'),
            'specificitydependsonhostarg')
        with self.assertRaises(configparser.NoOptionError):
            self.complex.get_option('10.0.3.123', 'fictional')
        with self.assertRaises(configparser.NoOptionError):
            self.complex.get_option('10.0.3.124', 'random_setting')


class InitConfigTestCase(unittest.TestCase):
    """
    These are stupid tests.
    """

    def tearDown(self):
        config.delete_config()

    def test_no_user_args(self):
        config.init_config()

    def test_empty_user_args(self):
        config.init_config({})

    def test_with_user_args(self):
        config.init_config({'something': 'with a value'})

    def test_with_bad_user_args(self):
        with self.assertRaises(TypeError):
            config.init_config(object())


class GetOptionTestCase(unittest.TestCase):

    def tearDown(self):
        config.delete_config()

    def test_get_nonexistant_option(self):
        config.init_config()
        with self.assertRaises(configparser.NoOptionError):
            config.get_option('10.0.3.123', 'fictional')

    def test_get_existing_option(self):
        config.init_config()
        expected = os.path.expandvars('$USER')
        actual = config.get_option('10.0.3.123', 'user')
        self.assertEqual(actual, expected)

    def test_get_user_arg_option(self):
        config.init_config({'not fictional': 'but real'})
        expected = 'but real'
        actual = config.get_option('10.0.3.123', 'not fictional')
        self.assertEqual(actual, expected)

    def test_get_option_without_init_config(self):
        with self.assertRaises(Exception):
            config.get_option('10.0.3.123', 'user')
