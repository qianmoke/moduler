#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from module import meta
import json
import os
from generator import entity

class Relation(object):
    def __init__(self, session):
        self.session = session
        self.column = "    %s = Column(%s)"
        self.relationship = "    %s = relationship('%s', back_populates='%s', cascade='all, delete, delete-orphan')"
        self.title = "from sqlalchemy import ForeignKey,Table\nfrom module import Base\nfrom sqlalchemy import ForeignKey, Column, Integer, String, Boolean\n\n"

    def write_line(self, fp, data):
        fp.writelines(data)
        fp.writelines("\n")

    def genarator(self, relation_name):
        re = self.session.query(meta.Relation).filter_by(name=relation_name).one()
        source = re.source
        destination = re.destination
        foreignkey = re.foreignkey
        associationforeinkey = re.associationforeinkey
        fp_s = open("./module/" + source + ".py", 'a+')
        fp_d = open("./module/" + destination + ".py", 'a+')
        if re.type == "many2many":
            # genarator_association_table
            association_table = "%s_%s_table" % (source, destination)
            fp_a = open("./module/" + association_table + ".py", 'w+')
            self.write_line(fp_a,self.title)
            self.write_line(fp_a, "%s = Table('%s', Base.metadata," % (association_table,association_table))
            self.write_line(fp_a, "    Column('%s', Integer, ForeignKey('%s.%s'))," % (
                foreignkey, destination, foreignkey))
            self.write_line(fp_a, "    Column('%s', Integer, ForeignKey('%s.%s'))" % (
                associationforeinkey, source, associationforeinkey))
            self.write_line(fp_a, ")")
            # write relation defination into a module class
            relationship = "    %s = relationship('%s', secondary=getattr(__import__('module.%s', globals(), locals(), ['%s']),'%s'), back_populates='%s')"
            self.write_line(fp_s, relationship % (
                destination, destination.capitalize(), association_table, association_table, association_table, source))
            self.write_line(fp_d, relationship % (
                source, source.capitalize(), association_table, association_table, association_table, destination))
        if re.type == "hasmany":
            self.write_line(fp_s, self.relationship %(destination, destination.capitalize(), source))
            self.write_line(fp_d, self.relationship % (source, source.capitalize(), destination))
            self.write_line(fp_d, "    %s = Column('%s', Integer, ForeignKey('%s.%s'))" % (
                associationforeinkey, source, source, foreignkey))
        if re.type == "hasone":
            relationship = "    %s = relationship('%s', uselist=False, back_populates='%s')"
            self.write_line(fp_s, relationship %(destination, destination.capitalize(), source))
            self.write_line(fp_d, relationship % (source, source.capitalize(), destination))
            self.write_line(fp_d, "    %s = Column('%s', Integer, ForeignKey('%s.%s'))" % (
                associationforeinkey, source, source, foreignkey))
        if re.type == "belongsto":
            self.write_line(fp_s, self.relationship % (destination, destination.capitalize(), source))
            self.write_line(fp_d, self.relationship % (source, source.capitalize(), destination))
            self.write_line(fp_s, "    %s = Column('%s', Integer, ForeignKey('%s.%s'))" % (
                foreignkey, source, destination, associationforeinkey ))

    def write_db(self, relation):
        name = relation["name"]
        type = relation["type"]
        source = relation["source"]
        destination = relation["destination"]
        foreignkey = relation["foreignkey"]
        associationforeinkey = relation["associationforeinkey"]
        e1 = self.session.query(meta.Entity).filter_by(name=source).one()
        record = meta.Relation(name=name, type=type, source=source, destination=destination, foreignkey=foreignkey,
                               associationforeinkey=associationforeinkey)
        record.entity = e1
        self.session.add(record)
        self.session.commit()

    def count(self, name):
        return self.session.query(meta.Relation).filter_by(name=name).count()

    def list(self):
        records = {"relations":[]}
        for instance in self.session.query(meta.Relation):
            record = self.read(getattr(instance, "name"))
            records["relations"].append(record)
        return records

    def create(self, name, relation):
        if self.count(name) != 0:
            return "Relation %s existed!" % name, 400
        # save relation into database
        self.write_db(relation)
        # update module class
        e1 = entity.Entity(self.session)
        e1.genarator(relation["source"])
        e1.genarator(relation["destination"])
        # genarate relationship in module class
        self.genarator(relation["name"])
        return "ok!"

    def update(self, name, relation):
        if self.count(name) != 1:
            return "Relation %s does not exist!" % name, 404
        # change record of  relation
        name = relation["name"]
        type = relation["type"]
        source = relation["source"]
        destination = relation["destination"]
        foreignkey = relation["foreignkey"]
        associationforeinkey = relation["associationforeinkey"]
        r1 = self.session.query(meta.Relation).filter_by(name=name).first()
        e1 = self.session.query(meta.Entity).filter_by(name=source).one()
        if r1.type == "many2many" and type != r1.type:
            association_table = "%s_%s_table" % (r1.source, r1.destination)
            os.remove("./module/" + association_table + ".py")
        r1.entity = e1
        r1.name = name
        r1.type = type
        r1.source = source
        r1.destination = destination
        r1.foreignkey = foreignkey
        r1.associationforeinkey = associationforeinkey
        # update relation
        self.session.commit()
        # update module class
        e1 = entity.Entity(self.session)
        e1.genarator(source)
        e1.genarator(destination)
        # genarate relationship in module class
        self.genarator(relation["name"])
        return "ok!"

    def delete(self, name):
        if self.count(name) != 1:
            return "Relation %s does not exist!" % name, 404
        r1 = self.session.query(meta.Relation).filter_by(name=name).first()
        self.session.delete(r1)
        e1 = entity.Entity(self.session)
        e1.genarator(r1.source)
        e1.genarator(r1.destination)
        # update module class
        if r1.type == "many2many":
            association_table = "%s_%s_table" % (r1.source, r1.destination)
            os.remove("../module/" + association_table + ".py")
        self.session.commit()
        return "ok!"

    def read(self, name):
        if self.count(name) != 1:
            return "Relation %s does not exist!" % name, 404
        query = self.session.query(meta.Relation).filter_by(name = name).first()
        relation = dict((k, v) for k, v in vars(query).items() if not k.startswith('_'))
        return relation