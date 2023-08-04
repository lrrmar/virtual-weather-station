# main.py
#   Sketch of the process

from * import *

if __name__ == '__main__':

    ### Initialisation ###

    station_store = StationStore(stations.csv)
    report_reference_store = ReportReferenceStore(forecasts.csv)
    forecast_store = ForecastStore(station_store.all_ids)
    # ^^^ should ForecastStore be able to access StationStore explicitly?

    # Adding class attributes
    ReadingTemplate.set_stations(station_store)
    ReadingTemplate.set_forecasts(forecast_store)



    ### Reading Phase ###

    # Set up parallelism

    man = Manager()
    task_queue, done_queue = man.Queue(), man.Queue()
    p = Pool(4)

    for report_reference in ReportReferenceStore:
        task_queue.put(report_reference)

        # OR

        task_queue.put(ReadingPhaseManager(report_reference))

    workers = []
    for i in range(len(ReportStoreManager)):
        workers.append(
            p.apply_async(reading_phase, (task_queue, done_queue)))
