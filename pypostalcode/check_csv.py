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


tf = TimezoneFinder()


def coords_to_utcoffset_and_isdst(lng, lat):
    timezone_name = tf.timezone_at(lng=lng, lat=lat)
    timezone = pytz.timezone(timezone_name)
    offset = timezone.utcoffset(BEFORE_DST_DATE).total_seconds() / 60 / 60
    dst = timezone.dst(DST_DATE).total_seconds() / 60 / 60
    return offset, dst, timezone_name


rows = []
with open("ca_postalcodes.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for fsa, city, province, lat, lng, timezone, dst in reader:
        # lat,lng in the csv becomes lng,lat in the package
        lng, lat = float(lng), float(lat)

        timezone_calculated, dst_calculated, tz_name = coords_to_utcoffset_and_isdst(
            lng=lng, lat=lat
        )

        if fsa == "H0H":
            pass
        elif not timezone or not dst:
            print(fsa, city, province, lat, lng, timezone, dst)
            print(f"setting to ({timezone_calculated},  {dst_calculated}) {tz_name}")
        elif float(timezone) != timezone_calculated or float(dst) != dst_calculated:
            print(fsa, city, province, lat, lng, timezone, dst)
            print(
                f"changing ({timezone}, {dst}) to ({timezone_calculated}, {dst_calculated}) {tz_name}"
            )

        if fsa != "H0H":
            timezone, dst = timezone_calculated, dst_calculated

        # Don't add ".0" to floats
        timezone = int(timezone) if int(timezone) == timezone else timezone
        dst = int(dst) if int(dst) == dst else dst
        lat = int(lat) if int(lat) == lat else lat
        lng = int(lng) if int(lng) == lng else lng

        rows.append([fsa, city, province, lat, lng, timezone, dst])

PROVINCES = {
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "New Brunswick": "NB",
    "Newfoundland and Labrador": "NL",
    "Northwest Territory": "NT",
    "Nova Scotia": "NS",
    "Nunavut Territory": "NT",
    "Ontario": "ON",
    "Prince Edward Island": "PE",
    "Quebec": "QC",
    "Saskatchewan": "SK",
    "Yukon": "YT",
}
# sort rows by province code then FSA code
rows = sorted(rows, key=lambda row: (PROVINCES[row[2]], row[0]))

with open("ca_postalcodes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
