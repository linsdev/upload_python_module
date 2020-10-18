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
