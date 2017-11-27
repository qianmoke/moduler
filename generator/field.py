#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from module import meta
from os import remove
from json import dumps
from generator import entity

class Field(object):
    def __init__(self, session):
        self.session = session

    def write_db(self, entity, data):
        e1 = self.session.query(meta.Entity).filter_by(name=entity).one()
        name = data["name"]
        type = data["type"]
        primary = data["primary"]
        default_value = data["default_value"]
        is_not_null = data["is_not_null"]
        record = meta.Field(name=name,type=type,primary=primary,default_value=default_value, is_not_null=is_not_null)
        record.entity = e1
        self.session.add(record)
        self.session.commit()

    def count(self, field_id):
        return self.session.query(meta.Field).filter_by(field_id=field_id).count()

    def list(self, entity):
        records = {"fields":[]}
        for instance in self.session.query(meta.Field):
            record = self.read(getattr(instance, "field_id"))
            records["fields"].append(record)
        return records

    def create(self, entity, data):
        # save relation into database
        self.write_db(entity, data)
        # update module class
        entity.Entity(self.session).genarator(entity)

    def update(self, entity, field_id, data):
        # change record of  relation
        if self.count(field_id) != 1:
            print("Field %s does not exist!" % field_id)
            return
        f1 = self.session.query(meta.Field).filter_by(field_id=field_id).one()
        f1.name = data["name"]
        f1.type = data["type"]
        f1.primary = data["primary"]
        f1.default_value = data["default_value"]
        f1.is_not_null = data["is_not_null"]
        # update entity
        self.session.commit()
        # update module class
        entity.Entity(self.session).genarator(entity)

    def delete(self, entity, field_id):
        if self.count(field_id) != 1:
            print("Field %s does not exist!" % field_id)
            return
        f1 = self.session.query(meta.Field).filter_by(field_id=field_id).first()
        self.session.delete(f1)
        self.session.commit()
        # update module class
        entity.Entity(self.session).genarator(entity)

    def read(self, entity, field_id):
        if self.count(field_id) != 1:
            print("Field %s does not exist!" % field_id)
            return
        query = self.session.query(meta.Field).filter_by(field_id = field_id).first()
        field = dict()
        field["field_id"] = query.field_id
        field["type"] = query.type
        field["name"] = query.name
        field["default_value"] = query.default_value
        field["is_not_null"] = query.is_not_null
        field["primary"] = query.primary
        return dumps(field)