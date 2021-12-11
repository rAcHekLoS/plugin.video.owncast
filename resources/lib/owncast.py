import sys
import urllib.request
import json
import xbmcaddon
import xbmc
import ssl

def owncast_directory(_handle):
    addon = xbmcaddon.Addon()
    show_nsfw = addon.getSetting('show_nsfw')

    url = urllib.request.Request("https://directory.owncast.online/api/home", data=None, headers={'User-Agent': xbmc.getUserAgent()})
    url_open = urllib.request.urlopen(url)
    data = json.loads(url_open.read())
    
    VIDEOS = {'Live':[], 'Offline':[]}

    for sections in data['sections']:

        for instance in sections['instances']:            
            instance_entry = {
                'name': instance['name'],
                'title': instance['streamTitle'],
                'url': instance['url'],
                'thumb': instance['url'] + '/thumbnail.jpg',
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
                url = urllib.request.Request(params['video'] + "/api/ping", data=None, headers={'User-Agent': xbmc.getUserAgent()})
                urllib.request.urlopen(url, context=ctx)
                xbmc.log("Owncast", level=xbmc.LOGDEBUG)       
            else:
                break     
        else:
            break