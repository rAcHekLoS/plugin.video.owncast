import sys
import urllib.request
import json
import xbmcaddon
import xbmc
import ssl

def owncast_directory(_handle):
    addon = xbmcaddon.Addon()
    show_nsfw = addon.getSetting('show_nsfw')
    VIDEOS = {'Live':[], 'Offline':[]}

    url = urllib.request.Request("https://directory.owncast.online/api/home", data=None, headers={'User-Agent': xbmc.getUserAgent()})
    
    try:
        url_open = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        xbmc.log("Owncast Directory Error: " + str(e.reason), level=xbmc.LOGERROR)
        return False

    data = json.loads(url_open.read())    

    for sections in data['sections']:

        for instance in sections['instances']:
            # Detect trailing slash and remove it
            if instance['url'].endswith('/'):
                url = instance['url'][:-1]
            else:
                url = instance['url']

            instance_entry = {
                'name': instance['name'],
                'title': instance['streamTitle'],
                'description': instance['description'],
                'url': url,
                'thumb': url + '/thumbnail.jpg',
                'genre': instance['tags'][0]['name'] if instance['tags'] else ''
            }

            if sections['name'] == "What's Streaming Now":
                if instance['nsfw'] == False:
                    VIDEOS['Live'].append(instance_entry)
                elif show_nsfw == 'true':
                    VIDEOS['Live'].append(instance_entry)
            else:
                if instance['nsfw'] == False:
                    VIDEOS['Offline'].append(instance_entry)
                elif show_nsfw == 'true':
                    VIDEOS['Offline'].append(instance_entry)

    return VIDEOS

def owncast_ping(params):
    while True:
        xbmc.sleep(6000)
        if xbmc.Player().isPlayingVideo():
            playnow = xbmc.Player().getPlayingFile()
            if params['video'] + '/hls/stream.m3u8' == playnow:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                ping_url = params['video'] + '/api/ping'
                url = urllib.request.Request(ping_url, data=None, headers={'User-Agent': xbmc.getUserAgent()})
                try:
                    urllib.request.urlopen(url, context=ctx)
                except urllib.error.URLError as e:
                    xbmc.log("Owncast Ping Error: " + ping_url + ", " + str(e.reason), level=xbmc.LOGERROR)  

                xbmc.log("Owncast Ping " + ping_url, level=xbmc.LOGDEBUG)       
            else:
                break     
        else:
            break