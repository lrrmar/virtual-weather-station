from multiprocessing import Pool, Manager, Queue
from referencing import ReportReference, Reports
from storage import ForecastStore
from ReadingPhaseManager import ReadingPhaseManager


class ParallelManager:

    def __init__(self, report_reference: ReportReference, num_workers: int, forecast_store: ForecastStore):
        self.report_reference = report_reference
        self.forecast_store = forecast_store
        self.num_workers = num_workers

    def setup_pool(self):

        self.man = Manager()
        self.task_queue = self.man.Queue()
        self.pool = Pool(self.num_workers)

        for report in self.report_reference:
            self.task_queue.put(report)

        self.tasks = []
        for i in range(len(self.report_reference)):
            self.tasks.append(self.pool.apply_async(worker_function,
                (self.task_queue,)))

        # Run each reading phase and ingest the resulting report stores
        [self.forecast_store.ingest_report_store(task.get())
            for task in self.tasks]

    def run_tasks(self):

        try:
            self.tasks
        except nameError:
            print('Tasks do not exist')
            return

        if self.tasks == []:
            print('Tasks not set up correctly')
            return

        print(f"Starting tasks on {self.num_workers} processes.")
        print(self.tasks)
        [task.get() for task in self.tasks]

def worker_function(input):

    report = input.get()
    print(f'Processing report for launch time {report.launch_time},\
        forecast valid time {report.forecast_time}')
    reading_man = ReadingPhaseManager(report)

    return reading_man.reading_phase()
