
import os
import json
import shutil
import unittest
from fdutil.path_tools import pop_path
from configurationutil import configuration
from jsonschema import SchemaError, ValidationError
from fdutil.parse_json import write_json_to_file

__author__ = u'Oli Davis'
__copyright__ = u'Copyright (C) 2016 Oli Davis'


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.0'
        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()  # Calling this here to ensure config re-inited following deletion in cleanup!

        self.addCleanup(self.clean)

    def tearDown(self):
        pass

    @staticmethod
    def clean():
        try:
            shutil.rmtree(pop_path(pop_path(configuration.Configuration().config_path)) + os.sep)

        except OSError:
            pass

    def test_instantiation(self):
        configuration.APP_NAME = u'PyTestApp2'
        self.cfg2 = configuration.Configuration()

        self.assertEqual(self.cfg1, self.cfg2,
                         msg=u'Configuration instantiation: Classes do not match, should be singleton!')

        self.assertEqual(self.cfg1.app_name, self.cfg2.app_name,
                         msg=u'Configuration instantiation: app_name does not match!')

        self.assertEqual(self.cfg1.app_version, self.cfg2.app_version,
                         msg=u'Configuration instantiation: app_version does not match!')

        self.assertEqual(self.cfg1.app_author, self.cfg2.app_author,
                         msg=u'Configuration instantiation: app_author does not match!')

    def test_instantiation_invalid_master_config(self):

        # make config invalid
        pth = self.cfg1.config_path
        cfg = json.load(open(os.path.join(pth, u'master_config.json')))
        fn, ext = u'master_config.json'.split(u'.')

        cfg[u'invalid_node'] = u'invalid_node_data'

        write_json_to_file(content=cfg,
                           output_dir=pth,
                           filename=fn,
                           file_ext=ext)

        with self.assertRaises(ValidationError):
            self.cfg1 = configuration.Configuration()
            self.cfg1.__init__()

    def test_check_registration(self):

        self.cfg1.register(config=u'test_check_registration',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_check_registration'))
        self.assertFalse(self.cfg1.check_registration(u'test_check_registration_missing'))

    def test_register(self):

        self.cfg1.register(config=u'test_register',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_register'))

    def test_register_valid_schema(self):

        self.cfg1.register(config=u'test_register_valid_schema',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_register_valid_schema'))

    def test_register_invalid_schema(self):
        with self.assertRaises(SchemaError):
            self.cfg1.register(config=u'test_invalid_schema',
                               config_type=configuration.CONST.json,
                               template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                               schema=os.path.join(pop_path(__file__), u'resources', u'invalid_schema.json'))

    def test_register_invalid_config_template(self):
        with self.assertRaises(ValidationError):
            self.cfg1.register(config=u'test_invalid_template',
                               config_type=configuration.CONST.json,
                               template=os.path.join(pop_path(__file__), u'resources', u'invalid_template.json'),
                               schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

    def test_unregister(self):

        self.cfg1.register(config=u'test_unregister',
                           config_type=configuration.CONST.json)

        self.cfg1.unregister(config=u'test_unregister')

        self.assertFalse(self.cfg1.check_registration(u'test_unregister'))

    def test_get(self):
        self.cfg1.register(config=u'test_get',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_get.testitem'] = u'Get some config!'

        self.assertEqual(self.cfg1[u'test_get.testitem'], u'Get some config!',
                         u'Get failed as we cannot retrieve the value we tried to set!')

    def test_get_all_items(self):
        self.cfg1.register(config=u'test_get_all_items',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_get_all_items.testitem'] = u'Get some config!'

        with self.assertRaises(NotImplementedError):
            _ = self.cfg1[u'test_get_all_items']

        # TODO: Will need re-writing once functionality has been decided!

    def test_get_missing_item(self):
        self.cfg1.register(config=u'test_get_missing_item',
                           config_type=configuration.CONST.json)

        with self.assertRaises(LookupError):
            _ = self.cfg1[u'test_get_missing_item.testitem']

    def test_get_master_config_unavailable(self):
        with self.assertRaises(KeyError):
            _ = self.cfg1[u'master_config']

    def test_get_config_file_removed(self):
        self.cfg1.register(config=u'test_get_remove_file',
                           config_type=configuration.CONST.json)

        cfg_type = configuration.CFG_TYPES.get(configuration.CONST.json)
        os.remove(os.path.join(self.cfg1.config_path, u'test_get_remove_file.' + cfg_type.get(u'ext')))

        self.cfg1[u'test_get_remove_file.testitem'] = u'Get some config!'

        self.assertEqual(self.cfg1[u'test_get_remove_file.testitem'], u'Get some config!',
                         u'Get failed as we cannot retrieve the value we tried to set!')

    def test_set(self):
        self.cfg1.register(config=u'test_set',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_set.testitem'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_set.testitem'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

    def test_set_all_items(self):
        self.cfg1.register(config=u'test_set_all_items',
                           config_type=configuration.CONST.json)

        with self.assertRaises(NotImplementedError):
            self.cfg1[u'test_set_all_items'] = None

        # TODO: Will need re-writing once functionality has been decided!

    def test_set_invalid_config(self):

        # Register a config that has a schema
        self.cfg1.register(config=u'test_set_invalid_config',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_set_invalid_config'))

        # Try and add an invalid config value
        with self.assertRaises(ValidationError):
            self.cfg1[u'test_set_invalid_config.cfg2'] = 123

    def test_del(self):
        self.cfg1.register(config=u'test_del',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_del.testitem'] = u'Del some config!'

        del self.cfg1[u'test_del.testitem']

        with self.assertRaises(LookupError):
            _ = self.cfg1[u'test_del.testitem']

    def test_del_all_items(self):
        self.cfg1.register(config=u'test_del_all_items',
                           config_type=configuration.CONST.json)

        with self.assertRaises(ValueError):
            del self.cfg1[u'test_del_all_items']

    def test_del_invalid_config(self):

        # Register a config that has a schema
        self.cfg1.register(config=u'test_set_invalid_config',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'valid_template.json'),
                           schema=os.path.join(pop_path(__file__), u'resources', u'valid_schema.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_set_invalid_config'))

        # Try and add an invalid config value
        with self.assertRaises(ValidationError):
            del self.cfg1[u'test_set_invalid_config.cfg1']

    def test_find(self):

        self.cfg1.register(config=u'test_find',
                           config_type=configuration.CONST.json)

        self.cfg1[u'test_find.testitem1'] = {u'A': 1, u'B': 2, u'C': 3}
        self.cfg1[u'test_find.testitem2'] = {u'A': 1, u'B': 5, u'C': 6}
        self.cfg1[u'test_find.testitem3'] = {u'A': 7, u'B': 2, u'C': 6}

        filters = [(u'C', 6)]

        expected_output = {
            u'testitem2': {u'A': 1, u'B': 5, u'C': 6},
            u'testitem3': {u'A': 7, u'B': 2, u'C': 6}
        }

        self.assertEqual(self.cfg1.find(u'test_find', filters), expected_output,
                         u'Find C = 6 failed!')

    def test_upgrade_instantiation(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.assertEqual(self.cfg1.app_name, configuration.APP_NAME,
                         msg=u'Configuration instantiation: app_name does not match!')

        self.assertEqual(self.cfg1.app_version, u'1.1',
                         msg=u'Configuration instantiation: app_version does not match!')

        self.assertEqual(self.cfg1.app_author, configuration.APP_AUTHOR,
                         msg=u'Configuration instantiation: app_author does not match!')

    def test_get_previous_versions(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        expected_output = [u'1.0', u'1.1']

        self.assertEqual(self.cfg1.previous_versions, expected_output,
                         u'Get previous versions does not match')

    def test_get_last_version(self):
        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.1'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        expected_output = u'1.1'

        self.assertEqual(self.cfg1.last_version, expected_output,
                         u'Get last version does not match')

    def test_get_last_version_none(self):

        expected_output = None

        self.assertEqual(self.cfg1.last_version, expected_output,
                         u'Get last version none does not match')

    def test_upgrade_config_merge(self):
        self.cfg1.register(config=u'test_upgrade',
                           config_type=configuration.CONST.json)

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade'))

        self.cfg1[u'test_upgrade.new_item'] = u'Set some config!'

        self.assertEqual(self.cfg1[u'test_upgrade.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.cfg1[u'test_upgrade.template_item'] = u'Set some config in the template!'

        self.assertEqual(self.cfg1[u'test_upgrade.template_item'], u'Set some config in the template!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        configuration.APP_NAME = u'PyTestApp'
        configuration.APP_AUTHOR = u'TEST'
        configuration.APP_VERSION = u'1.2'  # Skips a version to make sure this is ok!

        self.cfg1 = configuration.Configuration()
        self.cfg1.__init__()

        self.cfg1.register(config=u'test_upgrade',
                           config_type=configuration.CONST.json,
                           template=os.path.join(pop_path(__file__), u'resources', u'upgrade_template.json'))

        self.assertTrue(self.cfg1.check_registration(u'test_upgrade'))

        self.assertEqual(self.cfg1[u'test_upgrade.new_item'], u'Set some config!',
                         u'Set failed as we cannot retrieve the value we tried to set!')

        self.assertEqual(self.cfg1[u'test_upgrade.template_item'], u'Set some config in the template!',
                         u'Set failed as we cannot retrieve the value we tried to set!')


if __name__ == u'__main__':
    unittest.main()
