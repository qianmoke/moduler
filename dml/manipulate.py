#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from module import meta
from os import remove,walk
from json import dumps
from sqlalchemy import text

class Manipulate(object):
    def __init__(self, session, name):
        self.session = session
        self.name = name
        module_name = 'module.%s' % name
        self.class_meta = getattr(__import__(module_name, globals(), locals(), [name]), name.capitalize())
        self.init()

    def get_primarykey(self, name):
        where = "name='%s'" %  (name)
        data = self.session.query(meta.Entity).filter(text(where)).one()
        for field in data.fields:
            if field.primary:
                return field

    def get_fields(self, name):
        where = "name='%s'" %  (name)
        data = self.session.query(meta.Entity).filter(text(where)).one()
        fields = []
        for field in data.fields:
            fields.append(field.name)
        return fields

    def get_relations(self, name):
        fields = []
        where = "name='%s'" %  (name)
        data = self.session.query(meta.Entity).filter(text(where)).one()
        for relation in data.relations:
            if relation.source == name:
                fields.append(relation.destination)
            else:
                fields.append(relation.source)
        return fields

    def init(self):
        for dirpath, dirs, files in walk('../module'):
            for name in files:
                if name == "__init__.py":
                    continue
                elif name.split(".")[0][-4:] == "table":
                    __import__("module.%s" % name.split(".")[0], globals(), locals(), [name.split(".")[0]])
                else:
                    __import__("module.%s" % name.split(".")[0], globals(), locals(), [name.split(".")[0].capitalize()])

    def process_relation(self, key, value):
        class_meta = getattr(__import__("module.%s" % key, globals(), locals(), key.capitalize()), key.capitalize())
        fields = []
        for field in value:
            for k,v in field.items():
                where = "%s.%s='%s'" % (class_meta.__name__.lower(), k ,v )
                query = self.session.query(class_meta).filter(text(where))
                if query.count() == 0 :
                    c = class_meta()
                    setattr(c, k, v)
                else:
                    c = query.one()
            fields.append(c)
        return fields

    def create(self, record):
        entity = self.class_meta()
        for key,value in record.items():
            if type(value) == type([]):
                fields = self.process_relation(key, value)
                setattr(entity, key, fields)
            else:
                setattr(entity, key, value)
        self.session.add(entity)
        self.session.commit()

    def list(self):
        records = {self.name:[]}
        primary_name = self.get_primarykey(self.name).name
        for instance in self.session.query(self.class_meta).all():
            record = self.read(getattr(instance, primary_name))
            records[self.name].append(record)
        return records

    def update(self, id, record):
        # change record of  relation
        primary_name = self.get_primarykey(self.name).name
        where = "%s.%s='%s'" %(self.name, primary_name, id)
        query = self.session.query(self.class_meta).filter(text(where))
        if query.count() != 1:
            print("Record of %s does not exist!" % query)
            return
        for key, value in record.items():
            if type(value) == type([]):
                fields = self.process_relation(key, value)
                setattr(query.one(), key, fields)
            else:
                setattr(query.one(), key, value)
        # update entity
        self.session.commit()

    def delete(self, id):
        primary_name = self.get_primarykey(self.name).name
        query = "%s.%s='%s'" %(self.name, primary_name, id)
        count = self.session.query(self.class_meta).filter(text(query)).count()
        if count != 1:
            print("Record of %s does not exist!" % query)
            return
        r1 = self.session.query(self.class_meta).filter(text(query)).first()
        self.session.delete(r1)
        self.session.commit()
        # update module class

    def read(self, id):
        primary_name = self.get_primarykey(self.name).name
        query = "%s.%s='%s'" % (self.name, primary_name, id)
        count = self.session.query(self.class_meta).filter(text(query)).count()
        if count != 1:
            print("Record of %s does not exist!" % query)
            return
        data = self.session.query(self.class_meta).filter(text(query)).first()
        record = dict()
        for field in self.get_fields(self.name):
            record[field] = getattr(data, field)
        for field in self.get_relations(self.name):
            record[field] = []
            for obj in getattr(data, field):
                tmp = {}
                for f in self.get_fields(field):
                    value = getattr(obj, f)
                    tmp[f] = value
                record[field].append(tmp)
        return dumps(record)