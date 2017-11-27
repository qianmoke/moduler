from sqlalchemy import ForeignKey,Table
from module import Base
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean


operator_skill_table = Table('operator_skill_table', Base.metadata,
    Column('skill_id', Integer, ForeignKey('skill.skill_id')),
    Column('operator_id', Integer, ForeignKey('operator.operator_id'))
)
