import hashlib
import os
import re
import subprocess
import sys
import textwrap
import time
from functools import partial

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL, make_url

__version__ = '0.10.0'


class SQLConnector(object):
    def __init__(self, engine):
        self.engine = engine
        self.backend, self.driver, self.connection_args = self._get_backend_driver_connection_args(self.engine)

    @staticmethod
    def _get_backend_driver_connection_args(engine):
        url = make_url(engine.url)
        connection_args = url.translate_connect_args()
        connection_args['query'] = url.query
        return url.get_backend_name(), url.get_driver_name(), connection_args

    def get_connection_url(self, database=None):
        args = self.connection_args.copy()
        if database:
            args['database'] = database
        return URL(self.backend, **args)

    def execute(self, cmd, database=None, output=True):
        raise NotImplementedError()


class MySQLConnector(SQLConnector):
    def __init__(self, engine):
        super(MySQLConnector, self).__init__(engine)
        if self.backend != 'mysql':
            raise Exception("Invalid database connection engine: {}".format(self.backend))

        self.__jdbc_connection_url_partial = partial(
            self._jdbc_connection_url,
            self.connection_args['host'],
            self.connection_args['port'],
            self.connection_args['username'],
            self.connection_args['password'])

    @staticmethod
    def _jdbc_connection_url(host, port, username, password, database):
        return 'jdbc:mysql://{host}:{port}/{database}?user={username}&password={password}'.format(**locals())

    def get_jdbc_connection_url(self, database=None):
        return self.__jdbc_connection_url_partial(database or self.connection_args['database'])

    @staticmethod
    def _db_execute_cmd(host, port, username, password, database, charset, cmd):
        return (
            'mysql '
            '--default-character-set={charset} '
            '-u "{username}" '
            '--password="{password}" '
            '-h "{host}" '
            '-P "{port}" '
            '-e "{cmd}" '
            '{database}').format(**locals())

    def _get_db_execute_cmd(self, cmd, database=None):
        args = dict(
            host=self.connection_args['host'],
            port=self.connection_args['port'],
            username=self.connection_args['username'],
            password=self.connection_args['password'],
            database=database or self.connection_args['database'],
            charset=self.connection_args['query']['charset'],
            cmd=cmd)
        return self._db_execute_cmd(**args)

    def execute(self, cmd, database=None, output=True):
        exec_cmd = self._get_db_execute_cmd(cmd, database)
        if output:
            p = subprocess.Popen(
                exec_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            output, _stderr = p.communicate()
            if p.returncode != 0 or output.find('ERROR') != -1:
                raise Exception("Unable to execute SQL command: {}\nRaw output:\n{}".format(cmd, output))
            return output
        else:
            subprocess.check_call(exec_cmd, shell=True)


class DBManager(object):
    def __init__(self, sql_connector):
        self.sql_connector = sql_connector

    def __print_info(self):
        print '=' * 80
        print "DB Manager (v{})".format(__version__)
        print '=' * 80
        print "DB Connection URL:  {!r}".format(self.sql_connector.engine.url)
        print '-' * 80

    def __get_db_engine(self, database):
        if database:
            return create_engine(self.sql_connector.get_connection_url(database=database))
        return self.sql_connector.engine

    def _create_db(self, metadata, database=None):
        print "Creating tables ({} total)...".format(len(metadata.tables))
        metadata.create_all(self.__get_db_engine(database))

    def _drop_db(self, metadata, database=None):
        print "Dropping tables ({} total)...".format(len(metadata.tables))
        metadata.drop_all(self.__get_db_engine(database))

    def create_db(self, metadata):
        self.__print_info()
        print 'Creating database tables...'
        self._create_db(metadata)
        print 'Done.\n'

    def drop_db(self, metadata):
        self.__print_info()
        print 'Dropping database tables...'
        self._drop_db(metadata)
        print 'Done.\n'

    def print_info(self):
        self.__print_info()


class MySQLVersionManager(DBManager):
    DEFAULT_BASELINE_VERSION = 'baseline'
    DEFAULT_DB_VERSIONS_DIR = 'db/versions'
    DEFAULT_DB_VERSION_TABLE_NAME = 'property'
    VERSION_A_DB = 'db_0'
    VERSION_B_DB = 'db_1'

    def __init__(self, engine, mysql_diff_cmd, versions_dir=None, version_table_name=None):
        super(MySQLVersionManager, self).__init__(MySQLConnector(engine))
        self._mysql_diff_cmd = mysql_diff_cmd
        self.baseline_version = self.DEFAULT_BASELINE_VERSION
        self.versions_dir = versions_dir or self.DEFAULT_DB_VERSIONS_DIR
        self.version_table_name = version_table_name or self.DEFAULT_DB_VERSION_TABLE_NAME

    def __print_info(self):
        print '=' * 80
        print "MySQL DB Version Manager (v{})".format(__version__)
        print '=' * 80
        print "DB Connection URL:  {!r}".format(self.sql_connector.engine.url)
        print "Output directory:   {}".format(self.versions_dir)
        print "Version table:      {}".format(self.version_table_name)
        print "Next version:       {}".format(self._get_next_version())
        print '-' * 80

    def __select_version_statement(self):
        return "SELECT value FROM {} WHERE name='schema_version';".format(self.version_table_name)

    def __drop_version_table_statement(self):
        return "DROP TABLE {};".format(self.version_table_name)

    def __drop_create_version_database(self, database):
        return "DROP DATABASE IF EXISTS {database}; CREATE DATABASE {database};".format(database=database)

    def __create_version_table_statement(self):
        return textwrap.dedent('''\
            CREATE TABLE IF NOT EXISTS `{}` (
              `name` varchar(16) NOT NULL,
              `value` varchar(255) NOT NULL,
              PRIMARY KEY (`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(self.version_table_name))

    def __upsert_version_statement(self, version):
        return textwrap.dedent('''\
            INSERT INTO {table} (name, value) VALUES ('schema_version', '{value}')
              ON DUPLICATE KEY UPDATE value='{value}';'''.format(
            table=self.version_table_name, value=version))

    @staticmethod
    def __parse_version(select_version_output):
        _version_re = re.compile('^([a-zA-Z0-9]+)$')

        for line in select_version_output.split('\n'):
            line = line.strip()
            version_match = _version_re.match(line)
            if version_match is not None:
                version = version_match.group(0)
                if version != 'value':
                    break
        else:
            version = None
        return version

    def _get_next_version(self, database=None):
        try:
            output = self.sql_connector.execute(self.__select_version_statement(), database=database, output=True)
            version = self.__parse_version(output)
        except Exception:
            version = None

        return version or self.DEFAULT_BASELINE_VERSION

    def _get_new_version(self):
        m = hashlib.md5()
        m.update(str(time.time()))
        return m.hexdigest()

    def _get_versions(self):
        versions = {}
        version_file_re = re.compile('^(?P<hash>[a-zA-Z0-9]+)(?:-(?P<name>.*?))?.sql$')
        for dirpath, dirnames, filenames in os.walk(self.versions_dir):
            for filename in filenames:
                match = version_file_re.match(filename)
                if match:
                    matches = match.groupdict()
                    if matches['hash'] in versions:
                        raise Exception('Duplication hash found: {} and {}'.format(versions[matches['hash']][0], matches['name']))
                    versions[matches['hash']] = (matches['name'], os.path.join(dirpath, filename))
        return versions

    def __write_db_init_script(self, filename, version):
        with open(filename, 'wb') as f:
            f.write(self.__create_version_table_statement() + '\n\n')
            f.write(self.__upsert_version_statement(version) + '\n')

    def _prepare_version_dir(self):
        if not os.path.exists(self.versions_dir):
            os.makedirs(self.versions_dir)

    def _generate_init_script(self, version):
        self._prepare_version_dir()
        filename = os.path.join(self.versions_dir, "{}.sql".format(self.baseline_version))
        if not os.path.exists(filename):
            self.__write_db_init_script(filename, version)
        else:
            print "Warning: Baseline script already exists: {}".format(filename)
        return filename

    def _apply_db_upgrade(self, filename, version, database=None):
        print "Applying upgrade: {}".format(filename)
        sys.stdout.flush()
        script_start = time.time()
        self.sql_connector.execute("\\. {}".format(filename), database=database, output=False)
        run_time = int(time.time() - script_start)
        print "\t%d Minutes %d Seconds" % (run_time / 60, run_time % 60)

    def _upgrade_db(self, database=None):
        versions = self._get_versions()

        start_time = time.time()
        while True:
            version = self._get_next_version(database)
            if version not in versions:
                break

            _name, filename = versions.pop(version)
            self._apply_db_upgrade(filename, version, database)

        run_time = int(time.time() - start_time)
        print "%d Minutes %d Seconds Total" % (run_time / 60, run_time % 60)

    def _generate_db_diff(self, metadata):
        print "Preparing comparison databases: '{}' and '{}'...".format(self.VERSION_A_DB, self.VERSION_B_DB)
        self.sql_connector.execute(self.__drop_create_version_database(self.VERSION_A_DB), output=False)
        self.sql_connector.execute(self.__drop_create_version_database(self.VERSION_B_DB), output=False)

        print "Generating updated schema in '{}'...".format(self.VERSION_B_DB)
        self._create_db(metadata, self.VERSION_B_DB)

        print "Generating existing schema in '{}'...".format(self.VERSION_A_DB)
        self._upgrade_db(self.VERSION_A_DB)

        jdbc_db_a_url = self.sql_connector.get_jdbc_connection_url(self.VERSION_A_DB)
        jdbc_db_b_url = self.sql_connector.get_jdbc_connection_url(self.VERSION_B_DB)
        return self._mysql_diff_cmd(jdbc_db_a_url, jdbc_db_b_url)

    def __extract_db_upgrade_statements(self, db_diff_output):
        _drop_version_table_re = re.compile(self.__drop_version_table_statement())
        output_lines = db_diff_output.split('\n')
        output_lines = [l for l in output_lines if not _drop_version_table_re.search(l)]
        return '\n'.join(output_lines)

    def __write_db_upgrade_script(self, filename, version, contents, comment=None):
        with open(filename, 'wb') as f:
            if comment:
                f.write("-- {}\n\n".format(comment))
            f.write(contents + '\n\n')
            f.write(self.__upsert_version_statement(version) + '\n')

    def _generate_upgrade_script(self, version, upgrade_statements, comment=None):
        self._prepare_version_dir()
        filename = os.path.join(self.versions_dir, '{}.sql'.format(version))
        next_version = self._get_new_version()
        self.__write_db_upgrade_script(filename, next_version, upgrade_statements, comment)
        return filename

    def init_db(self, baseline_version=None):
        if baseline_version:
            self.baseline_version = baseline_version

        self.__print_info()
        print 'Initializing database...'
        start_time = time.time()
        next_version = self._get_new_version()
        filename = self._generate_init_script(next_version)
        self._apply_db_upgrade(filename, next_version)
        run_time = int(time.time() - start_time)
        print "%d Minutes %d Seconds Total" % (run_time / 60, run_time % 60)
        print 'Done.\n'

    def diff_db(self, metadata, comment=None, preview=False):
        self.__print_info()
        print 'Comparing database schemas...'
        db_diff_output = self._generate_db_diff(metadata)
        upgrade_statements = self.__extract_db_upgrade_statements(db_diff_output).strip()
        if upgrade_statements:
            print 'Creating new version...'
            version = self._get_next_version()
            if not preview:
                filename = self._generate_upgrade_script(version, upgrade_statements, comment)
                print "\t{}".format(filename)
            else:
                print "Previewing upgrade: '{}':".format(version)
                print '-' * 80
                print upgrade_statements
                print '-' * 80
        else:
            print 'No differences detected!'
        print 'Done.\n'

    def upgrade_db(self, database=None):
        self.__print_info()
        print 'Upgrading database...'
        self._upgrade_db(database)
        print 'Done.\n'
