import unittest
import queue
import time

from .uploader import Uploader
from ..helper import measure_the_running_time


class UploaderCase(unittest.TestCase):
    filenames = sorted((f'{i}' for i in range(100)))
    number_of_processes = 12
    time_to_stop = 1

    @staticmethod
    def mock(files_list, number_of_processes, f):
        q = queue.Queue()
        uploader = Uploader(files_list, number_of_processes, q)
        uploader.start()
        return f(uploader, q)

    @staticmethod
    def mock_wait_while_is_active(files_list, number_of_processes):
        def f(uploader, q):
            progress = []
            while uploader.is_active():
                progress.append(q.get())
            return uploader.get_report(), progress

        return UploaderCase.mock(files_list, number_of_processes, f)

    @staticmethod
    @measure_the_running_time
    def mock_stop_after_N_seconds(files_list, number_of_processes, seconds):
        def f(uploader, q):
            time.sleep(seconds)
            uploader.stop()
            return uploader.get_report()

        return UploaderCase.mock(files_list, number_of_processes, f)

    def stop_after_N_seconds(self, N):
        report, t = self.mock_stop_after_N_seconds(self.filenames, self.number_of_processes, N)
        self.assertLessEqual(t, N + self.time_to_stop)

    def test_stop_immediately(self):
        self.stop_after_N_seconds(0)

    def test_stop_after_2_seconds(self):
        self.stop_after_N_seconds(2)

    def test_upload(self):
        report, progress = self.mock_wait_while_is_active(self.filenames, self.number_of_processes)

        last_progress = progress[-1]
        self.assertEqual(last_progress.done, last_progress.total)
        self.assertEqual(last_progress.error, 0)

        self.assertEqual(sorted(report.uploaded_files), self.filenames)
        self.assertEqual(report.not_uploaded_files, [])


if __name__ == '__main__':
    unittest.main()
