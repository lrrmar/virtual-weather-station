# ReadingPhaseManager.py
#   Represents the parallelisable process of taking readings from data at a
#   given forecast time and generating the report.

from data_handling import *
from referencing import *
from storage import *
from ReadingTemplates import *
from itertools import product

class ReadingPhaseManager:

    # Attributes set prior to beginning reading phase i.e.
    # initiation of this object
    station_reference = None

    @classmethod
    def set_station_reference(cls, station_reference: StationReference):
        cls.station_reference = station_reference

    def __init__(self, report_template: Reports):

        if ReadingPhaseManager.station_reference == None:
            print("No access to station storage")
            raise ValueError

        self.report_template = report_template

    def open_report_store(self):
        # Allocate space for each station to store report
        ReportStore.set_report_format(self.report_template)
        ReadingTemplate.set_report_store(
            ReportStore(ReadingPhaseManager.station_reference.all_ids))

    def get_reading_templates(self):
        self._templates = [rhReading, ffReading, rr6Reading]

    def prep_loads(self):
        # Prepare list of (source_name, data_source) for loading to databank
        self.loads = list(set([tup for reading_template in self._templates \
            for tup in reading_template.loads]))

    def get_loads(self):
        # Configure databank to hold correct data for readingTemplates
        ReadingTemplate.set_databank(
            DataBank(
                *self.loads,
                forecast_issue_time = self.report_template.launch_time, 
                forecast_valid_time = self.report_template.forecast_time 
                ))

    def prep_readings(self):
        # Prepare list of (Station, readingTemplate) for read mapping
        self.readings = product(
            ReadingPhaseManager.station_reference, self._templates)

    def get_readings(self):
        # Map function that instigateis readingTemplate behaviour
        list(map(make_readings, self.readings))

    def save_report_to_forecast_store()
        # ForeCastStore.append(ReadingTemplate.report_store)



def make_readings(tup):
    reading = tup[1](tup[0])
    reading.extract()
    reading.interpolate()
    reading.process()
    reading.store()
