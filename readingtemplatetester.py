from ReadingTemplates import *
from ReadingPhaseManager import ReadingPhaseManager
from SetUpManager import SetUpManager
from data_handling import *
from referencing import *
from pathlib import Path
from netCDF4 import Dataset

if __name__ == '__main__':


    ### Set up ###

    setup_man = SetUpManager(2, '/home/force-woest/woest1300/uk/data/')
    setup_man.configure_databank()
    setup_man.get_report_reference(Path('./'), 'test_reports.csv', '2023-08-16')
    setup_man.get_station_reference(Path('./'), 'stations_csv.csv', '2023-08-16')

    #PARR

    ReadingPhaseManager.set_station_reference(setup_man.station_reference)
    read_man = ReadingPhaseManager(setup_man.report_reference[0])
    read_man.open_report_store()
    read_man.get_reading_templates()
    read_man.prep_loads()
    read_man.get_loads()
    read_man.prep_readings()
    read_man.get_readings()
    print(ReadingTemplate._report_store.data)

    exit()






    all_station_ids = [station.id for station in station_storage]
    report_store = ReportStore(all_station_ids)

    ReadingTemplate.set_report_store(report_store)

    reading_templates = [rhReading]

    print(list(product(station_storage, reading_templates)))



