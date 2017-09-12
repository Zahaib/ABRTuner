#!/usr/bin/python

import multiprocessing as mp
import time

#class MyProcess(multiprocessing.Process):
#
#    def __init__(self, ):
#        multiprocessing.Process.__init__(self)
#        self.exit = multiprocessing.Event()
#
#    def run(self):
#        while not self.exit.is_set():
#            pass
#        print "You exited!"
#
#    def shutdown(self):
#        print "Shutdown initiated"
#        self.exit.set()
#

def foo(name):
  print "Name given to me is " + name
  time.sleep(5)
  print "Done"


def main():
  p1 = mp.Process(target=foo, args=("Adam",))
  p1.start()
  #time.sleep(2)
  p1.join()
  print "Waited for child to end..."

if __name__ == "__main__":
  main()

#    process = MyProcess()
#    process.start()
#    print "Waiting for a while"
#    time.sleep(3)
#    process.shutdown()
#    time.sleep(3)
#    print "Child process state: %d" % process.is_alive()
