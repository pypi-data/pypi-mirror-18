import eventlet
import time

def func1():
  while True:
    time.sleep(1)
    print "111\n"

def func2():
  while True:
    time.sleep(1)
    print "222\n"

eventlet.spawn(func1)
eventlet.spawn(func2)


while True:
  time.sleep(1)
