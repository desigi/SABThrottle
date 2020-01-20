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
SAB_QUEUE = 'http://%s/sabnzbd/api?output=json&mode=queue&apikey=%s' % (SAB_URI, SAB_API)


def get_active_streams(plex_url):
    response = requests.get(plex_url)
    json_output = json.loads(response.text)
    return json_output['response']['data']['stream_count']

def sab_queue_status(sab_url):
    res = requests.get(sab_url)
    json_out = json.loads(res.text)
    return json_out['queue']['paused']

def set_queue_state(streams):
    if streams >= '1':
        while True:
            url_pause = SAB_PAUSE
            req = urllib2.Request(url_pause)
            result = urllib2.urlopen(req)
            is_paused = sab_queue_status(SAB_QUEUE)
            if is_paused == 'true':
                break
    elif streams == '0':
        while True:
            url_resume = SAB_RESUME
            req = urllib2.Request(url_resume)
            result = urllib2.urlopen(req)
            is_paused = sab_queue_status(SAB_QUEUE)
            if is_paused == 'false':
                break

active = get_active_streams(PMS_URL)

set_queue_state(active)