import subprocess


class MySQLDiffCommand(object):
    DEFAULT_MYSQL_DIFF_PATH = '/opt/mysql-diff/bin/mysql-diff'

    def __init__(self, mysql_diff_path=None):
        self._mysql_diff_path = mysql_diff_path or self.DEFAULT_MYSQL_DIFF_PATH

    @staticmethod
    def _exec_db_diff_command(mysql_diff_path, db_a_url, db_b_url):
        command = [mysql_diff_path, db_a_url, db_b_url]
        try:
            return subprocess.check_output(command, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            message = "mysql-diff failed:\n{}: {}\n{}".format(type(e).__name__, e, e.output)
            raise Exception(message)

    def __call__(self, jdbc_url_a, jdbc_url_b):
        return self._exec_db_diff_command(self._mysql_diff_path, jdbc_url_a, jdbc_url_b)
