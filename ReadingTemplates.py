# ReadingTemplates.py

from abc import ABC, abstractmethod
from itertools import product
from wrf import getvar, to_np, interplevel
import numpy as np
from datetime import datetime, timedelta
from data_handling import DataBank
from Interpolator import Interpolator
from referencing import Station
from netCDF4 import Dataset



class ReadingTemplate(ABC):



    # This attribute is set for a report regime, during reading
    _report_store = None
    _databank = None

    def __init__(self, station: Station):

        if ReadingTemplate._report_store == None:
            print('No access to report storage')
            raise ValueError
        if ReadingTemplate._databank == None:
            print('No access to databank')
    #        raise ValueError

        self.station = station


    @classmethod
    def set_report_store(cls, report_store):
        '''
        Set the report_store for a report regime
        '''
        cls._report_store = report_store

    @classmethod
    def set_databank(cls, databank: DataBank):
        '''
        Set the databank for a report regime
        '''
        cls._databank = databank

    @classmethod
    def get_report_store(cls):
        return cls._report_store

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def interpolate(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def store(self):
        pass

class rhReading(ReadingTemplate):

    loads = [('wrfoutp0', 'wrfout', timedelta(hours=0))]

    def dummy(self):
        print('I am a dummy')

    def extract(self):
        variables = ['rh', 'z']
        if not hasattr(self._databank, 'rh'):
            reads = {}
            for var in variables:
                reads[var] = to_np(getvar(self._databank.wrfoutp0, var))

            setattr(self._databank, 'rh', reads)

        self._extracted = getattr(self._databank, 'rh')

    def interpolate(self):
        # Issue with this interpolation... need to sort out array masking,
        # for now use 0th element (surface)
        vert_interp = to_np(interplevel(self._extracted['rh'],
            self._extracted['z'], self.station.elevation))
        vert_interp = self._extracted['rh'][0]
        interpolator = Interpolator(self.station.xy[1], self.station.xy[0])
        self._interpolated = [interpolator.interp(vert_interp)]

    def process(self):
        self._processed = self._interpolated

    def store(self):
        ReadingTemplate._report_store.store_reading(
            self.station.id, 'rh', *self._processed)

class ffReading(ReadingTemplate):

    loads = [('wrfoutp0', 'wrfout', timedelta(hours=0))]

    def dummy(self):
        print('I am a dummy')

    def extract(self):
        if  not hasattr(self._databank, 'ff'):
            #print(getvar(self._databank.wrfoutp0,
            #    'uvmet10_wspd_wdir', units='kt'))
            ff  = [to_np(getvar(self._databank.wrfoutp0,
                'uvmet10_wspd_wdir', units='kt')[0])]
            setattr(self._databank, 'ff', ff)

        self._extracted = getattr(self._databank, 'ff')

    def interpolate(self):
        interp= Interpolator(self.station.xy[1], self.station.xy[0])
        self._interpolated = [interp.interp(var) for\
            var in self._extracted]

    def process(self):
        self._processed = self._interpolated

    def store(self):
        ReadingTemplate._report_store.store_reading(
            self.station.id, 'ff', *self._processed)


class rrr6Reading(ReadingTemplate):

    loads = [
        ('wrfoutm6', 'wrfout', timedelta(hours=-6)),
        ('wrfoutp0', 'wrfout', timedelta(hours=0))
    ]

    def dummy(self):
        print('I am a dummy')

    def extract(self):
        if not hasattr(self._databank, 'rrr6'):
            nc_var_names = ['RAINC', 'RAINNC', 'SNOWNC', 'HAILNC', 'GRAUPELNC']
            # np.squeeze removes the axis of length 1 (time dimension)
            rrr6 = [np.array(data_source.variables[var]).squeeze(axis=0)
                for (data_source, var) in list(product(
                    [self._databank.wrfoutp0, self._databank.wrfoutm6],
                    nc_var_names))]

            setattr(self._databank, 'rrr6', rrr6)

        self._extracted = getattr(self._databank, 'rrr6')

    def interpolate(self):
        interp= Interpolator(self.station.xy[1], self.station.xy[0])
        self._interpolated = [interp.interp(var) for\
            var in self._extracted]

    def process(self):
        rrr6 = sum(self._interpolated[0:6])\
            - sum(self._interpolated[6:])
        self._processed = rrr6

    def store(self):
        ReadingTemplate._report_store.store_reading(
            self.station.id, 'rrr6', self._processed)

reading_template_key= {
    'rh': rhReading,
    'ff': ffReading,
    'rrr6': rrr6Reading
}
