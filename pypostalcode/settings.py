import os
db_filename = 'postalcodes.db'
directory = os.path.dirname(os.path.abspath(__file__))
db_location = os.path.join(directory, db_filename)
