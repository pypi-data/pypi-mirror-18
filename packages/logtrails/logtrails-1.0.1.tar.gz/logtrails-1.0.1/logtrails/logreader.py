"""
Log file readers

Implements classes to read logs
"""

import json
import re

from datetime import datetime
from multiprocessing import Process
from systematic.log import LogEntry, LogFile, LogfileTailReader, LogFileError

LOGFILE_DATE_PREFIX_PARSERS = (
    ( re.compile('^(?P<datetime>[^\s]+\s+\d+\s+\d+:\d+:\d+) (?P<line>.*)'), '%b %d %H:%M:%S', ),
    ( re.compile('^(?P<datetime>\d+-\d+-\d+ \d+:\d+:\d+.\d+) (?P<line>.*)'), '%Y-%m-%d %H:%M:%S.%f', ),
    ( re.compile('^(?P<datetime>\d+/[^/]+/\d+:\d+:\d+:\d+) (?P<tz>\+\d+) (?P<line>.*)'), '%d/%b/%Y:%H:%M:%S', ),
)

class JSONDataEncoder(json.JSONEncoder):
    """JSON encoder

    JSON encoder with datetime to isoformat() conversion
    """
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class LogEntryParser(dict):
    """Log entry

    Log entry processor for LogTrailReader and LogTrailLog
    """
    def __init__(self, reader, line, year):

        line = line.rstrip()
        self.reader = reader
        self.line = line
        self.message_fields = {}

        self['time'], line = self.__parse_date__(line)
        self['filename'] = self.reader.path
        self.message = line

        for pattern in self.reader.patterns:
            m = pattern.match(line)
            if m:
                self.channel = pattern.channel
                self['group'] = pattern.group.name
                self['label'] = pattern.name
                for key, value in m.groupdict().items():
                    value = self.__format_value__(pattern, key, value)
                    self[key] = value
                return

        raise LogFileError('Entry does not match patterns: {0}'.format(line))

    def __parse_date__(self, line):
        """Parse datetime prefix

        Parse known date/time prefix formats from line
        """
        for pattern, datefmt in LOGFILE_DATE_PREFIX_PARSERS:
            m = pattern.match(line)
            if m:
                value = datetime.strptime(m.groupdict()['datetime'], datefmt)
                return value, m.groupdict()['line']

        raise LogFileError('Error parsing entry time from line: {0}'.format(self.line))

    def __format_value__(self, pattern, key, value):
        """Format value

        """
        if key in pattern.list_fields:
            value = [v.strip() for v in value.split(pattern.list_field_separator)]
            if key in pattern.integer_fields:
                try:
                    value = [int(v) for v in value]
                except ValueError:
                    value = None
            if key in pattern.float_fields:
                try:
                    value = [float(v) for v in value]
                except ValueError:
                    value = None
        else:
            if key in pattern.integer_fields:
                try:
                    value = int(value)
                except ValueError:
                    value = None
            if key in pattern.float_fields:
                try:
                    value = float(value)
                except ValueError:
                    value = None
        return value

    def append(self, message):
        self.message = '{0}\n{1}'.format(self.message, message.rstrip())

    def to_json(self):
        return json.dumps(self, indent=2, cls=JSONDataEncoder)


class LogTrailLogFile(LogFile):
    """Logfile for trails

    Parser for offline logs
    """
    lineloader = LogEntryParser

    def __init__(self, path, patterns):
        super(LogTrailLogFile, self).__init__(path)
        self.patterns = patterns

    def readline(self):
        """Read line from log

        Parse entry from logfile
        """

        if self.fd is None:
            raise LogFileError('File is not loaded')

        try:
            line = self.fd.readline()
            if line == '':
                self.__loaded = True
                return None

            # Multiline log entry
            if line[:1] in [' ', '\t'] and len(self):
                self[-1].append(line)
                return self.readline()

            else:
                entry = self.lineloader(self, line, year=self.mtime.year)
                self.append(entry)
                return entry

        except OSError as e:
            raise LogFileError('Error reading file {0}: {1}'.format(self.path, e))


class LogTrailReader(LogfileTailReader):
    """Logfile parser

    Tail reader for one logfile with parser patterns as specified in config
    """
    lineparser = LogEntryParser

    def __init__(self, path, patterns):
        super(LogTrailReader, self).__init__(path)
        self.patterns = patterns

    def __format_line__(self, line):
        """Format line

        Formats line as log entry. Returns None if entry is not supported
        """
        return self.lineparser(self, line, self.year)


class LogTrailReaderProcess(Process):
    """Python multiprocessing process for LogTrailReader

    Runs with LogTrailReader, processing new log entries and runs callback
    with result entry as JSON
    """
    def __init__(self, path, patterns, callback, **kwargs):
        super(LogTrailReaderProcess, self).__init__(**kwargs)
        self.reader = LogTrailReader(path, patterns)
        self.callback = callback

    def run(self, *args, **kwargs):
        """Run log reader

        Seek to end of input file and start processing new entries
        """
        self.reader.seek_to_end()
        while True:
            self.callback(self.reader.next())
