#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dml import manipulate

engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
Session_class = sessionmaker(bind=engine)
session = Session_class()


def create_record(entityName, recordId, body) -> str:
    m = manipulate.Manipulate(session, entityName)
    m.create(recordId, body)


def delete_record(entityName, recordId) -> str:
    m = manipulate.Manipulate(session, entityName)
    m.delete(recordId)


def get_record(entityName, recordId, param = None, limit = None) -> str:
    m = manipulate.Manipulate(session, entityName)
    m.get(recordId, param, limit)


def list_record(entityName, param = None, limit = None) -> str:
    m = manipulate.Manipulate(session, entityName)
    m.list(param, limit)


def update_record(entityName, recordId, body) -> str:
    m = manipulate.Manipulate(session, entityName)
    m.update(recordId, body)
