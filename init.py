import time
import datetime
import Adafruit_DHT
import sys
import requests
import math
from system_info import get_temperature
import psutil
import datetime

tmp = 0
cpu_usage = 0

def terminalOptions():
    #Introduction
    global var
    print '-----------------\n'
    var = raw_input('What is your name? ')
    print '\n'
    print "Hello " + var
    print '-----------------\n'
    # Show questions    
    questions = ' 1. Change temperature and cpu usage manually? \n 2. Use temperature and cpu usage from Raspberry Pi 3 in real-time? \n 3. Exit'
    print questions
    var = raw_input('\nChoose what option you want: ') 
    print ('Option selected is: ' + var)
    print '\n-----------------\n'
    
def selectOption(val):
    if val == '1':
       global tmp, cpu_usage
       tmp = input('Enter the temperature value: ')
       cpu_usage = input('Enter the cpu usage value: ')
       tmp = float(tmp)
       cpu_usage = float(cpu_usage)
    elif val == '2':
        autoMode()
        print 'val'
    elif val == '3':
        print 'Have a nice day!'
        exit()  
    else: 
        print 'Error 404'

def runController():
    print 'Runcontroller is running'
    tmp = get_temperature()
    cpu_usage = psutil.cpu_percent()
    now = datetime.datetime.now()
    dt = datetime.datetime.now()
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")
    #dt = now.replace(microsecond=0)
    print(dt)
    print('Temperature: {0:0.1f} C'.format(tmp))
    print('Cpu usage:    {0:0.1f} %'.format(cpu_usage))    
    setDtState(dt)
    setTmpState(tmp)
    setHmdState(cpu_usage)
    
def setDtState(val):
    values = {'name': val}
    r = requests.put('http://127.0.0.1:8000/dt/5/', data=values, auth=('pi', 'D12345678'))
def setTmpState(val):
    values = {'name': val}
    r = requests.put('http://127.0.0.1:8000/tmp/5/', data=values, auth=('pi', 'D12345678'))
def setHmdState(val):
    values = {'name': val}
    r = requests.put('http://127.0.0.1:8000/cpu_usage/5/', data=values, auth=('pi', 'D12345678'))

def autoMode():
    while True:
        try:
            if cpu_usage is None or tmp is None:
                time.sleep(2)
                continue
            runController()
            time.sleep(1)
        except KeyboardInterrupt:
            exit()


#Show user options
terminalOptions()

#Allow user to select values manually or monitor RPI3
selectOption(var)


