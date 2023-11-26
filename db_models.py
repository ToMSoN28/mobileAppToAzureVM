from sqlalchemy import Column, Integer, Float, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

men_company = Table(
    'man_company',
    Base.metadata,
    Column('men_id', ForeignKey('mens.id')),
    Column('company_id', ForeignKey('company.id'))
   )

class Men(Base):
    __tablename__='mens'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    employer = relationship('Company', secondary=men_company, back_populates='employee')
    rectangles = relationship('Rectangle', backref='owner')
    wife = relationship('Wife', back_populates='husbend', uselist=False)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'employer_ids': [company.id for company in self.employer],
            'rectangles_ids': [rectangle.id for rectangle in self.rectangles],
            'wife_id': self.wife.id if self.wife else None
        }
    
class Rectangle(Base):
    __tablename__='rectangles'
    id = Column(Integer, primary_key = True)
    length = Column(Float)
    height = Column(Float)
    owner_id = Column(Integer, ForeignKey('mens.id'))
    
    def edit_json(self):
        return {
            'length': self.length,
            'height': self.height,
        }
    
    def to_json(self):
        return {
            'id': self.id,
            'length': self.length,
            'height': self.height,
            'owner_id': self.owner_id
        }
    
class Wife(Base):
    __tablename__='wifes'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    surname = Column(String)
    husbend_id = Column(Integer, ForeignKey('mens.id'))
    husbend=relationship('Men', back_populates='wife')
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'husbend_id': self.husbend_id
        }
    
class Company(Base):
    __tablename__='company'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    employee = relationship('Men', secondary=men_company, back_populates='employer')
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'employee_ids': [employee.id for employee in self.employee]
        }