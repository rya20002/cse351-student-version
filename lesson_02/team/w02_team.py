"""
Course: CSE 351 
Lesson: L02 team activity
File:   team.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- This program requires that the server.py program be started in a terminal window.
- The program will retrieve the names of:
    - characters
    - planets
    - starships
    - vehicles
    - species

- the server will delay the request by 0.5 seconds

TODO
- Create a threaded class to make a call to the server where
  it retrieves data based on a URL.  The class should have a method
  called get_name() that returns the name of the character, planet, etc...
- The threaded class should only retrieve one URL.
  
- Speed up this program as fast as you can by:
    - creating as many as you can
    - start them all
    - join them all

"""

from datetime import datetime, timedelta
import threading

from common import *

# Include cse 351 common Python files
from cse351 import *

# global
call_count = 0
call_count_lock = threading.Lock()

class GetNameThread(threading.Thread):
    def __init__(self, url:str):
        super().__init__()
        self.url = url
        self._name = None
    
    def run(self):
        global call_count

        item = get_data_from_server(self.url)

        with call_count_lock:
            call_count += 1

        if item is not None and "name" in item:
            self._name = item["name"]
        else:
            self._name + "<error>"
    
    def get_name(self) -> str:
        return self._name

def get_urls_threaded(film6, kind: str):
    urls = film6[kind]
    print(kind)

    threads = [GetNameThread(url) for url in urls]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    for t in threads:
        print(f" - {t.get_name()}")


def main():
    global call_count

    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    film6 = get_data_from_server(f'{TOP_API_URL}/films/6')
    with call_count_lock:
        call_count += 1
    
    print_dict(film6)

    # Retrieve people
    get_urls_threaded(film6, 'characters')
    get_urls_threaded(film6, 'planets')
    get_urls_threaded(film6, 'starships')
    get_urls_threaded(film6, 'vehicles')
    get_urls_threaded(film6, 'species')

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()
