#!/usr/bin/python
import subprocess
import collectd
from multiprocessing import cpu_count

def dispatch_value(type_instance, value):
    val = collectd.Values(plugin='load_per_cpu')
    val.type = 'gauge'
    val.type_instance  = type_instance
    val.values = [value]
    val.dispatch()

def read_callback():    
    get_metrics()   

def get_metrics():
    p = subprocess.Popen('uptime', stdout=subprocess.PIPE)
    info = p.stdout.readline().strip("\n")
    loadmsgs = info.split(" ")
    longload = float(loadmsgs[-1])
    midload = float(loadmsgs[-2][:-1])
    shortload = float(loadmsgs[-3][:-1])

    cpucorecount = cpu_count()
    longload = longload / cpucorecount
    midload = midload / cpucorecount
    shortload = shortload / cpucorecount

    dispatch_value("longload", longload)
    dispatch_value("midload", midload)
    dispatch_value("shortload", shortload)

collectd.register_read(read_callback)