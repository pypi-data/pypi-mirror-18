
import os
import shutil
from appdirs import AppDirs
from tempfile import mkdtemp
from jsonschema import validate, SchemaError, ValidationError

import logging_helper
from json_config import JSONConfig
from fdutil.list_tools import filter_list
from fdutil.path_tools import pop_path, ensure_path_exists
from classutils.singleton import SingletonType

__author__ = u'Oli Davis'
__copyright__ = u'Copyright (C) 2016 Oli Davis'

logging = logging_helper.setup_logging()

# App details
APP_NAME = None  # Once Configuration is initialised changes to this parameter will be ignored!
APP_AUTHOR = None  # Once Configuration is initialised changes to this parameter will be ignored!
APP_VERSION = None  # Once Configuration is initialised changes to this parameter will be ignored!


# Export constants
class _CONST:

    def __init__(self): pass

    # Master config properties
    @property
    def template(self): return u'master_config_template.json'

    @property
    def schema(self): return u'master_config_schema.json'

    # Config Keys
    @property
    def cfg_dir(self): return u'config'

    @property
    def cfg_schema(self): return u'schema'

    @property
    def cfg_template(self): return u'template'

    @property
    def cfg_fn(self): return u'filename'

    @property
    def cfg_type(self): return u'type'

    # Available Config types
    @property
    def json(self): return u'json'

CONST = _CONST()  # Initialise Constants


# Config Types
CFG_TYPES = {
    CONST.json: {
        u'class': JSONConfig,
        u'ext': u'json'
    }
}


