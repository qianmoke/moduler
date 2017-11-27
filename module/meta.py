from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey,Table
from sqlalchemy.orm import relationship
from module import Base



class Entity(Base):
    __tablename__ = 'entity'
    entity_id = Column(Integer,primary_key=True)
    name = Column(String(32))
    fields = relationship("Field", back_populates="entity")
    relations = relationship("Relation", back_populates="entity")


class Field(Base):
    __tablename__ = 'field'
    field_id = Column(Integer,primary_key=True)
    name = Column(String(32))
    type = Column(String(32))
    is_primary = Column(Boolean)
    default_value = Column(String(32))
    is_not_null = Column(Boolean)
    description = Column(String(255))
    entity_id =  Column(Integer, ForeignKey('entity.entity_id'))
    entity = relationship("Entity", back_populates="fields")


class Relation(Base):
    __tablename__ = 'relation'
    relation_id = Column(Integer, primary_key=True)
    name = Column(String(32))
    source = Column(String(32))
    destination = Column(String(32))
    type = Column(String(32))
    foreignkey = Column(String(32))
    associationforeinkey = Column(String(32))
    entity_id =  Column(Integer, ForeignKey('entity.entity_id'))
    entity = relationship("Entity", back_populates="relations")





