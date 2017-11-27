from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from module import Base


class Skill(Base):
    __tablename__ = 'skill'
    skill_id = Column(Integer,primary_key=True)
    name = Column(String)
    operator = relationship('Operator', secondary=getattr(__import__('module.operator_skill_table', globals(), locals(), ['operator_skill_table']),'operator_skill_table'), back_populates='skill')
