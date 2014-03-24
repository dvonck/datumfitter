datumfitter
===========

This is a set of Python scripts that can be used to fit Datum Conversion Models 
to transform geographic coordinates from one geodetic datum to another. 

My problem was that I could not find any software that could be used to do a least-
squares fit of such models.  I therefore implemented the equations from the 
European Petroleum Survey Group  (http://www.epsg.org) for transforming coordinates from 
geographic to geocentric coordinates.  These formulas were then used to fit a 
geocentric translation model of the form

[X']   [X + dX]
[Y'] = [Y + dY]
[Z']   [Z + dZ]

with parameters dX, dY, dZ that are estimates using least squares. 

The code was written for Python 2.7.6 with a dependency on scipy (http://www.scipy.org).

The script currently uses a csv file that consists of the following columns
1. Control Point Identifier
2. Source lattitude in decimal degrees
3. Source longitude in decimal degrees
4. Source height in m above ellipsoid
5. Target lattitude in decimal degrees
6. Target longitude in decimal degrees
7. Target height in m above ellipsoid

TODO:
I would like to implement the Helmert 7 Parameter Model as well to see if this will 
give a better fit to the dataset included.
