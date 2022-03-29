import requests
import cv2
import numpy as np

from threading_decorators import synchronized_with_attr
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread
from time import sleep
from threading import Lock, RLock

from sync_date_iterator import SyncDateIterator



class CancellationToken:
    def __init__(self):
        self.is_cancelled = False
        self.cancelleds = 0
        self.lock = RLock()

    @synchronized_with_attr("lock")
    def cancel(self):
        self.is_cancelled = True
        self.cancelleds += 1

def download_file(url, file_name):
    r = requests.get(url, allow_redirects=True)
    status_code = r.status_code
    if status_code == 200:
        f = open(file_name, 'wb')
        f.write(r.content)
        f.close()
    return status_code

def get_contents_file(url):
    r = requests.get(url, allow_redirects=True)
    status_code = r.status_code
    if status_code == 200:
        return (status_code, r.content)
    return (status_code, None)


def log_error(status, url):
    f = open('errors.txt', 'a')
    f.write(f'{datetime.now()},{status},{url}\n')
    f.close()


def download_all(date_iterator: SyncDateIterator, file_bytes_queue: Queue, cancellation: CancellationToken):
    print("Downloading images task starting...")
    try:
        for current_date in date_iterator:
            if cancellation.is_cancelled:
                break
            year = current_date.year
            month = str(current_date.month).zfill(2)
            day = str(current_date.day).zfill(2)
            hour = str(current_date.hour).zfill(2)
            minute = str(current_date.minute).zfill(2)
            url = f"http://satelite.cptec.inpe.br/repositoriogoes/goes16/goes16_web/ams_ret_ch13_baixa/{year}/{month}/S11635388_{year}{month}{day}{hour}{minute}.jpg"
            #file_name = f"goes16_ch13_{year}{month}{day}{hour}{minute}.jpg"
            status, content = get_contents_file(url)
            if status != 200:
                log_error(status, url)
            else:
                file_bytes_queue.put((content, f'goes16_ch13_{year}{month}{day}{hour}{minute}_rj_gray.jpg'))

        cancellation.cancel()
        print("Downloading images task finished")
    except Exception as e:
        cancellation.cancel()
        print("Downloading images task finished with error")
        print(e)



def crop_rj(file_bytes, cropped_file_name):
    try:
        img = cv2.imdecode(np.asarray(bytearray(file_bytes), dtype='uint8'), cv2.IMREAD_GRAYSCALE)
        cropped_image = img[1395:1510, 1708:1825]
        cv2.imwrite(cropped_file_name, cropped_image)
    except Exception as e:
        print(e)


def crop_rj_task(filename_queue, cancellation, cancellation_threshold = 1):
    print(f"Cropping images task starting with cancellation_threshold = {cancellation_threshold}")
    try:
        while (not cancellation.is_cancelled or cancellation.cancelleds < cancellation_threshold) or not filename_queue.empty():
            queued_tuple = None
            try:
                queued_tuple = filename_queue.get()
            except:
                queued_tuple = None
            if queued_tuple is not None:
                file_name, cropped_file_name = queued_tuple
                crop_rj(file_name, cropped_file_name)
            else:
                sleep(0.5)
        
        cancellation.cancel()
        print("Cropping images task finished")
    except Exception as e:
        cancellation.cancel()
        print("Cropping images task finished with error")
        print(e)


def init_tasks(begin_date:datetime, end_date:datetime, download_threads = 1, processing_threads = 1):
    file_name_queue = Queue(maxsize=10)
    cancellation = CancellationToken()
    date_iterator = SyncDateIterator(begin_date, end_date, timedelta(minutes=15))
    

    
    for i in range(download_threads):
        Thread(target=download_all, args=(date_iterator, file_name_queue, cancellation)).start()
    for i in range(processing_threads):
        Thread(target=crop_rj_task, args=(file_name_queue, cancellation),kwargs={"cancellation_threshold":download_threads}).start()


# goes16_ch13_201802122315

init_tasks(begin_date=datetime(2022,1,1), end_date=datetime(2022,3,28,23,59,59), download_threads=8, processing_threads=4)