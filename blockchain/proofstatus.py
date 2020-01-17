import threading
import requests
import time
import sys
from random import uniform


class ProofStatus():
    """
    Set up a thread to ping the server and see if any new blocks have been mined since last check.
    If so, set done to True to alert proof of work function to abort and start mining a new block.
    """
    finished = False
    delay = 2

    def __init__(self, node="http://localhost:5000/chain", delay=None):
        if delay and float(delay):
            self.delay = delay
        self.node = node

    def chain_checker_task(self):
        while not self.finished:
            try:
                r = requests.get(url=self.node)
                data = r.json()
            except ValueError:  # Handle non-json response
                print("Error:  Non-json response")
                print("Response returned:")
                print(r)
                break
            if data['proof'] != self.last_proof:
                self.finished = True
            else:
                time.sleep(self.delay)

    def __enter__(self):
        try:
            r = requests.get(url=self.node)
            data = r.json()
            self.last_proof = data['proof']
            self.finished = False
            threading.Thread(target=self.chain_checker_task).start()
        except ValueError:  # Handle non-json response
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            self.finished = True

        return self

    def __exit__(self, exception, value, tb):
        self.finished = True
        if exception is not None:
            return False

    @property
    def done(self):
        return self.finished


if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]

    with ProofStatus() as p:
        while not p.done:
            a = int(uniform(0, 1.8446744e+19))
    print("New block detected")