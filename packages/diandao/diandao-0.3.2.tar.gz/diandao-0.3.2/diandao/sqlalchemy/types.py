# -*- coding: utf-8 -*-
from sqlalchemy.types import UserDefinedType, Text
from flask import json


class JSONSerializer(Text):
    """JSON序列化数据格式.

    """
    __visit_name__ = 'text'

    def bind_processor(self, dialect):
        def process(value):
            return json.dumps(value)

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return json.loads(value)

        return process
