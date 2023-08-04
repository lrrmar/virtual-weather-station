# ReadingTemplates.py

from abc import ABC, abstractmethod
from wrf import getvar
from datetime import timedelta
from referencing import Station
from netCDF4 import Dataset


class ReadingTemplate(ABC):



    # This attribute is set for a report regime, during reading
    _report_store = None
    _databank = None

    def __init__(self, station: Station):

        if ReadingTemplate._report_store == None:
            print("No access to report storage")
            raise ValueError
        if ReadingTemplate._databank == None:
            print("No access to databank")
    #        raise ValueError

        self.station = station


    @classmethod
    def set_report_store(cls, report_store):
        """
        Set the report_store for a report regime
        """
        cls._report_store = report_store

    @classmethod
    def set_databank(cls, databank):
        """
        Set the databank for a report regime
        """
        cls._databank = databank

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

    loads = [("wrfout+0", timedelta(hours=0))]

    def dummy(self):
        print("I am a dummy")

    def extract(self):
        ff  = wrf.getvar('ff', _databank.wrfout)
        self._extracted = ff

    def interpolate(self):
        self._interpolated = bilinear_interp(self_extracted, self.station.xy)

    def process(self):
        self._processed = self._interpolated

    def store(self):
        _report_store.store_reading(
            self.station.station_id, 'ff', self._processed)

class ffReading(ReadingTemplate):

    loads = [("wrfout+0", timedelta(hours=0))]

    def dummy(self):
        print("I am a dummy")

    def extract(self):
        ff  = wrf.getvar('ff', _databank.wrfout)
        self._extracted = ff

    def interpolate(self):
        self._interpolated = bilinear_interp(self_extracted, self.station.xy)

    def process(self):
        self._processed = self._interpolated

    def store(self):
        _report_store.store_reading(
            self.station.station_id, 'ff', self._processed)


class rr6Reading(ReadingTemplate):

    loads = [("wrfout-6", "wrfout", timedelta(hours=-6))]

    def dummy(self):
        print("I am a dummy")

    def extract(self):
        nc_var_names = ['RAINC', 'RAINNC', 'SNOWNC', 'HAILNC', 'GRAUPELNC']
        nc_vars = [Dataset(tup[0]).variables(tup[1]) for tup in\
            list(product(
                [self._databank('wrfout+0'), self._databank('wrfout-6')],
                 nc_var_names))]
        self._extracted = nc_vars

    def interpolate(self):
        self._interpolated = [bilinear_interp(var, self.station.xy) for\
            var in self._extracted]

    def process(self):
        rr6 = sum(self._interpolated[0:6])
            - sum(self._interpolated[6:])
        self._processed = rr6

    def store(self):
        _report_store.store_reading(
            self.station.station_id, 'rr6', self._processed)

