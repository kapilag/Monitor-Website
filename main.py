import yaml
import argparse
import urllib2
import time
from model import FactoryObj
import thread
import jinja2
import logging

logging.basicConfig(filename='output.log',level=logging.INFO)


# get timeout interval
parser = argparse.ArgumentParser('Monitor servers')
parser.add_argument('timeinterval', type=int, nargs='?', help='time interval to make http calls')
args = parser.parse_args()

# parse yaml file
with open('config.yml', 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# set timeout interval
timeinterval = args.timeinterval
if timeinterval == None:
    timeinterval = cfg['timeinterval']
# create factory for model
factory = FactoryObj()

def ifStatusMatched(url):
    try:
        start_time = time.time()
        payload = urllib2.urlopen(url)
    except urllib2.HTTPError, err:
        return (False,'Nil','Nil')
    except urllib2.URLError, err:
        return (False,'Nil','Nil')
    elapsed_time = time.time() - start_time
    return (True, payload, elapsed_time)

def ifPageLoaded(payload, condition):
    print('condition:'+condition)
    data = payload.read()
    # print(data)
    if condition in data:
        return 'True'
    return 'False'

def compute(url):
    obj = factory.getModel(url['path'])
    print(url['path'])

    (status, payload, elapsed_time) = ifStatusMatched(url['path'])
    obj.setStatusResult(str(status))
    if status:
        obj.setPageLoadResult(ifPageLoaded(payload,url['match']))
        obj.setTimeToLoad(elapsed_time)
    else:
        obj.setPageLoadResult('Null')
        obj.setTimeToLoad(0)

    logging.info(url['path'])
    logging.info('  currentStatus:'+obj.getCurrentStatusResult())
    logging.info('  previousStatus:'+obj.getPrevStatusResult())
    logging.info('  currentPageLoad:'+obj.getCurrentPageLoadResult())
    logging.info('  previousPageLoad:'+obj.getPrevPageLoadResult())
    logging.info('  Time:'+str(obj.getTimeToLoad()))
    logging.info('  PrevTime:'+str(obj.getPrevTimeToLoad()))

env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
template = env.get_template('index.html')

def getTemplate():
    print template.render(navigation=factory.getModelList())
    return template.render(navigation=factory.getModelList())

while True:
    for url in cfg['urls']:
        thread.start_new_thread(compute,(url,))
    print('Sleeping for:'+str(timeinterval))
    time.sleep(timeinterval)


# render templates
