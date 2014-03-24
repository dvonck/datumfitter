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

import csv, Geocentric, math, scipy.optimize

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

    def ResidualDistance(self):
        return math.sqrt( (self.trgtX - self.predX)**2 + (self.trgtY - self.predY)**2 + (self.trgtZ - self.predZ)**2 )

controlPointList = []

def SSGeocentric(P):
    ssResidualDistance = 0.0
    global controlPointList
    for controlPoint in controlPointList:
        controlPoint.PredictGeocentricTranslation(P[0], P[1], P[2])
        ssResidualDistance += controlPoint.ResidualDistance()**2
    print P, ssResidualDistance
    return ssResidualDistance

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
    LoadControlPoints(r'd:\Projects\Geocentric\Tshwane.csv')
    # Calculate the Geocentric Coordinates
    capeGeocentric = Geocentric.Geocentric(6378249.1450, 6356514.9664)
    wgsGeocentric = Geocentric.Geocentric(6378137.0000, 6356752.3142)
    for controlPoint in controlPointList:
        controlPoint.CalculateGeocentricSource(capeGeocentric)
        controlPoint.CalculateGeocentricTarget(wgsGeocentric)
    # Initial guess
    P = [-150.0,-100.0,-300.0]
    P1 = scipy.optimize.fmin_powell(SSGeocentric, P)
    objFun = SSGeocentric(P1)


if __name__ == '__main__':
    main()
