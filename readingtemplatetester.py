from ReadingTemplates import *
from ReadingPhaseManager import ReadingPhaseManager
from data_handling import *
from referencing import *
from pathlib import Path
from netCDF4 import Dataset

if __name__ == '__main__':


    station_reference = StationReference(dataset_path, filename, wrfin)
    report_reference = ReportReference('./', 'test_reports.csv', '2023-08-16')

    ReadingPhaseManager.set_station_reference(station_reference)
    man = ReadingPhaseManager(report_reference[0])
    man.open_report_store()
    man.get_reading_templates()
    man.prep_loads()
    man.prep_readings()
    man.get_readings()

    exit()






    all_station_ids = [station.id for station in station_storage]
    report_store = ReportStore(all_station_ids)

    ReadingTemplate.set_report_store(report_store)

    reading_templates = [rhReading]

    print(list(product(station_storage, reading_templates)))