class Configuration(object):

    __metaclass__ = SingletonType

    def __init__(self,
                 preload=False):

        """ Initialise Config class

            APP_NAME Must be set before initialisation.
            APP_AUTHOR is optional
            APP_VERSION is optional

            :param preload: Set True to preload all config objects
        """

        logging.info(u'Initialising configuration...')

        # Initialisation fails if APP_NAME has not been configured!
        if APP_NAME is None:
            raise ValueError(u'Cannot initialise configuration: APP_NAME not defined.')

        # Prepare app_dirs so we can setup paths
        self.__app_kwargs = {
            u'appname': APP_NAME
        }

        if APP_AUTHOR is not None:
            self.__app_kwargs[u'appauthor'] = APP_AUTHOR

        # Get reference to version agnostic paths for version checking
        self.__app_dirs_all_versions = AppDirs(**self.__app_kwargs)

        if APP_VERSION is not None:
            self.__app_kwargs[u'version'] = APP_VERSION

        # Set paths to users OS default locations.
        self.__app_dirs = AppDirs(**self.__app_kwargs)

        logging.debug(u'Config file path: {p}'.format(p=self.config_path))
        logging.debug(u'Config schema path: {p}'.format(p=self.schema_path))
        logging.debug(u'Config template path: {p}'.format(p=self.template_path))
        logging.debug(u'Cache path: {p}'.format(p=self.cache_path))
        logging.info(u'Data path: {p}'.format(p=self.data_path))
        logging.info(u'Log path: {p}'.format(p=self.log_path))

        # Set temp path
        self.__temp_path = mkdtemp(prefix=u'{app_name}_Temp_'.format(app_name=APP_NAME))
        logging.info(u'Temp path: {p}'.format(p=self.temp_path))

        # Set the master config path.  Any config required for this class to work will be stored here.
        self.__master_cfg_file = os.path.join(self.config_path, u'master_config.json')

        # Load the master config schema
        self.__master_cfg_schema_file = os.path.join(pop_path(__file__), CONST.schema)
        self.__master_cfg_schema_obj = self.__get_schema_obj(self.__master_cfg_schema_file)

        # Initialise master config
        self.__master_cfg = self.__init_cfg(config_file=self.__master_cfg_file,
                                            config_type=CONST.json,
                                            template=os.path.join(pop_path(__file__), CONST.template),
                                            schema=self.__master_cfg_schema_file)

        # Keep reference to registered configurations
        self.__registered_cfg = self.__master_cfg.cfg.get(u'registered_cfg')  # Keep a record of all registered config.
        self.__registered_cfg_objs = {}  # Keeping this record separate as they should not be dumped into config files.

        # If preload is set attempt to preload each registered config.
        if preload:
            for cfg in self.__registered_cfg:
                try:
                    self.__load_cfg(config=cfg)

                except (SchemaError, ValidationError) as err:
                    logging.warning(u'Failed pre-loading {cfg}: {err}'.format(cfg=cfg,
                                                                              err=err))

        logging.info(u'Configuration initialised.')

    def __init_cfg(self,
                   config_file,
                   config_type,
                   template=None,
                   schema=None):

        """ Initialise the config file

        If this is the first run the config will be created (either blank, from template or from previous config),
        otherwise, it will be loaded.

        :param config_file: Path to config file being created / loaded
        :param config_type: Config type from types available in CFG_TYPES.
        :param template:    Path to template file
        :param schema:      Path to schema file
        """

        cfg_type = CFG_TYPES.get(config_type)
        cfg_class = cfg_type.get(u'class')

        schema_obj = None

        if schema is not None:
            schema_obj = self.__get_schema_obj(schema)

        new = False if os.path.exists(config_file) else True

        cfg_obj = cfg_class(config_file=config_file,
                            create=True)

        if new:
            # initialise from a template (this is done whether template is set or not as there should be a default
            # template provided with the config class being initialised)
            self.__init_from_template(cfg_obj=cfg_obj,
                                      config_type=config_type,
                                      template=template,
                                      schema=schema)

            self.__init_from_previous_version(config_file=config_file,
                                              cfg_obj=cfg_obj,
                                              config_type=config_type,
                                              schema=schema)

        # If a schema is specified make sure the cfg_obj is valid before returning
        if schema is not None:
            validate(cfg_obj.cfg, schema_obj.cfg)  # if invalid this raises either SchemaError or ValidationError.

        return cfg_obj

    def __init_from_template(self,
                             cfg_obj,
                             config_type,
                             template=None,
                             schema=None):

        """ Initialise the configuration object from provided template

        :param cfg_obj:     Config object to initialise
        :param config_type: Config type from types available in CFG_TYPES.
        :param template:    Path to template file
        :param schema:      Path to schema file
        """

        cfg_type = CFG_TYPES.get(config_type)
        cfg_class = cfg_type.get(u'class')

        # Load template
        cfg_template_obj = cfg_class(config_file=template if template is not None else cfg_class.DEFAULT_TEMPLATE)

        # Validate & apply template
        try:
            if schema is not None:
                schema_obj = self.__get_schema_obj(schema)
                validate(cfg_template_obj.cfg, schema_obj.cfg)

            # This will only apply the config if the template has a valid schema
            cfg_obj.cfg = cfg_template_obj.cfg
            cfg_obj.save()

        except SchemaError as err:
            logging.error(u'Invalid schema for config template: {err}'.format(err=err))

        except ValidationError as err:
            logging.error(u'Template configuration is invalid: {err}'.format(err=err))

    def __init_from_previous_version(self,
                                     config_file,
                                     cfg_obj,
                                     config_type,
                                     schema=None):

        """ Initialise the configuration object from a previous version of configuration.

        :param config_file: Current config file path, used to lookup old config.
        :param cfg_obj:     Config object to initialise
        :param config_type: Config type from types available in CFG_TYPES.
        :param schema:      Path to schema file
        """

        cfg_type = CFG_TYPES.get(config_type)
        cfg_class = cfg_type.get(u'class')

        # Check for previous config version
        previous_version = self.last_version

        if previous_version is not None:
            # Load the previous config
            cfg_fn = config_file.split(os.sep).pop()
            old_cfg_path = os.path.join(self.__app_dirs_all_versions.user_config_dir,
                                        previous_version, CONST.cfg_dir, cfg_fn)

            old_cfg = cfg_class(config_file=old_cfg_path)

            # Validate & apply previous config
            try:
                if schema is not None:
                    # Load current schema
                    schema_obj = self.__get_schema_obj(schema)

                    # Get & load old schema
                    schema_fn = schema.split(os.sep).pop()
                    old_schema = os.path.join(self.__app_dirs_all_versions.user_config_dir,
                                              previous_version, CONST.cfg_schema, schema_fn)

                    if os.path.exists(old_schema):
                        old_schema_obj = self.__get_schema_obj(old_schema)
                        validate(old_cfg.cfg, old_schema_obj.cfg)  # Validate old config against it's own schema

                    # Validate old config against the new schema
                    # TODO: how should we handle a schema change that invalidates the old config?
                    validate(old_cfg.cfg, schema_obj.cfg)

                # This will only upgrade the config if the previous config has a valid schema
                for cfg_key, cfg_item in old_cfg.cfg.iteritems():
                    cfg_obj.cfg[cfg_key] = cfg_item

                cfg_obj.save()

            except SchemaError as err:
                logging.error(u'Invalid schema for old config, not applying: {err}'.format(err=err))

            except ValidationError as err:
                logging.error(u'Old configuration is invalid, not applying: {err}'.format(err=err))

    @staticmethod
    def __get_previous_versions(path):

        """ Check for and return the previous versions available

        :param path: The path in which to check for previous versions.

        :return:     List of version numbers (floats).
        """

        return filter_list(os.listdir(path),
                           filters=[],
                           exclude=True)

    def __get_last_version(self):

        """ Work out the latest version of the app installed (not including the loaded version)

        Note: logs a warning if current version is older than the latest available

        :return: version number (float)
        """

        # Get the previous versions filtering out the current version
        previous_versions = filter_list(self.previous_versions,
                                        filters=[self.app_version],
                                        exclude=True)

        previous_versions.sort()

        ver = previous_versions.pop() if len(previous_versions) > 0 else None

        if ver > self.app_version and ver is not None:
            logging.warning(u'You are running a version of config older than has been previously installed!')

        return ver

    def __load_cfg(self,
                   config):

        """ Load config file

        :param config: The name of the config to load.
        """

        if self.check_registration(config=config):
            cfg = self.__registered_cfg.get(config)

            cfg_type = CFG_TYPES.get(cfg.get(CONST.cfg_type))
            cfg_class = cfg_type.get(u'class')

            try:
                cfg_obj = cfg_class(config_file=os.path.join(self.config_path, cfg.get(CONST.cfg_fn)))

            except IOError:
                cfg_obj = self.__init_cfg(config_file=os.path.join(self.config_path, cfg.get(CONST.cfg_fn)),
                                          config_type=cfg.get(CONST.cfg_type),
                                          template=cfg.get(CONST.cfg_template),
                                          schema=cfg.get(CONST.cfg_schema))

            self.__validate_schema(config=config,
                                   obj=cfg_obj)

        else:
            raise KeyError(u'Cannot load config: {cfg}; Config not registered.'.format(cfg=config))

        self.__registered_cfg_objs[config] = cfg_obj

    def register(self,
                 config,
                 config_type,
                 template=None,
                 schema=None):

        """ Register a config file.

        :param config:          The name of the config item being registered.  This will also be the filename.
        :param config_type:     The type of file this config item will be.
        :param template:        Template file to initialise config from.
        :param schema:          Schema file, conforming to the JSON schema format, to validate config with.
        """

        if not self.check_registration(config):
            cfg_type = CFG_TYPES.get(config_type)

            if cfg_type is None:
                raise LookupError(u'Config Type not found: {c}'.format(c=config_type))

            cfg_filename = u'{c}.{ext}'.format(c=config,
                                               ext=cfg_type.get(u'ext'))

            self.__init_cfg(config_file=os.path.join(self.config_path, cfg_filename),
                            config_type=config_type,
                            template=template,
                            schema=schema)

            self.__registered_cfg[config] = {
                CONST.cfg_fn: cfg_filename,
                CONST.cfg_type: config_type
            }

            if template is not None:
                # Place a copy of the template in self.template_path
                ensure_path_exists(self.template_path)
                template_copy = os.path.join(self.template_path,
                                             u'{cfg}.template.{ext}'.format(cfg=config,
                                                                            ext=cfg_type.get(u'ext')))
                shutil.copyfile(template, template_copy)

                # Register the template
                self.__registered_cfg[config][CONST.cfg_template] = template_copy

            if schema is not None:
                # Place a copy of the schema in self.schema_path
                ensure_path_exists(self.schema_path)
                schema_copy = os.path.join(self.schema_path, u'{cfg}.schema.{ext}'.format(cfg=config,
                                                                                          ext=CONST.json))
                shutil.copyfile(schema, schema_copy)

                # Register the schema
                self.__registered_cfg[config][CONST.cfg_schema] = schema_copy

            # if invalid this raises either SchemaError or ValidationError.
            validate(self.__master_cfg.cfg, self.__master_cfg_schema_obj.cfg)

            self.__master_cfg.save()

            logging.info(u'Configuration registered: {cfg}'.format(cfg=config))

        else:
            logging.debug(u'Configuration already registered: {cfg}'.format(cfg=config))

    def unregister(self,
                   config):

        """ Unregister a config file.  This will also delete the config file.

        :param config:  The name of the config item being unregistered.
        """

        if self.check_registration(config):

            # Get the config file path
            pth = os.path.join(self.config_path, self.__registered_cfg[config].get(CONST.cfg_fn))

            # Remove the config file
            os.remove(pth)

            # Remove registration
            del self.__registered_cfg[config]
            self.__master_cfg.save()

            # Remove object if loaded
            if self.__check_loaded(config):
                del self.__registered_cfg_objs[config]

            logging.info(u'Configuration unregistered: {cfg}'.format(cfg=config))

        else:
            logging.debug(u'Configuration does not exist: {cfg}'.format(cfg=config))

    def check_registration(self, config):

        """ Check whether config is already registered.

        :param config:  The name of the config item being checked.
        :return: boolean.  True if already registered.
        """

        return True if config in self.__registered_cfg.keys() else False

    def __check_loaded(self, config):

        """ Check whether config is already loaded.

        :param config:  The name of the config item being checked.
        :return: boolean.  True if already loaded.
        """

        if config not in self.__registered_cfg.keys():
            return False

        return True if config in self.__registered_cfg_objs.keys() else False

    def __get_config_obj(self,
                         config):

        """ Get and return config object (loading it where necessary)

        :param config:  The config object requested
        :return:        An object exporting pre-defined config obj methods with the specified config loaded
        """

        if not self.__check_loaded(config):
            self.__load_cfg(config)

        return self.__registered_cfg_objs.get(config)

    @staticmethod
    def __get_schema_obj(schema_path):

        """ Loads and returns the schema object from the provided path.

        :param schema_path: Full path to schema file
        :return: Json schema object
        """

        # Load schema
        schema_type = CFG_TYPES.get(CONST.json)
        schema_class = schema_type.get(u'class')
        schema_obj = schema_class(config_file=schema_path)

        return schema_obj

    def __validate_schema(self,
                          config,
                          obj):

        """ Validate the provided config object against its schema if a schema is available.

        :param config: The config that the config object relates to (so we can retrieve the schema
        :param obj:    The Config object to be validated
        """

        cfg = self.__registered_cfg.get(config)

        schema = cfg.get(CONST.cfg_schema)
        if schema is not None:
            # Load schema
            schema_obj = self.__get_schema_obj(schema)

            # Ensure loaded config & schema are still valid (i.e any external modification hasn't corrupted them)
            validate(obj.cfg, schema_obj.cfg)

    def __validate_config_key(self, key):

        """ Get and return config item

        :param key: The config key to be validated
        :return:    obj - The config object for the validated config key,
                    config - The entry from the registered config dict,
                    item - The config item reference from the config object for the validated config key.
        """

        try:
            config, item = key.split(u'.')
        except ValueError:
            # We requested the entire config file?!
            config = key
            item = None

        obj = self.__get_config_obj(config)  # This will raise a KeyError if the config is not registered.

        return obj, config, item

    def __getitem__(self, key):

        """ Get and return config item

        :param key: The config key used to retrieve the config item
        :return:    The requested config item
        """

        obj, config, item = self.__validate_config_key(key)

        if item is None:
            # Entire config was requested!
            # TODO: When entire config requested return a dict of the config.  Does this need to be an OrderedDict?
            raise NotImplementedError(u'Getting the entire config is not yet supported!')

        else:
            try:
                return obj[item]

            except KeyError:
                raise LookupError(u'Item ({i}) not found in {cfg}'.format(i=item, cfg=config))

    def __setitem__(self, key, value):

        """ Set and return config item

        :param key:     The config key used to retrieve the config item
        :param value:   The new value for the config item
        """

        obj, config, item = self.__validate_config_key(key)

        if item is None:
            # Entire config overwrite was requested!
            # TODO: When entire config overwrite requested expect a dict.  Does this need to be an OrderedDict?
            raise NotImplementedError(u'Overwriting the entire config is not yet supported!')

        else:
            # Save the old value
            old_value = obj.get(item)

            # Update & validate the item (where schema is present)
            obj[item] = value

            try:
                self.__validate_schema(config=config,
                                       obj=obj)

            except ValidationError:
                # Reset the value to keep the config valid
                if old_value is None:
                    del obj[item]

                else:
                    obj[item] = old_value

                # pass the exception on
                raise

    def __delitem__(self, key):

        """ Delete the specified config item

        :param key: The config key used to retrieve the config item being deleted
        """

        obj, config, item = self.__validate_config_key(key)

        if item is None:
            # Delete entire config?!  This is what the unregister function is for!
            # We raise an error rather than call unregister for the user to avoid accidental config removal!
            raise ValueError(u'Removal of the entire config via the del method is not supported; '
                             u'Please use the Configuration.unregister method instead!')

        else:
            # Save the old value
            old_value = obj.get(item)

            # Delete & validate the item (where schema is present)
            del obj[item]

            try:
                self.__validate_schema(config=config,
                                       obj=obj)

            except ValidationError:
                # Reset the value to keep the config valid
                obj[item] = old_value

                # pass the exception on
                raise

    def find(self,
             config,
             filters):

        """ Get and return filtered config items

        :param config:  Registered config name
        :param filters: List of filter tuples.
                        Tuple format: (Search Key, Search Value, Condition)
                        First should not have a condition
                        i.e [("A", 123), ("A", 789, u'AND')]
        :return:        dict containing filtered items
        """

        obj, _, _ = self.__validate_config_key(config)

        return obj.find(filters)

    # Properties
    @property
    def config_path(self):
        return os.path.join(self.__app_dirs.user_config_dir, CONST.cfg_dir)

    @property
    def schema_path(self):
        return os.path.join(self.__app_dirs.user_config_dir, CONST.cfg_schema)

    @property
    def template_path(self):
        return os.path.join(self.__app_dirs.user_config_dir, CONST.cfg_template)

    @property
    def data_path(self):
        return self.__app_dirs.user_data_dir

    @property
    def cache_path(self):
        return self.__app_dirs.user_cache_dir

    @property
    def log_path(self):
        return self.__app_dirs.user_log_dir

    @property
    def temp_path(self):
        return self.__temp_path

    @property
    def app_name(self):
        return self.__app_kwargs.get(u'appname')

    @property
    def app_version(self):
        return self.__app_kwargs.get(u'version')

    @property
    def app_author(self):
        return self.__app_kwargs.get(u'appauthor')

    @property
    def previous_versions(self):
        return self.__get_previous_versions(self.__app_dirs_all_versions.user_config_dir)

    @property
    def last_version(self):
        return self.__get_last_version()
