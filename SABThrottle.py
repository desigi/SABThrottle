import sys
import urllib
import json
import urllib2
import requests
from xml.dom import minidom
from config import config



PMS_IP = config['PMS_IP']
PMS_PORT = config['PMS_PORT']
PMS_API = config['PMS_API']

SAB_URI = config['SAB_URL']
SAB_API = config['SAB_API']

PMS_URL = 'http://%s:%s/api/v2?apikey=%s&cmd=get_activity' % (PMS_IP, PMS_PORT, PMS_API)
SAB_PAUSE = 'http://%s/sabnzbd/api?mode=pause&apikey=%s' % (SAB_URI, SAB_API)
SAB_RESUME = 'http://%s/sabnzbd/api?mode=resume&apikey=%s' % (SAB_URI, SAB_API)



def get_active_streams(url):
        response = requests.get(url)
	json_output = json.loads(response.text)
	return json_output['response']['data']['stream_count']

active = get_active_streams(PMS_URL)

if active >= '1':
	url = SAB_PAUSE
	print url
	req = urllib2.Request(url)
	result = urllib2.urlopen(req)
elif active == '0':
        url = SAB_RESUME
	print url
        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
