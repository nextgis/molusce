# encoding: utf-8

import gdal

import numpy as np
from numpy import ma as ma

from utils import reclass

class ProviderError(Exception):
    '''Base class for exceptions in this module.'''
    def __init__(self, msg):
        self.msg = msg

class Raster(object):
    def __init__(self, filename):
        # TODO: Get mask values from the raster metadata.
        self.filename = filename
        self.maskVals = None
        self.data = None
        self.bands = None
        self._read()
    
    def binaryzation(self, trueVals, bandNum):
        '''Reclass band bandNum to true/false mode. Set true for pixels from trueVals.'''
        r = self.getBand(bandNum)
        r = reclass(r, trueVals)
        self.setBand(r, bandNum)
    
    def getBand(self, band):
        return self.bands[band-1]
    
    def getBandsCount(self):
        return len(self.bands)
        
    def getFileName(self):
        return self.filename
        
    def get_dtype(self):
        if self.getBandsCount() != 1:
            raise ProviderError('You can get dtype of the one-band raster only!')
        band = self.getBand(0)
        return band.dtype
    
    def setBand(self, raster, bandNum):
        self.bands[bandNum] = raster
    
    def setMask(self):
        #TODO: Get mask values from the raster metadata.
        #      Don't use mask now.
        maskVals = []
        
        for i in range(self.getBandsCount()):
            r = self.getBand(i)
            mask = reclass(r, maskVals)
            r = ma.array(data = r, mask=mask)
            self.setBand(r, i)
        
    def _read(self):
        self.data = gdal.Open( self.filename )
        if self.data is None:
          raise ProviderError("Can't read the file '%s'" % self.filename)
        self.bands = []
        for i in range(1, self.data.RasterCount+1):
            r = self.data.GetRasterBand(i)
            r = r.ReadAsArray()
            self.bands.append(r)
        self.setMask()
        
        
        