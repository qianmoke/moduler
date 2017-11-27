#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
from generator import entity,relation,field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
Session_class = sessionmaker(bind=engine)
session = Session_class()
re = relation.Relation(session)


def create_relation(name, body) -> str:
    return re.create(name, body)


def delete_relation(name) -> str:
    return re.delete(name)


def get_relation(name) -> str:
    return re.read(name)


def list_relation() -> str:
    return re.list()


def update_relation(name, body) -> str:
    return re.update(name, body)
