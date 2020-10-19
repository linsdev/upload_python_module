# Upload python module
A module to upload in parallel files to the remote server.
Real uploading is not part of this module, some dummy function to emulate upload used.

#### Input data:
* List of files to upload
* Maximum number of parallel uploading process
* Queue for passing progress to the caller

#### Output data:
* Uploading progress
* Final uploading report (uploaded files and not uploaded)

## Usage example
```python
import queue

from net.fileoperations.uploader import Uploader

if __name__ == '__main__':
    files_list = sorted((f'{i}' for i in range(100)))

    q = queue.Queue()
    uploader = Uploader(files_list, 12, q)
    uploader.start()

    while uploader.is_active():
        progress = q.get()
        print(progress.done, progress.error, progress.total)

    print(uploader.get_report())
```

## Documentation
* Flowchart and Use Case Diagram | [download (PDF)](https://github.com/linsdev/upload_python_module/raw/main/diagrams.pdf)
* Task list | [view](/task_list.txt)
