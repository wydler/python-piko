import os
import sys
from sqlalchemy import Column
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class History(Base):
    __tablename__ = 'history'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(INTEGER, primary_key=True)
    time = Column(TIMESTAMP(timezone=True))
    dc1_u = Column(INTEGER)
    dc1_i = Column(INTEGER)
    dc1_p = Column(INTEGER)
    dc1_t = Column(INTEGER)
    dc1_s = Column(INTEGER)
    dc2_u = Column(INTEGER)
    dc2_i = Column(INTEGER)
    dc2_p = Column(INTEGER)
    dc2_t = Column(INTEGER)
    dc2_s = Column(INTEGER)
    dc3_u = Column(INTEGER)
    dc3_i = Column(INTEGER)
    dc3_p = Column(INTEGER)
    dc3_t = Column(INTEGER)
    dc3_s = Column(INTEGER)
    ac1_u = Column(INTEGER)
    ac1_i = Column(INTEGER)
    ac1_p = Column(INTEGER)
    ac1_t = Column(INTEGER)
    ac2_u = Column(INTEGER)
    ac2_i = Column(INTEGER)
    ac2_p = Column(INTEGER)
    ac2_t = Column(INTEGER)
    ac3_u = Column(INTEGER)
    ac3_i = Column(INTEGER)
    ac3_p = Column(INTEGER)
    ac3_t = Column(INTEGER)
    ac_f = Column(INTEGER)
    fc_i = Column(INTEGER)
    ain1 = Column(INTEGER)
    ain2 = Column(INTEGER)
    ain3 = Column(INTEGER)
    ain4 = Column(INTEGER)
    ac_s = Column(INTEGER)
    err = Column(INTEGER)
    ens_s = Column(INTEGER)
    ens_err = Column(INTEGER)

    @staticmethod
    def find_or_create(session, **kwargs):
        q = session.query(History).filter(History.time == kwargs['time'])
        ret = session.query(q.exists()).scalar()
        print ret
        if ret:
            print 'exists'
        else:
            session.add(History(**kwargs))

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///history.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)