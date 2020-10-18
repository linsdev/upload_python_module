from . import datatypes


class Uploader:
    def __init__(self, filenames, number_of_processes, loading_progress):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def get_report(self):
        return datatypes.UploadReport([], [])

    def is_active(self):
        return False

    def wait_for_uploaded(self):
        pass
