#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
from parse import load_json
from generator import entity,relation,field
from module import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from module import meta
from dml import manipulate

def import_class(module_name, class_name):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    # obj = class_meta(*args, **kwargs)
    return class_meta


def get_obj(class_meta, *args, **kwargs):
    obj = class_meta(*args, **kwargs)
    return obj


def create(session):
    with open("skill.json",'r') as fp:
        skill=load_json(fp)
        entity.Entity(session).create("skill", skill)

    with open("operator.json",'r') as fp:
        operator = load_json(fp)
        entity.Entity(session).create("operator", operator)

    with open("operator_skill.json", 'r') as fp:
        data = load_json(fp)
        relation.Relation(session).create("operator_skill", data)



def main():
    #engine = create_engine("mysql+pymysql://root:passw0rd@localhost/test",encoding='utf-8')
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')

    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    create(session)

    class_operator = import_class("module.operator", "Operator")
    class_skill = import_class("module.skill", "Skill")
    Base.metadata.create_all(engine)

    o1 = class_operator(name="zhangsan")
    o2 = class_operator(name="lisi")
    o3 = class_operator(name="wanger")

    s1 = class_skill(name="java")
    s2 = class_skill(name="python")
    s3 = class_skill(name="golang")

    o1.skill = [s1,s2,s3]
    o2.skill = [s1,s2]
    o3.skill = [s3]

    session.add_all([o1,o2,o3,s1,s3,s3])
    session.commit()

    operator_obj = session.query(class_operator).filter(class_operator.name == "zhangsan").first()
    for s in operator_obj.skill:
        print(s.name)


def relation_create():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    with open("operator_skill.json", 'r') as fp:
        data = load_json(fp)
        re = relation.Relation(session)
        re.create(data)
        print(data["name"])
        print(re.read(data["name"]))


def relation_update():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    with open("operator_skill_test.json", 'r') as fp:
        data = load_json(fp)
        re = relation.Relation(session)
        re.update(data)
        print(data["name"])
        print(re.read(data["name"]))


def relation_delete():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    re = relation.Relation(session)
    re.delete("operator_skill")

def relation_list():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    re = relation.Relation(session)
    print(re.list())

def entity_create():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    with open("operator.json", 'r') as fp:
        data = load_json(fp)
        en = entity.Entity(session)
        en.create(data)
        print(data["name"])
        #print en.read(data["name"])
        print(en.list())


def entity_delete():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    with open("operator.json", 'r') as fp:
        data = load_json(fp)
        en = entity.Entity(session)
        en.delete(data["name"])
        print(data["name"])
        print(en.read(data["name"]))


def entity_update():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    with open("operator_test.json", 'r') as fp:
        data = load_json(fp)
        en = entity.Entity(session)
        en.update(data)
        print(data["name"])
        print(en.read(data["name"]))


def field_delete():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    f1 = field.Field(session)
    #f1.delete("operator",28)


def field_create():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    f1 = field.Field(session)
    data = {"default_value": "test", "name": "name",  "primary": False, "type": "String", "is_not_null": True}
    f1.create("operator", data)
    #f1.delete("operator",28)

def field_update():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    f1 = field.Field(session)
    data = {"default_value": "test11", "name": "name",  "primary": False, "type": "String", "is_not_null": True}
    f1.update("operator", 30, data)
    print(f1.read(30))

def field_list():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    f1 = field.Field(session)
    print(f1.list())

def data_create():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    m = manipulate.Manipulate(session,"operator")
    record = {"name": "test", "skill": [{"name": "python"}, {"name": "golang"}]}
    m.create(record)

def data_delete():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    m = manipulate.Manipulate(session,"operator")
    record = {"name":"test","skill":[{"name":"python"},{"name":"golang"}]}
    m.delete(7)

def data_read():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    m = manipulate.Manipulate(session,"operator")
    print(m.read(7))

def data_update():
    engine = create_engine("postgresql://module:passw0rd@localhost/metadata", encoding='utf-8')
    Base.metadata.create_all(engine)
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    m = manipulate.Manipulate(session,"operator")
    record = {"name":"test","skill":[{"name":"python"}]}
    m.update(8, record)
    print(m.list())

main()
