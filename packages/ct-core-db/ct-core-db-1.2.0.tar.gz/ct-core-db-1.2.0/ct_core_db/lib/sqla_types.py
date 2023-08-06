import simplejson as json
from sqlalchemy import TypeDecorator
from sqlalchemy_types import types

__all__ = ['JsonUnicodeText']


class JsonUnicodeText(TypeDecorator):
    impl = types.UnicodeText

    def __init__(self, *args, **kwargs):
        self.validator = None

        TypeDecorator.__init__(self, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value
