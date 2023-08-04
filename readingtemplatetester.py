from ReadingTemplates import *
from ReadingPhaseManager import ReadingPhaseManager
from data_handling import *
from referencing import *
from pathlib import Path
from netCDF4 import Dataset

if __name__ == '__main__':

    dataset_path = Path('./')
    filename = 'stations_csv.csv'
    wrfin = Dataset('wrfout_d03_2023-06-01_18:00:00')

    station_storage = Station_storage(dataset_path, filename, wrfin)
    report_reference = ReportReference(True, False)
    ReadingPhaseManager.set_station_store(station_storage)
    man = ReadingPhaseManager(report_reference)
    man.open_report_store()
    man.get_reading_templates()
    man.prep_loads()
    print(man.loads)
    man.prep_readings()
    #man.get_readings()

    exit()






    all_station_ids = [station.id for station in station_storage]
    report_store = ReportStore(all_station_ids)

    ReadingTemplate.set_report_store(report_store)

    reading_templates = [rhReading]

    print(list(product(station_storage, reading_templates)))



