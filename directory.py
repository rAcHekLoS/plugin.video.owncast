import urllib.request
import json

def owncast_directory():
    url = urllib.request.Request("https://directory.owncast.online/api/home", data=None, headers={'User-Agent': 'Mozilla'})
    url_open = urllib.request.urlopen(url)
    data = json.loads(url_open.read())
    VIDEOS = {'Live':[], 'Other':[]}

    for section in data['sections']:        
        for section_live in section['instances']:            
            section_live_entry = {
                'name': section_live['name'],
                'title': section_live['streamTitle'],
                'video': section_live['url'] + '/hls/stream.m3u8',
                'thumb': section_live['url'] + '/thumbnail.jpg',
                'genre': section_live['tags'][0]['name'] if section_live['tags'] else ''
            }

            if section['name'] == "What's Streaming Now":
                VIDEOS['Live'].append(section_live_entry)
            else:
                VIDEOS['Other'].append(section_live_entry)

    return VIDEOS