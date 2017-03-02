from django.shortcuts import render
from myapp.models import LocationData, Dt, Tmp, cpu_usage
from rest_framework import viewsets
from django.template import RequestContext
from myapp.serializers import DtSerializer, TmpSerializer, HmdSerializer
from system_info import get_temperature
from pytz import timezone
import requests
import json
import psutil
import datetime


# Create your views here.
class DtViewSet(viewsets.ModelViewSet):
    queryset = Dt.objects.all()
    serializer_class = DtSerializer

class TmpViewSet(viewsets.ModelViewSet):
    queryset = Tmp.objects.all()
    serializer_class = TmpSerializer

class HmdViewSet(viewsets.ModelViewSet):
    queryset = cpu_usage.objects.all()
    serializer_class = HmdSerializer

def home(request):
    locData = LocationData.objects.order_by('-id')[0]
    lat = locData.lat
    lon = locData.lon
    
    
# Show values from database, remove comments.     
    #dtstate = '2016-10-30T14:26:00-05:00'
    r = requests.get('http://127.0.0.1:8000/dt/5/', auth=('pi', 'D12345678'))
    result = r.text
    output = json.loads(result)
    dtstate = output['name']

    #tmpstate = '88'
    r = requests.get('http://127.0.0.1:8000/tmp/5/', auth=('pi', 'D12345678'))
    result = r.text
    output = json.loads(result)
    tmpstate = output['name']
    
    #cpu_usage = '50'
    r = requests.get('http://127.0.0.1:8000/cpu_usage/5/', auth=('pi', 'D12345678'))
    result = r.text
    output = json.loads(result)
    cpu_usage = output['name']

# Monitor Device in real-time 
    # Show current device date and time in UTC format
    #dtstate = datetime.datetime.now()
    #dtstate = dtstate.strftime("%Y-%m-%d %H:%M:%S")    
   
    #Show current temperature of the device
    #tmpstate = get_temperature()

    #Show current cpu_percentage of the device 
    #cpu_usage = psutil.cpu_percent()	
    
    return render(request, 'myapp/index.html',
{'lat': lat, 'lon': lon, 'dtstate':dtstate, 'tmpstate':tmpstate, 'cpu_usage':cpu_usage})


