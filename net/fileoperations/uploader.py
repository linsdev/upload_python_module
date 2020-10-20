import threading
import queue

from . import datatypes
from . import uploader_func


class Uploader:
    def __init__(self, filenames, number_of_processes, loading_progress):
        if number_of_processes < 1:
            raise ValueError("Number of processes must be at least 1")

        self._stop_event = threading.Event()
        self._stop_event.set()

        self._filenames = filenames
        self._uploaded_files = []

        imap_next_thread_iter_queue = queue.Queue()
        imap_next_thread_result_queue = queue.Queue()

        self._imap_next_thread = threading.Thread(
            target=uploader_func.imap_next_thread,
            args=(imap_next_thread_iter_queue, imap_next_thread_result_queue)
        )

        self._processing_thread = threading.Thread(
            target=uploader_func.processing_thread,
            args=(filenames, number_of_processes, loading_progress,
                  imap_next_thread_iter_queue, imap_next_thread_result_queue,
                  self._stop_event, self._uploaded_files)
        )

    def start(self):
        self._stop_event.clear()
        self._imap_next_thread.start()
        self._processing_thread.start()

    def stop(self):
        self._stop_event.set()

    def get_report(self):
        return datatypes.UploadReport(
            uploaded_files=self._uploaded_files,
            not_uploaded_files=list(set(self._filenames) - set(self._uploaded_files))
        )

    def is_active(self):
        return not self._stop_event.is_set()

    def wait_for_uploaded(self):
        self._stop_event.wait()
