#!/usr/bin/python

from datetime import datetime
import requests
import socket
import sqlite3

def req():
    r = requests.get('http://192.168.0.39/LogDaten.dat', auth=('pvserver', 'pvwr'), stream=True)
    start = False

    keys = None
    with open('test.txt', 'w') as f:
        if r.status_code == 200:
            for line in r.iter_lines():
                if line:
                    f.write(line+'\n')
                    if line.startswith('akt. Zeit'):
                        print datetime.fromtimestamp(int(line.split('\t')[1])).strftime('%Y-%m-%d %H:%M:%S')
                    if line.startswith('Zeit'):
                        print line.split('\t')
                        keys = line.split('\t')
                        print 'keyslen: ' + str(len(keys))
                        start = True
                    else:
                        values = [x.strip() for x in line.split('\t')]
                        #print len(values)
                        if start:
                            print datetime.fromtimestamp(int(line.split('\t')[0])).strftime('%Y-%m-%d %H:%M:%S')
                            dictionary = dict(zip(keys, values))
                            #print dictionary
                            try:
                                print int(dictionary['AC1 P'])+int(dictionary['AC2 P'])+int(dictionary['AC3 P'])
                            except:
                                pass
        else:
            print 'error: ' + r.status_code

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("req()", setup="from __main__ import req", number=1))