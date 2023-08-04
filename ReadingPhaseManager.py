# ReadingPhaseManager.py
#   Represents the parallelisable process of taking readings from data at a
#   given forecast time and generating the report.

from data_handling import *
from referencing import *
from ReadingTemplates import *
from itertools import product

class ReadingPhaseManager:

    # Attributes set prior to beginning reading phase i.e.
    # initiation of this object
    station_store = None

    @classmethod
    def set_station_store(cls, station_store: Station_storage):
        cls.station_store = station_store

    def __init__(self, report_reference):#: ReportReference):

        if ReadingPhaseManager.station_store == None:
            print('No access to station storage')
            raise ValueError

        self.report_reference = report_reference

    def open_report_store(self):
        ReadingTemplate.set_report_store(
            ReportStore(ReadingPhaseManager.station_store.all_ids))

    def get_reading_templates(self):
        self._templates = [rhReading, ffReading, rr6Reading]

    def prep_loads(self):
        self.loads = list(set([tup for reading_template in self._templates \
            for tup in reading_template.loads]))

    def get_loads(self):

        print('regular loads are ', self.loads)
        print('asterisked loads are ', *self.loads)
        ReadingTemplate.set_databank(
            DataBank(
            self.report_reference.forecast_issue_time,
            self.report_reference.forecast_valid_at,
            *self.loads))

    def prep_readings(self):
        self.readings = product(
            ReadingPhaseManager.station_store, self._templates)

    def get_readings(self):
        list(map(make_readings, self.readings))



def make_readings(tup):
    reading = tup[1](tup[0])
    reading.extract()
