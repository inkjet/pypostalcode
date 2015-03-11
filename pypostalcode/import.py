
import sqlite3
import os
import csv
try:
    from settings import db_location
except:
    from pyzipcode.settings import db_location

conn = sqlite3.connect(db_location)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS PostalCodes;")
c.execute("CREATE TABLE PostalCodes(fsa VARCHAR(3), city TEXT, province TEXT, longitude DOUBLE, latitude DOUBLE, timezone INT, dst INT);")
c.execute("CREATE INDEX fsa_index ON PostalCodes(fsa);")
c.execute("CREATE INDEX city_index ON PostalCodes(city);")
c.execute("CREATE INDEX province_index ON PostalCodes(province);")

reader = csv.reader(open('ca_postalcodes.csv', "rb"))
reader.next() # prime it
    
for row in reader:
    fsa, city, province, lat, longt, timezone, dst = row
    
    c.execute('INSERT INTO PostalCodes values("%s", "%s", "%s", %s, %s, %s, %s)' % (
        fsa,
        city,
        province,
        float(longt),
        float(lat),
        timezone,
        dst
    ))
    
conn.commit()

# We can also close the cursor if we are done with it
c.close()
