from sqlalchemy import (
    BigInteger, Integer, Column, String, inspect, Text, ForeignKey, create_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative

from sqlalchemy import Sequence

import os

ROOT_PATH = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])


def primary_key(seq_label=None):
    if seq_label:
        return Column(Integer, Sequence(seq_label), primary_key=True, autoincrement=True)

    return Column(Integer, primary_key=True, autoincrement=True)


@as_declarative()
class Base:
    def to_dict_underline(self):
        ret = {}

        for c in inspect(self).mapper.column_attrs:
            ret[c.key] = getattr(self, c.key, None)
        return ret

    def to_dict(self, is_format=True):
        ret = {}

        for c in inspect(self).mapper.column_attrs:
            if is_format:
                keys = c.key.split("_")
                key = ""
                for i in range(0, len(keys)):
                    if i == 0:
                        key += keys[i]
                    elif keys[i] == 'id':
                        key += keys[i].upper()
                    else:
                        key += keys[i].capitalize()
            else:
                key = c.key

            ret[key] = getattr(self, c.key, None)

        return ret


class DB:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:///{database}".format(database=os.path.join(ROOT_PATH, "geoip" + '.db')))
        self.session = sessionmaker(bind=self.engine, autocommit=True)


db = DB()

__ = (BigInteger, Integer, Column, String, Text, ForeignKey, inspect)


class DBResult:
    suc = False
    rows = None
    result = None
    error = None

    def __init__(self):
        self.session = db.session()

    def __enter__(self):
        if not self.session.is_active:
            self.session.begin()

        return self.session

    def __exit__(self, type_, value, traceback):
        try:
            if self.session.is_active:
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.error = e

        if not self.error:
            self.suc = True


class QueryDBResult(DBResult):
    suc = False
    rows = None
    result = None
    error = None

    def __enter__(self):
        return self.session

    def __exit__(self, type_, value, traceback):
        if not self.error:
            self.suc = True
