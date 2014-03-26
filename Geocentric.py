#-------------------------------------------------------------------------------
# Name:        Geocentric
# Purpose:     Routines to convert from Geographic to Geocentric coodinate
#              systems and vice versa
#
# Author:      Derck Vonck
#
# Created:     22-03-2014
# Copyright:   (c) Derck Vonck 2014
# Licence:     CC 3.0 BY SA
#-------------------------------------------------------------------------------

import math

class Geocentric:
    """
    Routines to convert from Geographic to Geocentric coodinate
    systems and vice versa
    """
    def __init__(self, semiMajorAxis, semiMinorAxis):
        self.a = semiMajorAxis
        self.b = semiMinorAxis
        self.e = math.sqrt((self.a**2 - self.b**2) / self.a**2)

    def GeographicToGeocentric(self, lat, lon, h):
        """
        Convert geographic latitude, longitude, and height coordinates to
        geocentric coordinates
        Parameters
            lat = latitude in decimal degrees meassured from the equator
            lon = longitude in decimal degrees mesaure from the Greenwich meridian
            h = height above the elipsoid in meters
        Returns
            a tuple of the X,Y,Z coordinates in meters measured from the centre of the ellipsoid

        Based on EPSG Guidance Note Number 7, Section 2.2.1 page 94-95 http://www.epsg.org
        """
        v = self.a / math.sqrt(1 - (self.e**2 * math.sin(math.radians(lat))**2))
        X = (v+h) * math.cos(math.radians(lat)) * math.cos(math.radians(lon))
        Y = (v+h) * math.cos(math.radians(lat)) * math.sin(math.radians(lon))
        Z = ((1.0-self.e**2)*v + h) * math.sin(math.radians(lat))
        return (X,Y,Z)

    def GeocentricToGeographic(self, X, Y, Z):
        """
        Convert geocentric x,y,z coordinates to geographic coordinates
        Parameters
            x,y,z = Cartesian coordinates in meters from the centre of the ellipsoid
        Returns
            a tuple of lattitude in decimal degrees, longitude in decimal degrees
            and height above ellipsoid in meters

        Based on EPSG Guidance Note Number 7, Section 2.2.1 page 94-95 http://www.epsg.org
        """
        epsilon = self.e**2 / (1.0 - self.e**2)
        p = math.sqrt(X**2 + Y**2)
        q = math.atan((Z * self.a) / (p * self.b))
        lat = math.atan2((Z + epsilon * self.b * math.sin(q)**3),(p - self.e**2 * self.a * math.cos(q)**3))
        lon = math.atan2(Y,X)
        v = self.a / math.sqrt(1.0 - self.e**2 * math.sin(lat)**2)
        h = (p/math.cos(lat))-v
        return (math.degrees(lat), math.degrees(lon), h)

def main():
##    ### Forward
##    geoC = Geocentric(6378137, 6356752.314)
##    #geoC = Geocentric(6378249.1450,  6356514.9664)
##    lat = 53.0 + (48.0/60.0) + (33.820/3600.0) # -25.994413584931
##    print math.radians(lat)
##    lon = 2.0 + (7.0/60.0) + (46.380/3600.0) #  27.884247784032 #
##    print math.radians(lon)
##    h = 73.0
##    G = geoC.GeographicToGeocentric(lat, lon ,h)
##    print G
##    ### Backward
##    #print geoC.GeocentricToGeographic(G[0], G[1], G[2])
##    print geoC.GeocentricToGeographic(3771793.968, 140253.342, 5124304.349)
    pass

if __name__ == '__main__':
    main()
