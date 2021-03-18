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

BEFORE_DST_DATE = datetime.datetime(2021, 2, 1)
DST_DATE = datetime.datetime(2021, 4, 1)

conn = sqlite3.connect(db_location)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS PostalCodes;")
c.execute("CREATE TABLE PostalCodes(fsa VARCHAR(3), city TEXT, province TEXT, longitude DOUBLE, latitude DOUBLE, timezone INT, dst INT);")
c.execute("CREATE INDEX fsa_index ON PostalCodes(fsa);")
c.execute("CREATE INDEX city_index ON PostalCodes(city);")
c.execute("CREATE INDEX province_index ON PostalCodes(province);")

reader = csv.reader(open('ca_postalcodes.csv', newline='', encoding='utf-8'))
next(reader)  # skip the header row


tf = TimezoneFinder()
def coords_to_utcoffset_and_isdst(lng, lat):
    timezone_name = tf.timezone_at(lng=lng, lat=lat)

    timezone = pytz.timezone(timezone_name)
    timezone_now = datetime.datetime.now(timezone)
    offset = timezone.utcoffset(BEFORE_DST_DATE).total_seconds()/60/60

    dst = timezone.dst(DST_DATE).total_seconds()/60/60

    return offset, dst, timezone_name



for row in reader:
    fsa, city, province, lat, lng, timezone, dst = row

    # lat,lng in the csv becomes lng,lat in the package
    lng, lat = float(lng), float(lat) 

    timezone_calculated, dst_calculated, tz_name = coords_to_utcoffset_and_isdst(lng, lat)

    if not timezone or not dst:
        timezone = timezone_calculated
        dst = dst_calculated
        print(fsa, city, province, lat, lng, timezone, dst)
        print(f"setting to ({timezone_calculated},  {dst_calculated}) {tz_name}")

    if (float(timezone) != timezone_calculated or float(dst) != dst_calculated) and fsa != 'H0H':
        print(fsa, city, province, lat, lng, timezone, dst)
        print(f"({timezone}, {dst}) should be ({timezone_calculated},  {dst_calculated}) {tz_name}")
    
    c.execute(
        'INSERT INTO PostalCodes values(?,?,?,?,?,?,?)',
        (fsa, city, province, lng, lat, timezone, dst),
    )
    
conn.commit()

# We can also close the cursor if we are done with it
c.close()
