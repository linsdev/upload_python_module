import dataclasses
import typing


@dataclasses.dataclass
class UploadReport:
    uploaded_files: typing.List[str]
    not_uploaded_files: typing.List[str]


@dataclasses.dataclass
class UploadProgress:
    done: int
    error: int
    total: int
