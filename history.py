#!/usr/bin/python

from datetime import datetime
import requests
import socket
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_declarative import Base, History

engine = create_engine('sqlite:///history.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


def req():
    r = requests.get('http://192.168.0.39/LogDaten.dat', auth=('pvserver', 'pvwr'), stream=True)
    start = False

    keys = ['time', 'dc1_u', 'dc1_i', 'dc1_p', 'dc1_t', 'dc1_s', 'dc2_u', 'dc2_i', 'dc2_p', 'dc2_t', 'dc2_s', 'dc3_u', 'dc3_i', 'dc3_p', 'dc3_t', 'dc3_s', 'ac1_u', 'ac1_i', 'ac1_p', 'ac1_t', 'ac2_u', 'ac2_i', 'ac2_p', 'ac2_t', 'ac3_u', 'ac3_i', 'ac3_p', 'ac3_t', 'ac_f', 'fc_i', 'ain1', 'ain2', 'ain3', 'ain4', 'ac_s', 'err', 'ens_s', 'ens_err', 'kb_s', 'total_e', 'iso_r', 'event']
    with open('test.txt', 'w') as f:
        if r.status_code == 200:
            for line in r.iter_lines():
                if line:
                    f.write(line+'\n')
                    if line.startswith('akt. Zeit'):
                        print datetime.fromtimestamp(int(line.split('\t')[1])).strftime('%Y-%m-%d %H:%M:%S')
                    if line.startswith('Zeit'):
                        #print line.split('\t')
                        #keys = line.split('\t')
                        #print 'keyslen: ' + str(len(keys))
                        start = True
                    else:
                        values = [x.strip() for x in line.split('\t')]
                        #print len(values)
                        if start:
                            dt = datetime.fromtimestamp(int(line.split('\t')[0]))
                            dictionary = dict(zip(keys, values))
                            dictionary['time'] = dt
                            if len(dictionary) == 38:
                                #print dictionary
                                try:
                                    History.find_or_create(session, **dictionary)
                                    #session.add(data)
                                    #print int(dictionary['AC1 P'])+int(dictionary['AC2 P'])+int(dictionary['AC3 P'])
                                except Exception as e:
                                    print e.message
                                    pass
        else:
            print 'error: ' + r.status_code

    session.commit()

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("req()", setup="from __main__ import req", number=1))