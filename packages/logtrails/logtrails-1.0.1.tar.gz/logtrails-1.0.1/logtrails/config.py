"""
Configuration files for logtrails parsers
"""

import os
import re
import sre_constants

from collections import OrderedDict
from configobj import ConfigObj, ConfigObjError

from logtrails.logreader import LogTrailReaderProcess
from logtrails.queue import RedisConnection

DEFAULT_CONFIGURATION_FILE = '~/.logtrails.cfg'

DEFAULT_PARSER_CONFIG = {
    'channel': 'logtrails',
    'list_field_separator': ',',
    'list_fields': [],
    'integer_fields': [],
    'float_fields': [],
}

class ConfigurationError(Exception):
    pass


class QueueConfiguration(object):
    """Queue configuration

    """
    def __init__(self, hostname, port, channels=[]):
        self.hostname = hostname
        self.port = int(port)
        if isinstance(channels, str):
            channels = [channels]
        self.channels = channels

    def __repr__(self):
        return '{0}:{1}'.format(self.hostname, self.port)


class LogPatternConfiguration(object):
    """Log pattern

    Parse and regexp matcher to object for log readers
    """
    def __init__(self, group, name, pattern):
        self.group = group
        self.name = name
        self.regexp = re.compile(pattern)

    def __getattr__(self, attr):
        return getattr(self.regexp, attr)

    @property
    def integer_fields(self):
        """Integer fields in configuration

        """
        fields = self.group.parser.settings['integer_fields']
        if isinstance(fields, str):
            fields = [v.strip() for v in fields.split(',')]
        return fields

    @property
    def float_fields(self):
        """Float fields in configuration

        """
        fields = self.group.parser.settings['float_fields']
        if isinstance(fields, str):
            fields = [v.strip() for v in fields.split(',')]
        return fields

    @property
    def list_fields(self):
        """List fields in configuration

        """
        fields = self.group.parser.settings['list_fields']
        if isinstance(fields, str):
            fields = [v.strip() for v in fields.split(',')]
        return fields

    @property
    def list_field_separator(self):
        """List field separator

        """
        return self.group.parser.settings['list_field_separator']

    @property
    def channel(self):
        """Redis pubsub channel

        """
        return self.group.parser.settings['channel']


class LogPatternGroupConfiguration(object):
    """Pattern group configuration

    Group of patterns for a log parser
    """
    def __init__(self, parser, name, patterns):
        self.parser = parser
        self.name = name

        self.pattern_map = OrderedDict()
        for key, pattern in patterns.items():
            if key not in self.pattern_map:
                self.pattern_map[key] = []
            try:
                self.pattern_map[key].append(LogPatternConfiguration(self, key, pattern))
            except sre_constants.error as e:
                print 'WARNING: {0} {1} invalid regexp pattern {2}: {3}'.format(self.parser, name, pattern, e)

    def __repr__(self):
        return '{0}'.format(self.name)

    @property
    def patterns(self):
        """Return all patterns

        """
        patterns = []
        for key in self.pattern_map:
            patterns.extend(self.pattern_map[key])
        return patterns


class LogParserConfiguration(object):
    """Patterns configuration

    """
    def __init__(self, path, patterns_config):
        self.path = path
        self.settings = {}
        self.patterngroups = OrderedDict()

        try:
            config = ConfigObj(patterns_config, list_values=False)
        except ConfigObjError as e:
            raise ConfigurationError('Error reading {0}: {1}'.format(patterns_config, e))

        if 'settings' in config:
            for key in DEFAULT_PARSER_CONFIG:
                self.settings[key] = config['settings'].get(key, DEFAULT_PARSER_CONFIG[key])
        else:
            self.settings = DEFAULT_PARSER_CONFIG.copy()

        for key, patterns in config.items():
            if key in ( 'settings', ):
                continue
            self.patterngroups[key] = LogPatternGroupConfiguration(self, key, patterns)

    def __repr__(self):
        return '{0}'.format(self.path)

    @property
    def patterns(self):
        """Return configured patterns

        """
        patterns = []
        for name in self.patterngroups:
            patterns.extend(self.patterngroups[name].patterns)
        return patterns


class Configuration(object):
    """Logtrails configuration

    """

    def __init__(self, path=DEFAULT_CONFIGURATION_FILE):
        self.path = os.path.expandvars(os.path.expanduser(path))
        self.queue_configuration = None
        self.system_channel = 'logtrails'
        self.handlers = []

    @property
    def patterns(self):
        """All configured pattern groups

        Return all known pattern groups, regardless of associated logfile
        """
        patterns = []
        for handler in self.handlers:
            patterns.extend(handler.patterns)
        return patterns

    def load(self):
        """Load configuration

        """
        if not os.path.isfile(self.path):
            raise ConfigurationError('No such file: {0}'.format(self.path))

        if not os.access(self.path, os.R_OK):
            raise ConfigurationError('Permission denied: {0}'.format(self.path))

        try:
            config = ConfigObj(self.path)
        except Exception as e:
            raise ConfigurationError('Error parsing {0}: {1}'.format(path, e))

        try:
            self.queue_configuration = QueueConfiguration(**config['queue'])
        except KeyError:
            raise ConfigurationError('Missing queue configuration: {0}'.format(path))

        if 'parsers' in config:
            for key in config['parsers']:
                if not isinstance(config['parsers'][key], list):
                    config['parsers'][key] = [config['parsers'][key]]
                for patterns_config in config['parsers'][key]:
                    self.handlers.append(LogParserConfiguration(key, patterns_config))
        else:
            raise ConfigurationError('Missing log parser configuration: {0}'.format(path))

    def get_redis_connection(self):
        """Return configured redis connection

        """
        return RedisConnection(
            hostname=self.queue_configuration.hostname,
            port=self.queue_configuration.port,
            channels=self.queue_configuration.channels,
        )

    def configure_readers(self, callback):
        """Configure log readers processes

        Return log reader processes for configured parsers
        """
        processes = []
        for handler in self.handlers:
            processes.append(LogTrailReaderProcess(handler.path, handler.patterns, callback))
        return processes
