from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from module import Base


class Operator(Base):
    __tablename__ = 'operator'
    operator_id = Column(Integer,primary_key=True)
    name = Column(String)
    skill = relationship('Skill', secondary=getattr(__import__('module.operator_skill_table', globals(), locals(), ['operator_skill_table']),'operator_skill_table'), back_populates='operator')
