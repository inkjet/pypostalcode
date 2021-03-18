### pypostalcode

`pypostalcode` is a fork of Nathan Van Gheem's excellent `pyzipcode` package. The zipcode database has been replaced with Canadian cities and their postal codes. The general usage is the same.

Canadian postal codes are six characters with this format: A1A 1A1, where A is a letter and 1 is a digit, with a space separating the third and fourth characters. The first three digits are the Forward Sortation Area (FSA), and the last three are the Local Delivery Unit (LDU). The FSA information is available from the report "Forward Sortation Area Boundary File, 2011 Census. Statistics Canada Catalogue no. 92-179-X" retrieved from
 http://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2011-eng.cfm

This module only uses the FSA designator for location. There are over 800,000 FSA+LDU combinations, but the 1,645 unique FSA values provide coarse resolution for most applications.

To install:

```
pip install pypostalcode
```

Basic usage:

```pycon
>>> from pypostalcode import PostalCodeDatabase
>>> pcdb = PostalCodeDatabase()
>>> pc = 'V5K'
>>> location = pcdb[pc]
>>> location.postalcode
'V5K'
>>> location.city
'Vancouver (North Hastings- Sunrise)'
>>> location.province
'British Columbia'
>>> location.longitude
-123.0489
>>> location.latitude
49.293
>>> location.timezone
-8
>>> location.dst
1
```

Get a list of postal codes given a radius in kilometers:

```pycon
>>> from pypostalcode import PostalCodeDatabase
>>> pcdb = PostalCodeDatabase()
>>> pc = 'T3Z'
>>> radius = 25
>>> results = pcdb.get_postalcodes_around_radius(pc, radius)
>>> for r in results:
...     print(f'{r.postalcode}: {r.city}, {r.province}')
... 
T3B: Calgary (Montgomery / Bowness / Silver Springs / Greenwood), Alberta
T3G: Calgary (Hawkwood / Arbour Lake / Royal Oak / Rocky Ridge), Alberta
T3H: Calgary (Discovery Ridge / Signal Hill / Aspen Woods / Patterson / Cougar Ridge), Alberta
T3L: Calgary (Tuscany / Scenic Acres), Alberta
T3R: Calgary Northwest, Alberta
T3Z: Redwood Meadows, Alberta
T4C: Cochrane, Alberta
```

© This data includes information copied with permission from Canada Post Corporation

This data include data from [GeoNames](https://www.geonames.org/), which is distributed under a [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license
