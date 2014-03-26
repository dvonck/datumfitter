#-------------------------------------------------------------------------------
# Name:        FitTransform
# Purpose:     Given an input csv file of control points in lat, lon of the
#              source and target spheroid fit a transformation
#
# Author:      Derck Vonck
#
# Created:     23-03-2014
# Copyright:   (c) Derck Vonck 2014
# Licence:     CC 3.0 BY SA
#-------------------------------------------------------------------------------

import csv, Geocentric, math, scipy.optimize, numpy

class ControlPoint:
    def __init__(self, controlPointId, sourceLat, sourceLon, sourceHeight, targetLat, targetLon, targetHeight):
        self.Id = controlPointId
        self.srcLat = sourceLat
        self.srcLon = sourceLon
        self.srcHt = sourceHeight
        self.trgtLat = targetLat
        self.trgtLon = targetLon
        self.trgtHt = targetHeight


    def CalculateGeocentricSource(self, geoCentricSrc):
        (self.srcX, self.srcY, self.srcZ) = geoCentricSrc.GeographicToGeocentric(self.srcLat, self.srcLon, self.srcHt)

    def CalculateGeocentricTarget(self, geoCentricTrgt):
        (self.trgtX, self.trgtY, self.trgtZ) = geoCentricTrgt.GeographicToGeocentric(self.trgtLat, self.trgtLon, self.trgtHt)

    def PredictGeocentricTranslation(self, dX, dY, dZ):
        self.predX = self.srcX + dX
        self.predY = self.srcY + dY
        self.predZ = self.srcZ + dZ

    def PredictHelmert7P(self, dX, dY, dZ, s, rX, rY, rZ):
        scale = (1+s/1e6)
        radX = math.radians(rX/3600.0)
        radY = math.radians(rY/3600.0)
        radZ = math.radians(rZ/3600.0)
        self.predX = dX + scale * (self.srcX + radZ*self.srcY - radY*self.srcZ)
        self.predY = dY + scale * (-radZ*self.srcX + self.srcY + radX*self.srcZ)
        self.predZ = dZ + scale * (radY*self.srcX - radX*self.srcY + self.srcZ)

    def ResidualDistance(self):
        return math.sqrt( (self.trgtX - self.predX)**2 + (self.trgtY - self.predY)**2 + (self.trgtZ - self.predZ)**2 )

controlPointList = []

def SSGeocentric(P):
    ssResidualDistance = 0.0
    global controlPointList
    for controlPoint in controlPointList:
        controlPoint.PredictGeocentricTranslation(P[0], P[1], P[2])
        ssResidualDistance += controlPoint.ResidualDistance()**2
    #print P, ssResidualDistance
    return ssResidualDistance

def SSHelmert7P(P):
    ssResidualDistance = 0.0
    global controlPointList
    for controlPoint in controlPointList:
        controlPoint.PredictHelmert7P(P[0], P[1], P[2], P[3], P[4], P[5], P[6])
        ssResidualDistance += controlPoint.ResidualDistance()**2
    print P, ssResidualDistance
    return ssResidualDistance

def SSGeocentricPrime(P):
    dFdx = 0.0
    dFdy = 0.0
    dFdz = 0.0
    global controlPointList
    for controlPoint in controlPointList:
        controlPoint.PredictGeocentricTranslation(P[0], P[1], P[2])
        xts = P[0] - controlPoint.trgtX + controlPoint.srcX
        yts = P[1] - controlPoint.trgtY + controlPoint.srcY
        zts = P[2] - controlPoint.trgtZ + controlPoint.srcZ
        divisor = math.sqrt(xts**2 + yts**2 + zts**2)
        dFdx += (xts / divisor)
        dFdy += (yts / divisor)
        dFdz += (zts / divisor)
    return numpy.array([dFdx, dFdy, dFdz])

def LoadControlPoints(controlPointFilename):
    with open(controlPointFilename, 'rb') as f:
        csvReader = csv.reader(f)
        csvReader.next()
        global controlPointList
        controlPointList = []
        for row in csvReader:
            controlPoint = ControlPoint(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]))
            controlPointList.append(controlPoint)

def main():
    LoadControlPoints(r'd:\Projects\datumfitter\Tshwane.csv')
    # Calculate the Geocentric Coordinates
    capeGeocentric = Geocentric.Geocentric(6378249.1450, 6356514.9664)
    wgsGeocentric = Geocentric.Geocentric(6378137.0000, 6356752.3142)
    for controlPoint in controlPointList:
        controlPoint.CalculateGeocentricSource(capeGeocentric)
        controlPoint.CalculateGeocentricTarget(wgsGeocentric)
    # Initial guess
    ###P = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    P = [-109.096367,-60.770521,-240.766639,-6.066600,2.757766,-0.883306,0.026513]
    P1 = scipy.optimize.fmin_powell(SSHelmert7P, P)
    print 'Best fit parameters %s'  % P1
    for controlPoint in controlPointList:
        controlPoint.PredictHelmert7P(P1[0], P1[1], P1[2], P1[3], P1[4], P1[5], P1[6])
        print controlPoint.Id, controlPoint.ResidualDistance()

if __name__ == '__main__':
    main()
