import threading
import queue
import typing

from . import datatypes


class Uploader:
    _stop_event: threading.Event
    _filenames: typing.Iterable[str]
    _uploaded_files: typing.List[str]
    _imap_next_thread: threading.Thread
    _processing_thread: threading.Thread

    def __init__(self, filenames: typing.Iterable[str],
                 number_of_processes: int, loading_progress: queue.Queue): ...

    def start(self) -> None: ...

    def stop(self) -> None: ...

    def get_report(self) -> datatypes.UploadReport: ...

    def is_active(self) -> bool: ...

    def wait_for_uploaded(self) -> None: ...
