from piko.db import session, History, Devices

for obj in session.query(Devices).all():
    print obj.name
