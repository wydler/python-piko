import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import Column
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Devices(Base):
    __tablename__ = 'devices'

    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    active = Column(BOOLEAN)
    sn = Column(TEXT)
    ip = Column(TEXT)
    port = Column(INTEGER)
    addr = Column(INTEGER)
    install_date = Column(TIMESTAMP)
    max_power = Column(INTEGER)

    @staticmethod
    def create(**kwargs):
        session.add(Device(**kwargs))


class History(Base):
    __tablename__ = 'history'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(INTEGER, primary_key=True)
    time = Column(TIMESTAMP, index=True)
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

    @property
    def serialize(self):
        tm = self.time
        #tm = tm - timedelta(minutes=tm.minute % 15, seconds=tm.second, microseconds=tm.microsecond)
        return [
            int(tm.strftime('%s')) * 1000,
            self.ac1_p + self.ac2_p + self.ac3_p
        ]

    @staticmethod
    def create(**kwargs):
        q = session.query(History).filter(History.time == kwargs['time'])
        ret = session.query(q.exists()).scalar()
        if not ret:
            session.add(History(**kwargs))

engine = create_engine('sqlite:///history.db')

Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
