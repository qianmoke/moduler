#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from module import meta
from os import remove

class Entity(object):
    def __init__(self, session):
        self.session = session
        self.title = "from sqlalchemy import ForeignKey, Column, Integer, String\nfrom sqlalchemy.orm import relationship\nfrom module import Base\n\n\nclass %s(Base):"
        self.table_name = "    __tablename__ = '%s'"
        self.column = "    %s = Column(%s)"

    def write_line(self, fp, data):
        fp.writelines(data)
        fp.writelines("\n")

    def write_columns(self, fp, name):
        entity = self.session.query(meta.Entity).filter_by(name=name).one()
        for field in entity.fields:
            name = field.name
            type = field.type
            if field.is_primary:
                self.write_line(fp, self.column %(name, type+',primary_key=True'))
            else:
                self.write_line(fp, self.column %(name, type))

    def genarator(self, name):
        fp = open("./module/" + name + ".py", 'w+')
        self.write_line(fp, self.title % (name.capitalize()))
        self.write_line(fp, self.table_name % (name))
        self.write_columns(fp, name)
        fp.close()

    def write_db(self, data):
        e1 = meta.Entity(name=data["name"])
        for field in data["fields"]:
            name = field["name"]
            type = field["type"]
            is_primary = field["is_primary"]
            default_value = field["default_value"]
            is_not_null = field["is_not_null"]
            description = field["description"]
            record = meta.Field(name=name, type=type, is_primary=is_primary, default_value=default_value,
                                is_not_null=is_not_null, description=description)
            record.entity = e1
            self.session.add(record)
        self.session.commit()

    def count(self, name):
        return self.session.query(meta.Entity).filter_by(name=name).count()

    def create(self, entity_name, data):
        # save relation into database
        if self.count(entity_name) != 0:
            return "Entity %s existed!" % entity_name, 400
        self.write_db(data)
        # update module class
        # genarate relationship in module class
        self.genarator(entity_name)
        return "ok!"

    def list(self):
        records = {"entities":[]}
        for instance in self.session.query(meta.Entity):
            record = self.read(getattr(instance, "name"))
            records["entities"].append(record)
        return records

    def update(self, entity_name, data):
        # change record of  relation
        fields = data["fields"]
        if self.count(entity_name) != 1:
            return "Entity %s does not exist!" % entity_name, 404
        e1 = self.session.query(meta.Entity).filter_by(name=entity_name).one()
        e1.name = data["name"]
        for i in range(len(e1.fields)):
            for field in fields:
                if e1.fields[i].name == field["name"]:
                    e1.fields[i].type = field["type"]
                    e1.fields[i].default_value = field["default_value"]
                    e1.fields[i].is_not_null = field["is_not_null"]
                    e1.fields[i].is_primary = field["is_primary"]

        # update entity
        self.session.commit()
        # update module class
        self.genarator(entity_name)
        return "ok!"

    def delete(self, name):
        if self.count(name) != 1:
            return "Entity %s does not exist!" % name, 404
        e1 = self.session.query(meta.Entity).filter_by(name=name).first()
        self.session.delete(e1)
        self.session.commit()
        # update module class
        remove("../module/" + name + ".py")
        return 'ok!'

    def read(self, name):
        if self.count(name) != 1:
            return "Entity %s does not exist!" % name, 404
        query = self.session.query(meta.Entity).filter_by(name = name).first()
        entity = dict()
        entity["fields"] = []
        entity["name"] = query.name
        for field in query.fields:
            f = dict((k, v) for k, v in vars(field).items() if not k.startswith('_'))
            entity["fields"].append(f)
        return entity

    def list_field(self, name):
        result = self.read(name)
        if isinstance(result, dict):
            return {"fields": result["fields"]}
        else:
            return result

    def get_field(self,name, field_id):
        result = self.read(name)
        if isinstance(result, dict):
            field_ids = [(k["field_id"]) for k in result["fields"]]
            if field_id not in field_ids:
                return "Field %s does not exist!" % field_id, 404
            else:
                for k in result["fields"]:
                    if k["field_id"] == field_id:
                        return k
        else:
            return result
