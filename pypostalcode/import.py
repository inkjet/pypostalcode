import csv
import datetime
import os
import sqlite3

import pytz
from timezonefinder import TimezoneFinder

try:
    from settings import db_location
except:
    from pyzipcode.settings import db_location

conn = sqlite3.connect(db_location)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS PostalCodes;")
c.execute("CREATE TABLE PostalCodes(fsa VARCHAR(3), city TEXT, province TEXT, longitude DOUBLE, latitude DOUBLE, timezone DOUBLE, dst INT);")
c.execute("CREATE INDEX fsa_index ON PostalCodes(fsa);")
c.execute("CREATE INDEX city_index ON PostalCodes(city);")
c.execute("CREATE INDEX province_index ON PostalCodes(province);")

reader = csv.reader(open('ca_postalcodes.csv', newline='', encoding='utf-8'))
next(reader)  # skip the header row


for row in reader:
    fsa, city, province, lat, lng, timezone, dst = row

    # lat,lng in the csv becomes lng,lat in the package
    lng, lat = float(lng), float(lat) 

    timezone, dst = float(timezone), float(dst)

    c.execute(
        'INSERT INTO PostalCodes values(?,?,?,?,?,?,?)',
        (fsa, city, province, lng, lat, timezone, dst),
    )
    
conn.commit()

# We can also close the cursor if we are done with it
c.close()
