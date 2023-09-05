from ReadingTemplates import *
from SetUpManager import SetUpManager
from ParallelManager import ParallelManager
from ReadingPhaseManager import ReadingPhaseManager
from WritingPhaseManager import WritingPhaseManager
from data_handling import *
from referencing import *
from pathlib import Path
from netCDF4 import Dataset

if __name__ == '__main__':


    ### Set up ###

    setup_man = SetUpManager(2, '/home/force-woest/woest1300/uk/data/')
    setup_man.configure_databank()
    setup_man.get_report_reference(Path('./'), 'test_reports.csv', '2023-08-16')
    [print(report) for report in setup_man.report_reference]


    setup_man.get_station_reference(Path('./'), 'stations_csv.csv', '2023-08-16')
    setup_man.get_forecast_store()
    [print(station) for station in setup_man.station_reference]
    print(ReadingPhaseManager.station_reference)
    setup_man.configure_reading_phase_manager()
    setup_man.configure_writing_phase_manager()


    parr_man = ParallelManager(setup_man.report_reference, 4, setup_man.forecast_store)
    parr_man.setup_pool()
    exit()

    write_man = WritingPhaseManager()
    write_man.write_to_file('path')


    #PARR

    read_man = ReadingPhaseManager(setup_man.report_reference[0])
    read_man.read_phase()

    exit()






    all_station_ids = [station.id for station in station_storage]
    report_store = ReportStore(all_station_ids)

    ReadingTemplate.set_report_store(report_store)

    reading_templates = [rhReading]

    print(list(product(station_storage, reading_templates)))



