#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# @name: autonice
# @author: shekk <https://null/>
# @date: 2014/04/10
# @copyright: <https://www.gnu.org/licenses/gpl-3.0.html>

import operator,sys,os,psutil,datetime

percents = list(enumerate(psutil.cpu_percent(interval=.1, percpu=True)))
cpuz = psutil.NUM_CPUS
#percents.sort(lambda _: _[1])
#least_used = min(enumerate(psutil.cpu_percent(interval=.1, percpu=True)), key=operator.itemgetter(1))
def get_percents():
	global least_used 
	least_used = min(enumerate(psutil.cpu_percent(interval=.1, percpu=True)), key=operator.itemgetter(1))
	global most_used 
	most_used = max(enumerate(psutil.cpu_percent(interval=.1, percpu=True)), key=operator.itemgetter(1))
	global cpu_percent 
	cpu_percent = psutil.cpu_percent(interval=.1, percpu=True)

def renice_proc(proc_pid, niceness=0):
	global proc_name 
	proc_name = proc.name			
    	global old_affinity 
	old_affinity = proc.get_cpu_affinity()
    	global old_nice 
	old_nice = proc.get_nice()
        global proc_ionice 
        proc_ionice = proc.get_ionice()
	proc.set_cpu_affinity([least_used[0]])
    	proc.set_nice(niceness)
    	proc.set_ionice(psutil.IOPRIO_CLASS_BE)
    	return proc.get_nice()		

#def ionice_proc(pid=proc_pid, ioniceness='IOPRIO_CLASS_BE'):
	global proc_name
	proc_name = proc.name
	global io_counters
	io_counters = proc.get_io_counters() #(read_count=454556, write_count=3456, read_bytes=110592, write_bytes=0)
	global old_ionice
	old_ionice = proc.get_ionice()
	proc.set_ionice(psutil.ioniceness) #set_ionice(ioclass, value=None)
	#psutil.IOPRIO_CLASS_NONE
	#psutil.IOPRIO_CLASS_RT
	#psutil.IOPRIO_CLASS_BE
	#psutil.IOPRIO_CLASS_IDLE
	return proc.get_ionice()

def get_status():
#psutil.STATUS_RUNNING
#psutil.STATUS_SLEEPING
#psutil.STATUS_DISK_SLEEP
#psutil.STATUS_STOPPED
#psutil.STATUS_TRACING_STOP
#psutil.STATUS_ZOMBIE
#psutil.STATUS_DEAD
#psutil.STATUS_WAKE_KILL
#psutil.STATUS_WAKING
#psutil.STATUS_IDLE
#psutil.STATUS_LOCKED
#psutil.STATUS_WAITING
	return proc.status

threshhold=input('Threshhold in %:')
renice_value=input('Renice to:')
print "Current processor use %:"
print percents
get_percents()
print "Most used core:"
print most_used
print "Least used core:"
print least_used
print "-"
for proc in psutil.get_process_list():
               	print proc.name
		proc_pid = proc.pid
		proc_percent = proc.get_cpu_percent(interval=.1)
                print proc_percent
                if proc_percent > threshhold:
			renice_proc(proc_pid, renice_value)
			msg = 'Set IO Niceness to IDLE instead?'
			shall = True if raw_input("%s (y/N) " % msg).lower() == 'y' else False
			while shall == True:
				proc.set_ionice(psutil.IOPRIO_CLASS_IDLE)
        			shall = False
