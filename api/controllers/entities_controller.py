#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
from generator import entity,relation,field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from module import Base
from os import walk

engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
Session_class = sessionmaker(bind=engine)
session = Session_class()
en = entity.Entity(session)


def init():
    for dirpath, dirs, files in walk('../module'):
        for name in files:
            if name == "__init__.py":
                continue
            elif name.split(".")[0][-4:] == "table":
                __import__("module.%s" % name.split(".")[0], globals(), locals(), [name.split(".")[0]])
            else:
                __import__("module.%s" % name.split(".")[0], globals(), locals(), [name.split(".")[0].capitalize()])


def create_entity(entity_name, body) -> str:
    init()
    result = en.create(entity_name, body)
    __import__("module.%s" % entity_name, globals(), locals(), [entity_name.capitalize()])
    Base.metadata.create_all(engine)
    return result


def create_field(entity_name, field_id, body) -> str:
    return f1.create(entity_name, field_id, body)


def delete_entity(entity_name) -> str:
    return en.delete(entity_name)


def delete_field(entity_name, field_id) -> str:
    return f1.delete(entity_name, field_id)


def get_entity(entity_name) -> str:
    return en.read(entity_name)


def get_field(entity_name, field_id) -> str:
    return en.get_field(entity_name, field_id)


def list_entity() -> str:
    return en.list()


def list_field(entity_name) -> str:
    return en.list_field(entity_name)


def update_entity(entity_name, body) -> str:
    return en.update(entity_name, body)


def update_field(entity_name, field_id, body) -> str:
    return f1.update(entity_name, field_id, body)
