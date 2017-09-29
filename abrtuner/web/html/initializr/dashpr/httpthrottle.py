#
# httpthrottle.py
# mod_python script for simulating bad HTTP connections.
#
from __future__ import with_statement
from mod_python import apache

import re
import time
import math
import sys
import os
import mmap
import traceback
import fcntl
import logging

#logging.basicConfig(level=logging.DEBUG, filename='/tmp/httpthrottle.log', filemode='a+')
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s', filename='/tmp/httpthrottle.log', filemode='a+')
log = logging.getLogger('httpthrottle')


# How many times a second file chunks are sent to client when forcing speed.
# A higher number will result in a more even speed, but also more overhead.
transfer_frequency = 30
lock_file = "/tmp/httpthrottle.lock"
shmem_file = "/tmp/httpthrottle.run"
conffile = "/var/www/httpthrottle.conf"

start_time = -1
active_conns = -1
#shmem_fd = None 
shmem = None

#
# Return immediately to client with the specified HTTP response code.
#
def http_response(filter, code):
	filter.req.status = code

#
# Sleep for <delay> seconds (can be fractional), then send file back to client.
#
def send_file_with_delay(filter, delay):
    time.sleep(delay)

    data = filter.read(1024)
    while data:
	filter.write(data)
	filter.flush()
	data = filter.read(1024)	

#
# Send file back to client at a fixed speed (bytes/sec).
#
def send_file_at_speed(filter, speed):
    data = filter.read(int(float(speed)/transfer_frequency))
    while data:
	time.sleep(1.0/transfer_frequency)
	filter.write(data)
	filter.flush()
	data = filter.read(int(float(speed)/(transfer_frequency*active_conns)))	


#
# Read speed from config file, poll at regular intervals.
#	
def send_file_at_speed_polled(filter):
    counter = 10
    data = True
    while data:
	if counter == 10:
	    f = open(conffile, "r")
	    conf = eval(f.read())
	    f.close()
	    speed = conf['fixed_bw'] * 125
	    counter = 0

	time.sleep(1.0/transfer_frequency)
	counter += 1

        if speed != 0:
	    read_globals()
	    data = filter.read(int(speed/(active_conns*transfer_frequency)))
	    if not data:
	        break
	    filter.write(data)
	    filter.flush()

#
# Use input from a logfile to throttle bandwidth. 
# One log line each second, given in kbit/sec.
#	
def send_file_at_log_speed(filter, logfile):
    f = open(logfile, "r")
    log_line = f.readline()

    prev_pos = 0
    data = True
    while data:
	t = time.time() - start_time
	transfers = int(math.floor(t + 1.0) * transfer_frequency - round(t * transfer_frequency))
	for i in range(prev_pos, int(t)):
	    log_line = f.readline()
	    if log_line is None or not log_line.strip().isdigit():
                filter.pass_on()
                return

        prev_pos = int(t)
		
	speed = int(log_line) * 125
	log.info("time: %f, speed: %d" % (t, int(speed/125)))
        prev_time = time.time()
	for i in range(transfers):
	    time.sleep(1.0/transfer_frequency)
	    read_globals()
	    if active_conns < 0 or active_conns > 2:
		log.info("FFFFFFFUUUUUUUUUUUUU")
	    cur_time = time.time()
	    tdiff = cur_time - prev_time
	    prev_time = cur_time
            if speed != 0:
                data = filter.read(int(speed*tdiff/active_conns))	
	        if not data:
		    break
	        filter.write(data)
	        filter.flush()

	if transfers == 0:
	    time.sleep(0.5/transfer_frequency)

    f.close()

def update_lock(count=1):
    global active_conns

    fcntl.flock(shmem_fd, fcntl.LOCK_EX)
    read_globals()
    log.info("update active_conns %d %d" % (active_conns, count))
    active_conns += count
    write_globals()
    fcntl.flock(shmem_fd, fcntl.LOCK_UN)

def read_globals():
    global start_time
    global active_conns
    global shmem_fd

    shmem_fd.seek(0)
    start_time = float(shmem_fd.readline())
    active_conns = int(shmem_fd.readline())
    #log.info("read active_conns = %d" % active_conns)

def write_globals():
    global active_conns
    global shmem_fd
#    log.info("writing active_conns = %d" % active_conns)
    shmem_fd.seek(0)
    shmem_fd.write("%020f\n" % start_time)
    shmem_fd.write("%010d" % active_conns)
    shmem_fd.flush()


def outputfilter(filter):
    log.info('control reached here')
    global active_conns
    global start_time
    global shmem_fd

    log.info("starting up ...")

#	if os.path.exists(shmem_file):
#		fs = os.stat(shmem_file)
#		if time.time() > fs.st_mtime + 10:
#		    os.remove(shmem_file)

    if not os.path.exists(shmem_file):
	log.info("creating new shmem file")
	f = open(shmem_file, "w")
	f.write("%020f\n" % time.time())
	f.write("%010d" % 0)
	f.close()
	            
    shmem_fd = open(shmem_file, "r+")
#    shmem = mmap.mmap(f.fileno(), 0)

    update_lock(1)

    ret = None
    try:
	ret = _outputfilter(filter)
	log.info("successful run? ret = %s" % str(ret))
    except Exception, e:
	log.info('*** exception: %s' % str(e))
	log.info('traceback: %s' % traceback.format_exc())

    update_lock(-1)

    shmem_fd.close()
#    f.close()

    log.info("closing down ...")

    return ret

#
# The output filter handler called by the apache module mod_python.
#
def _outputfilter(filter):
    if not os.path.isfile(conffile):
        filter.pass_on()
        filter.close()
        return

    with open(conffile) as f:
        conf = eval(f.read())

    full_uri = str(filter.req.filename) + '?' + str(filter.req.args) 
    log.info('filename: ' + full_uri)
    if conf['match'] not in full_uri:
        filter.pass_on()
        filter.close()
        return
   
    #args = filter.req.args.split('&')
    #if len(args) > 4:
    #    log.info(str(time.time() - start_time) + ' ' + args[4].split('=')[1])
    if 'fixed_bw' not in conf or conf['fixed_bw'] < 0:
        send_file_at_log_speed(filter, conf['logfile'])
    else:
        send_file_at_speed_polled(filter)
    
    filter.close()

