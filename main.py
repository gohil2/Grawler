import threading
from queue import Queue
from domain import *
from Spider import Spider
from general import *

PROJECT_NAME = 'Grawler'
HOMEPAGE = 'https://www.python.org/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker spiders/threads (will die if/when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):      # Using _ because we don't need to use value
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()  # Notifies main module that job is done. helps free up memory


# crawl() checks if items are present in the to-do queue file, if yes - then crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:  # check if there are links present in the queue
        print(str(len(queued_links)) + 'links in the queue')
        create_jobs()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()    # blocks the main threads until the workers have processed everything
    crawl()


create_workers()
crawl()
