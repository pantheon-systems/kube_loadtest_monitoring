import requests
import json
import sys,os
import time
import calendar
import datetime
from datetime import timedelta

if __name__ == '__main__':

    external_ip = sys.argv[1]
    slack_key = sys.argv[2]
    git_username = sys.argv[3]
    mode = sys.argv[4]
    target_url = sys.argv[5]
    date_created = sys.argv[6]
    cluster = sys.argv[7]
    date_now = (datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')) #2020-01-14T07:21:19+00:00
    timeko=(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ts = calendar.timegm(time.gmtime())
    datetimeFormat = '%Y-%m-%dT%H:%M:%S+00:00'
    diff = datetime.datetime.strptime(date_now, datetimeFormat)  -  datetime.datetime.strptime(date_created, datetimeFormat)
    webhook_url = 'https://hooks.slack.com/services/' + slack_key
    seconds = diff.seconds 
    days = diff.days
    data = ""
    if mode == 'notification':
        if seconds > 600 and seconds < 1200 or True:
            with open("capacity.txt", "r") as file:
                 stats = ""
                 lines = file.readlines()
                 for line in lines:
                      stats = stats + line.strip()

            data='{"attachments": [{"fallback":\
            "Required plain-text summary of the attachment.","color": "#FF0000","pretext": \
            "Loadtest for ' + target_url + '","author_name": "' + git_username + '","author_link": "#","author_icon": \
            "http://dev-mapinas.pantheonsite.io/sites/default/files/Octocat.png","title": \
            "Sending capacity status of your clusters cpu and memory","title_link": "http://' + external_ip + ':8089","text": \
            "' + str(stats) + '","fields": \
            [{"title": "Priority","value": "High","short": false}],"image_url": \
            "http://my-website.com/path/to/image.jpg","thumb_url": \
            "https://d1qb2nb5cznatu.cloudfront.net/startups/i/907-cbdae2927a54d2281280f41e954e8a3d-medium_jpg.jpg",\
            "footer": "Slack API","footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png","ts": '+ str(ts) +'}]}'

        else:
            print "do nothing"

    if not data:
        print "do nothing"
    else:
        response = requests.post(webhook_url, data=data, headers={'Content-type': 'application/json'})

