import multiprocessing

from . import datatypes


def _dummy_loading(filename):
    t = int(str(hash(filename))[-1])
    return [i for i in range(6 ** t)][-1]


def _load_file(filename):
    if filename:
        _dummy_loading(filename)
        return filename, True
    else:
        return filename, False


def imap_next_thread(iter_queue, result_queue):
    while True:
        i = iter_queue.get()
        if i is None:
            break
        result_queue.put_nowait(next(i, None))


def processing_thread(filenames, number_of_processes, loading_progress_queue,
                      iter_queue, result_queue, stop_event, uploaded_files):
    stop_event.clear()
    progress_value = datatypes.UploadProgress(0, 0, total=len(filenames))

    pool = multiprocessing.Pool(number_of_processes)
    result_iter = pool.imap_unordered(_load_file, filenames)

    while True:
        if stop_event.is_set():
            break  # exit the main loop

        # Signal to start getting next uploaded file
        iter_queue.put_nowait(result_iter)

        while result_queue.empty():  # wait for a next uploaded file
            if stop_event.is_set():
                break  # go to exit the main loop
        else:
            ''' File uploaded '''
            result = result_queue.get_nowait()

            if result is None:
                ''' All files uploaded '''
                loading_progress_queue.put_nowait(progress_value)
                stop_event.set()
                break  # exit the main loop

            if result[1]:
                ''' File uploaded successfully '''
                progress_value.done += 1
                uploaded_files.append(result[0])
            else:
                ''' Error while upload '''
                progress_value.error += 1

            loading_progress_queue.put_nowait(progress_value)
            continue  # continue the main loop bypassing 'break'

        break  # exit the main loop

    iter_queue.put_nowait(None)  # terminate imap_next_thread
    pool.close()
    pool.join()
