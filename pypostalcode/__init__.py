from .settings import db_location
import sqlite3
import time
from math import degrees, sin, asin, cos, radians

'''
(c) This data includes information copied with permission from Canada Post Corporation.
'''

class ConnectionManager(object):
    """
    Assumes a database that will work with cursor objects
    """
    
    def __init__(self):
        # test out the connection...
        conn = sqlite3.connect(db_location)
        conn.close()
            
    def query(self, sql, args=()):
        conn = None
        retry_count = 0
        while not conn and retry_count <= 10:
        # If there is trouble reading the file, retry for 10 attempts
        # then just give up...
            try:
                conn = sqlite3.connect(db_location)
            except sqlite3.OperationalError:
                retry_count += 1
                time.sleep(0.001)
        
        if not conn and retry_count > 10:
            raise sqlite3.OperationalError("Can't connect to sqlite database.")
                
        cursor = conn.cursor()
        cursor.execute(sql, args)
        res = cursor.fetchall()
        conn.close()
        return res

PC_QUERY = "SELECT * FROM PostalCodes WHERE fsa=?"
PC_RANGE_QUERY = "SELECT * FROM PostalCodes WHERE longitude >= ? and longitude <= ? AND latitude >= ? and latitude <= ?"
PC_FIND_QUERY = "SELECT * FROM PostalCodes WHERE city LIKE ? AND province LIKE ?"

class PostalCode(object):
    def __init__(self, data):
        self.postalcode = data[0]
        self.city = data[1]
        self.province = data[2]
        self.longitude = data[3]
        self.latitude = data[4]
        self.timezone = data[5]
        self.dst = data[6]

    def __repr__(self):
        attrs = ["postalcode", "city", "province", "longitude", "latitude", "timezone", "dst"]
        attrs = ', '.join(f'{a}={repr(getattr(self, a))}' for a in attrs)
        return f"{self.__class__.__name__}({attrs})"


def format_result(postalcodes):
    if len(postalcodes) > 0:
        return [PostalCode(code) for code in postalcodes]
    else:
        return None

class PostalCodeNotFoundException(Exception):
    pass
    
class PostalCodeDatabase(object):
    
    def __init__(self, conn_manager=None):
        if conn_manager is None:
            conn_manager = ConnectionManager()
        self.conn_manager = conn_manager
        
    def get_postalcodes_around_radius(self, pc, radius):
        postalcodes = self.get(pc)
        if postalcodes is None:
            raise PostalCodeNotFoundException("Could not find postal code you're searching for.")
        else:
            pc = postalcodes[0]
        
        radius = float(radius)
        
        '''
        Bounding box calculations updated from pyzipcode
        '''        
        earth_radius  = 6371
        dlat = radius / earth_radius
        dlon = asin(sin(dlat) / cos(radians(pc.latitude)))
        lat_delta = degrees(dlat)
        lon_delta = degrees(dlon)
             
        if lat_delta < 0:
            lat_range = (pc.latitude + lat_delta, pc.latitude - lat_delta)
        else:
            lat_range = (pc.latitude - lat_delta, pc.latitude + lat_delta)
        
        long_range  = (pc.longitude - lat_delta, pc.longitude + lon_delta)    
        
        return format_result(self.conn_manager.query(PC_RANGE_QUERY , (
            long_range[0], long_range[1],
            lat_range[0], lat_range[1]
        )))
                    
    def find_postalcode(self, city=None, province=None):
        if city is None:
            city = "%"
        else:
            city = city.upper()
            
        if province is None:
            province = "%"
        else:
            province = province.upper()
            
        return format_result(self.conn_manager.query(PC_FIND_QUERY , (city, province)))
        
    def get(self, pc):
        return format_result(self.conn_manager.query(PC_QUERY , (pc,)))
            
    def __getitem__(self, pc):
        pc = self.get(str(pc))
        if pc is None:
            raise IndexError("Couldn't find postal code")
        else:
            return pc[0]
            
    
        
        
        
        
